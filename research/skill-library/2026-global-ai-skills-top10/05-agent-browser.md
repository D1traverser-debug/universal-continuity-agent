# 05 — `agent-browser`

Selection status: **PENDING_10_OF_10_SYNTHESIS**
Distillation status: **COMPLETE_SOURCE_NORMALIZATION**

## A. Identity and evidence provenance

- Source: `vercel-labs/agent-browser`
- Pinned HEAD: `d9570915f4dd6504dee4070379d2c4f79d81dbb2`
- Installed discovery Skill: `skills/agent-browser/SKILL.md`
- Discovery Skill blob: `dc9bb54a22e9cd7ad9c982a0fe5ae2e204751b12`
- Runtime-served core Skill: `skill-data/core/SKILL.md`
- Runtime skill architecture docs: `docs/content/docs/skills.mdx`
- Eval Harness: `evals/README.md`
- Trust boundaries: `skill-data/core/references/trust-boundaries.md`
- Snapshot/ref model: `skill-data/core/references/snapshot-refs.md`
- Session model: `skill-data/core/references/session-management.md`
- Current pinned commit itself fixes duplicate mutation execution after uncertain transport outcomes, providing direct implementation evidence for idempotency/failure-semantics thinking.

This entry is not merely a browser-tool summary. It is a rich example of **thin Skill + version-matched runtime knowledge + deterministic CLI + state isolation + explicit trust model + eval Harness**.

## B. Problem model and intended outcome

Problem: AI agents need reliable browser interaction without placing a huge, stale DOM/tool/manual surface into every prompt. Browser tasks additionally have state, authentication, concurrency, timing, prompt-injection and duplicate-action risks.

Desired outcome:
- give the agent a very small discovery entry point;
- load the exact current browser workflow/reference from the installed runtime;
- represent the page compactly;
- act through stable references/typed tools;
- isolate sessions;
- verify changing page state after actions;
- contain credentials/network scope;
- test that agents actually load/select/use the intended runtime knowledge.

Architectural role:
- installed Skill = **thin discovery router**;
- CLI/runtime = **executor + dynamic knowledge server**;
- skill-data = **version-coupled operating procedures**;
- evals = **behavioral Harness**.

## C. Activation and invocation model

Installed Skill has broad browser-related triggers:
- navigate/open site;
- click/fill/form;
- screenshot;
- scrape/extract;
- login/auth;
- web app QA/testing;
- Electron/Slack/cloud browser specializations.

The installed Skill is intentionally **not the usage guide**. First action is to load live runtime instructions:

- `agent-browser skills get core`
- or `core --full` for full reference/templates.

Specialized tasks load specialized runtime Skills (`electron`, `slack`, `dogfood`, `derive-client`, cloud-provider variants).

Stop/cleanup: close browser/session when done unless a persistence use case explicitly requires restore state.

## D. Inputs, outputs, side effects

Inputs:
- URL/site/application;
- authorized user task;
- browser/session state;
- page accessibility tree/rendered content;
- optional WebMCP catalog;
- credentials via safer vault/file mechanisms;
- specialized task parameters.

Outputs:
- compact accessibility snapshots;
- extracted text/data;
- screenshots/video/HAR/state files where requested;
- browser mutations (click/fill/navigation/upload/etc.);
- structured JSON output for automation;
- dashboard observability.

Side effects range from read-only inspection to high-impact form submission/browser mutations. The runtime distinguishes these operationally in retry behavior.

## E. End-to-end workflow

### B0 — Load version-matched operating knowledge

Installed Skill tells agent to retrieve live core Skill from CLI. This avoids stale static instructions.

### B1 — Create/choose isolated session

Before normal use, derive a named session—recommended from worktree scope.

Reason: unnamed default browser is shared across agents/conversations and can hijack the wrong page.

Optional persistence uses restore keys/state validation.

### B2 — Open target

`open <url>`.

Inspect response for automatically advertised WebMCP summary.

### B3 — Capability branch: WebMCP or UI

If a relevant advertised WebMCP tool exactly matches authorized task:
- inspect only that tool's metadata/schema;
- check effect against task;
- invoke it.

