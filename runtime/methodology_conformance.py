from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Iterable, Mapping


EvidenceVerifier = Callable[[str], bool]
HookAssessmentVerifier = Callable[[str, str, str, str, tuple[str, ...]], bool]


@dataclass(frozen=True)
class MethodologyConformanceResult:
    status: str
    active_profiles: tuple[str, ...]
    errors: tuple[str, ...]


@dataclass(frozen=True)
class OperationalMethodologyConformanceResult:
    status: str
    required_profiles: tuple[str, ...]
    verified_profiles: tuple[str, ...]
    errors: tuple[str, ...]


def _resolve_path(root: Mapping[str, Any], dotted_path: str) -> Any:
    current: Any = root
    for part in dotted_path.split("."):
        if not isinstance(current, Mapping) or part not in current:
            raise KeyError(dotted_path)
        current = current[part]
    return current


def _composition(contract: Mapping[str, Any]) -> Mapping[str, Any] | None:
    value = contract.get("methodology_composition")
    return value if isinstance(value, Mapping) else None


def evaluate_methodology_conformance(
    owner_declaration: Mapping[str, Any],
    contract: Mapping[str, Any],
) -> MethodologyConformanceResult:
    """Validate declaration-level composable methodology conformance.

    Declaration conformance validates every bound profile and forces the owner to assess the
    applicability of every current contract profile. It does not prove that a real action invoked
    the profile. Use ``evaluate_operational_methodology_conformance`` for action-level proof.
    """

    composition = _composition(contract)
    if composition is None:
        return MethodologyConformanceResult(
            status="FAIL",
            active_profiles=(),
            errors=("missing_contract_methodology_composition",),
        )

    profiles = composition.get("profiles")
    if not isinstance(profiles, Mapping):
        return MethodologyConformanceResult(
            status="FAIL",
            active_profiles=(),
            errors=("missing_contract_profiles",),
        )

    methodology = owner_declaration.get("methodology")
    if not isinstance(methodology, Mapping):
        return MethodologyConformanceResult(
            status="FAIL",
            active_profiles=(),
            errors=("missing_owner_methodology",),
        )

    profile_refs = methodology.get("profile_refs")
    profile_applicability = methodology.get("profile_applicability")
    hook_bindings = methodology.get("hook_bindings")
    overrides = methodology.get("overrides", {})
    if not isinstance(profile_refs, Mapping):
        return MethodologyConformanceResult("FAIL", (), ("missing_or_invalid_profile_refs",))
    if not isinstance(profile_applicability, Mapping):
        return MethodologyConformanceResult("FAIL", (), ("missing_or_invalid_profile_applicability",))
    if not isinstance(hook_bindings, Mapping):
        return MethodologyConformanceResult("FAIL", (), ("missing_or_invalid_hook_bindings",))
    if not isinstance(overrides, Mapping):
        return MethodologyConformanceResult("FAIL", (), ("invalid_overrides",))

    errors: list[str] = []
    active_profiles: list[str] = []

    forbidden_overrides = set(str(item) for item in composition.get("forbidden_override_keys", ()))
    for key in overrides:
        if str(key) in forbidden_overrides:
            errors.append(f"forbidden_override:{key}")

    for raw_profile_id in profile_applicability:
        profile_id = str(raw_profile_id)
        if profile_id not in profiles:
            errors.append(f"unknown_profile_applicability:{profile_id}")

    for raw_profile_id in profiles:
        profile_id = str(raw_profile_id)
        assessment = profile_applicability.get(profile_id)
        if not isinstance(assessment, Mapping):
            errors.append(f"missing_profile_applicability:{profile_id}")
            continue

        status = str(assessment.get("status", "")).strip()
        reason = str(assessment.get("reason", "")).strip()
        refs_raw = assessment.get("evidence_refs")
        refs = (
            [str(ref).strip() for ref in refs_raw if isinstance(ref, str) and str(ref).strip()]
            if isinstance(refs_raw, list)
            else []
        )

        if status not in {"APPLIES", "NOT_APPLICABLE"}:
            errors.append(f"invalid_profile_applicability_status:{profile_id}:{status}")
        if not reason:
            errors.append(f"missing_profile_applicability_reason:{profile_id}")
        if not refs:
            errors.append(f"missing_profile_applicability_evidence_refs:{profile_id}")

        if status == "APPLIES" and profile_id not in profile_refs:
            errors.append(f"applicable_profile_not_declared:{profile_id}")
        if status == "NOT_APPLICABLE" and profile_id in profile_refs:
            errors.append(f"profile_declared_but_marked_not_applicable:{profile_id}")

    for profile_id, requested_version in profile_refs.items():
        profile = profiles.get(profile_id)
        if not isinstance(profile, Mapping):
            errors.append(f"unknown_profile:{profile_id}")
            continue

        expected_version = str(profile.get("version", ""))
        if str(requested_version) != expected_version:
            errors.append(
                f"profile_version_mismatch:{profile_id}:requested={requested_version}:expected={expected_version}"
            )
            continue

        required_hooks_from = str(profile.get("required_hooks_from", ""))
        try:
            required_hooks = _resolve_path(contract, required_hooks_from)
        except KeyError:
            errors.append(f"invalid_required_hooks_ref:{profile_id}:{required_hooks_from}")
            continue

        if not isinstance(required_hooks, list):
            errors.append(f"required_hooks_not_list:{profile_id}:{required_hooks_from}")
            continue

        for hook in required_hooks:
            binding = hook_bindings.get(hook)
            if not isinstance(binding, str) or not binding.strip():
                errors.append(f"missing_hook_binding:{profile_id}:{hook}")

        active_profiles.append(f"{profile_id}@{expected_version}")

    return MethodologyConformanceResult(
        status="PASS" if not errors else "FAIL",
        active_profiles=tuple(active_profiles),
        errors=tuple(errors),
    )


