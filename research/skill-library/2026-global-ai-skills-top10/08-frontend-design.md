# 08 — `frontend-design`

Selection status: **PENDING_10_OF_10_SYNTHESIS**
Distillation status: **COMPLETE_SOURCE_NORMALIZATION**

## A. Identity and evidence provenance

- Source: `anthropics/skills`
- Pinned HEAD: `dbd4588f9e1033efb41dad4bef2f7947c8993d44`
- Skill: `skills/frontend-design/SKILL.md`
- Skill blob: `a5333457c414d20d625f307df945842c0952ecc3`
- Repository/model-migration material mentioning frontend-design prompt behavior was inspected as contextual evidence, but no dedicated frontend-design eval Harness was located in this pass.

## B. Problem model and intended outcome

Problem: generated interfaces converge on recognizable template defaults—same palettes, cards, typography tricks, layout chrome and motion—rather than expressing the actual subject, audience and job of the product.

Desired outcome:
- derive design direction from subject matter;
- make deliberate visual decisions rather than accept model defaults;
- critique the design plan before coding;
- spend visual boldness selectively;
- retain usability/accessibility quality floor;
- treat interface copy as part of design.

Architectural role: **creative design methodology/instruction Skill**, not a deterministic design-system runtime.

## C. Activation and invocation model

Use when building new UI or materially reshaping existing UI where aesthetic direction matters.

If brief lacks subject/audience/job, the agent should propose them and confirm before designing.

The Skill is not mainly for tiny mechanical styling edits where design direction is already fixed.

Stop rule is qualitative: after plan, brief-specific critique, implementation and iterative self-critique reach an acceptable design. No deterministic closure gate is defined.

## D. Inputs, outputs, side effects

Inputs:
- product/subject brief;
- audience;
- primary job/use case;
- user/client preferences/context;
- real content when available;
- existing UI/code if reshaping.

Outputs:
- compact design plan/token direction;
- color palette;
- typography roles;
- layout concept/ASCII wireframes;
- design principles;
- implementation code;
- screenshots/self-critique where environment supports it;
- interface copy/content decisions.

## E. End-to-end workflow

### F0 — Ground in subject

Identify what the product is, who it serves and what the page/interface must accomplish.

Do not begin from a generic aesthetic moodboard.

### F1 — Extract subject-specific visual material

Use industry, physical/material references, vernacular, content and audience as design sources.

The method asks: what would make this project visually unlike an unrelated project?

### F2 — Build compact design plan

Before code, define:
- 4–6 named colors with hex values;
- typefaces and roles;
- type scale/weights/widths/spacing;
- layout concept and alignment;
- ASCII wireframe(s);
- high-level principles that make this specific.

### F3 — Counterfactual genericity review

Review each plan element against the brief:
- would this same choice appear in a generic answer to a similar prompt?
- is it one of the model's habitual defaults rather than evidence from this brief?

If yes, revise and state what changed and why.

This is a **pre-implementation anti-template critique gate**.

### F4 — Build

Implement the revised plan, paying attention to CSS specificity and accidental style cancellation.

### F5 — Self-critique visually

Where tools allow, take screenshots and inspect rendered result rather than judging only source code.

### F6 — Restraint pass

“Spend boldness in one place.” Remove decorations that do not serve brief. Maintain responsive/accessibility/reduced-motion baseline.

### F7 — Copy pass

Check that words help users understand/act:
- plain user-facing vocabulary;
- active voice;
- consistent action names;
- actionable errors;
- useful empty states;
- no decorative filler.

## F. Core methodology / mental model

### Subject-matter-grounded aesthetics

Distinctive design comes from the object's world rather than generic design trends.

### Defaults are hypotheses, not neutral

The Skill explicitly names recurring AI-generated visual clusters so the model can recognize its own priors.

### Counterfactual uniqueness test

Ask whether the same plan would emerge for another similar prompt. If so, redesign the unconstrained axes.

### Planned intentionality

Palette/type/layout/principles are chosen before coding.

### One memorable gesture

