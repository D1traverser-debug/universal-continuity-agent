---
name: universal-continuity
description: Resume durable cross-chat tasks from authoritative owner checkpoints with compatibility checks, single-writer takeover, visible pre-resume progress, and verified turn-level progress receipts.
---

# Universal Continuity Skill

This Skill is a thin capability map. It is **not** the engineering authority and must not duplicate the full protocol.

## Authority

Read, in order:

1. repository root `ENTRYPOINT.md`;
2. `CONTINUITY_CONTRACT.json`;
3. `PROGRESS_OBSERVABILITY_POLICY.json`;
4. `OWNER_REGISTRY.json`;
5. the exact owner manifest/checkpoint selected by the root protocol.

When media/research learning is involved, also follow `MEDIA_DISTILLATION_PROTOCOL.md` and `CONTINUOUS_LEARNING_POLICY.md`.

## Core execution

- Explicit `继承 / 继续 / 恢复` intent is CONTINUE, not NEW_TASK.
- Bare continuation must satisfy the complete required-owner discovery quorum before claiming a total.
- Named continuation routes to the exact owner/task first.
- Capture and surface **继承前进度** from authoritative persisted state before takeover mutation.
- Run compatibility before replaying executable state.
- Acquire and verify the single-writer lease for the selected task.
- Load context progressively: metadata -> short handoff -> exact artifacts -> selective history only if needed.
- Continue from the real `current_stage / next_action`.
- Before every final user-facing response on an active durable task, persist any material state change, re-read the authority, and report **进度提交** using `PROGRESS_OBSERVABILITY_POLICY.json`.
- If nothing material changed, do not create a heartbeat write; report `NO_MATERIAL_CHANGE` and the unchanged durable resume point.
- If persistence/verification fails, report it explicitly; never claim progress is safe for the next chat.

## Scope boundary

Owner repositories keep business logic. This Skill routes, verifies and resumes; it does not rewrite domain state machines.