def _verified_refs(
    refs_raw: Any,
    *,
    profile_id: str,
    label: str,
    evidence_verifier: EvidenceVerifier,
    errors: list[str],
) -> tuple[str, ...]:
    refs = (
        tuple(str(ref).strip() for ref in refs_raw if isinstance(ref, str) and str(ref).strip())
        if isinstance(refs_raw, list)
        else ()
    )
    if not refs:
        errors.append(f"missing_{label}_evidence_refs:{profile_id}")
        return ()

    verified_refs: list[str] = []
    for ref in refs:
        try:
            verified = bool(evidence_verifier(ref))
        except Exception:
            verified = False
        if not verified:
            errors.append(f"unverified_{label}_evidence_ref:{profile_id}:{ref}")
        else:
            verified_refs.append(ref)
    return tuple(verified_refs)


def evaluate_operational_methodology_conformance(
    owner_declaration: Mapping[str, Any],
    contract: Mapping[str, Any],
    execution_evidence: Mapping[str, Any] | None,
    *,
    required_profiles: Iterable[str] | None = None,
    evidence_verifier: EvidenceVerifier | None = None,
    assessment_verifier: HookAssessmentVerifier | None = None,
) -> OperationalMethodologyConformanceResult:
    """Validate event-activated methodology use with independent semantic support.

    Receipt contract 1.2 separates two verification questions:
    1. ``evidence_verifier``: does each evidence reference resolve to trusted evidence?
    2. ``assessment_verifier``: does that verified evidence actually support this hook's claim
       (INVOKED or NOT_APPLICABLE_FOR_ACTION) and stated reason?

    This prevents a real but irrelevant evidence reference from laundering a false hook claim.
    Legacy invoked-hooks-only receipts are no longer admissible for operational PASS under 1.2.
    """

    declared = evaluate_methodology_conformance(owner_declaration, contract)
    if declared.status != "PASS":
        return OperationalMethodologyConformanceResult(
            status="FAIL",
            required_profiles=(),
            verified_profiles=(),
            errors=tuple(f"declaration:{error}" for error in declared.errors),
        )

    composition = _composition(contract)
    assert composition is not None
    profiles = composition.get("profiles")
    assert isinstance(profiles, Mapping)

    methodology = owner_declaration.get("methodology")
    assert isinstance(methodology, Mapping)
    declared_refs = methodology.get("profile_refs")
    assert isinstance(declared_refs, Mapping)

    if required_profiles is None:
        required = tuple(str(profile_id) for profile_id in declared_refs)
    else:
        required = tuple(dict.fromkeys(str(profile_id) for profile_id in required_profiles))

    errors: list[str] = []
    verified_profiles: list[str] = []

    for profile_id in required:
        if profile_id not in declared_refs:
            errors.append(f"required_profile_not_declared:{profile_id}")
        elif profile_id not in profiles:
            errors.append(f"required_profile_unknown:{profile_id}")

    if errors:
        return OperationalMethodologyConformanceResult("FAIL", required, (), tuple(errors))

    if not isinstance(execution_evidence, Mapping):
        return OperationalMethodologyConformanceResult(
            "FAIL", required, (), ("missing_operational_execution_evidence",)
        )

    runs = execution_evidence.get("profile_runs")
    if not isinstance(runs, list):
        return OperationalMethodologyConformanceResult(
            "FAIL", required, (), ("missing_or_invalid_profile_runs",)
        )

    if evidence_verifier is None:
        return OperationalMethodologyConformanceResult(
            "FAIL", required, (), ("independent_evidence_verifier_required",)
        )
    if assessment_verifier is None:
        return OperationalMethodologyConformanceResult(
            "FAIL", required, (), ("independent_hook_assessment_verifier_required",)
        )

    receipt_contract = composition.get("operational_profile_run_contract")
    expected_receipt_version = (
        str(receipt_contract.get("receipt_contract_version_required", ""))
        if isinstance(receipt_contract, Mapping)
        else ""
    )
    if not expected_receipt_version:
        return OperationalMethodologyConformanceResult(
            "FAIL", required, (), ("missing_operational_receipt_contract_version",)
        )

    indexed: dict[str, Mapping[str, Any]] = {}
    for raw in runs:
        if not isinstance(raw, Mapping):
            continue
        profile_id = raw.get("profile_id")
        if isinstance(profile_id, str) and profile_id and profile_id not in indexed:
            indexed[profile_id] = raw

    for profile_id in required:
        profile_error_start = len(errors)
        profile = profiles[profile_id]
        assert isinstance(profile, Mapping)
        expected_profile_version = str(profile.get("version", ""))
        run = indexed.get(profile_id)
        if run is None:
            errors.append(f"missing_operational_profile_run:{profile_id}")
            continue

        observed_receipt_version = str(run.get("receipt_contract_version", "")).strip()
        if observed_receipt_version != expected_receipt_version:
            errors.append(
                f"operational_receipt_contract_version_mismatch:{profile_id}:observed={observed_receipt_version or 'MISSING'}:expected={expected_receipt_version}"
            )

        if str(run.get("profile_version", "")) != expected_profile_version:
            errors.append(
                f"operational_profile_version_mismatch:{profile_id}:observed={run.get('profile_version')}:expected={expected_profile_version}"
            )

        activation_id = run.get("activation_id")
        if not isinstance(activation_id, str) or not activation_id.strip():
            errors.append(f"missing_activation_id:{profile_id}")

        trigger = run.get("trigger")
        if not isinstance(trigger, str) or not trigger.strip():
            errors.append(f"missing_activation_trigger:{profile_id}")

        required_hooks_from = str(profile.get("required_hooks_from", ""))
        try:
            required_hooks_raw = _resolve_path(contract, required_hooks_from)
        except KeyError:
            errors.append(f"invalid_required_hooks_ref:{profile_id}:{required_hooks_from}")
            continue
        if not isinstance(required_hooks_raw, list):
            errors.append(f"required_hooks_not_list:{profile_id}:{required_hooks_from}")
            continue
        required_hooks = tuple(str(item) for item in required_hooks_raw)
        required_hook_set = set(required_hooks)

        invoked_hooks_raw = run.get("invoked_hooks")
        if not isinstance(invoked_hooks_raw, list):
            errors.append(f"missing_or_invalid_invoked_hooks:{profile_id}")
            reported_invoked_hooks: set[str] = set()
        else:
            reported_invoked_hooks = {str(item) for item in invoked_hooks_raw}

        unknown_invoked = sorted(reported_invoked_hooks - required_hook_set)
        for hook in unknown_invoked:
            errors.append(f"unknown_invoked_hook:{profile_id}:{hook}")

        hook_assessments = run.get("hook_assessments")
        if not isinstance(hook_assessments, Mapping):
            errors.append(f"missing_or_invalid_hook_assessments:{profile_id}")
            _verified_refs(
                run.get("evidence_refs"),
                profile_id=profile_id,
                label="profile",
                evidence_verifier=evidence_verifier,
                errors=errors,
            )
            continue

        for raw_hook in hook_assessments:
            hook = str(raw_hook)
            if hook not in required_hook_set:
                errors.append(f"unknown_hook_assessment:{profile_id}:{hook}")

        assessed_invoked: set[str] = set()
        for hook in required_hooks:
            assessment = hook_assessments.get(hook)
            if not isinstance(assessment, Mapping):
                errors.append(f"missing_hook_assessment:{profile_id}:{hook}")
                continue

            status = str(assessment.get("status", "")).strip()
            reason = str(assessment.get("reason", "")).strip()
            if status not in {"INVOKED", "NOT_APPLICABLE_FOR_ACTION"}:
                errors.append(f"invalid_hook_assessment_status:{profile_id}:{hook}:{status}")
            if not reason:
                errors.append(f"missing_hook_assessment_reason:{profile_id}:{hook}")

            verified_refs = _verified_refs(
                assessment.get("evidence_refs"),
                profile_id=profile_id,
                label=f"hook_assessment:{hook}",
                evidence_verifier=evidence_verifier,
                errors=errors,
            )

            if status in {"INVOKED", "NOT_APPLICABLE_FOR_ACTION"} and reason and verified_refs:
                try:
                    supported = bool(
                        assessment_verifier(profile_id, hook, status, reason, verified_refs)
                    )
                except Exception:
                    supported = False
                if not supported:
                    errors.append(f"unsupported_hook_assessment_claim:{profile_id}:{hook}:{status}")

            if status == "INVOKED":
                assessed_invoked.add(hook)

        if not assessed_invoked:
            errors.append(f"no_invoked_hooks_for_action:{profile_id}")

        if reported_invoked_hooks != assessed_invoked:
            errors.append(
                f"invoked_hooks_mismatch:{profile_id}:reported={','.join(sorted(reported_invoked_hooks))}:assessed={','.join(sorted(assessed_invoked))}"
            )

        _verified_refs(
            run.get("evidence_refs"),
            profile_id=profile_id,
            label="profile",
            evidence_verifier=evidence_verifier,
            errors=errors,
        )

        if len(errors) == profile_error_start:
            verified_profiles.append(f"{profile_id}@{expected_profile_version}")

    return OperationalMethodologyConformanceResult(
        status="PASS" if not errors else "FAIL",
        required_profiles=required,
        verified_profiles=tuple(verified_profiles),
        errors=tuple(errors),
    )
