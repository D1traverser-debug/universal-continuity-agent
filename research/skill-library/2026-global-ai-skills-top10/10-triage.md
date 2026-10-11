# 10 — `triage`

Selection status: **PENDING_10_OF_10_SYNTHESIS**
Distillation status: **COMPLETE_SOURCE_NORMALIZATION**

## A. Identity and evidence provenance

- Source: `mattpocock/skills`
- Pinned HEAD: `49dd158d1076134a641b33efb035946536778336`
- Skill: `skills/engineering/triage/SKILL.md`
- Skill blob: `3fd5617e906cf9b71a6b17424791adb905fc248b`
- Agent-brief contract: `skills/engineering/triage/AGENT-BRIEF.md`
- Rejected-request knowledge base: `skills/engineering/triage/OUT-OF-SCOPE.md`
- GitHub auto-intake workflow: `.github/workflows/triage-label.yml`
- Needs-info expiration/re-entry workflow: `.github/workflows/needs-info.yml`
- Setup dependency/configuration conventions inspected through `setup-matt-pocock-skills`.

This Skill is best understood as a **human-supervised issue/PR state machine** with durable briefs and negative institutional memory, plus CI/workflow automation for parts of the lifecycle.

## B. Problem model and intended outcome

Problem: incoming issues/PRs are noisy, incomplete, duplicated, already implemented, unverifiable, unsuitable for autonomous agents, or repeatedly relitigate rejected ideas. Throwing them directly at an implementation agent shifts ambiguity downstream and wastes execution cycles.

Desired outcome:
- every request has one category and one triage state;
- claims are checked against repository reality before delegation;
- missing information is made explicit;
- ambiguous requests are clarified only when needed;
- agent-ready work receives a durable behavior-focused brief;
- requests requiring human judgement remain human-owned;
- durable rejections become institutional memory;
- stale needs-info requests age predictably.

Architectural role: **intake gate + state machine + verification/briefing workflow**.

## C. Activation and invocation model

Manual (`disable-model-invocation: true`). Maintainer invokes natural-language intents such as:
- show requests needing attention;
- inspect #N;
- move #N to a state;
- show ready-for-agent queue.

Bare `#42` is resolved through configured tracker semantics because GitHub issue/PR number spaces overlap.

External PRs may be included only if repo configuration says PRs are a request surface. Explicitly named PR can still be triaged.

## D. Inputs, outputs, side effects

Inputs:
- issue/PR body, comments, labels, author/dates;
- PR diff when applicable;
- prior triage notes;
- repository code/tests;
- glossary/ADRs;
- `.out-of-scope/` knowledge;
- tracker setup and label mapping;
- maintainer decisions.

Outputs/mutations:
- category/state labels;
- comments/triage notes;
- agent brief or human brief;
- issue close/reopen lifecycle;
- `.out-of-scope/<concept>.md` for rejected enhancements;
- optional glossary/ADR updates during grilling.

Every posted triage comment must contain an AI-generated disclaimer.

## E. End-to-end workflow

### R0 — Queue discovery

Present oldest-first attention buckets:
1. unlabeled/new;
2. `needs-triage`;
3. `needs-info` where reporter has replied since prior notes.

If external PRs are configured in scope, include them and mark issue/PR type.

### R1 — Gather complete context

Read issue/PR and history. For PR include diff.

Parse prior triage notes so resolved questions are not re-asked.

Explore relevant code using glossary and ADRs.

Run two mandatory repository-memory checks:
- **redundancy**: search for existing implementation by domain concept, not only wording;
- **prior rejection**: compare against `.out-of-scope/` concepts.

### R2 — Recommend classification

Recommend:
- category: `bug` or `enhancement`;
- state: one of five canonical state roles;
- reasoning;
- relevant repository summary.

Wait for maintainer direction.

### R3 — Verify claim before grilling

Bug: reproduce from reporter steps.

PR: checkout/inspect and run relevant tests/commands to see whether diff does what it claims.

Result should be:
- confirmed with evidence/code path;
- failed to reproduce/verify;
- insufficient detail.

This prevents a long clarification interview around a false premise.

### R4 — Grill only if needed

If request remains ambiguous, invoke `grilling` + `domain-modeling`.

Clarify in rounds, update terminology/ADRs as necessary.

### R5 — Apply outcome

#### ready-for-agent

Write/post Agent Brief.

#### ready-for-human

Use similar brief but explicitly state why agent delegation is inappropriate (judgement/external access/design/manual testing/etc.).

#### needs-info

Post structured notes:
- established facts;
- exact outstanding questions.

#### wontfix

Differentiate reasons:
- already implemented → point to implementation; do **not** poison `.out-of-scope`;
- rejected bug → explain/close;
- rejected enhancement → persist concept/reason in `.out-of-scope`, link, close.

#### needs-triage

Keep/apply state for partial work.

### R6 — Resume/re-entry

When reporter replies to needs-info:
- read prior notes;
- identify answered questions;
- update picture;
- do not repeat resolved questions.

