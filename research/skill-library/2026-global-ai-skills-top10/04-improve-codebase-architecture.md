# 04 — `improve-codebase-architecture`

Selection status: **PENDING_10_OF_10_SYNTHESIS**
Distillation status: **COMPLETE_SOURCE_NORMALIZATION**

## A. Identity and evidence provenance

- Source: `mattpocock/skills`
- Pinned HEAD: `49dd158d1076134a641b33efb035946536778336`
- Skill: `skills/engineering/improve-codebase-architecture/SKILL.md`
- Skill blob: `44cc7d3136c44534d68ac523fa6cd37e759d2846`
- User docs: `docs/engineering/improve-codebase-architecture.md`
- Shared vocabulary: `skills/engineering/codebase-design/SKILL.md`
- HTML report reference: `skills/engineering/improve-codebase-architecture/HTML-REPORT.md`
- Related `grilling` and `domain-modeling` primitives inspected through entries 02/03.

## B. Problem model and intended outcome

Problem: codebases accumulate **shallow modules**, leaky seams, scattered knowledge and test surfaces that expose too much structure. Generic “clean code” reviews produce low-value cleanup lists and often refactor cold code that will not repay the effort.

Desired outcome:
- identify a small number of **deepening opportunities**;
- focus attention where future change makes the payoff likely;
- visualize the before/after architecture before touching code;
- let the human pick a candidate;
- then clarify that candidate through a decision interview;
- feed the resulting decision back into the normal build flow.

Architectural role: **periodic/read-only architecture survey + candidate generator + decision-analysis entry point**. It is explicitly not the refactoring executor.

## C. Activation and invocation model

- Manual only (`disable-model-invocation: true`).
- Suitable for:
  - routine architecture upkeep;
  - pre-big-build preparation;
  - brownfield/legacy survey;
  - finding seams before test work.
- User may specify a subsystem/pain point; otherwise recent-change history determines scan focus.

Stop conditions:
- initial phase stops after HTML report and waits for user selection;
- selected candidate phase ends with a clarified decision, not a code change.

Wrong-trigger risks:
- applying it to every code change creates refactoring theater;
- using it for a specific bug when the issue is not architectural wastes time;
- large legacy codebases can overwhelm the model.

## D. Inputs, outputs, side effects

Inputs:
- repository;
- git history;
- optionally user-specified area/spec;
- `GLOSSARY.md`/map;
- relevant ADRs;
- shared `codebase-design` vocabulary.

Outputs:
- temp-directory self-contained HTML architecture review;
- ranked candidates (`Strong`, `Worth exploring`, `Speculative`);
- top recommendation;
- user-selected candidate decision conversation;
- possible glossary updates/ADR from the grilling stage.

Explicit non-output: no source-code refactor is performed during the survey.

## E. End-to-end workflow

### A0 — Scope by payoff

If user provides scope, use it.

Otherwise inspect a meaningful git-history window and identify repeatedly changed files/areas. The methodology assumes architectural improvement pays only where future change is likely.

This is a **change-frequency prior** against YAGNI refactoring.

### A1 — Load domain/architecture language

- read relevant glossary/ADRs;
- load `codebase-design` vocabulary: module, interface, implementation, depth, seam, adapter, leverage, locality.

The Skill strongly controls terminology to force consistent analysis.

### A2 — Organic exploration

Spawn an exploration sub-agent and look for experienced friction rather than a rigid linter checklist:
- concept understanding requires many files;
- interface nearly as complex as implementation;
- pure-function extraction improves unit tests but loses call-site locality;
- coupled modules leak through seams;
- important behavior is difficult to test through the current interface.

### A3 — Deletion test

For suspected shallow module, imagine deleting it.

If complexity simply spreads into callers, the module was providing useful concentration/depth.

If complexity effectively disappears or only pass-through remains, it may be shallow/redundant.

Only candidates with credible payoff proceed.

### A4 — Produce visual candidate report

Write `<tmpdir>/architecture-review-<timestamp>.html` outside repository.

Each candidate includes:
- files/modules;
- concrete friction;
- proposed deepening in plain language;
- locality/leverage/test benefits;
- before/after visual;
- recommendation-strength badge;
- ADR conflict warning where applicable.

The report ends with top recommendation.

Critical gate: **do not propose the final interface yet**. Ask user which candidate to explore.

### A5 — Candidate selection

User chooses candidate. No code has changed.

### A6 — Grilling decision loop

Invoke `grilling` to clarify:
- constraints;
- dependencies;
- what belongs behind seam;
- which tests survive;
- desired deepened interface shape.

### A7 — Domain-model updates