Concentrate visual risk/boldness rather than scatter novelty everywhere.

### Structure encodes information

Borders, numbers, labels, eyebrow text and dividers must communicate hierarchy/sequence/state, not be decorative reflexes.

### Copy as interface design

Language consistency and action naming are navigation infrastructure.

## G. Decision-rights model

User/brief:
- explicit visual direction wins;
- product/audience/job constraints are authoritative.

Agent:
- fills open design axes;
- proposes subject/audience when missing;
- chooses/revises aesthetic direction;
- performs self-critique.

Rendered UI/user response:
- should provide evidence during screenshot/review iteration, but no external reviewer is required by the Skill.

Potential self-reference problem: same model designs and judges distinctiveness.

## H. State machine and lifecycle

Implicit lifecycle:

`BRIEF → SUBJECT_GROUNDED → DESIGN_PLAN → GENERICITY_REVIEW → REVISED_PLAN → BUILD → RENDER/CRITIQUE → RESTRAINT/COPY PASS → DONE`

No durable state machine or explicit evidence receipt.

Re-entry naturally occurs if screenshot critique reveals weakness.

## I. Memory, durability, provenance

Durability is primarily code/design artifacts.

The Skill suggests keeping notes about prior attempts if a memory surface exists, to avoid repeating itself in future designs, but does not prescribe a standard durable file/schema.

No provenance model binds a visual decision back to the specific brief rationale.

## J. Composition and dependency graph

No mandatory delegated Skill/runtime identified in the inspected main Skill.

Relies on:
- coding environment;
- optional screenshot/rendering tools;
- fonts/assets/framework chosen for project.

The methodology could be invoked by broader website/app-building agents.

## K. Skill / Agent / Runtime / Harness architecture

Behavior lives overwhelmingly in `SKILL.md` as creative instructions.

No dedicated deterministic runtime, design state machine or frontend-design-specific eval Harness was observed.

The Skill uses model self-critique as its primary reviewer.

This is structurally different from `agent-browser`, where Skill is merely a router into runtime + evals.

## L. Context engineering and progressive disclosure

The Skill is relatively monolithic because the design principles themselves are the capability.

It uses **procedural compression** rather than many references:
- subject grounding;
- plan;
- genericity critique;
- build;
- critique.

The source repository's model-migration material notes newer models may require less anti-generic prompting, highlighting model-version sensitivity and potential future prompt slimming.

## M. Concurrency, isolation, idempotency, replay

No concurrency protocol.

Potential multi-agent risk: parallel designers could overwrite same code unless external worktree/process isolation exists.

No anti-replay mechanism for aesthetic defaults, though suggested memory of prior experiments is intended to reduce repetition.

## N. Safety and trust boundaries

Not a security-focused Skill.

Quality/safety floor includes:
- responsive mobile behavior;
- visible keyboard focus;
- reduced motion;
- visual accessibility/harmonious colors.

No explicit accessibility test Harness observed; these are instruction-level requirements.

If memory is used for client preferences, ordinary privacy/authority boundaries must be provided by host system; Skill itself does not define them.

## O. Failure semantics and recovery

### Generic AI look

Detection: plan contains repeated known defaults unrelated to brief.
Recovery: revise before build.

### Decoration without information

Detection: labels/numbers/dividers do not encode structure.
Recovery: remove or make them meaningful.

### Motion overload

Detection: repeated fade/slide/hover patterns everywhere.
Recovery: concentrate motion into one purposeful orchestrated moment; keep action-response motion where informative.

### CSS specificity conflict

Detection: generated selectors override/cancel each other.
Recovery: inspect selector structure and rendering.

### Self-critique blindness

Not solved. Same actor can rationalize its own output as distinctive.

## P. Verification / Harness / Eval model

Observed verification is mostly qualitative/self-review:
- compare plan to brief;
- run counterfactual “would I do this for another prompt?”;
- screenshot critique where available;
- accessibility/responsive floor.

No dedicated frontend-design eval suite was observed in this research pass.