If no relevant/trusted tool:
- do not probe broadly;
- continue through UI.

All site-provided metadata is treated as untrusted data.

### B4 — Snapshot

Preferred UI path:
- `snapshot -i` to get interactive accessibility nodes + compact `@eN` refs.

This is the primary context compression strategy.

### B5 — Act

Use ref-based action when possible:
- click/fill/type/select/check/upload/etc.

Fallback order:
1. snapshot refs;
2. semantic find by role/text/label/etc.;
3. raw CSS selector.

### B6 — Wait on a semantic milestone

After page-changing action, wait for:
- expected element/text;
- URL pattern;
- app JS condition;
- relevant lifecycle event.

`networkidle` is explicitly not a universal default; fixed sleep is last resort.

### B7 — Re-observe

Re-snapshot after navigation/dynamic changes. Ref lifecycle tracks surviving/replaced nodes; invalidated IDs are not recycled in the session.

### B8 — Extract/verify result

Read resulting state/data/screenshot/etc. For high-value evals, independent grader can inspect final application state rather than trusting agent narrative.

### B9 — Cleanup/persist

Close session, or persist restore state according to explicit task design.

## F. Core methodology / mental model

### Snapshot → reference → action → re-snapshot

The browser is treated as an evolving observable state machine. Agent does not continually parse full DOM.

### Progressive tool disclosure

- tiny installed Skill;
- dynamic `skills get` core;
- specialized Skill only when needed;
- full command/reference only on demand;
- paginated MCP discovery rather than preload-all tools.

### Prefer semantic/declared capability over reconstruction

If a trusted, relevant WebMCP tool describes the exact operation, prefer it to manually recreating the flow through DOM clicks.

### Condition-based synchronization

Wait for meaning, not arbitrary time.

### Session isolation first

Browser state is an owned execution context, not a global ambient resource.

### Fail closed on ambiguous mutation outcome

Current pinned commit changes retries so a mutating command that was written to daemon but lost its response is not blindly replayed; result becomes `outcome_unknown`.

This is a mature distributed-systems principle embedded in browser automation.

## G. Decision-rights model

User:
- authorizes target/task and sensitive/destructive intent.

Agent:
- selects appropriate runtime Skill/tool path;
- decides snapshots/waits/locators;
- interprets page state.

Runtime:
- maintains browser/session/ref lifecycle;
- enforces command semantics, containment, retry rules.

Page/site:
- supplies data/UI/WebMCP metadata, but is explicitly **not instruction authority**.

Grader/Eval:
- can independently verify browser-side outcome in dedicated tests.

## H. State machine and lifecycle

Key states:
- session absent/created;
- browser active;
- page loaded;
- snapshot baseline/ref set;
- mutation in flight;
- page changed/ref invalidation;
- persisted restore state;
- closed/idle timeout.

Shared-browser pinning adds `tab_gone` fail-closed state rather than silently switching tabs.

Restore lifecycle distinguishes:
- session identity;
- persistence key;
- load validation;
- periodic auto-save;
- close/idle shutdown.

## I. Memory, durability, provenance

Memory layers:
- live browser session: cookies, storage, tabs, history;
- optional restore/state files: durable browser state;
- runtime Skill data: version-matched operational knowledge;
- snapshots/refs: short-lived execution references;
- screenshots/HAR/video: optional durable evidence.

Security consequence: state/HAR/screenshot artifacts may contain secrets and require sensitive handling.

## J. Composition and dependency graph

Installed discovery Skill → CLI skill registry → core/specialized runtime Skills → CLI commands/CDP/browser/provider.

MCP is an alternate typed exposure of the runtime, with profile-based tool subsets.

Specializations include Electron, Slack, testing/dogfood, client derivation, cloud/sandbox providers.

Composition is more mechanical than most prompt-only Skills because live skill content is served by the executable itself.

## K. Skill / Agent / Runtime / Harness architecture

This is one of the clearest layered systems in the Top10:

- **Thin Skill:** activation words + pointer.
- **Runtime Skill service:** current workflows/reference, tied to installed binary version.
- **CLI:** deterministic execution and state management.
- **MCP:** typed alternative tool surface.
- **References:** deeper trust/auth/session/command guidance.
- **Evals:** skill-loading, skill-selection, command-use and context-footprint validation.
- **Live eval fixtures:** verify outcome against browser/application state.

