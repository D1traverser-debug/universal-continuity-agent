# Cold-start / new-owner topology incident — 2026-10-11

Status: `MECHANICAL_TOPOLOGY_HARDENED__REAL_NEW_OWNER_FRESH_CHAT_PRODUCT_E2E_PENDING`
Owner: `UNIVERSAL_CONTINUITY_HARNESS`
Related incident: `UNIVERSAL_OPERATOR_DEPENDENCE_RELIABILITY_INCIDENT_2026-10-10.md`

## Trigger

The maintenance system had repeatedly reached a local green state and described the system as "done" while the user still had to prompt a broader perspective. The material missing perspective in this incident was not another known defect example. It was an open-world continuity question:

- what happens when a truly fresh chat knows none of the previous conversation context; and
- what happens when a completely new business Agent/owner is admitted to the Universal control plane.

This reminder is additional evidence for the existing operator-dependence incident. The maintenance writer must not require the user to enumerate further analogous cases.

## Root cause

The prior control plane had a duplicated owner-topology model.

`OWNER_REGISTRY.json` looked like an owner registry, but owner membership was also copied into:

- `BARE_INHERIT_DISCOVERY.json.required_sources`;
- `runtime/system_audit.py:BUSINESS_OWNERS`;
- regressions that asserted the current owner names or `required_owner_quorum == 5`.

That meant adding a new Agent was not one admission operation. A maintainer had to remember several separate owner-name lists. The existing checks could prove that all *known copied lists* agreed while still failing to prove that an unknown future owner would be discovered.

A second root cause was claim calibration. The historical fresh-chat E2E evidence was real, but its scope was the owner topology that existed when the test ran. It did not prove open-world new-owner admission. Treating `fresh-chat E2E PASS` as if it implied arbitrary future-owner cold-start support was an evidence-ceiling error.

## Alternatives considered

### Keep a central static business-owner list

Rejected. It preserves a second membership authority and repeats the exact failure class.

### Add an onboarding/challenge Agent

Rejected. A new role does not remove duplicated topology and does not create an independent execution identity or product trace. It would add another declarative surface that itself must be kept in sync.

### Make `OWNER_REGISTRY` the sole membership authority

Accepted.

Business membership is now selected by `owner_kind == BUSINESS`; bare-discovery participation is selected independently by `bare_inherit_participant == true`. Discovery and audit scope are derived from the registry rather than copied owner names.

The execution and protocol-adaptation registries remain rebuildable conformance/status caches. They must converge to the derived BUSINESS set; incomplete convergence fails closed.

## Mechanical hardening

Implemented surfaces:

- `runtime/owner_topology.py`
  - derives BUSINESS owner membership;
  - derives bare-inherit source quorum;
  - validates owner admission metadata, aliases and required BUSINESS pointers.
- `OWNER_REGISTRY.json`
  - schema 3.1;
  - declares `SOLE_CONTROL_PLANE_OWNER_MEMBERSHIP_AUTHORITY`;
  - adds explicit `owner_kind`;
  - forbids parallel hard-coded owner lists.
- `BARE_INHERIT_DISCOVERY.json`
  - removes concrete `required_sources` owner list;
  - derives participants from current `OWNER_REGISTRY`.
- `runtime/system_audit.py`
  - removes `BUSINESS_OWNERS` constant;
  - derives metadata sweep scope dynamically;
  - verifies execution/adaptation cache convergence against current membership;
  - treats owner membership as a core invariant.

## Synthetic unknown-owner regression

The regression suite creates a synthetic fifth business owner, `SYNTHETIC_NEW_AGENT`, without adding that name to production code or a discovery policy.

Required behavior:

1. after registry admission, it automatically appears in the derived bare-discovery quorum;
2. it automatically appears in full control-plane audit scope;
3. while protocol-adaptation and execution caches are missing the owner, audit FAILs closed;
4. after those rebuildable caches converge, audit PASSes and includes the synthetic owner in both business-owner and bare-inherit scopes.

This proves topology mechanics and negative-space enforcement. It does **not** prove ChatGPT product cold-start behavior for a real newly admitted owner.

## Validation

Intermediate head `4535ce6fcada3d04fc8bde60d87211432edd00f7`:

- `runtime.system_audit`: PASS;
- pytest: 139 PASS / 1 FAIL;
- the only failure was a stale exact assertion that `OWNER_REGISTRY.schema_version == 3.0`.

The stale topology assertion was removed rather than downgrading the 3.1 design.

Validated behavioral head `e878f8b217356d67ad986033ca04705179197164`:

- Actions run `38067271852` / job `114257353885`;
- `runtime.system_audit`: PASS;
- full pytest: PASS.

Assurance ceiling: `REGRESSION_VERIFIED` for dynamic membership/admission mechanics.

## Corrected product-evidence boundary

Historical existing-chat and fresh-chat E2E evidence remains valid for the topology that existed when those trajectories ran.

It must not be generalized to:

- an arbitrary future business owner;
- a newly registered owner whose derived caches have not converged;
- a truly fresh ChatGPT product session routing to that new owner;
- a first real business action executed by that owner.

A broad new-owner cold-start PASS requires a real newly admitted owner plus a genuinely fresh product chat/trace. The current maintenance chat cannot manufacture that independence by role-play or by creating a synthetic Python fixture.

Until such evidence exists:

`KNOWN_TOPOLOGY_FRESH_CHAT_E2E = PASS`

`DYNAMIC_OWNER_MEMBERSHIP_MECHANICS = REGRESSION_VERIFIED`

`REAL_NEW_OWNER_FRESH_CHAT_PRODUCT_E2E = OPEN`

## Reusable lesson

A registry is not a true membership authority if a new member requires editing additional name allowlists elsewhere.

For extensible control planes, test the mutation operation itself: add an unknown synthetic member to the canonical registry and verify that every derived scope either discovers it automatically or fails closed because a declared dependency has not converged.

Known-topology E2E evidence is closed-world evidence. It must not be promoted into an open-world extensibility claim without a real admission trajectory.
