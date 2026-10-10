from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Iterable, Mapping, Sequence


class Assurance(str, Enum):
    DECLARED_ONLY = "DECLARED_ONLY"
    HARNESS_WIRED = "HARNESS_WIRED"
    SESSION_EXECUTABLE = "SESSION_EXECUTABLE"
    ATTESTED_ISOLATED = "ATTESTED_ISOLATED"


ASSURANCE_RANK = {
    Assurance.DECLARED_ONLY: 0,
    Assurance.HARNESS_WIRED: 1,
    Assurance.SESSION_EXECUTABLE: 2,
    Assurance.ATTESTED_ISOLATED: 3,
}


class Availability(str, Enum):
    AVAILABLE = "AVAILABLE"
    PARTIAL = "PARTIAL"
    BLOCKED = "BLOCKED"
    UNKNOWN = "UNKNOWN"


class RouteStatus(str, Enum):
    READY = "READY"
    DEGRADED = "DEGRADED"
    BLOCKED = "BLOCKED"


@dataclass(frozen=True)
class CapabilitySpec:
    capability_id: str
    scope: str
    assurance_ceiling: Assurance
    invocation_path: str
    executor_type: str
    evidence_contract: tuple[str, ...]
    side_channel_allowed: bool
    safe_degraded_modes: tuple[str, ...] = ()

    @classmethod
    def from_mapping(cls, raw: Mapping[str, Any]) -> "CapabilitySpec":
        missing = [
            field
            for field in (
                "capability_id",
                "scope",
                "assurance_ceiling",
                "invocation_path",
                "executor_type",
                "evidence_contract",
                "side_channel_allowed",
            )
            if field not in raw
        ]
        if missing:
            raise ValueError(f"capability missing required fields: {missing}")
        evidence = raw.get("evidence_contract")
        if not isinstance(evidence, (list, tuple)) or not evidence:
            raise ValueError(f"{raw.get('capability_id')}: evidence_contract must be non-empty")
        return cls(
            capability_id=str(raw["capability_id"]),
            scope=str(raw["scope"]),
            assurance_ceiling=Assurance(str(raw["assurance_ceiling"])),
            invocation_path=str(raw["invocation_path"]).strip(),
            executor_type=str(raw["executor_type"]).strip(),
            evidence_contract=tuple(str(item) for item in evidence if str(item).strip()),
            side_channel_allowed=bool(raw["side_channel_allowed"]),
            safe_degraded_modes=tuple(str(item) for item in raw.get("safe_degraded_modes", ()) if str(item).strip()),
        )


@dataclass(frozen=True)
class SessionObservation:
    capability_id: str
    availability: Availability
    observed_assurance: Assurance
    execution_mode: str
    executor_identity: str | None = None
    proof_ref: str | None = None

    @classmethod
    def from_mapping(cls, raw: Mapping[str, Any]) -> "SessionObservation":
        return cls(
            capability_id=str(raw["capability_id"]),
            availability=Availability(str(raw["availability"])),
            observed_assurance=Assurance(str(raw["observed_assurance"])),
            execution_mode=str(raw["execution_mode"]),
            executor_identity=(str(raw["executor_identity"]) if raw.get("executor_identity") else None),
            proof_ref=(str(raw["proof_ref"]) if raw.get("proof_ref") else None),
        )


@dataclass(frozen=True)
class CapabilityRequirement:
    capability_id: str
    min_assurance: Assurance = Assurance.SESSION_EXECUTABLE
    hard: bool = True
    accepted_modes: tuple[str, ...] = ()


@dataclass(frozen=True)
class RouteDecision:
    status: RouteStatus
    ready_capabilities: tuple[str, ...]
    degraded_capabilities: tuple[str, ...]
    blockers: tuple[str, ...]
    execution_modes: tuple[str, ...]


def validate_owner_profile(raw: Mapping[str, Any]) -> list[str]:
    problems: list[str] = []
    if not str(raw.get("owner") or "").strip():
        problems.append("missing:owner")
    if not str(raw.get("repository") or "").strip():
        problems.append("missing:repository")
    capabilities = raw.get("capabilities")
    if not isinstance(capabilities, list):
        return problems + ["missing_or_invalid:capabilities"]
    seen: set[str] = set()
    for idx, item in enumerate(capabilities):
        try:
            spec = CapabilitySpec.from_mapping(item)
        except Exception as exc:  # validation surface, not execution path
            problems.append(f"capability[{idx}]:{exc}")
            continue
        if not spec.invocation_path:
            problems.append(f"{spec.capability_id}:empty_invocation_path")
        if not spec.executor_type:
            problems.append(f"{spec.capability_id}:empty_executor_type")
        if spec.capability_id in seen:
            problems.append(f"duplicate_capability:{spec.capability_id}")
        seen.add(spec.capability_id)
        if spec.assurance_ceiling != Assurance.DECLARED_ONLY and spec.invocation_path.lower() in {
            "prompt only",
            "prompt-only",
            "documentation only",
            "docs only",
        }:
            problems.append(f"{spec.capability_id}:non_declared_assurance_without_real_invocation")
    return problems


