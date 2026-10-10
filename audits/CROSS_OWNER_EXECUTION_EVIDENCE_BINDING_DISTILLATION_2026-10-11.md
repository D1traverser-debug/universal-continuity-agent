# Cross-owner execution evidence binding distillation — 2026-10-11

Status: ACTIVE MAINTENANCE EVIDENCE  
Scope: Universal Continuity cross-agent control plane; no domain business-state advancement  
Trigger: user supplied three owner self-audit trajectories (Video Growth, A-share Market, Financial Writing) and requested system-level critique/distillation/learning/evolution rather than another owner-local patch.

## 1. What the three owner audits have in common

The owner symptoms differed:

- Video Growth: inline PASS / configured roles could be mistaken for executed professional review; a hard-coded subset of stages controlled process proof; pre-generation proof needed exact brief/work-order/execution binding.
- A-share Market: ReplayEval structure and thresholds could exist without mechanical replay execution/cassette identity; independent-audit prose exceeded actual attested execution capability.
- Financial Writing: pairwise judge evidence could exist but still be stale, foreign or replayed unless tied to the exact candidate/change/run; held-out coverage claims also needed stronger generalization evidence.

The reusable mother defect is not any of those business rules. It is:

**PROOF_PRESENCE_WITHOUT_EXACT_CLAIM_BINDING** — a real receipt, trace, ID, PASS, replay report or evidence reference can exist while still failing to prove this exact task, stage, capability, action, subject/candidate/brief/replay set, immutable input version and claimed result.

A second recurring class is:

**SHADOW_OBLIGATION_LIST** — a canonical machine-readable plan/config says work is required, but runtime enforcement depends on a separately maintained stage/role/name list. Newly configured work can then exist without automatically acquiring the corresponding proof obligation.

These defects explain why multiple owners independently hardened evidence binding and plan-derived enforcement. The system had already documented adjacent principles (evidence existence != semantic support, declaration != operation, CI != product outcome), but did not yet provide a generic executable exact-binding gate.

## 2. Second-order self-audit findings inside Universal

### U1 — Execution contract stronger than central executable enforcement

`EXECUTION_READINESS_CONTRACT.json` already required material execution receipts bound to task/stage/capability/executor/input/output/result, but `runtime/execution_readiness.py` only evaluated pre-execution capability readiness. Universal had no generic post-execution receipt-binding validator.

Effect: each owner had to rediscover and implement its own version of exact subject/input binding and anti-replay semantics.

### U2 — Closed-world owner topology remained in an execution-readiness test

After `OWNER_REGISTRY.json` became the sole owner-membership authority, `tests/test_execution_readiness.py` still asserted the current four business owner names explicitly.

Effect: a future fifth business owner could make the test suite require a manual name-list edit even though production owner-topology derivation was already dynamic. This was another residual shadow membership list.

### U3 — Persistence status and operational assurance were accidentally coupled

`PROGRESS_OBSERVABILITY_POLICY.json` defined `COMMITTED` as verified durable persistence. Later `ENTRYPOINT.md` language made operational methodology conformance appear necessary before `COMMITTED` itself.

That coupling is wrong. A task must be able to durably checkpoint the truthful fact that a methodology/execution/quality gate is still OPEN or BLOCKED. Otherwise the system creates a paradox: missing evidence prevents the system from safely persisting the fact that evidence is missing.

Correct separation:

- `COMMITTED` = durable persistence verified by authoritative reread.
- execution/methodology/review/quality assurance = separate gate state with its own evidence ceiling.
- a COMMITTED OPEN/BLOCKED checkpoint remains OPEN/BLOCKED; persistence does not upgrade assurance.

## 3. Candidate comparison

### Candidate A — Create a new meta-review/challenge Agent

REJECTED.

A new persona does not create exact receipt binding, provider identity, independent attestation or anti-replay enforcement. It would add another declarative surface and split authority.

### Candidate B — Let every owner continue implementing bespoke proof rules

REJECTED as the sole architecture.

Owners must keep domain-specific subject identities and business gates, but repeating the invariant itself in every repository invites inconsistent semantics and repeated rediscovery.

### Candidate C — Extend the existing execution contract with a generic binding primitive; retain owner-local business bindings

ADOPTED.

Universal now owns the reusable invariant and validator; each domain owner remains responsible for selecting the exact subject/input identities and stronger assurance requirements relevant to its gate.

This preserves owner boundaries while eliminating the need to copy Video/Replay/Financial-specific rules into the control plane.

## 4. Applied evolution

### 4.1 Generic exact-action receipt binding

New runtime: `runtime/execution_receipt.py`

It validates:

- required receipt identity and result fields;
- exact `task_id` / `stage` / `capability_id` / `action_id` match;
- owner-supplied `subject_bindings` (candidate, brief, replay set, review packet, etc.);
- owner-supplied immutable `input_bindings` (artifact/version/digest identities);
- non-empty output references;
- default receipt-id anti-replay;
- optional owner-selected single-use identities such as execution/provider/work-order/review IDs.

