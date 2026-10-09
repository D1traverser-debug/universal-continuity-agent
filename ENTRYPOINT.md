# Universal Continuity — Entry Point

Status: ACTIVE
Contract: v3.5
Engineering authority: this repository `main`

## Critical startup boundary

GitHub and ChatGPT Library are durable storage/discovery surfaces; they are **not automatic event listeners** for a new chat.

Therefore bare commands such as `继承`, `继续`, or `恢复` require an account-level startup instruction that tells the new chat to invoke Universal Continuity. The canonical hook is documented in `STARTUP_HOOK.md`.

Without that hook, a new chat may answer from generic Memory/past-chat context and never query this repository. Such a response is `CONTINUITY_BOOTSTRAP_NOT_TRIGGERED`, not a successful continuity resume.

Do not claim bare-inherit end-to-end readiness merely because GitHub CI/discovery is healthy.

## Core model

Chat is an ephemeral execution window. Task is the durable object.

Universal Continuity owns only task discovery, routing, resume eligibility, compatibility, takeover lease semantics, human-readable task labeling, and recovery pointers. It does not duplicate domain business logic or domain state machines.

## Intent precedence

The durable principle `学习继承，任务不继承` applies to **NEW_TASK** only.

When the user's primary intent is an explicit continuation command such as `继承`, `继续`, `恢复`, `接着上次`, `继承：<任务名>`, or `继续：<任务名>`, classify as `CONTINUE` first and invoke Universal Continuity. Do not answer with a learning-only inheritance acknowledgement before attempting bootstrap.

## Task identity

Every durable USER task has two distinct identities:

- `task_id`: stable machine identity. It never changes because the user renames the task.
- `display_name_zh`: user-facing Chinese display name used in candidate lists and status reports.

If a durable USER task has no `display_name_zh`, ask once: `这个任务你希望用什么中文名？` Persist the answer, then continue the original work immediately. Do not ask for an extra confirmation to resume. Renaming only changes `display_name_zh`; it must not create a new task ID.

## New chat bootstrap

Once the account-level startup hook has routed the message here:

1. Classify `CONTINUE` vs `NEW_TASK`.
2. `NEW_TASK`: inherit durable learning only. Never import another task's stage, draft, blocker, or next action.
3. If the new work is durable/multi-step, establish stable `task_id`, owner and `display_name_zh`, then persist its checkpoint before deep work.
4. Bare `CONTINUE` such as `继承` with no exact task hint: execute `BARE_INHERIT_DISCOVERY.json` and query every required owner source before claiming how many recoverable tasks exist.
5. If any required source was not queried or failed, return `INCOMPLETE_DISCOVERY`; partial results may be shown only as incomplete and must never be described as the full list.
6. Explicit `CONTINUE` such as `继承：A股荐股` or `继续金融文章写作`: route directly to the matching owner/task first; a global scan is not required.
7. Once a task/owner is selected, exit global discovery and stay on the domain hot path.

## Bare inherit eligibility

A task may appear for plain `继承/继续` only if all are true:

- `task_class == USER`
- `resume_eligible == true`
- `resume_visibility == DEFAULT`
- status is `ACTIVE`, `WAITING`, or `BLOCKED`

`SYSTEM_INFRA`, `TEST`, `FIXTURE`, `EVAL`, `MIGRATION`, `PAUSED`, hidden, archived and explicit-only tasks are excluded.

## Bare inherit completeness

The authoritative required-source list lives in `BARE_INHERIT_DISCOVERY.json`.

A resolver may say “当前有 N 个默认可继承任务” only after all required sources have been queried successfully and candidates have been deduplicated by `task_id`.

If discovery is incomplete, it must say so. This is fail-closed behavior: inconsistent partial counts are worse than an explicit incomplete result.

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

## Performance invariant

Continuity must stay off the steady-state business hot path:

- account-level startup hook only routes explicit continuation intent; it does not scan tasks on ordinary new-chat messages;
- global discovery runs only on bare continuation, explicit re-inherit, task switch, or detected authority drift;
- bare discovery reads metadata/index surfaces only;
- full domain checkpoint loads only after owner/task selection;
- one-shot questions proceed without creating durable tasks or asking for a task name;
- if global continuity routing is unavailable but an exact domain task is known, the domain owner may recover it directly.

## Authority order

1. Compatible authoritative domain runtime/checkpoint.
2. Authoritative per-task/per-system manifest when the domain uses generic durable storage.
3. Universal Continuity pointer/cache.
4. Mirrors/history only as recovery evidence.
5. Chat memory is never execution authority.

Read next: `STARTUP_HOOK.md`, `PROTOCOL.md`, `CONTINUITY_CONTRACT.json`, `BARE_INHERIT_DISCOVERY.json`, `OWNER_ADAPTER_CONTRACT.json`, `OWNER_REGISTRY.json`, `NEW_CHAT_BOOTSTRAP.json`.
