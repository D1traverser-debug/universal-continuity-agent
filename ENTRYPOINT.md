# Universal Continuity — Entry Point

Status: ACTIVE
Contract: v3.7
Engineering authority: this repository `main`

## Critical startup boundary

GitHub and ChatGPT Library are durable storage/discovery surfaces; they are **not automatic event listeners** for a new chat.

Therefore bare commands such as `继承`, `继续`, or `恢复` require an account-level startup instruction that tells the new chat to invoke Universal Continuity. The canonical hook is documented in `STARTUP_HOOK.md`.

Without that hook, a new chat may answer from generic Memory/past-chat context and never query this repository. Such a response is `CONTINUITY_BOOTSTRAP_NOT_TRIGGERED`, not a successful continuity resume.

## Core model

Chat is an ephemeral execution window. Task is the durable object.

Universal Continuity owns task discovery, routing, resume eligibility, compatibility, takeover lease semantics, human-readable task labels, progress observability and recovery pointers. It does not duplicate domain business logic or domain state machines.

## Intent precedence

The durable principle `学习继承，任务不继承` applies to **NEW_TASK** only.

When the user's primary intent is an explicit continuation command such as `继承`, `继续`, `恢复`, `接着上次`, `继承：<任务名>`, or `继续：<任务名>`, classify as `CONTINUE` first and invoke Universal Continuity.

## Task identity

Every durable USER task has two distinct identities:

- `task_id`: stable machine identity. It never changes because the user renames the task.
- `display_name_zh`: user-facing Chinese display name used in candidate lists and status reports.

If a durable USER task has no `display_name_zh`, ask once: `这个任务你希望用什么中文名？` Persist the answer, then continue the original work immediately.

## New chat bootstrap

Once the account-level startup hook has routed the message here:

1. Classify `CONTINUE` vs `NEW_TASK`.
2. Bare `CONTINUE`: execute `BARE_INHERIT_DISCOVERY.json`; query every required owner source before reporting a total count.
3. Named `CONTINUE`: route directly to the matching owner/task first.
4. Read the exact authoritative task manifest plus short owner handoff/checkpoint.
5. Capture the **pre-takeover persisted state** and surface a `继承前进度` receipt according to `PROGRESS_OBSERVABILITY_POLICY.json`.
6. Resolve compatibility.
7. Acquire/verify the new writer lease for same-task takeover.
8. Load only the exact referenced artifacts needed for the current `next_action`.
9. Continue from the real `current_stage / next_action`.

The pre-resume receipt must be captured before `resume_epoch` / `active_lease` is mutated. It should tell the user where the previous durable checkpoint actually stopped, including stage, next action and any blocker/waiting state.

If any required bare-inherit source fails, return `INCOMPLETE_DISCOVERY`; never present partial results as the authoritative total.

## Progressive recovery

Follow `CONTEXT_RECOVERY_POLICY.json`.

Default context load order:

1. metadata/index/manifest;
2. short authoritative HANDOFF/checkpoint;
3. exact artifact refs needed for the next action;
4. selective owner search/history only for a concrete gap;
5. old conversation transcript as last-resort recovery evidence.

Do not preload the entire old conversation simply because a large context window exists.

A HANDOFF is current execution truth, not a transcript summary. If a spec, plan, issue, commit, diff, artifact or domain rule already exists elsewhere, reference it instead of copying it into the handoff.

## Progress observability

Follow `PROGRESS_OBSERVABILITY_POLICY.json`.

### Resume Progress Receipt

Once an exact task has been selected and its authoritative checkpoint is known, show **继承前进度** before substantive resumed work. The receipt is a snapshot of the durable state that existed before this chat took over; do not rewrite history with the new lease epoch.

### Turn Commit Receipt

For every final user-facing response while a durable task is active, report **进度提交** with one of:

- `COMMITTED`: material progress was persisted and authoritative state was re-read/verified;
- `NO_MATERIAL_CHANGE`: this turn did not change the durable resume point, so no meaningless heartbeat write was created;
- `COMMIT_FAILED`: material progress should have been persisted but the write or verification failed; explicitly warn that the new progress may not survive the next chat;
- `STALE_WRITER`: this chat no longer owns the writer lease and must not checkpoint;
- `NOT_APPLICABLE`: no durable task is active.

A successful tool call is not enough to claim `COMMITTED`; authoritative re-read verification is required.