def load_capabilities(raw: Mapping[str, Any]) -> dict[str, CapabilitySpec]:
    problems = validate_owner_profile(raw)
    if problems:
        raise ValueError("invalid execution capability profile: " + "; ".join(problems))
    return {
        spec.capability_id: spec
        for spec in (CapabilitySpec.from_mapping(item) for item in raw.get("capabilities", []))
    }


def _effective_assurance(spec: CapabilitySpec, obs: SessionObservation) -> Assurance:
    rank = min(ASSURANCE_RANK[spec.assurance_ceiling], ASSURANCE_RANK[obs.observed_assurance])
    for assurance, assurance_rank in ASSURANCE_RANK.items():
        if assurance_rank == rank:
            return assurance
    return Assurance.DECLARED_ONLY


def evaluate_execution(
    owner_profile: Mapping[str, Any],
    requirements: Sequence[CapabilityRequirement],
    session_observations: Iterable[Mapping[str, Any] | SessionObservation],
) -> RouteDecision:
    """Evaluate whether the current execution window can satisfy an owner's next action.

    Repository declarations establish only a maximum assurance ceiling. Current-session
    observations are required to claim actual execution readiness. This prevents a Skill,
    agent registry row, or code path from being mistaken for a currently runnable executor.
    """

    capabilities = load_capabilities(owner_profile)
    observations: dict[str, SessionObservation] = {}
    for raw in session_observations:
        obs = raw if isinstance(raw, SessionObservation) else SessionObservation.from_mapping(raw)
        observations[obs.capability_id] = obs

    ready: list[str] = []
    degraded: list[str] = []
    blockers: list[str] = []
    modes: list[str] = []

    for req in requirements:
        spec = capabilities.get(req.capability_id)
        if spec is None:
            message = f"missing_owner_capability:{req.capability_id}"
            (blockers if req.hard else degraded).append(message)
            continue

        if spec.assurance_ceiling == Assurance.DECLARED_ONLY:
            message = f"declared_only:{req.capability_id}"
            (blockers if req.hard else degraded).append(message)
            continue

        obs = observations.get(req.capability_id)
        if obs is None:
            message = f"session_capability_unobserved:{req.capability_id}"
            (blockers if req.hard else degraded).append(message)
            continue

        if obs.availability in {Availability.BLOCKED, Availability.UNKNOWN}:
            message = f"session_{obs.availability.value.lower()}:{req.capability_id}"
            (blockers if req.hard else degraded).append(message)
            continue

        effective = _effective_assurance(spec, obs)
        if ASSURANCE_RANK[effective] < ASSURANCE_RANK[req.min_assurance]:
            message = (
                f"insufficient_assurance:{req.capability_id}:"
                f"required={req.min_assurance.value}:effective={effective.value}"
            )
            (blockers if req.hard else degraded).append(message)
            continue

        if req.accepted_modes and obs.execution_mode not in req.accepted_modes:
            message = f"execution_mode_not_allowed:{req.capability_id}:{obs.execution_mode}"
            (blockers if req.hard else degraded).append(message)
            continue

        if req.min_assurance == Assurance.ATTESTED_ISOLATED and (not obs.executor_identity or not obs.proof_ref):
            message = f"isolated_execution_missing_attestation:{req.capability_id}"
            (blockers if req.hard else degraded).append(message)
            continue

        if obs.availability == Availability.PARTIAL:
            if spec.safe_degraded_modes and obs.execution_mode in spec.safe_degraded_modes:
                degraded.append(f"safe_degraded:{req.capability_id}:{obs.execution_mode}")
                modes.append(obs.execution_mode)
                continue
            message = f"partial_without_safe_degraded_path:{req.capability_id}"
            (blockers if req.hard else degraded).append(message)
            continue

        ready.append(req.capability_id)
        modes.append(obs.execution_mode)

    status = RouteStatus.BLOCKED if blockers else (RouteStatus.DEGRADED if degraded else RouteStatus.READY)
    return RouteDecision(
        status=status,
        ready_capabilities=tuple(ready),
        degraded_capabilities=tuple(degraded),
        blockers=tuple(blockers),
        execution_modes=tuple(dict.fromkeys(modes)),
    )