Invoke `domain-modeling` as decisions crystallize:
- add/clarify glossary terms;
- if user rejects a candidate for durable/load-bearing reason, optionally record ADR so future review does not propose it again.

### A8 — Design-it-twice branch

If interface alternatives need exploration, use `codebase-design`'s parallel design pattern rather than immediately locking onto one interface.

### A9 — Return to build flow

Chosen architecture decision goes to `to-spec` / ticketing / implementation later. Survey itself is complete.

## F. Core methodology / mental model

### Deep modules

A good module provides lots of behavior behind a small stable interface.

Depth is treated as **leverage at the interface**, not lines-of-code ratio.

### Locality

Change, bugs, knowledge and verification should concentrate rather than leak across callers.

### Seam discipline

The public interface is both caller surface and test surface. A seam should correspond to meaningful variation; one adapter is considered hypothetical, two adapters evidence a real seam.

### Deletion test

Delete mentally to distinguish useful concentration from pass-through abstraction.

### Payoff-weighted architecture work

Recent/hot code receives more attention than untouched cold areas.

### Survey before commitment

Generate multiple visual candidates before user picks one; do not let first model idea become implementation by default.

### Candidate strength calibration

`Strong / Worth exploring / Speculative` provides explicit uncertainty instead of one undifferentiated recommendation list.

## G. Decision-rights model

Agent:
- scopes likely hot spots (unless user scopes);
- explores code;
- proposes/ranks candidates;
- builds report;
- recommends top candidate.

User:
- chooses which candidate deserves deeper exploration;
- owns trade-off decisions during grilling;
- may reject candidates and decide whether rejection deserves durable ADR.

Repository artifacts:
- glossary determines domain language;
- ADRs constrain prior decisions unless friction justifies reopening.

## H. State machine and lifecycle

`SCOPE → EXPLORE → FILTER_BY_DELETION_TEST → REPORT → WAIT_FOR_SELECTION → GRILL_SELECTED → DOMAIN_UPDATE → DECISION_READY → RETURN_TO_BUILD_FLOW`

Periodic lifecycle: intended to run repeatedly over time, not once per project.

Rejection memory can become ADR so future runs avoid repeating a discarded architectural proposal.

## I. Memory, durability, provenance

- HTML report: temporary, outside repo.
- architecture decision conversation: contextual until formalized downstream.
- glossary/ADR updates: durable repository memory.
- git history: used as prioritization evidence.

Interesting asymmetry: candidate report is deliberately ephemeral, while durable rejection rationale can become ADR. The system tries not to pollute repo with every speculative scan result.

## J. Composition and dependency graph

Calls/depends on:
- `codebase-design` for vocabulary/theory;
- exploration sub-agent;
- `grilling` after candidate choice;
- `domain-modeling` during decision refinement;
- optional design-it-twice pattern.

Feeds:
- `to-spec` / normal build pipeline.

Known portability issue: source names Claude Code's `Agent`/Explore behavior; other harnesses may not reproduce equivalent exploration.

## K. Skill / Agent / Runtime / Harness architecture

- main Skill: session driver/orchestration;
- `codebase-design`: shared architecture reference/method;
- sub-agent: repository exploration executor;
- HTML reference: presentation contract;
- glossary/ADR: durable knowledge surfaces;
- no code-mutating runtime for refactor itself.

The source deliberately separates **survey** from **implementation**, reducing blast radius.

## L. Context engineering and progressive disclosure

Positive:
- shared vocabulary stays in a reusable reference Skill;
- report is written outside conversational prose, reducing repeated explanation;
- one candidate per follow-up session is recommended to avoid context saturation;
- only chosen candidate enters detailed grilling.

Negative:
- report + code exploration + grilling can still create very large context;
- large legacy repos degrade quality;
- CDN visuals are external runtime dependencies.

## M. Concurrency, isolation, idempotency, replay

No explicit writer lease. Survey is mostly read-only.

Durable side effects during grilling (glossary/ADR) inherit domain-modeling concurrency risks.

Temp report names include timestamp, avoiding overwrite collision between runs.

Periodic reruns can re-suggest rejected ideas unless rejection is captured durably as ADR—an informal anti-replay mechanism for architecture proposals.

## N. Safety and trust boundaries

The initial survey does not modify source code, which strongly limits risk.

Potential external trust surface:
- report loads Tailwind/Mermaid from CDNs;
- locked-down/offline/SRI environments can fail.

The report may contain repository structure/source-derived data and is opened locally; source does not define redaction/classification policy for sensitive codebases.

## O. Failure semantics and recovery

### Grill-first failure

Weaker models may skip report-first gate and start interviewing about first idea. Source docs call this a common complaint.