The validator deliberately does **not** claim to establish executor trust, provider issuance, chronology, reviewer independence or semantic quality. Those remain separate assurance gates.

Regression: `tests/test_execution_receipt.py` rejects wrong task/stage/capability/action, wrong candidate/change binding, wrong input digest, receipt reuse, configured execution-ref reuse and incomplete output evidence.

### 4.2 Execution contract now owns the reusable invariant

`EXECUTION_READINESS_CONTRACT.json` now includes `execution_receipt_binding_contract_version=1.0`, the validator pointer, required fields, anti-replay semantics, and two explicit invariants:

1. receipt existence is not proof for the wrong claim;
2. machine-readable configured obligations should be enforced from their canonical plan rather than a shadow allowlist when such a plan exists.

### 4.3 Evolution semantics learned the failure classes

`CONTINUOUS_LEARNING_POLICY.md` second-order challenge now explicitly asks:

- Is proof bound to the exact claim/action/subject/inputs/result?
- Can a stale/foreign proof be replayed?
- Are distinct execution identities reused where independence/single-use is required?
- Is runtime proof obligation derived from canonical configuration or from a shadow stage/role list?

Reusable failure taxonomy now includes:

- `unbound-proof replay / wrong-subject evidence`;
- `shadow obligation list / configured-obligation drift`.

### 4.4 Residual hard-coded owner test removed

`tests/test_execution_readiness.py` now derives expected business owners with `runtime.owner_topology.business_owner_names(OWNER_REGISTRY)` instead of naming Financial/A-share/Novel/Video explicitly.

### 4.5 Persistence and assurance separated

`PROGRESS_OBSERVABILITY_POLICY.json`, `ENTRYPOINT.md` and `tests/test_progress_observability.py` now make the boundary explicit:

- COMMITTED is persistence status only;
- COMMITTED is not methodology/execution/quality attestation;
- OPEN/BLOCKED gates are checkpointable;
- a verified commit cannot raise the assurance level of what was persisted.

## 5. Adversarial validation history

The integration was not treated as green after the first successful local/control-plane check.

Intermediate head `58c330697b74e9638a592321ac2a92708fa34d11`:

- `runtime.system_audit`: PASS
- full pytest: **FAIL** — 148 passed / 1 failed
- failing test: `test_entrypoint_requires_action_level_operational_methodology_evidence`

The failure exposed a stale regression assumption that `COMMITTED` and methodology operational conformance must be coupled. The new architecture was not rolled back to satisfy that assumption. Instead the entrypoint was clarified so operational conformance remains mandatory for claiming the profile-dependent gate/action complete while persistence remains independently checkpointable.

Validated behavioral head: `563a10476e889b132ef66dcd4cc186ef0ad5fe1f`

- GitHub Actions run: `38071270624`
- job: `114269000183`
- `runtime.system_audit`: PASS
- full pytest: PASS

## 6. Evidence ceiling

Current assurance for this cross-owner hardening is:

**REGRESSION_VERIFIED**

This means the central invariant, validator and negative tests execute and pass in CI. It does **not** mean:

- every existing owner has already routed every live gate through the normalized validator;
- this maintenance reasoning has an independent semantic hook-assessment verifier;
- a provider-issued reviewer/executor identity has been proven for every owner;
- product/business outcomes improved;
- new-owner cold-start product E2E is proven.

GitHub CI is independent execution evidence for code/tests. It is not an independent semantic grader of all maintenance claims.

## 7. Propagation boundary and next work

Universal now supplies the reusable contract and executable primitive. Existing and future owners should use either this validator or an owner-local equivalent that preserves the same invariant at gates where execution receipts are used.

Owner migration remains owner-local because Universal maintenance must not rewrite business state or steal leases. In particular:

- Video retains its domain-specific brief/work-order/reviewer/provider binding and live trusted-reviewer blockers.
- A-share retains replay-cassette, time/freeze and independent-audit business semantics.
- Financial retains candidate/change/pairwise/held-out quality semantics.

The common invariant is no longer owner-specific.

Still OPEN:

1. real new-owner + genuinely fresh ChatGPT cold-start product E2E;
2. Universal operator-dependence incident closure via independently graded live/held-out trajectories;
3. owner-specific live adoption/attestation where exact execution proof is required;
4. independent semantic methodology verification where receipt-contract 1.2 requires it;
5. domain live-outcome/quality promotion gates already tracked by each owner.

## 8. Distilled rule

**A proof object is admissible only for the claim it is bound to. Existence, authenticity and semantic relevance are separate questions. Canonical configuration must generate obligations; shadow allowlists must not decide which configured work deserves proof. Persistence success is also separate from assurance success.**