## Task topology

- Same goal, same work: keep the same task identity.
- Same goal, fresh context preferred: handoff and take over the same task in the new chat.
- Temporary side question: do not mutate durable stage by default.
- Materially different major branch that must coexist: create a child task with `parent_task_id`.
- Independent work: create a new task and inherit durable learning only.

Opening a new chat does not itself create a new task.

## Bare inherit eligibility

A task may appear for plain `继承/继续` only if all are true:

- `task_class == USER`
- `resume_eligible == true`
- `resume_visibility == DEFAULT`
- status is `ACTIVE`, `WAITING`, or `BLOCKED`

`SYSTEM_INFRA`, `TEST`, `FIXTURE`, `EVAL`, `MIGRATION`, `PAUSED`, hidden, archived and explicit-only tasks are excluded.

An explicitly named `SYSTEM_INFRA` task may be resumed only when it is `resume_eligible == true` and `resume_visibility == EXPLICIT_ONLY`; this never makes it a bare-inherit candidate.

## Candidate behavior

- Candidate UI prefers `display_name_zh`; falls back to `title` only for legacy unnamed tasks.
- One strong eligible candidate: resume directly.
- Multiple candidates: show at most five metadata-only choices; do not merge them.
- Explicit semantic hint routes to the matching domain owner first.
- No trustworthy state: fail closed rather than reconstruct executable state from chat guesswork.

## Single-writer takeover

When a task is inherited into a new chat:

1. Read the authoritative task manifest/checkpoint.
2. Capture the pre-takeover progress receipt.
3. Increment `resume_epoch` and acquire a new `active_lease`.
4. Persist using the storage owner's compare-and-swap/version guard when available.
5. Re-read and verify the new lease before substantive work.
6. The old chat is retired. A stale lease must not checkpoint.

The canonical epoch lives at top-level `resume_epoch`. Older/current owner manifests may omit a duplicate nested `active_lease.resume_epoch`; the harness must tolerate that and use the top-level epoch.

Different tasks may proceed independently in different chats.

## Compatibility before resume

Every resumed task must be classified as one of:

- `COMPATIBLE`: resume normally.
- `MIGRATABLE`: migrate to the current contract, then resume.
- `INCOMPATIBLE`: do not replay obsolete execution semantics; preserve only still-valid requirements/evidence/artifacts.
- `UNKNOWN`: fail closed until authority is resolved.

## Continuous learning

Follow `CONTINUOUS_LEARNING_POLICY.md` and `MEDIA_DISTILLATION_PROTOCOL.md`.

Continuity should proactively study relevant agent systems, Skills, harnesses, durable-execution patterns, official product documentation and media when maintaining the system or when a real failure exposes a gap. Do not put broad research on the ordinary business hot path.

External advice is input, not authority. Important product claims require current first-party verification; media evidence levels remain distinct. Accepted learning must be encoded in the smallest appropriate policy/Skill/runtime surface and mechanically tested when testable.

## Performance invariant

Continuity must stay off the steady-state business hot path:

- the startup hook only reacts to explicit continuation intent;
- global discovery runs only when needed;
- discovery reads metadata only;
- recovery reads a short handoff before deeper artifacts;
- progress receipts do not trigger new global scans;
- no material state change means no heartbeat checkpoint write;
- proactive research runs during maintenance/gap resolution, not every business turn;
- old chat history is a last resort;
- one-shot questions do not create durable tasks or trigger task-name prompts.

## Authority order

1. Compatible authoritative domain runtime/checkpoint.
2. Authoritative per-task/per-system manifest when generic durable storage is used.
3. Universal Continuity pointer/cache.
4. Mirrors/history only as recovery evidence.
5. Chat memory is never execution authority.

Read next: `STARTUP_HOOK.md`, `PROTOCOL.md`, `CONTINUITY_CONTRACT.json`, `BARE_INHERIT_DISCOVERY.json`, `CONTEXT_RECOVERY_POLICY.json`, `PROGRESS_OBSERVABILITY_POLICY.json`, `CONTINUOUS_LEARNING_POLICY.md`, `MEDIA_DISTILLATION_PROTOCOL.md`, `OWNER_ADAPTER_CONTRACT.json`, `OWNER_REGISTRY.json`, `NEW_CHAT_BOOTSTRAP.json`.