The separation explicitly solves Skill/version drift.

## L. Context engineering and progressive disclosure

Major design theme.

Mechanisms:
- installed Skill intentionally thin/stable;
- runtime serves current instructions;
- `skills get core --full` only when full docs needed;
- specialized Skills loaded only for specialized tasks;
- accessibility snapshots reduce page context dramatically;
- `--delta` snapshots reduce repeated unchanged state;
- MCP profiles/pagination avoid loading full tool surface;
- docs-friendly `read` mode avoids launching browser/full DOM when not needed.

The project includes deterministic context-footprint measurements and behavior evals specifically for this architecture.

## M. Concurrency, isolation, idempotency, replay

### Session isolation

Named sessions isolate browser contexts. Worktree-based naming supports parallel agent work.

### Shared CDP caveat

When sharing one Chrome, cookies/storage are shared; only tab selection is isolated. `--pin-tab` enforces stable target binding.

If pinned tab disappears, fail `tab_gone`; do not silently adopt a different tab.

### Duplicate mutation protection

Current commit explicitly treats uncertain post-send mutation failures as `outcome_unknown` rather than auto-retrying, because replay could double-click/double-submit/navigate twice.

Read-only actions may retry safely under broader conditions.

This distinction between **pre-send failure**, **read-only retry**, and **post-send mutating unknown outcome** is a strong reusable failure model.

## N. Safety and trust boundaries

Explicit and unusually detailed.

### Untrusted page model

DOM, aria labels, console, network bodies, WebMCP descriptions/schemas/results are treated as untrusted site data, not instructions.

### Secrets

- do not echo secrets into model/log/transcript;
- prefer file/vault credential paths;
- state files are secret;
- HAR may contain auth headers;
- screenshots/videos can expose secrets.

### Navigation scope

Stay on user's target; do not follow site/model-invented URLs without task relevance.

### Domain containment

`--allowed-domains` blocks supported browser network channels and adds WebRTC/worker protections where enforceable, with explicit caveat that this is browser containment, not OS firewall.

Unsupported attachment modes reject containment rather than claim a boundary they cannot enforce.

### Prompt injection

Hostile WebMCP eval modes test some attack handling, but project explicitly refuses to generalize this into proof of prompt-injection resistance.

## O. Failure semantics and recovery

Examples:
- stale/missing ref → re-snapshot;
- dynamic page → wait/re-snapshot;
- pinned tab gone → structured `tab_gone`, explicit recovery;
- mutation request sent but response lost → `outcome_unknown`, no blind replay;
- read-only transient failure → retry permitted;
- pre-write transport failure → retry/respawn remains safe;
- restore validation failure → auto-save policy can avoid overwriting known-good state;
- unsupported containment mode → reject rather than silently weaken boundary.

This system generally prefers explicit degraded/unknown states over pretending success.

## P. Verification / Harness / Eval model

Strongest among inspected Top10 so far.

### Eval categories

- Skill loading: did agent load live runtime Skill before commands?
- Skill selection: did it choose appropriate specialized Skill?
- Command usage: did it produce correct browser workflow?
- Context footprint: measure thin Skill/CLI/MCP context costs.

### Evaluation mechanisms

- deterministic regex expected/forbidden patterns;
- optional LLM judge;
- Claude/Codex provider comparison;
- structured JSON outputs.

### Live WebMCP smoke E2E

- isolated workspace;
- actual agent;
- local app fixture;
- dynamic tool registration;
- final wishlist read independently;
- ordinary control mode;
- hostile description/schema/result modes;
- can compare baseline binary/skill-data against candidate.

Source carefully calibrates claim: smoke evals do not prove general reliability or injection resistance.

## Q. Portability and compatibility

- intended for many coding agents;
- CLI independent of a single model;
- Linux/macOS/Windows commands documented;
- MCP alternative for compatible hosts;
- specialized browser/provider modes.

