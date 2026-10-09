# Universal Continuity — Entry Point

Status: ACTIVE
Contract: v3.3
Engineering authority: this repository `main`

## Core model

Chat is an ephemeral execution window. Task is the durable object.

Universal Continuity owns only task discovery, routing, resume eligibility, compatibility, takeover lease semantics, human-readable task labeling, and recovery pointers. It does not duplicate domain business logic or domain state machines.

## Task identity

Every durable USER task has two distinct identities:

- `task_id`: stable machine identity. It never changes because the user renames the task.
- `display_name_zh`: user-facing Chinese display name used in candidate lists and status reports.

If a durable USER task has no `display_name_zh`, ask once: `这个任务你希望用什么中文名？` Persist the answer, then continue the original work immediately. Do not ask for an extra confirmation to resume. Renaming only changes `display_name_zh`; it must not create a new task ID.

## New chat bootstrap

On the first substantive message of a new chat:

1. Classify `CONTINUE` vs `NEW_TASK`.
2. `NEW_TASK`: inherit durable learning only. Never import another task's stage, draft, blocker, or next action.
3. If the new work is durable/multi-step, establish stable `task_id`, owner and `display_name_zh`, then persist its checkpoint before deep work.
4. `CONTINUE`: resolve resumable USER tasks through registered owner adapters and authoritative task manifests/checkpoints. If the recovered USER task lacks `display_name_zh`, perform the one-time naming handshake before substantive work.
5. Once a task/owner is selected, exit global discovery and stay on the domain hot path.

## Bare inherit eligibility

A task may appear for plain `继承/继续` only if all are true:

- `task_class == USER`
- `resume_eligible == true`
- `resume_visibility == DEFAULT`
- status is `ACTIVE`, `WAITING`, or `BLOCKED`

`SYSTEM_INFRA`, `TEST`, `FIXTURE`, `EVAL`, `MIGRATION`, hidden and explicit-only tasks are excluded.

## Candidate behavior

- Candidate UI prefers `display_name_zh`; falls back to `title` only when an old task has not yet completed its naming handshake.
- One strong eligible candidate: resume directly.
- Multiple candidates: show at most five metadata-only choices; do not merge them.
- Explicit semantic hint such as `继续小说` or `继续荐股`: route to the matching domain/owner first.
- No trustworthy state: fail closed rather than reconstruct executable state from chat guesswork.

## Single-writer takeover

The user's workflow is single-active-chat per task.

When a task is inherited into a new chat:

1. Read the authoritative task manifest/checkpoint.
2. Increment `resume_epoch` and acquire a new `active_lease`.
3. Persist using the storage owner's compare-and-swap/version guard when available.
4. Re-read and verify the new lease before substantive work.
5. The old chat is retired. A stale lease must not checkpoint.

Different tasks may proceed independently in different chats.

## Compatibility before resume

Every resumed task must be classified as one of:

- `COMPATIBLE`: resume normally.
- `MIGRATABLE`: migrate to the current contract, then resume.
- `INCOMPATIBLE`: do not replay obsolete execution semantics; preserve only still-valid requirements/evidence/artifacts.
- `UNKNOWN`: fail closed until authority is resolved.

## Checkpoint triggers

Checkpoint on material execution changes, including:

- goal/constraint/authorization changes;
- stage or next-action changes;
- important decisions;
- `display_name_zh` assignment or rename;
- completed material work batches;
- key artifact changes;
- blocker/waiting changes;
- owner/contract/runtime changes;
- task switch;
- before/after long or high-risk tool chains;
- pause/complete/archive/reopen;
- interruption risk.

Checkpoint the latest execution truth, not a transcript.

## Performance invariant

Continuity must stay off the steady-state business hot path:

- global discovery runs only on the first substantive message, explicit re-inherit, task switch, or detected authority drift;
- candidate discovery uses metadata first;
- full domain checkpoint loads only after owner/task selection;
- one-shot questions proceed without creating durable tasks or asking for a task name;
- if global continuity routing is unavailable but an exact domain task is known, the domain owner may recover it directly.

## Authority order

1. Compatible authoritative domain runtime/checkpoint.
2. Authoritative per-task/per-system manifest when the domain uses generic durable storage.
3. Universal Continuity pointer/cache.
4. Mirrors/history only as recovery evidence.
5. Chat memory is never execution authority.

Read next: `PROTOCOL.md`, `CONTINUITY_CONTRACT.json`, `OWNER_ADAPTER_CONTRACT.json`, `NEW_CHAT_BOOTSTRAP.json`.
