---
name: universal-continuity
description: Resume durable cross-chat tasks from authoritative owner checkpoints with compatibility checks, single-writer takeover, visible pre-resume progress, and verified turn-level progress receipts.
---

# Universal Continuity Skill

This Skill is a thin capability map. It is **not** the engineering authority and must not duplicate the full protocol.

## Authority bootstrap

Always begin with exactly:

1. repository root `ENTRYPOINT.md`;
2. `CURRENT_PROTOCOL.json`.

Then follow the current `ENTRYPOINT.md` event-driven loading map. Do **not** maintain or preload a second fixed list of contracts, registries, policies, owner files, audits, or historical transcripts in this Skill. If the current protocol or entrypoint changes, this router delegates to that authority rather than pinning an older read order.

When an event activates media/research learning, maintenance, artifact handling, owner execution, architecture review, protocol reconciliation, or recovery, load only the exact authority surfaces named by the current `ENTRYPOINT.md` for that event.

## Core execution

- Explicit `继承 / 继续 / 恢复` intent is CONTINUE, not NEW_TASK.
- Bare continuation must satisfy the complete required-owner discovery quorum before claiming a total.
- Named continuation routes to the exact owner/task first.
- Capture and surface **继承前进度** from authoritative persisted state before takeover mutation.
- Run compatibility before replaying executable state.
- Acquire and verify the single-writer lease for the selected task.
- Load context progressively: bootstrap -> metadata -> short handoff -> exact artifacts -> selective history only if needed.
- Continue from the real `current_stage / next_action`.
- Before every final user-facing response on an active durable task, persist any material state change, re-read the authority, and report **进度提交** using the current repository authority.
- If nothing material changed, do not create a heartbeat write; report `NO_MATERIAL_CHANGE` and the unchanged durable resume point.
- If persistence/verification fails, report it explicitly; never claim progress is safe for the next chat.

## Scope boundary

Owner repositories keep business logic. This Skill routes, verifies and resumes; it does not rewrite domain state machines.
