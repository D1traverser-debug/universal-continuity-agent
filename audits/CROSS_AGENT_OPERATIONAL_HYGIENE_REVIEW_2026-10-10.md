# Cross-Agent Operational Hygiene Review — 2026-10-10

Status: ACTIVE BASELINE
Scope: Universal Continuity control plane + Financial Writing + Video Growth engineering surfaces

## Problem
The user reported a recurring pattern: system answers can identify many latent risks (“thorns”), but if those risks remain as chat advice, the user must keep discovering and restating them. Financial Writing and Video Growth were also perceived as repeatedly forgetting requirements or making the same classes of mistakes despite having maintenance/evolution language.

The maintenance question is therefore not “add another reminder” but: what operational-management model prevents repeated drift, stale rules, forgotten feedback, unsafe cleanup, declared-but-unexecuted evolution roles, and regression-test staleness?

## External management patterns distilled
The review compared current design with mature patterns from software reliability and durable-agent/workflow systems:

- controller/reconciliation loops: compare actual state with desired authority and continually reconcile drift;
- observability/evals: execution traces and repeatable evals are evidence, not self-report;
- owner-aware garbage collection: cleanup depends on ownership/dependency/retention, not age alone;
- incidents/postmortems: repeated failures are recorded, root-caused and converted into regression protection;
- error-budget/change-freeze discipline: when core reliability is unhealthy, freeze unrelated feature expansion in the affected scope until reliability is restored;
- durable workflow history/versioning: long-running state survives code changes through explicit history/checkpoint/version semantics;
- evidence-gated evolution: trace/feedback -> hypothesis/candidate -> eval/prototype -> accepted harness change -> removal/demotion of superseded mechanism.

These patterns support a prevention-first model rather than prompt accumulation or unrestricted self-modification.

## Adopted cross-agent model
The control-plane baseline is:

`RECONCILER + OBSERVABILITY/EVAL + OWNER-AWARE GC + INCIDENT/POSTMORTEM + RELIABILITY GUARD + EVOLUTION GATE`

This is implemented by extending existing authority surfaces rather than creating another root policy:

- `SYSTEM_MAINTENANCE_POLICY.json` v1.3 adds `REPEATED_OWNER_FAILURE_OR_REGRESSION` and a scoped `reliability_guard`.
- `OWNER_ADAPTER_CONTRACT.json` adds `operational_hygiene_and_learning` conformance requirements.
- Existing artifact/context governance remains the owner of cache/file cleanup semantics.

## Reliability guard
A repeated material failure is a reliability signal when, for example:

- the same defect class recurs after an accepted fix;
- the user repeatedly has to restate the same durable requirement;
- a mandatory gate is repeatedly bypassed or falsely reported;
- stale rules/state/artifacts repeatedly drive execution;
- CI/eval/product evidence shows regression in a core owner responsibility.

Required closure:

`persist failure evidence -> classify root-cause layer -> inspect refresh/execution path -> patch true owner -> add/update regression/eval -> remove/demote contradictory mechanism -> verify with fresh evidence`

While the affected owner/capability has an unresolved core reliability defect, unrelated feature expansion in that affected scope should freeze. The freeze does not spread to unrelated healthy owners. A chat apology, reminder or role-played “lesson learned” is not a fix.

## Self-cleaning boundary
“Self-cleaning” does not mean autonomous deletion of arbitrary old files or accepted business evidence. Safe cleanup is limited to artifacts whose ownership, dependency and retention semantics prove they are stale/rebuildable/superseded. Durable task state and owner-retained business evidence remain protected.

## Financial Writing review
### Existing strengths
Financial Writing already has a comparatively strong software substrate: persisted task state, a Python workflow/state-machine path, learning-sample runtime tools, trajectory/regression tests, executable contract evals, static ownership/version audit, isolated package smoke and DOCX render smoke.

### Gap found
The owner exposed `record_writing_learning_sample`, but its Skill did not make capture of material explicit user corrections/acceptance/rejection mandatory before durable-learning claims or revision-loop closure. The execution capability manifest also did not expose that existing learning-evidence path as a session capability.

This left a real failure mode: the current chat could obey the correction while the correction remained chat-only and therefore was not guaranteed to survive into a future chat.

### Changes
- `skills/financial-writing-agent/SKILL.md`: material explicit user feedback on a persisted writing task must be captured through `record_writing_learning_sample` or equivalent owner receipt before claiming durable learning; if capture is unavailable, obey the current edit but explicitly report that durable learning was not persisted.
- maintenance reference and its mirrors: repeated writing failures are runtime/trajectory reliability defects, not another reminder-writing opportunity.
- `continuity/EXECUTION_CAPABILITIES.json` profile v2: added `learning_evidence_capture` as `SESSION_EXECUTABLE`, bound to the real plugin/runtime invocation path and a persisted sample receipt.
- regression test added for the real durable-learning path; an initial brittle exact-string assertion was corrected to semantic containment rather than distorting the capability contract.

### Validation
Final Financial Writing CI:
- run: `38032299542`
- job: `114155603504`
- head: `a6e69993787394f1abeef4b5da6e5bb3cb0b5e9d`
- pytest: `50 passed`
- OpenAI Agents SDK smoke: PASS
- MCP Streamable HTTP smoke: PASS (`17` typed/annotated tools)
- executable contract eval baseline: PASS/SPEC_ONLY as designed, no failing contract cases
- static ownership/version/bundle audit: PASS
- isolated wheel install: PASS
- DOCX render smoke: PASS

