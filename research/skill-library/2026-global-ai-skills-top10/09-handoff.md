# 09 — `handoff`

Selection status: **PENDING_10_OF_10_SYNTHESIS**
Distillation status: **COMPLETE_SOURCE_NORMALIZATION**

## A. Identity and evidence provenance

- Source: `mattpocock/skills`
- Pinned HEAD: `49dd158d1076134a641b33efb035946536778336`
- Production Skill: `skills/productivity/handoff/SKILL.md`
- Skill blob: `a224edc643a20ddb989f9bca1547440169159810`
- OpenAI interface config inspected: implicit invocation disabled.
- Related in-progress execution variant: `skills/in-progress/claude-handoff/SKILL.md`, blob `77f82fc59c89c3a83ed5a92521dc2869f0533724`, used only as comparative evidence—not conflated with production Skill.

No separate full documentation or dedicated eval Harness was found in the inspected source; the production Skill is intentionally compact.

## B. Problem model and intended outcome

Problem: long-running work crosses context/session boundaries. Copying the whole transcript is expensive and noisy; manually re-explaining causes loss, duplication and inconsistent state.

Desired outcome:
- create a compact handoff for a fresh agent/session;
- preserve current execution truth and next-session focus;
- point to existing durable artifacts rather than copying them;
- recommend relevant Skills for the next agent;
- avoid leaking secrets/PII;
- keep the handoff outside the working repository unless deliberately promoted elsewhere.

Architectural role: **explicit context-compaction / session-boundary Skill**.

It is not itself a durable project state machine or authoritative checkpoint contract.

## C. Activation and invocation model

- Explicit/manual only (`disable-model-invocation: true`; OpenAI config disallows implicit invocation).
- Optional argument describes what the next session is for and shapes the summary.
- Intended at a deliberate session/phase boundary.

Stop condition: a handoff document exists in OS temp directory with enough information/pointers for a fresh agent to continue.

## D. Inputs, outputs, side effects

Inputs:
- current conversation;
- optional next-session objective;
- already-existing specs/plans/ADRs/issues/commits/diffs;
- known relevant Skills.

Output:
- temporary handoff document.

Required content:
- compact current-context summary;
- suggested Skills;
- references to existing artifacts instead of duplicated content;
- redacted sensitive data.

Mutation scope is intentionally outside current workspace (`$TMPDIR` / `/tmp` / `%TEMP%`).

## E. End-to-end workflow

### H0 — Determine continuation target

If user provided argument, treat it as next-session focus.

### H1 — Inventory current truth

Identify:
- what was being done;
- what is already decided/completed;
- what remains;
- what durable artifacts already contain detail.

### H2 — Deduplicate against existing artifacts

Do not copy specs/plans/ADRs/issues/commits/diffs into handoff. Reference by path/URL.

This is a **pointer-over-replication** rule.

### H3 — Redact

Remove API keys, passwords, PII and similar sensitive information before handoff becomes another agent's prompt/context.

### H4 — Add capability hints

Include `suggested skills` so the new agent knows which methods/capabilities to load next.

### H5 — Tailor to next session

Emphasize information relevant to stated next purpose; omit irrelevant transcript history.

### H6 — Write temp artifact

Store outside workspace, preserving project tree cleanliness and signaling that this is transfer context rather than canonical project state.

### H7 — Consumer starts fresh session

Production Skill stops after writing. Related in-progress `claude-handoff` demonstrates a further execution pattern: seed a background agent with the file content and give it a descriptive name.

## F. Core methodology / mental model

### State compression, not transcript copying

The handoff should represent **current execution truth**, not conversation chronology.

### References over duplicated authority

Existing durable artifacts should remain canonical; handoff points to them.

### Purpose-conditioned compaction

What to retain depends on next session's intended work.

### Capability prefetch hint

Suggest relevant Skills without embedding all their instructions.

### Boundary artifact separation

Temporary handoff is a transport artifact, not automatically project authority.

## G. Decision-rights model

User:
- explicitly decides to hand off;
- may specify next-session purpose.

Current agent:
- decides what is salient;
- compresses state;
- redacts;
- identifies references and suggested Skills.

Next agent:
- consumes handoff and referenced artifacts;
- should not treat duplicated/summary prose as stronger than referenced authority.

Potential problem: current agent is both summarizer and importance judge; omitted information may be unrecoverable to next session without reopening transcript.

## H. State machine and lifecycle

Minimal lifecycle:

`ACTIVE_SESSION → HANDOFF_REQUESTED → CURRENT_TRUTH_COMPACTED → REDACTED → TEMP_HANDOFF_WRITTEN → FRESH_SESSION_CONSUMES`

No built-in acknowledgment, receipt, version, supersession or stale-handoff invalidation in production Skill.

Related in-progress variant adds:

`TEMP_HANDOFF_WRITTEN → BACKGROUND_AGENT_LAUNCHED`

but that is not the target production behavior.

## I. Memory, durability, provenance

The handoff is durable enough to cross sessions but stored in temporary OS storage, not repository authority.

Strong rule: avoid copying already-durable artifact content.

Weaknesses:
- no explicit source commit/HEAD binding;
- no task/version identity schema;
- no expiry/staleness marker;
- no receipt confirming next agent read the exact references;
- no machine-readable distinction between claim, fact, open question and next action.

## J. Composition and dependency graph

Inputs reference any artifacts generated by other workflows.

Output contains `suggested skills`, functioning as a lightweight capability-routing bridge.

Could be used between phases of any other Skill.

