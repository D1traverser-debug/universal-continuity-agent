# Universal Continuity Protocol v3.6

## Scope
Universal Continuity handles cross-chat task discovery, routing, resume eligibility, compatibility, user-facing task naming, writer takeover and checkpoint pointers. Domain agents retain their own business logic and state machines.

## Startup trigger
Universal Continuity is not automatically invoked merely because its files exist in GitHub or ChatGPT Library. A new chat needs an account-level startup instruction that maps explicit continuation intent (`继承`, `继续`, `恢复`, `接着上次`, or a named continuation command) to this bootstrap. Canonical wording and acceptance criteria live in `STARTUP_HOOK.md`.

If that trigger is absent, a generic memory-based response is not a Continuity success. Record it as `CONTINUITY_BOOTSTRAP_NOT_TRIGGERED`.

The principle `学习继承，任务不继承` applies to NEW_TASK classification. It must not suppress an explicit continuation command. Continuation intent has routing precedence.

## Task identity
A durable task has a stable `task_id` independent from any chat ID and a user-facing `display_name_zh`. The task ID is the machine identity; the Chinese display name is for the user. Renaming must never create a new task or break checkpoint history. A task can span multiple chats. After successful takeover, the prior chat is retired for that task.

If a durable USER task lacks `display_name_zh`, ask the user once which Chinese name they want, persist it, and immediately continue the original work. One-shot work does not need a task name.

## New work and task topology
New work inherits durable learning, not another task's unfinished stage, draft, blocker or next action.

Classify task topology before mutating durable state:
- `CONTINUE_SAME_GOAL`: same durable task and goal; keep the same task identity.
- `FRESH_HANDOFF_SAME_GOAL`: same durable task but a fresh chat/context is preferable; take over the same task after checkpoint/compatibility/lease verification.
- `SIDE_QUERY`: answer a temporary side question without changing durable stage/next_action unless the answer materially changes the task.
- `FORK_CHILD_TASK`: a materially different major goal that should coexist with the original work gets a new child task with `parent_task_id`.
- `NEW_TASK`: a genuinely independent work unit gets a new task identity and inherits learning only.

Do not create a new task merely because the user opened a new chat.

## Bare inherit discovery quorum
Plain `继承/继续/恢复` without an exact task hint is a global discovery operation after the startup trigger fires. It MUST follow `BARE_INHERIT_DISCOVERY.json`.

Before reporting a total number of recoverable tasks, the resolver must query every required bare-inherit source listed in that policy, deduplicate by `task_id`, and apply the default USER predicate.

If any required source is unavailable or was not queried, the result is `INCOMPLETE_DISCOVERY`. Partial candidates may be shown only when clearly labeled incomplete. A partial list must never be described as “全部任务”, “一共 N 个”, or otherwise presented as the authoritative total.

## Resume discovery
Plain continuation considers only USER tasks that are resumable, default-visible and ACTIVE/WAITING/BLOCKED. Infrastructure, test, fixture, eval, migration, paused, hidden and archived tasks are excluded.

For bare continuation, discovery is quorum-based rather than best-effort. For an explicit semantic hint such as `继承：A股荐股`, the resolver may route directly to the matching owner and exact task without scanning unrelated owners.

## Progressive context recovery
Recovery MUST follow `CONTEXT_RECOVERY_POLICY.json`.

The default load order is:
1. task metadata/index/manifest;
2. short authoritative handoff/checkpoint;
3. only the exact artifacts referenced by the handoff and required for `next_action`;
4. selective owner search/history to resolve concrete ambiguity;
5. old conversation transcript only as last-resort recovery evidence.

A large context window is capacity, not a reason to preload everything. The goal is the smallest working set that preserves correctness.

### Handoff contract
A handoff is a compact execution-state document, not a compressed transcript.

It should carry current truth such as:
- task identity and owner;
- current status/stage;
- exact next action;
- blockers/waiting state;
- authority/contract/runtime context;
- stable artifact references needed to verify and execute the next action;
- only recent material decisions that are not already authoritative elsewhere.

