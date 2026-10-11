# 2026 Global AI Skills Top10 — Distillation Library

Status: COLLECTION_AND_DISTILLATION_IN_PROGRESS
Selection/adoption: FROZEN_UNTIL_10_OF_10_COMPLETE
Owner: Universal Continuity maintenance / evolution research

## Purpose

This is a **research library first, architecture input second**. The ten Skills are captured at pinned source revisions, reverse-engineered beyond their marketing descriptions, and normalized into one schema before any cross-skill adoption decision is made.

The goal is not to copy prompts. The goal is to recover the underlying **workflow, methodology, control model, state model, tool model, evidence model, failure semantics, context strategy, human/agent decision split, portability constraints, and hidden design assumptions**.

## Two-phase rule

### Phase A — Complete the library

For every Skill:

1. pin repository + source revision + exact files inspected;
2. inspect the Skill itself;
3. follow delegated/shared primitives when the Skill is only a thin wrapper;
4. inspect implementation/runtime when behavior lives outside the Skill text;
5. inspect tests/evals/workflows/references when available;
6. capture documented complaints, failure modes and out-of-scope decisions;
7. distill into the common schema in `SCHEMA.md`;
8. record evidence gaps explicitly.

During Phase A, **no final ADOPT / REJECT / MERGE decision is allowed**. A local observation may note an interesting primitive, but it is not promoted into Universal authority yet.

### Phase B — Compare and select

Only after all ten entries are complete:

- build a cross-skill primitive matrix;
- detect duplicated ideas under different names;
- separate complementary mechanisms from mutually exclusive ones;
- compare against the existing Universal/owner architecture;
- identify missing capabilities, bloat risks and replacement opportunities;
- choose what to adopt, adapt, merge, reject, or leave as reference;
- apply changes only after regression/eval design exists.

## Library entries

1. `01-find-skills.md`
2. `02-grill-me.md`
3. `03-grill-with-docs.md`
4. `04-improve-codebase-architecture.md`
5. `05-agent-browser.md`
6. `06-tdd.md`
7. `07-setup-matt-pocock-skills.md`
8. `08-frontend-design.md`
9. `09-handoff.md`
10. `10-triage.md`

`INDEX.json` is the machine-readable progress/source manifest.

## Evidence discipline

Popularity/install counts are discovery signals only. They do not prove correctness, safety, portability, or suitability.

The strongest source order is:

1. original Skill source;
2. implementation/runtime source;
3. tests/evals/workflows;
4. original documentation and changelog/out-of-scope notes;
5. repository issue/PR evidence when needed;
6. leaderboard/community popularity only as context.

A documented behavior is not treated as mechanically enforced unless implementation/test evidence supports it. A test is not treated as live product outcome evidence. A source author's own warning is preserved rather than edited away.
