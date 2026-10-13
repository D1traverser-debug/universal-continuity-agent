# 02 — Evolutionary Architecture, Group Flow and Interaction Topology

## Evolutionary architecture

Thoughtworks' definition is useful because it makes architecture change itself an engineered object: an evolutionary architecture supports **guided, incremental change across multiple dimensions**. “Guided” is implemented with architecture fitness functions—tests, metrics or other objective checks that protect important characteristics while allowing the system to evolve.

For Universal this means evolution should not be “add another policy after every incident.” It should identify architecture characteristics that must remain true—authority integrity, recovery correctness, hot-path latency, owner isolation, evidence honesty, change reversibility, etc.—and make them measurable where possible.

### Current Universal analogue

Universal already has deterministic tests, architecture audits, second-order review, fault-injection scenarios, anti-bloat rules and supersession requirements. These behave like **implicit fitness functions**, but they are distributed across tests/policies rather than exposed as a coherent architecture-characteristic → fitness-function map.

### Current gap

The system can prove that many named tests pass, but it cannot yet answer in one derived view:

> “What are the architectural qualities we are protecting, what instrument measures each one, what threshold is acceptable, and which quality has no executable fitness function?”

That makes negative-space omissions harder to see.

## Inter-group interaction: Team Topologies as an analogy

Team Topologies distinguishes four broad team types and, more importantly for Universal, three interaction modes:

- **Collaboration** — high-bandwidth, temporary joint discovery;
- **X-as-a-Service** — one group provides a stable product/service boundary consumed with low coordination cost;
- **Facilitation** — temporary enablement that helps another group acquire a capability.

The deeper lesson is flow and cognitive load, not organization-chart mimicry. A platform should remove complexity from consumers instead of centralizing every responsibility.

### Mapping to Universal

Potential interaction classes among Universal and BUSINESS owners already exist informally:

- routing/continuity contracts resemble X-as-a-Service;
- maintenance support or migration help resembles facilitation;
- cross-owner architecture changes sometimes require temporary collaboration;
- owner-local execution remains stream/domain aligned.

However, `OWNER_REGISTRY.json` primarily defines membership and authority pointers. It does **not** formally declare the permitted interaction mode, dependency direction, service expectation, backpressure behavior, escalation path or temporary-vs-permanent nature of cross-owner coordination.

### Group-internal flow

Within an owner, healthy flow means evidence and state move through explicit stages without parallel shadow paths. Universal has owner state-machine requirements and action-bound receipts, but it lacks a shared derived model of:

`input -> stage -> producer -> artifact/evidence -> reviewer/checker -> transition -> consumer`

across every owner. That is not a reason for Universal to own business workflows; it is a visibility/verification question.

## Platform-bloat test

Universal currently owns or coordinates continuity, routing, lease/CAS, execution-readiness handshake, profile composition, signal transport, remote observations, maintenance, learning/evolution, architecture validation and progress observability. That may be justified, but Team Topologies supplies a useful counter-question:

> Is Universal still reducing owner cognitive load, or is it becoming a platform monolith whose consumers must understand too many central abstractions?

The answer is not yet quantitatively measured.

## Candidate fitness dimensions for later evaluation

Non-authoritative candidates only:

- bootstrap byte/latency budget;
- required remote reads per healthy business action;
- number of authority surfaces a BUSINESS owner must understand;
- number of cross-owner mutations required for a local business change;
- stale/shadow rule count;
- time/steps from detected drift to isolated blocker;
- ability to add a new owner without editing parallel lists;
- percentage of architectural invariants with executable fitness functions.

## What not to transplant

Do not rename agents as “teams” or add platform/enabling agents merely to imitate an organizational framework. Human team cognitive load and software-agent context/runtime load are related but not identical. The useful parts are explicit interaction modes, bounded platform responsibilities, flow orientation and measurable architecture fitness.

## Current assessment

- Evolution feedback / regression: **PRESENT, but fitness-function map is fragmented**.
- Inter-owner ownership boundaries: **PRESENT**.
- Inter-owner interaction contract: **CURRENT GAP**.
- Group-internal artifact/evidence flow visibility: **PARTIAL / owner-specific**.
- Platform cognitive-load observability: **CURRENT GAP**.
