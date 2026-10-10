# Cross-Agent Execution Readiness Audit — 2026-10-10

Status: **PASS — CONTROL PLANE ACTIVE, OWNER RUNTIME AVAILABILITY REMAINS SESSION-DEPENDENT**  
Continuity protocol: **v3.7**  
Execution-readiness contract: **v1.0**

## Why this audit exists

Moving agent systems from Notion/Google documentation into GitHub improves precision only when GitHub becomes executable authority rather than a larger document store.

The failure pattern under review was: a repository could contain many named agents, Skills, role prompts, workflow stages and governance rules, while the conversational execution path could still bypass those roles or lack a real executor binding.

The system therefore needs a cross-agent control plane that distinguishes declared capability from real execution.

## Implemented universal control plane

Added:

- `ORCHESTRATION_BLUEPRINT.md`
- `EXECUTION_READINESS_CONTRACT.json`
- `OWNER_EXECUTION_REGISTRY.json`
- `runtime/execution_readiness.py`
- `tests/test_execution_readiness.py`

`OWNER_REGISTRY.json`, `SYSTEM_BLUEPRINT.md` and `ENTRYPOINT.md` now route GitHub-backed business owners into this execution-readiness layer after exact task/owner resolution.

This is deliberately a sibling control plane to Continuity. Continuity retains task discovery/recovery/leases; domain owners retain business state machines; the execution control plane only decides whether a needed capability is actually runnable with sufficient assurance.

## Assurance model

The dispatcher now distinguishes:

1. `DECLARED_ONLY` — role/prompt/config/docs exist, but no proven invocation path;
2. `HARNESS_WIRED` — real owner invocation path exists and fails closed, but the current session/runtime has not proved availability;
3. `SESSION_EXECUTABLE` — current execution window has the required runtime/tool binding;
4. `ATTESTED_ISOLATED` — execution is bound to a distinct inspectable identity/context/proof when true independence matters.

Repository readiness is a ceiling, not current-session proof.

## Owner capability surfaces added

The following GitHub business owners now expose the same owner-level file:

`continuity/EXECUTION_CAPABILITIES.json`

### Financial Writing

Repository: `D1traverser-debug/financial-writing-agent`

Observed architecture:

- Python workflow/state machine exists;
- high-judgment stages have a concrete OpenAI Agents SDK executor path;
- deterministic checks/finalization exist;
- current-session SDK/model/runtime availability still requires handshake;
- no claim of `ATTESTED_ISOLATED` review is made.

Disposition: **EXECUTOR-WIRED; SESSION AVAILABILITY DEPENDENT**.

### A-share Market Agent

Repository: `D1traverser-debug/a-share-event-driven-agent`

Observed architecture:

- market-day state machine/runner exists;
- runtime service/plugin contracts enforce stage/schema boundaries;
- analytical payload authoring can be bridged only through owner-gated structured submissions;
- live source/data access remains per-session/per-market-day capability;
- no strict isolated auditor is currently claimed.

Disposition: **OWNER-RUNTIME-WIRED; LIVE SOURCE + SESSION BINDING DEPENDENT**.

### Video Growth

Repository: `D1traverser-debug/video-growth-agent`

Observed architecture:

- work-order runtime, blind packet construction, self-review prohibition and receipts exist;
- ordinary work packets can in principle use an approved external/chat executor substrate;
- critical blind multimodal review has an attestation contract but production trusted executors are currently empty;
- generation preflight exists as a deterministic guard;
- a single enforced quality-critical generation gateway is not yet implemented;
- Production Methodologist / Evolution Engineer are treated as an on-demand capability-gap sidecar until explicit trigger/scheduling wiring is complete.

Disposition: **GOVERNANCE-WIRED; CRITICAL REVIEW + GENERATION GATEWAY BLOCKERS EXPLICIT**.

## Routing behavior

For a material business next action, the universal dispatcher should now:

`owner/task -> owner capability manifest -> exact required capabilities -> current-session handshake -> readiness evaluator -> owner-native/chat-bridged/deterministic/isolated route -> execution receipt -> owner gate -> owner checkpoint`

It must not scan every capability on every turn. Only the capabilities required by the current authoritative `next_action` are handshaken.

## No-deployment mode

The user does not need to deploy every owner before GitHub orchestration becomes useful.

Where owner policy permits and the current ChatGPT window has the required tools, `CHAT_BRIDGED` execution may satisfy ordinary `SESSION_EXECUTABLE` work while preserving owner stage/schema/receipt boundaries.

It may **not** satisfy a gate requiring `ATTESTED_ISOLATED` execution. One model changing role labels is not proof of independent reviewers.

## Anti-bloat rule

A new named agent is not the default repair for a failure.

Before adding a permanent role, classify the missing function as:

- existing role responsibility;
- deterministic guard;
- stage capability;
- on-demand specialist sidecar;
- permanent operational agent.

A permanent agent is operational only if it has both an invocation/event path and an executor/evidence contract. Otherwise it remains `DECLARED_ONLY`.

## CI evidence

Initial execution-control-plane run `38016204633` correctly failed with `1 failed, 76 passed` because `HARNESS_STATUS.json` had accidentally lost previously persisted account-hook `acceptance_evidence` during an earlier status rewrite.

The fix restored the evidence rather than weakening the old regression test.

Final validation:

- GitHub Actions run: `38016256163`
- job: `114107069402`
- head: `ca865a831120d61039ffc347ede50aabd8899741`
- package: `universal-continuity-agent==3.7.0`
- pytest: **77 passed in 0.12s**
- conclusion: **success**

## Remaining boundary

This control plane can mechanically distinguish repository readiness from session readiness, but it cannot manufacture unavailable external executor substrates.

Therefore future business turns should use the handshake rather than global assumptions. Examples:

- GitHub file access does not imply the owner Python runtime is running;
- an image generator being available does not authorize bypassing an owner generation gateway;
- a single ChatGPT context does not become isolated merely because it adopts multiple reviewer roles;
- a missing strict capability blocks only the affected hard gate, not unrelated owner work.

## Result

The cross-agent problem is now managed as **Runtime/Harness Engineering**, not prompt proliferation.

The universal dispatcher has a shared executable standard for current and future GitHub business agents, while business logic and state remain owner-local.