Recovery: explicitly request report-only/no-grill, choose candidate after.

### Visual report failure

CDN blocked/offline → raw/unrendered report.

Recovery: inline CSS and hand-built SVG.

### Candidate flood

Too many candidates → work one per session; turn others into later tickets.

### Large legacy repo

Model may circle/produce weak graph; no specialized refactor mode exists.

### Portability degradation

Harness without Claude Explore tool may skip/weakly emulate parallel exploration.

### Findings bias

Because the Skill exists to find improvements, it rarely concludes “architecture is fine.” Source suggests treating all-`Speculative` report as effective no-finding result.

## P. Verification / Harness / Eval model

No dedicated machine eval inspected for the architecture quality itself.

Operational rubrics in docs:
- candidates use domain concepts, not arbitrary class names;
- candidates focus on recently changed areas;
- source code remains untouched;
- stops after report for user choice;
- benefits expressed in locality/leverage/testability;
- rejected durable candidate can become ADR.

The source documentation includes candid user complaints/known issues, which is useful qualitative failure evidence but not a benchmark.

## Q. Portability and compatibility

- Git repository assumed for history-based scoping.
- HTML opening commands differ by OS and are documented.
- CDN report requires network unless customized.
- Claude-specific sub-agent invocation weakens cross-harness parity.
- architecture vocabulary is language-agnostic, but concrete implementation guidance (e.g. TypeScript module layouts) is explicitly missing.

## R. Cost, latency, complexity and ergonomics

Costs:
- repository scan/sub-agent;
- history review;
- visual report generation;
- human candidate selection;
- potentially long grill.

Efficiency mechanisms:
- hot-spot targeting;
- deletion test filter;
- rank strength;
- stop before code change;
- one candidate per session.

Ergonomic insight: visual comparison is treated as a decision tool, not decoration.

## S. Anti-patterns and negative knowledge

- Don't refactor untouched code just because it looks imperfect.
- Don't equate “more modules” with modularity/depth.
- Don't design the final interface before candidate selection.
- Don't re-litigate ADRs without real friction.
- Don't push all report findings into one conversation/session.
- Don't assume the report rendered just because HTML was written.
- Don't use vague “cleaner/easier to maintain” claims; tie payoff to locality/leverage/test surface.

## T. Hidden assumptions and inferred invariants

1. Recent change frequency predicts future payoff well enough.
2. The model can organically detect architecture friction without rigid metrics.
3. The deletion test can be judged from static exploration.
4. Visual before/after aids human choice.
5. User will choose among candidates rather than defer to top recommendation automatically.
6. Git history is meaningful and not dominated by generated/vendor churn.
7. Domain glossary/ADRs are accurate enough to constrain proposals.

## U. Reusable primitives — neutral extraction

### U1 — Payoff-weighted maintenance scan

Use change history/future work to scope architecture review before analyzing everything.

### U2 — Deletion test

Evaluate whether an abstraction concentrates or merely forwards complexity.

### U3 — Report-before-decision

Separate candidate generation/presentation from detailed solution design.

### U4 — Ephemeral visual diagnostic artifact

Keep speculative review outside repo; persist only accepted/rejected durable decisions later.

### U5 — Confidence badges

Expose strength/uncertainty per candidate.

### U6 — Durable rejection memory

Record load-bearing rejection reason so future maintenance doesn't re-propose it.

### U7 — Design-it-twice

Explore multiple interface designs before convergence.

## V. Cross-Top10 links

- `grill-me` / `grill-with-docs`: shares interview/domain primitives.
- `tdd`: deep seams define useful test surfaces.
- `frontend-design`: both use plan→critique→build separation and attack generic defaults.
- `triage`: both classify/rank before executing.
- `handoff`: one-candidate-per-session transition may need compact handoff.

## W. Open questions for final synthesis

- Can architecture findings be evaluated mechanically enough to prevent “always find something” bias?
- Should change-frequency be one signal among risk/complexity/incidents rather than the primary prior?
- Should visual reports use bundled assets to avoid external rendering failures?
- Can architecture candidate generation use independent parallel reviewers rather than one exploration actor?
- How should a control plane decide when periodic maintenance has enough expected value to run?

## X. Evidence ceiling

- Main Skill inspected: **YES**
- Shared design methodology inspected: **YES**
- Report contract inspected: **YES**
- Detailed source-authored failure documentation inspected: **YES**
- Automated architecture-quality eval observed: **NO**
- Live refactor outcome evidence inspected: **NO**
- Cross-harness parity proven: **NO**

The workflow is well-articulated and intentionally low-blast-radius, but candidate quality and payoff are still model-judgement-heavy rather than independently measured.