Limits:
- some containment unavailable for attached/preexisting browsers/Safari/iOS/etc.; system rejects unsupported promises;
- runtime install/browser dependencies required.

## R. Cost, latency, complexity and ergonomics

Performance optimizations:
- native CLI;
- compact accessibility state;
- delta snapshots;
- on-demand skills;
- tool profiles;
- docs read without browser where possible.

Complexity cost is significant: daemon, sessions, CDP, auth, providers, MCP, evals. But much of that complexity is deliberately hidden behind thin Skill/runtime layers.

The design treats **context tokens as an engineering resource** with explicit measurement rather than vague optimization.

## S. Anti-patterns and negative knowledge

- Never use unnamed default session in multi-agent task if isolation matters.
- Never blindly retry mutating command after request may have executed.
- Never treat page content/tool metadata as instructions/authorization.
- Never use fixed sleep as normal synchronization.
- Never use `networkidle` universally on streaming/polling apps.
- Never put secrets directly in command transcript when safer file/vault path exists.
- Never assume browser-level domain containment equals host firewall.
- Never preload huge Skill/tool reference when dynamic retrieval works.

## T. Hidden assumptions and inferred invariants

1. Installed CLI is trusted enough to serve authoritative matching Skill content.
2. Accessibility tree adequately represents most user-relevant interactions.
3. Named-session identity is stable enough across commands.
4. Agent will obey the thin Skill instruction to load runtime content—hence explicit evals test it.
5. Compact refs improve reasoning more than raw DOM for common tasks.
6. WebMCP metadata can be safely used only under a strict untrusted-data model.
7. Final state can sometimes be verified independently of agent narration, which enables stronger evals.

## U. Reusable primitives — neutral extraction

### U1 — Thin stable discovery Skill + runtime-served versioned knowledge

Minimal Skill points to executable source that always matches runtime version.

### U2 — Context-footprint Harness

Measure bytes/tokens of competing capability exposure paths instead of assuming “thin”.

### U3 — Snapshot/ref interaction model

Compress rich environment state into stable action references.

### U4 — Session-by-default isolation

Derive explicit task/worktree execution identity; reject ambient shared state.

### U5 — Mutation unknown-outcome semantics

If execution may have happened, do not retry non-idempotent action blindly.

### U6 — Conditional waits

Synchronize on observable expected state, not time.

### U7 — Capability progressive disclosure

Core first, specialized on demand, full references only when needed.

### U8 — Site content as untrusted data

Tool/page-provided text never becomes authorization/instruction authority.

### U9 — Final-state independent verification

In evals, inspect actual application result rather than trust agent self-report.

### U10 — Unsupported assurance rejection

If a containment/isolation mode cannot be guaranteed in an execution mode, reject that option instead of silently claiming equivalent protection.

## V. Cross-Top10 links

- `find-skills`: both rely on tiny discovery layer plus dynamic capability acquisition.
- `handoff`: both care about context economy and state continuity, but browser has stronger machine state.
- `tdd`: both value short deterministic feedback loops and behavior-level verification.
- `triage`: both separate discovery/state classification from mutating action.
- `setup-matt-pocock-skills`: both bootstrap environment conventions, but agent-browser serves live version-coupled instructions instead of copying static guidance.

## W. Open questions for final synthesis

- Which parts of “runtime-served Skill” architecture generalize to non-CLI owners?
- Should all mutating owner tools have explicit `outcome_unknown` semantics?
- Can Universal measure hot-path context footprint for every owner like agent-browser does?
- How much live E2E/final-state verification is feasible for text-heavy/business agents?
- When is MCP tool schema exposure more expensive than CLI-like progressive command reference?

## X. Evidence ceiling

- Installed Skill inspected: **YES**
- Runtime-served Skill inspected: **YES**
- Deep references inspected: **YES**
- Runtime/commit behavior evidence inspected: **YES**
- Automated behavioral eval Harness inspected: **YES**
- Live isolated E2E methodology inspected: **YES**
- Broad real-world reliability proven: **NO**
- Prompt-injection resistance proven: **NO; source explicitly limits claim**

This entry has materially stronger executable/Harness evidence than prompt-only Skills, while still maintaining explicit boundaries around what its evals do not prove.