A scheduled workflow can close needs-info after 14 days with no response and send updated issues back to `needs-triage` when activity returns.

## F. Core methodology / mental model

### State machine before execution

Incoming work must be classified into explicit states instead of relying on conversational judgement each time.

### Verify before elaborate

Check whether claim is real before spending human attention on design/interview.

### Durable brief as delegation contract

The `Agent Brief` is authoritative for delegated work; original issue discussion is context.

Brief principles:
- behavior, not procedure;
- interfaces/contracts, not brittle line numbers;
- independently testable acceptance criteria;
- explicit out-of-scope boundaries;
- durable against code movement/refactor.

### Negative institutional memory

Rejected enhancements are grouped by **concept**, with durable rationale and prior requests, so future intake can avoid re-litigating them.

### Concept similarity over keyword matching

Both redundancy and prior rejection are semantic/domain-concept checks rather than exact phrase matching.

## G. Decision-rights model

Maintainer/human:
- ultimately approves unusual transitions/classification;
- can quick-override state;
- decides rejection/reconsideration;
- owns cases requiring human judgement.

Agent:
- gathers, verifies, recommends, drafts durable brief, searches repository/prior decisions.

Runtime/workflows:
- automatically add initial triage label;
- age needs-info items according to schedule.

Reporter:
- supplies missing external facts when genuinely unavailable elsewhere.

Quick override intentionally trusts maintainer, but confirms mutation and asks about brief when moving directly to agent-ready.

## H. State machine and lifecycle

Categories:
- `bug`
- `enhancement`

States:
- `needs-triage`
- `needs-info`
- `ready-for-agent`
- `ready-for-human`
- `wontfix`

Invariant: exactly one category + one state. Conflicting state roles require maintainer clarification before action.

Normal transitions:
- new/unlabeled → needs-triage;
- needs-triage → needs-info / ready-for-agent / ready-for-human / wontfix;
- needs-info + reporter response → needs-triage;
- maintainer override possible anytime but unusual transition should be flagged.

Terminal-ish `wontfix` closes request; rejections can later be reconsidered by deleting/updating out-of-scope concept and processing a new issue normally.

## I. Memory, durability, provenance

Durable memory layers:
- issue/PR history;
- triage notes;
- labels/state;
- Agent Brief;
- `.out-of-scope` concept records;
- glossary/ADRs;
- tracker config.

Agent Brief deliberately avoids transient file paths/line numbers to survive code churn.

Out-of-scope record avoids temporary reasons (“too busy”) and stores durable strategic/technical rationale.

This is one of the Top10's strongest **negative-memory** patterns.

## J. Composition and dependency graph

Depends on setup-provided:
- tracker location/commands;
- label mapping;
- domain docs.

Optional composition:
- `grilling` + `domain-modeling` for ambiguous reports.

Produces:
- work suitable for downstream implementation agents.

Automation:
- GitHub Action labels every new issue `needs-triage` so it cannot bypass intake queue;
- scheduled needs-info lifecycle automation.

## K. Skill / Agent / Runtime / Harness architecture

- `SKILL.md`: triage state-machine orchestration.
- tracker CLI/API: state mutations and discovery.
- `AGENT-BRIEF.md`: delegation contract/reference.
- `OUT-OF-SCOPE.md`: negative-memory schema/process.
- GitHub Actions: mechanical intake/aging transitions.
- setup config: repository-specific binding.

Unlike purely prompt-driven Skills, part of the state machine is externally automated, though most semantic classification/verification remains model/human-driven.

## L. Context engineering and progressive disclosure

Efficiency mechanisms:
- attention buckets avoid reading everything;
- prior notes prevent re-asking;
- only grill if verification/context still leaves ambiguity;
- Agent Brief compacts long issue discussion into authoritative actionable contract;
- out-of-scope KB avoids repeated reanalysis.

Potential context cost:
- full issue/PR + diff + code search + prior decisions can be large;
- semantic duplicate/rejection search is model-heavy.

## M. Concurrency, isolation, idempotency, replay

State labels provide coarse shared coordination.

Potential concurrent-maintainer conflict is detected partly through conflicting state roles, but there is no explicit lease/CAS.

GitHub Actions automatically guarantee new issues enter queue regardless of how opened.

Needs-info automation is time-based and uses labels as machine state.

Prior notes/out-of-scope records act as replay suppression for resolved/rejected questions.

## N. Safety and trust boundaries

- AI-generated triage comments are explicitly disclosed.
- Agent must verify reported claims rather than trust issue text.
- External PR code is inspected/tested before acceptance.
- `ready-for-human` provides an explicit non-delegation state.
- Maintainer remains authority for state decisions/overrides.

No full hostile-input/prompt-injection model is specified for issue bodies/comments; external request text is implicitly untrusted in practice but not deeply formalized.

## O. Failure semantics and recovery

### Conflicting labels

Fail to maintainer clarification before further action.

### Bug not reproducible / PR claim fails

Do not grill as though premise is true; downgrade to insufficient/needs-info or report verification failure.