Do not copy full specs, plans, issues, commits, diffs, research corpora or unchanged domain rules into the handoff when they already exist as addressable artifacts. Reference them.

If a summary conflicts with an authoritative artifact, the artifact wins.

## Semantic routing
When the user names a task/domain/topic, query that owner first. Candidate lists prefer `display_name_zh` and fall back to `title`. One strong eligible candidate resumes directly. Multiple strong matches return a compact metadata list; checkpoints are never merged.

## Owner adapter contract
Each owner must provide equivalent capabilities for resumable metadata discovery, exact task checkpoint read, class/status/visibility metadata, compatibility check and legal resume/migrate/block behavior. Persisted USER tasks should expose `display_name_zh`; missing names trigger the one-time naming handshake rather than a guessed permanent label. Legacy missing execution metadata still fails closed.

Owners should expose concise checkpoint/handoff state and stable artifact references rather than forcing the universal layer to preload their full history.

## Compatibility
Before resume, classify persisted execution state:
- COMPATIBLE: resume normally.
- MIGRATABLE: migrate to the current contract, then resume.
- INCOMPATIBLE: do not replay stale stages/gates; retain only still-valid requirements, evidence and artifacts.
- UNKNOWN: do not replay executable state until authority is resolved.

## Single active writer
New-chat takeover creates a new resume epoch and writer lease. Prior lease holders become stale. Checkpoint writes must validate the current lease/epoch and use the storage owner's version guard when available. Different tasks may proceed independently in different chats.

## Registries
Global task/system registries are rebuildable caches, not execution authority. A stale cache never overrides a fresher owner checkpoint. Cache entries may include `display_name_zh` for fast user-facing candidate rendering.

## Checkpoint discipline
Checkpoint material state changes rather than every message. A useful checkpoint carries current stage, exact next action, blockers, authority/version context, `display_name_zh` and key artifact references.

Checkpoint the latest execution truth. Do not checkpoint the entire conversation.

## Context health
Do not hard-code a fixed token threshold as a continuity invariant. External heuristics such as a “150K smart zone” may be useful observations, but they are not durable system rules.

Prefer a fresh handoff when the current chat has accumulated contradictory branches, obsolete plans, authority changes or enough historical material that the next action can no longer be stated compactly. A user may also explicitly request a clean new chat.

## Media/research distillation
When external videos, articles, talks or community guidance are used to evolve Continuity, follow `MEDIA_DISTILLATION_PROTOCOL.md`.

Keep evidence levels separate. A complete transcript proves full spoken-content coverage; it does not prove full visual review. Important product claims that affect the system should be checked against current first-party documentation before adoption.

External advice is input, not authority. Adopt only principles that fit Continuity's scope and survive verification.

## Verification
Verification depth should match the change:
- low-risk reversible documentation/state change: targeted checks;
- contract/router/discovery change: targeted regressions plus cross-owner invariants;
- authority/persistence/takeover change: the full relevant Continuity harness and end-to-end acceptance where available.

Do not run broad unrelated tests merely because they exist.

## Degraded mode
One-shot work proceeds even if continuity storage is unavailable. Exact known-domain tasks may recover directly from their owner. Unknown old-state recovery fails closed rather than guessing. A bare inherit with an unavailable required owner returns `INCOMPLETE_DISCOVERY` instead of inventing a total count. A continuation command that never reaches the bootstrap must be reported as `CONTINUITY_BOOTSTRAP_NOT_TRIGGERED`, not silently converted into learning-only inheritance.

## Performance
The account-level startup hook is intent-gated: ordinary new-chat messages do not cause a task scan. Global discovery runs only after explicit continuation intent, explicit re-inherit, task switch or detected authority drift. After owner selection, work stays on the domain path.

Bare inherit reads metadata/index surfaces only. Resume reads a short handoff before deep artifacts. Old chat history is loaded only when stronger durable state is insufficient.

## Engineering authority
The universal resolver, contract, startup-hook contract, discovery policy, context-recovery policy, media-distillation protocol, tests and CI live in this repository. Business agents implement adapters/checkpoints and do not fork the universal resolver.
