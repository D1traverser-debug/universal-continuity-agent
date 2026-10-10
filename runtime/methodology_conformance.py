from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Iterable, Mapping


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

    Declaration conformance has two jobs:
    1. validate every profile the owner binds; and
    2. make profile omission explicit by requiring an applicability assessment for every
       profile in the current contract.

    This still does *not* prove that any hook was invoked during a real maintenance,
    artifact or evolution action. Call ``evaluate_operational_methodology_conformance``
    when operational evidence is required.
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

    # Negative-space validation: every contract profile must be consciously assessed.
    # This prevents a missing profile from silently passing simply because the owner never
    # mentioned it in profile_refs.
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

        assessment = profile_applicability.get(profile_id)
        if not isinstance(assessment, Mapping) or str(assessment.get("status", "")).strip() != "APPLIES":
            # The detailed applicability error is emitted above. Keep validating the rest so
            # callers get the complete defect set in one pass.
            pass

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

    status = "PASS" if not errors else "FAIL"
    return MethodologyConformanceResult(
        status=status,
        active_profiles=tuple(active_profiles),
        errors=tuple(errors),
    )


def _verify_evidence_refs(
    refs_raw: Any,
    *,
    profile_id: str,
    label: str,
    evidence_verifier: Callable[[str], bool],
    errors: list[str],
) -> list[str]:
    refs = (
        [str(ref).strip() for ref in refs_raw if isinstance(ref, str) and str(ref).strip()]
        if isinstance(refs_raw, list)
        else []
    )
    if not refs:
        errors.append(f"missing_{label}_evidence_refs:{profile_id}")
        return []
    for ref in refs:
        try:
            verified = bool(evidence_verifier(ref))
        except Exception:
            verified = False
        if not verified:
            errors.append(f"unverified_{label}_evidence_ref:{profile_id}:{ref}")
    return refs


def evaluate_operational_methodology_conformance(
    owner_declaration: Mapping[str, Any],
    contract: Mapping[str, Any],
    execution_evidence: Mapping[str, Any] | None,
    *,
    required_profiles: Iterable[str] | None = None,
    evidence_verifier: Callable[[str], bool] | None = None,
) -> OperationalMethodologyConformanceResult:
    """Validate event-activated methodology use with independently verified evidence.

    Operational PASS is deliberately stronger than declaration PASS. A self-authored receipt is
    only an index: every referenced evidence item must be independently accepted by the caller's
    ``evidence_verifier``.

    A profile contains the complete set of hooks that its owner must be capable of supporting,
    but a single action does not necessarily execute every hook. New receipts therefore assess
    every hook for the current action as either ``INVOKED`` or
    ``NOT_APPLICABLE_FOR_ACTION``. This preserves negative-space checking without forcing fake
    executions of unrelated hooks. Legacy receipts without ``hook_assessments`` remain valid only
    under the previous all-hooks-invoked semantics.

    ``required_profiles`` should be the event-activated subset for the current action. If omitted,
    every declaration-conformant profile is required.
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

    indexed: dict[str, Mapping[str, Any]] = {}
    for raw in runs:
        if not isinstance(raw, Mapping):
            continue
        profile_id = raw.get("profile_id")
        if isinstance(profile_id, str) and profile_id and profile_id not in indexed:
            indexed[profile_id] = raw

    for profile_id in required:
        profile = profiles[profile_id]
        assert isinstance(profile, Mapping)
        expected_version = str(profile.get("version", ""))
        run = indexed.get(profile_id)
        if run is None:
            errors.append(f"missing_operational_profile_run:{profile_id}")
            continue

        if str(run.get("profile_version", "")) != expected_version:
            errors.append(
                f"operational_profile_version_mismatch:{profile_id}:observed={run.get('profile_version')}:expected={expected_version}"
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
        reported_invoked_hooks = (
            {str(item) for item in invoked_hooks_raw}
            if isinstance(invoked_hooks_raw, list)
            else None
        )

        hook_assessments = run.get("hook_assessments")
        if hook_assessments is None:
            # Backward-compatible legacy receipts: absence of action-scoped assessments means
            # the receipt is interpreted exactly as before -- every profile hook must have run.
            invoked_hooks = reported_invoked_hooks or set()
            missing_hooks = sorted(required_hook_set - invoked_hooks)
            for hook in missing_hooks:
                errors.append(f"required_hook_not_observed:{profile_id}:{hook}")
            unknown_hooks = sorted(invoked_hooks - required_hook_set)
            for hook in unknown_hooks:
                errors.append(f"unknown_invoked_hook:{profile_id}:{hook}")
        elif not isinstance(hook_assessments, Mapping):
            errors.append(f"invalid_hook_assessments:{profile_id}")
        else:
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

                refs_raw = assessment.get("evidence_refs")
                refs = (
                    [str(ref).strip() for ref in refs_raw if isinstance(ref, str) and str(ref).strip()]
                    if isinstance(refs_raw, list)
                    else []
                )
                if not refs:
                    errors.append(f"missing_hook_assessment_evidence_refs:{profile_id}:{hook}")
                else:
                    for ref in refs:
                        try:
                            verified = bool(evidence_verifier(ref))
                        except Exception:
                            verified = False
                        if not verified:
                            errors.append(f"unverified_hook_assessment_evidence_ref:{profile_id}:{hook}:{ref}")

                if status == "INVOKED":
                    assessed_invoked.add(hook)

            if not assessed_invoked:
                errors.append(f"no_invoked_hooks_for_action:{profile_id}")

            if reported_invoked_hooks is not None and reported_invoked_hooks != assessed_invoked:
                errors.append(
                    f"invoked_hooks_mismatch:{profile_id}:reported={','.join(sorted(reported_invoked_hooks))}:assessed={','.join(sorted(assessed_invoked))}"
                )

        _verify_evidence_refs(
            run.get("evidence_refs"),
            profile_id=profile_id,
            label="profile",
            evidence_verifier=evidence_verifier,
            errors=errors,
        )

        profile_errors = [error for error in errors if f":{profile_id}" in error]
        if not profile_errors:
            verified_profiles.append(f"{profile_id}@{expected_version}")

    status = "PASS" if not errors else "FAIL"
    return OperationalMethodologyConformanceResult(
        status=status,
        required_profiles=required,
        verified_profiles=tuple(verified_profiles),
        errors=tuple(errors),
    )
