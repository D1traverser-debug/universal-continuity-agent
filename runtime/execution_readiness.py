from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, Iterable, Mapping, Sequence


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
        if not isinstance(raw.get("side_channel_allowed"), bool):
            raise ValueError(f"{raw.get('capability_id')}: side_channel_allowed must be boolean")
        return cls(
            capability_id=str(raw["capability_id"]),
            scope=str(raw["scope"]),
            assurance_ceiling=Assurance(str(raw["assurance_ceiling"])),
            invocation_path=str(raw["invocation_path"]).strip(),
            executor_type=str(raw["executor_type"]).strip(),
            evidence_contract=tuple(str(item) for item in evidence if str(item).strip()),
            side_channel_allowed=raw["side_channel_allowed"],
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
    route_ref: str | None = None

    @classmethod
    def from_mapping(cls, raw: Mapping[str, Any]) -> "SessionObservation":
        return cls(
            capability_id=str(raw["capability_id"]),
            availability=Availability(str(raw["availability"])),
            observed_assurance=Assurance(str(raw["observed_assurance"])),
            execution_mode=str(raw["execution_mode"]),
            executor_identity=(str(raw["executor_identity"]) if raw.get("executor_identity") else None),
            proof_ref=(str(raw["proof_ref"]) if raw.get("proof_ref") else None),
            route_ref=(str(raw["route_ref"]) if raw.get("route_ref") else None),
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


AttestationVerifier = Callable[[SessionObservation], bool]


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
        except Exception as exc:
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
            "prompt only", "prompt-only", "documentation only", "docs only",
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
    *,
    attestation_verifier: AttestationVerifier | None = None,
) -> RouteDecision:
    """Evaluate current-session execution readiness without trusting self-asserted assurance.

    Repository declarations are ceilings. Session observations are control inputs: duplicate
    observations fail closed, owner-forbidden side channels require the observed route to bind
    the owner invocation path, and ATTESTED_ISOLATED additionally requires a caller-supplied
    verifier for the asserted executor/proof identity. The verifier contract is separate from
    the observation so a non-empty proof_ref cannot attest itself.
    """

    capabilities = load_capabilities(owner_profile)
    observations: dict[str, SessionObservation] = {}
    duplicate_observations: set[str] = set()
    for raw in session_observations:
        obs = raw if isinstance(raw, SessionObservation) else SessionObservation.from_mapping(raw)
        if obs.capability_id in observations:
            duplicate_observations.add(obs.capability_id)
        else:
            observations[obs.capability_id] = obs

    ready: list[str] = []
    degraded: list[str] = []
    blockers: list[str] = []
    modes: list[str] = []

    for req in requirements:
        spec = capabilities.get(req.capability_id)
        target = blockers if req.hard else degraded
        if spec is None:
            target.append(f"missing_owner_capability:{req.capability_id}")
            continue
        if req.capability_id in duplicate_observations:
            target.append(f"duplicate_session_observation:{req.capability_id}")
            continue
        if spec.assurance_ceiling == Assurance.DECLARED_ONLY:
            target.append(f"declared_only:{req.capability_id}")
            continue

        obs = observations.get(req.capability_id)
        if obs is None:
            target.append(f"session_capability_unobserved:{req.capability_id}")
            continue
        if obs.availability in {Availability.BLOCKED, Availability.UNKNOWN}:
            target.append(f"session_{obs.availability.value.lower()}:{req.capability_id}")
            continue

        if not spec.side_channel_allowed:
            if not obs.route_ref:
                target.append(f"owner_route_unobserved:{req.capability_id}")
                continue
            if obs.route_ref != spec.invocation_path:
                target.append(f"owner_route_mismatch:{req.capability_id}")
                continue

        effective = _effective_assurance(spec, obs)
        if ASSURANCE_RANK[effective] < ASSURANCE_RANK[req.min_assurance]:
            target.append(
                f"insufficient_assurance:{req.capability_id}:required={req.min_assurance.value}:effective={effective.value}"
            )
            continue

        if req.accepted_modes and obs.execution_mode not in req.accepted_modes:
            target.append(f"execution_mode_not_allowed:{req.capability_id}:{obs.execution_mode}")
            continue

        if req.min_assurance == Assurance.ATTESTED_ISOLATED:
            if obs.execution_mode != "ISOLATED_EXTERNAL":
                target.append(f"isolated_execution_mode_invalid:{req.capability_id}:{obs.execution_mode}")
                continue
            if not obs.executor_identity or not obs.proof_ref:
                target.append(f"isolated_execution_missing_attestation:{req.capability_id}")
                continue
            if attestation_verifier is None:
                target.append(f"isolated_execution_attestation_verifier_required:{req.capability_id}")
                continue
            try:
                attested = bool(attestation_verifier(obs))
            except Exception:
                attested = False
            if not attested:
                target.append(f"isolated_execution_attestation_unverified:{req.capability_id}")
                continue

        if obs.availability == Availability.PARTIAL:
            if spec.safe_degraded_modes and obs.execution_mode in spec.safe_degraded_modes:
                degraded.append(f"safe_degraded:{req.capability_id}:{obs.execution_mode}")
                modes.append(obs.execution_mode)
                continue
            target.append(f"partial_without_safe_degraded_path:{req.capability_id}")
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