The in-progress variant composes with an external `claude --bg` agent runtime, showing how a transfer artifact can seed actual delegation.

## K. Skill / Agent / Runtime / Harness architecture

- production `SKILL.md`: entire method;
- OS temp filesystem: transfer storage;
- no dedicated state runtime;
- no dedicated Harness/eval observed;
- optional in-progress wrapper demonstrates active spawn but is not production authority.

This is extremely small prompt architecture with little mechanical enforcement.

## L. Context engineering and progressive disclosure

This Skill is fundamentally context engineering.

Mechanisms:
- compact current state;
- omit transcript chronology;
- reference large existing artifacts;
- tailor summary to future objective;
- suggest Skills by name rather than embed them.

It is an explicit answer to context-window/session-boundary cost.

## M. Concurrency, isolation, idempotency, replay

No concurrency control.

Temp filename behavior is not specified in inspected Skill; simultaneous handoffs could theoretically collide depending on implementation choice.

No single-writer/lease model.

Stale handoff can be replayed without automatic detection because no authority version/HEAD binding is required.

In-progress launch variant uses a file in command substitution specifically to avoid shell interpreting backticks/`$` in summary—useful injection/escaping detail at execution boundary.

## N. Safety and trust boundaries

Explicit:
- redact API keys/passwords/PII;
- do not duplicate sensitive artifacts unnecessarily.

In-progress launch variant treats summary as a prompt and takes care to avoid shell expansion by passing file content safely.

Missing:
- formal classification/redaction Harness;
- repository-authority precedence rules;
- integrity/signature/hash;
- permission scoping for next agent.

## O. Failure semantics and recovery

Potential failures:
- omission of important state;
- stale references;
- over-copying creates contradiction with canonical artifacts;
- secrets leak into transfer prompt;
- next agent misunderstands summary as authority;
- temp file disappears.

Production Skill defines preventative instructions but little machine recovery.

Recovery generally requires reopening source conversation/artifacts and regenerating handoff.

## P. Verification / Harness / Eval model

No dedicated handoff eval observed.

No automatic check that:
- fresh agent can actually resume successfully;
- all referenced paths exist;
- handoff contains no secrets;
- no critical current-state field is missing;
- the next agent's actions match intended continuation.

This is a major evidence gap relative to its importance in long-running agent systems.

## Q. Portability and compatibility

Highly portable because it relies on plain text and temp storage.

OS temp directory rules cover major platforms.

Active background-agent spawn in related variant is Claude-specific and therefore not production portable.

## R. Cost, latency, complexity and ergonomics

Very low implementation complexity.

Benefits:
- large context reduction;
- fresh-session reset;
- avoids repeated artifact copying;
- small user interaction cost.

Risk/cost:
- lossy summarization;
- no formal consistency guarantees;
- depends heavily on summarizer judgement.

The “suggested skills” section improves next-session ramp-up at minimal context cost.

## S. Anti-patterns and negative knowledge

- Do not paste full transcript.
- Do not duplicate already-canonical specs/plans/ADRs/issues/commits/diffs.
- Do not put transfer artifact in project workspace by default.
- Do not include credentials/PII.
- Do not assume next session has same capability context; name suggested Skills.

## T. Hidden assumptions and inferred invariants

1. Current agent can accurately distinguish durable truth from conversational noise.
2. Referenced artifacts remain accessible to next agent.
3. Temporary file survives long enough.
4. Fresh context benefit outweighs information lost by compaction.
5. Next agent knows how to resolve referenced paths/URLs.
6. A human/user initiates boundary at the right time because implicit invocation is disabled.

## U. Reusable primitives — neutral extraction

### U1 — Purpose-conditioned handoff

Compact for what the next session will do, not for archival completeness.

### U2 — Pointer-over-copy rule

Reference existing authoritative artifacts instead of duplicating them.

### U3 — Suggested-capability bridge

Pass names of methods/Skills the successor should load, not their full contents.

### U4 — Temporary transport vs canonical state separation

Keep transfer document outside project by default.

### U5 — Redact before context transfer

Treat summaries as new prompts/loggable artifacts and strip secrets.

### U6 — Prompt-to-process handoff

Comparative in-progress variant shows a handoff can directly seed a fresh process when shell escaping is handled safely.

## V. Cross-Top10 links

- `grill-me`: stateless decisions need capture before context clears.
- `grill-with-docs`: durable glossary/ADR should be referenced, while ordinary decisions may need handoff/spec capture.
- `agent-browser`: contrast between prose handoff and structured persistent session state.
- `triage`: agent brief is a more structured/authoritative form of future-agent handoff.
- `setup-matt-pocock-skills`: stable setup docs should be referenced, never copied.

## W. Open questions for final synthesis

- What is the minimal machine-readable schema for a trustworthy handoff?
- Should handoff bind task_id, authority HEAD, lease/epoch, exact next action and evidence refs?
- Can a fresh-agent resume eval mechanically grade handoff quality?
- Which information should never be compressed and must remain authoritative reference?
- When should transfer artifact become durable project state versus temporary context?

## X. Evidence ceiling

- Production Skill inspected: **YES**
- Interface invocation policy inspected: **YES**
- Comparative active-handoff variant inspected: **YES**
- Dedicated runtime/state machine: **NO**
- Dedicated eval/Harness: **NOT OBSERVED**
- Fresh-agent continuation success benchmark: **NOT OBSERVED**
- Independent completeness/redaction verification: **NO**

The Skill is a highly economical context-compaction method, but its correctness is almost entirely dependent on summarizer judgement and lacks the machine-readable recovery guarantees found in more durable continuity systems.