### Missing information

Persist what is established + exact unanswered questions, then resume later.

### Reporter never responds

Scheduled close after 14 days under needs-info policy; later comment can return work to needs-triage behavior.

### Duplicate/already implemented

Point to existing implementation; do not store false rejection.

### Repeated rejected enhancement

Match concept to out-of-scope record; surface prior rationale for maintainer confirmation/reconsideration.

## P. Verification / Harness / Eval model

Verification is embedded in workflow:
- reproduce bugs;
- run PR tests/commands;
- search code for existing behavior;
- inspect diff;
- use concrete acceptance criteria in delegation brief.

Mechanical workflow evidence:
- GitHub workflow ensures every new issue gets triage label;
- scheduled workflow handles needs-info aging.

Not observed:
- dedicated eval measuring classification accuracy;
- independent grader of Agent Brief completeness;
- benchmark of semantic duplicate/out-of-scope matching;
- safety eval for adversarial issue content.

## Q. Portability and compatibility

Tracker abstraction supports configured backends through setup docs, though the inspected automation examples are GitHub-specific.

PR-as-request behavior is configurable.

State roles are canonical while actual label strings may map to existing repo labels, separating semantics from provider vocabulary.

## R. Cost, latency, complexity and ergonomics

Adds deliberate front-loaded intake cost but aims to reduce expensive downstream agent failures.

Efficiency levers:
- oldest-first attention queues;
- verify before interview;
- grill only when needed;
- compact durable Agent Brief;
- persistent rejection memory;
- automated aging.

Human attention is reserved for classification/decision points rather than repetitive queue mechanics.

## S. Anti-patterns and negative knowledge

- Do not delegate vague request directly.
- Do not trust bug/PR claim before reproduction/check.
- Do not repeat questions already answered in prior notes.
- Do not classify “already implemented” as rejected/out-of-scope.
- Do not store temporary deferral as permanent rejection.
- Do not write agent briefs with brittle line numbers/file-path instructions.
- Do not omit acceptance criteria or out-of-scope boundaries.
- Do not allow conflicting states to proceed silently.

## T. Hidden assumptions and inferred invariants

1. Label state accurately represents current triage state.
2. Maintainer is available for recommendations/overrides.
3. Repository/test environment can reproduce reported behavior.
4. Agent can semantically match concepts across issue wording/code/out-of-scope docs.
5. Agent Brief can remain stable despite code changes if written behaviorally.
6. 14-day needs-info policy is appropriate for this repo; it is operational policy, not universal truth.
7. Issue tracker is a durable enough control surface for agents/humans.

## U. Reusable primitives — neutral extraction

### U1 — Intake state machine

Explicit queue states prevent ambiguous work from entering execution.

### U2 — Verify-before-clarify

Check premise in environment before spending interview effort.

### U3 — Agent-ready durable brief

Separate authoritative execution contract from noisy historical discussion.

### U4 — Behavioral brief, not procedural snapshot

Specify desired behavior/interfaces/acceptance/out-of-scope rather than line-number implementation instructions.

### U5 — Negative institutional memory

Persist durable rejection rationale by concept to suppress repeated relitigation.

### U6 — Needs-info resumability

Persist established facts and missing facts so work can re-enter after external response without restarting.

### U7 — Human-only state

Explicitly represent “cannot/should not delegate to agent” rather than force automation.

### U8 — Automatic queue admission

Infrastructure labels every new request so intake process cannot be bypassed by entry channel.

## V. Cross-Top10 links

- `setup-matt-pocock-skills`: configures tracker/labels/domain conventions.
- `grill-me` / `grill-with-docs`: clarification primitive for ambiguous work.
- `tdd`: verified bug/agent brief can feed behavioral test implementation.
- `handoff`: Agent Brief is a stronger structured handoff artifact for future executor.
- `find-skills`: triage may reveal missing reusable capability rather than custom implementation.
- `agent-browser`: external UI bugs may need browser-based reproduction/evidence.

## W. Open questions for final synthesis

- Should every owner/business system have an explicit `ready-for-agent / ready-for-human / needs-info` analogue?
- Can semantic duplicate/rejection search be independently evaluated?
- How should intake state and execution lease interact in concurrent agent systems?
- Should Agent Brief format become a generic work-order contract beyond code issues?
- How can external untrusted issue text be sandboxed against prompt injection?
- What expiration policy should be owner-specific rather than copied from 14-day default?

## X. Evidence ceiling

- Main Skill inspected: **YES**
- Agent Brief contract inspected: **YES**
- Out-of-scope memory system inspected: **YES**
- GitHub automation for intake/needs-info inspected: **YES**
- Semantic classification/duplicate eval: **NOT OBSERVED**
- Live delegation quality benchmark: **NOT OBSERVED**
- Prompt-injection resistance: **NOT PROVEN**

The Skill combines prompt-level semantic judgement with real durable state/automation. Its queue and memory mechanics are concrete; classification quality and brief quality remain largely model/human judged.
