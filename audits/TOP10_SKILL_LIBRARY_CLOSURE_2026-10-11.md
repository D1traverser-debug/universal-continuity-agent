# Top10 Skill Library Closure — 2026-10-11

Status: `DISTILLATION_COMPLETE_10_OF_10__PHASE_B_SELECTION_COMPLETE__PRODUCTION_PROMOTION_SEPARATE`

## User requirement

The initial rank-#1-only pass was insufficient because it selected a method before the rest of the comparison set was normalized. The corrected requirement was:

1. completely distill all ten Skills;
2. include workflow, methodology and additional non-obvious dimensions;
3. build one Skill library;
4. only after 10/10 completion, compare and select useful mechanisms.

## Completed library

Root: `research/skill-library/2026-global-ai-skills-top10/`

- `README.md`
- `SCHEMA.md`
- `INDEX.json`
- ten normalized Skill entries
- `CROSS_SKILL_PRIMITIVE_MATRIX.md`
- `PHASE_B_SELECTION.md`

The schema covers identity/provenance, purpose, activation, inputs/outputs, workflow, methodology, decision rights, state machine, durability, composition, Skill/Agent/Runtime/Harness placement, context engineering, concurrency/idempotency, safety, failures/recovery, eval/Harness, portability, cost/complexity, negative knowledge, hidden assumptions, neutral reusable primitives, cross-Skill links and evidence ceiling.

## Source set pinned

- `vercel-labs/skills@13e4063a1cf913f5606d57d42ab83a86f5001e04`
- `mattpocock/skills@49dd158d1076134a641b33efb035946536778336`
- `vercel-labs/agent-browser@d9570915f4dd6504dee4070379d2c4f79d81dbb2`
- `anthropics/skills@dbd4588f9e1033efb41dad4bef2f7947c8993d44`

Popularity/install rank was retained as discovery context only and was not used as a quality proof.

## Major synthesis

The library rejects the simplistic conclusion that “excellent Skills are only a few lines.” The stronger architecture finding is:

> A Skill can be tiny when behavior has a stronger owner: reusable primitive, executable/runtime-versioned instruction surface, workflow/state machine, progressive references, repository configuration, or Harness.

`grill-me` and `grill-with-docs` show both the elegance and fragility of thin prose delegation: their own source documentation reports dependency-loading failures. `agent-browser` shows the stronger implementation: thin discovery Skill + runtime-versioned live Skill content + executable runtime + context-footprint/behavior evals.

## Phase B selections

Strong cross-agent candidates:

- capability reuse-before-build funnel (`find-skills`);
- facts-vs-decisions and bounded decision frontier (`grilling`);
- payoff-weighted architecture scan/deletion test (`improve-codebase-architecture`);
- runtime-versioned Skill delivery, context-footprint measurement, session isolation, `outcome_unknown`, final-state eval (`agent-browser`);
- evidence seam / independent expected truth / tracer bullet (`tdd`);
- inspect → default → ask only genuine choices / evidence-gated complexity (`setup-matt-pocock-skills`);
- verify-before-clarify, durable agent-ready brief, negative institutional memory (`triage`).

Owner-local only:

- `frontend-design` creative/visual methodology.

Reference-only because current Universal is already stronger:

- `handoff` context recovery.

Explicit rejects include fixed popularity thresholds as hard gates, global install by default, prose-only dependency invocation as proof, chat-only durable state, prompt-only chronology claims, same-actor self-review as independent assurance, mandatory CDN report infrastructure, fixed question counts and copying all Top10 rules into startup/Skill context.

## Validation

`tests/test_top10_skill_distillation_library.py` mechanically requires:

- 10 unique entries/ranks;
- every normalized entry exists;
- source heads are pinned;
- schema/matrix/selection files exist;
- no final entry remains `PENDING_PHASE_B`;
- complete-before-selection rule remains explicit.

GitHub Actions run `38110768456`: `SUCCESS`.

## Assurance boundary

This closure proves the **library process and source normalization structure are present and regression-guarded**. It does not prove:

- every source Skill is high quality;
- leaderboard popularity predicts quality;
- selected primitives improve Universal or owner live outcomes;
- production promotion has occurred;
- future upstream Skill revisions behave the same.

Production promotion is a separate engineering change and must modify existing authorities/runtime/harness only when the selected primitive closes a real gap with regression evidence. No new permanent Top10 supervisory Agent or root policy is admitted by this research event.