Repository model-migration material separately advocates eval-driven prompt changes for behavioral regressions, but that is not evidence of a frontend-design-specific held-out benchmark.

## Q. Portability and compatibility

Methodology is broadly frontend-stack agnostic.

Implementation details depend on available web stack/fonts/assets/rendering.

Model sensitivity is explicitly relevant: stronger/newer models may need less anti-slop prompting.

Without screenshot/render tools, visual feedback is weaker.

## R. Cost, latency, complexity and ergonomics

Adds one deliberate planning pass and one critique pass before/after build.

This increases latency versus “generate code immediately” but is intended to reduce generic rework.

Human attention can stay low when brief is strong; missing brief requires clarification/proposal.

Prompt itself is substantial; model improvements may make some anti-default enumeration obsolete over time.

## S. Anti-patterns and negative knowledge

Explicit recurring generated-design tells include:
- warm cream + contrast serif + terracotta default;
- near-black + acid accent default;
- broadsheet hairline newspaper default;
- identical rounded SaaS card grids/shadows/gradient washes;
- all-caps eyebrow labels everywhere;
- one highlighted headline word as generic trick;
- meta strings joined with dots/em-dashes;
- automatic monospace data labels/arrows;
- meaningless numbered sequences;
- repeated section fade-slide reveals.

Important nuance: none is forbidden when the brief genuinely calls for it. The anti-pattern is **defaulting without brief-specific reason**.

## T. Hidden assumptions and inferred invariants

1. The model can recognize and escape its own aesthetic priors after being reminded of them.
2. A short explicit plan improves implementation consistency.
3. Screenshot review can reveal issues source inspection misses.
4. Distinctiveness and usability can coexist if boldness is concentrated.
5. The brief contains enough domain signal, or user accepts agent-proposed subject framing.
6. Self-critique is sufficiently adversarial—an unproven assumption.

## U. Reusable primitives — neutral extraction

### U1 — Brief-grounded generation

Derive unconstrained choices from subject/audience/job, not generator defaults.

### U2 — Pre-build compact design contract

Set tokens/type/layout/principles before implementation.

### U3 — Counterfactual genericity test

Ask whether same unconstrained choice would appear for another similar task; revise if yes.

### U4 — Known-default blacklist as self-bias detector

Catalog recurring generator priors as things requiring justification, not absolute bans.

### U5 — Rendered-artifact critique

Review screenshots/rendered output, not only source text.

### U6 — One-bold-gesture restraint

Concentrate novelty; remove non-functional decoration.

### U7 — Vocabulary/action consistency in UI copy

Treat interface language as navigational state, not marketing filler.

## V. Cross-Top10 links

- `grill-me`: could clarify vague product/design direction before visual plan.
- `improve-codebase-architecture`: both use plan/candidate → critique → user/implementation separation and attack generic defaults.
- `tdd`: highlights domains where visual outcomes need different evals than deterministic unit tests.
- `agent-browser`: browser/screenshot tooling could provide stronger external rendering/interaction feedback.
- `handoff`: design plan can become compact cross-session artifact if implementation spans sessions.

## W. Open questions for final synthesis

- Can visual distinctiveness be evaluated with held-out pairwise judges without Goodharting into another style formula?
- Should screenshots be mandatory for UI work where a browser runtime exists?
- How should generator-default catalogs evolve per model version?
- What parts of creative self-critique should be independent reviewer versus same-agent pass?
- Can a compact design-plan schema improve portability across frontend agents?

## X. Evidence ceiling

- Original Skill inspected: **YES**
- Detailed methodology inspected: **YES**
- Runtime implementation: **NOT APPLICABLE/NOT OBSERVED**
- Dedicated frontend-design Harness/eval: **NOT OBSERVED**
- Screenshot/self-review method described: **YES**
- Independent visual-quality verification: **NO**
- Live comparative outcome evidence: **NO**

This is a sophisticated creative-method prompt with explicit self-bias countermeasures, but its quality guarantees remain primarily qualitative and self-evaluated rather than harness-backed.
