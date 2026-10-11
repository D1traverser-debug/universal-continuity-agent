# 2026 Global AI Skills Top10 — Distillation Library

Status: **COMPLETE_10_OF_10__PHASE_B_SELECTION_COMPLETE**
Selection/adoption: **SELECTION_COMPLETE__PRODUCTION_PROMOTION_REQUIRES_SEPARATE_REGRESSION_BACKED_CHANGE**
Owner: Universal Continuity maintenance / evolution research

## Purpose

This is a **research library first, architecture input second**. The ten Skills were captured at pinned source revisions, reverse-engineered beyond their marketing descriptions, normalized into one schema, and only then compared for selection.

The goal is not to copy prompts. The goal is to recover the underlying **workflow, methodology, control model, state model, tool model, evidence model, failure semantics, context strategy, human/agent decision split, portability constraints, implementation architecture, Harness model, and hidden design assumptions**.

## Phase A — complete library

For every Skill the pass:

1. pinned repository + source revision + exact files inspected;
2. inspected the Skill itself;
3. followed delegated/shared primitives when the Skill was only a thin wrapper;
4. inspected implementation/runtime when behavior lived outside Skill text;
5. inspected tests/evals/workflows/references when available;
6. captured documented complaints, failure modes and out-of-scope decisions;
7. normalized findings through `SCHEMA.md`;
8. recorded evidence gaps explicitly.

No final selection was made before 10/10 completion.

## Phase B — cross-skill comparison and selection

After all ten entries were complete:

- `CROSS_SKILL_PRIMITIVE_MATRIX.md` decomposed the ten Skills into comparable mechanisms;
- duplicate ideas under different names were merged conceptually;
- prompt-only methods were separated from mechanically enforced behavior;
- each mechanism was compared with current Universal/owner architecture;
- `PHASE_B_SELECTION.md` classified what is worth adapting, what is owner-local, what Universal already does more strongly, and what should be rejected.

Selection does **not** automatically mutate production authority. Promotion into Universal/owner runtime/policy/harness is a separate engineering change requiring the normal evidence/regression gates.

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

Cross-skill outputs:

- `SCHEMA.md`
- `INDEX.json`
- `CROSS_SKILL_PRIMITIVE_MATRIX.md`
- `PHASE_B_SELECTION.md`

## Evidence discipline

Popularity/install counts are discovery signals only. They do not prove correctness, safety, portability, or suitability.

The evidence order used for adoption decisions was:

1. original Skill source;
2. implementation/runtime source;
3. tests/evals/workflows;
4. original documentation and changelog/out-of-scope notes;
5. repository issue/PR evidence when needed;
6. leaderboard/community popularity only as context.

A documented behavior is not treated as mechanically enforced unless implementation/test evidence supports it. A test is not treated as live product outcome evidence. A source author's own warning is preserved rather than edited away.

## Key library-level finding

The Top10 does **not** support the simplistic rule “a good Skill is only a few lines.” It supports a more precise rule:

> A Skill can be extremely small **when the missing behavior has a stronger home** — a reusable primitive, executable runtime, workflow/state machine, progressive reference, repository configuration, or Harness.

`grill-me` and `grill-with-docs` demonstrate the upside and the fragility of thin prose delegation; their own documentation reports dependency-loading failures. `agent-browser` demonstrates the stronger form: a thin stable discovery Skill points to version-matched runtime-served instructions and is backed by explicit evals measuring loading, selection, command use and context footprint.

Therefore line count alone is not an architecture goal. **Responsibility placement + observable loading/execution + evidence** is the goal.