Conclusion: Financial Writing is not structurally collapsed. Its main forgetting boundary was that material feedback persistence was not a mandatory durability contract. That boundary is now explicit and machine-guarded, but real-session behavior still depends on the chat refreshing current Skill/capabilities and actually invoking the evidence path.

## Video Growth review
### Structural gap found
Video had a more serious declared-vs-operational mismatch:

- `agents.json` declared `production_methodologist` and `evolution_engineer`;
- self-learning documentation described an evidence/prototype/promotion loop;
- but the actual `LEARN` execution plan did not schedule those learning roles: it previously let `showrunner` produce `learning_receipt` and `red_team` review it;
- existing learning tests did not prove those roles were invoked or distinguish a learning artifact from a durable production-rule change.

This meant the repository could sound more self-evolving than the execution plan actually was.

### Changes
- `agents.json` v0.5.1: Evolution Engineer now explicitly produces a candidate change package; it may not claim production authority changed. Durable promotion requires approval plus owner maintenance apply/test/verify.
- `execution-plan.json` LEARN now schedules:
  `production_methodologist -> evolution_engineer -> red_team -> showrunner`.
- `self-learning.md`: repeated material failure is a reliability incident; chat reminders/prompt tweaks are not durable learning; normal LEARN is an operational evidence pipeline, while unrestricted autonomous repository mutation is not.
- `continuity/EXECUTION_CAPABILITIES.json` profile v2 distinguishes:
  - `scheduled_learning_evidence_pipeline`: `SESSION_EXECUTABLE` for the post-performance LEARN stage;
  - `learning_evolution_sidecar`: only `HARNESS_WIRED` for mid-stage/repeated-failure triggers until an explicit event/invocation path is fully operational.
- tests now assert the actual LEARN role sequence, candidate/receipt boundaries and truthful assurance levels.
- CI installed-smoke had two stale exact version assertions (`agents` 0.5.0 and planner 0.4.0); both were corrected to semantic current-contract checks instead of reverting valid config changes.

### Remaining hard blockers
Video is not a fully self-healing production system:

- production trusted isolated-review executors remain absent, so critical blind multimodal review cannot currently satisfy `ATTESTED_ISOLATED`;
- quality-critical generation preflight exists, but a single enforced generation gateway is still not implemented;
- mid-stage/repeated-failure learning remains `HARNESS_WIRED`, not a universal event-driven automatic sidecar;
- scheduled learning artifacts are evidence/proposals and do not mutate GitHub production authority by themselves.

### Validation
Final Video Growth CI:
- run: `38032673305`
- job: `114156701436`
- head: `81f3f96e168128de42b9d1661f25f8189c93dc3a`
- pytest: `84 passed in 1.26s`
- installed CLI / packaged AgenticStudio smoke: PASS

No Video business task checkpoint or active lease was modified by this Universal maintenance task.

## Adjacent drift caught by the same maintenance loop
Universal CI after the new reliability/owner-conformance changes initially failed with six stale tests because the Novel owner had already completed a valid `NOVEL_OS -> NOVEL_WRITING_AGENT` / Continuity v3.7 GitHub cutover while old tests still asserted the legacy owner name/protocol assumptions.

The valid Novel authority was not rolled back and the tests were not suppressed. Tests were reconciled to the current owner/alias/manifest/execution-registry invariants.

Final Universal Continuity CI:
- run: `38032272822`
- job: `114155522633`
- head: `0651195c95e7697dd57700bdad6ce193b6a8a5ff`
- package: `3.7.0`
- pytest: `93 passed in 0.26s`

This is the intended hygiene behavior: a maintenance change may expose adjacent stale verification; if the current authority is valid, repair the verification drift instead of reverting authority or ignoring the failure.

## Behavioral effect
- The user should not have to maintain an internal defect backlog or repeatedly restate accepted durable requirements.
- Repeated failures become durable reliability incidents/evidence, not just conversational apologies.
- Owner learning must have invocation/evidence/promotion paths; named roles or good documentation alone do not count as operational evolution.
- Safe self-cleaning is owner/dependency-aware GC, not blanket deletion.
- Reliability restoration precedes unrelated feature expansion inside the affected owner/capability.
- Evolution remains evidence-gated and reversible; unrestricted self-modification is not authorized.

## Remaining boundaries
1. No background/event scheduler means these control loops execute on active material/maintenance turns unless a separate scheduler/watch infrastructure is installed. Do not claim continuous off-chat self-maintenance.
2. A-share and Novel need the new operational-hygiene owner-conformance audit on their next valid maintenance/writer turns; Universal must not steal their active business leases.
3. The latest account-level Custom Instructions execution-readiness/autonomous-maintenance extension is still awaiting user confirmation/product E2E; GitHub remains non-push for already-open chats that never refresh authority.
4. Broader unrestricted “Evolution System” design remains a separate future topic; this baseline only defines safe hygiene/reliability and evidence-gated improvement.

## Current stage
`V3_7_OPERATIONAL_HYGIENE_BASELINE_ACTIVE__OWNER_EVOLUTION_CONFORMANCE_AND_PRODUCT_E2E_PENDING`

## Next action
Roll the operational-hygiene conformance contract through durable owners during their valid maintenance/writer turns, beginning with A-share/Novel while preserving active leases and business truth. Continue existing-chat session-refresh/handshake E2E and fresh-chat Continuity product E2E. Treat any repeated core owner failure as a scoped reliability incident before allowing unrelated feature expansion in that affected owner.
