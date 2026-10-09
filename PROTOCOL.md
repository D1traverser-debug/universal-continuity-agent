# Universal Continuity Protocol v3.2

## Scope
Universal Continuity handles cross-chat task discovery, routing, resume eligibility, compatibility and checkpoint pointers. Domain agents retain their own business logic and state machines.

## Task identity
A durable task has a stable task ID independent from any chat ID. A task can span multiple chats. After successful takeover, the prior chat is retired for that task.

## New work
New work inherits durable learning, not another task's unfinished stage, draft, blocker or next action. Multi-step work expected to span chats should persist identity/checkpoint before deep execution.

## Resume discovery
Plain continuation considers only USER tasks that are resumable, default-visible and ACTIVE/WAITING/BLOCKED. Infrastructure, test, fixture, eval and migration tasks require explicit targeting.

Discovery order:
1. registered domain-owner resumable metadata;
2. generic durable tasks when no stronger owner exists;
3. legacy persistent evidence only when the first two layers cannot resolve the task.

## Semantic routing
When the user names a task/domain/topic, query that owner first. One strong match resumes directly. Multiple strong matches return a compact metadata list; checkpoints are never merged.

## Owner adapter contract
Each owner must provide equivalent capabilities for resumable metadata discovery, exact task checkpoint read, class/status/visibility metadata, compatibility check and legal resume/migrate/block behavior. Legacy missing metadata fails closed.

## Compatibility
Before resume, classify persisted execution state:
- COMPATIBLE: resume normally.
- MIGRATABLE: migrate to the current contract, then resume.
- INCOMPATIBLE: do not replay stale stages/gates; retain only still-valid requirements, evidence and artifacts.
- UNKNOWN: do not replay executable state until authority is resolved.

## Single active writer
New-chat takeover creates a new resume epoch and writer lease. Prior lease holders become stale. Checkpoint writes must validate the current lease/epoch and use the storage owner's version guard when available. Different tasks may proceed independently in different chats.

## Registries
Global task/system registries are rebuildable caches, not execution authority. A stale cache never overrides a fresher owner checkpoint.

## Checkpoint discipline
Checkpoint material state changes rather than every message. A useful checkpoint carries current stage, exact next action, blockers, authority/version context and key artifact references.

## New system bootstrap
Unknown recurring domains begin under GENERIC_HANDOFF only as a bootstrap. Once a domain becomes recurring, rule-heavy or executable, create a dedicated domain owner/home and leave Universal Continuity as routing infrastructure.

## Degraded mode
One-shot work proceeds even if continuity storage is unavailable. Exact known-domain tasks may recover directly from their owner. Unknown old-state recovery fails closed rather than guessing. Cross-chat durability is only claimed after persistence succeeds.

## Performance
Global discovery runs only at new-chat bootstrap, explicit re-inherit, task switch or detected authority drift. After owner selection, work stays on the domain path.

## Engineering authority
The universal resolver, contract, tests, templates and CI live in this repository. Business agents implement adapters/checkpoints and do not fork the universal resolver.
