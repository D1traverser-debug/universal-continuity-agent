# Cross-Skill Primitive Matrix — Top10

Status: PHASE_B_ANALYSIS
Prerequisite: 10/10 normalized entries complete.

This matrix compares mechanisms, not popularity or branding.

| Primitive / concern | Find | Grill | Grill+Docs | Arch Improve | Browser | TDD | Setup | Frontend | Handoff | Triage |
|---|---|---|---|---|---|---|---|---|---|---|
| Thin router / delegation | — | **Yes** | **Yes** | Partial | **Strong** | Reference | Driver | No | Small | Driver |
| Runtime-served versioned knowledge | No | No | No | No | **Strong** | No | No | No | No | No |
| Reuse-before-build | **Core** | — | — | Partial | Specialized skills | — | Conditional setup | — | Suggested skills | Duplicate check |
| Progressive disclosure | Search funnel | Shared primitive | Shared primitives | Select candidate then deepen | **Strong + measured** | References | **Strong** | Moderate | Pointer-based | Conditional grill |
| Human decision ownership | Install choice | **Core** | **Core** | Candidate selection | Authorization | Seam approval | Config branches | Brief wins | Handoff trigger | Maintainer state |
| Facts/environment owned by agent | Search metadata | **Core** | **Core + code** | **Core** | Browser state | Test runner | Repo scan | Render/brief | Artifact scan | **Verify claim** |
| Decision-tree/frontier | — | **Core** | **Core** | Via grill | — | Slice sequence | Sections | Plan/review | — | Via grill |
| Durable domain memory | Installed Skill | None | **Glossary/ADR** | Glossary/ADR | Browser state | Tests/code | **Repo config** | Code | Temp handoff | **Issue/brief/out-of-scope** |
| Negative institutional memory | No | No | ADR rejection | ADR rejection | Evals/failure semantics | Anti-patterns | Existing config | Anti-default catalog | No | **Core** |
| Explicit state machine | Weak | Implicit | Implicit | Phased | **Runtime** | Loop | Setup lifecycle | Implicit | Minimal | **Strong** |
| Resume/re-entry | Installed lifecycle | Same context | Same context/files | New session recommended | **Session restore** | Tests/code | Config persists | Code | **Core purpose** | **needs-info resume** |
| Concurrency/isolation | Weak | Fact parallelism | Weak writer model | Read-only survey | **Strong sessions** | External | Weak | External | Weak | Labels only |
| Unknown-outcome / idempotency | No | No | No | Temp timestamp | **Strong** | Test rerun | In-place update | No | No | State workflow |
| Untrusted-input model | Weak | — | Code contradiction | Repo evidence | **Strong** | Spec/oracle | Repo scan | Brief | Redaction | Verify reports |
| Independent expected truth | Weak | User decisions | Code/user | Deletion/friction judgment | **Final-state evals** | **Core** | User preview | Weak self-review | Weak | **Reproduction/tests** |
| Automated Harness/Eval | Unit search tests | Not observed | Not observed | Not observed | **Strong** | Repo tests, weak process Harness | Not observed | Not observed | Not observed | Partial workflows |
| Context-footprint measurement | No | No | No | No | **Strong** | No | No | No | Compaction by design | No |
| Visual artifact review | — | Prototype detour | — | HTML report | Screenshot/video | — | — | **Core** | — | PR diff |
| Pre-action clarification gate | Search screen | **Core** | **Core** | Report choice | Auth/task | Seam approval | Preview | Plan review | Explicit request | **Recommend+verify** |
| Durable execution brief | Skill package | No | No | Decision→spec | Commands | Tests | Config | Plan/code | Handoff | **Agent Brief** |
| Capability-conditional setup | Search result | — | — | — | Specialized skills | — | **Core** | — | Suggested skills | PR scope/config |
| Complexity/YAGNI control | Reuse first | Scope split | ADR sparsity | **Hotspot + deletion test** | Context profiles | One slice | **Evidence-gated complexity** | Restraint | Reference-only | Conditional grill |
| Self-bias countermeasure | Candidate screening | User pushback | Code/glossary | Multiple candidates | Evals | Independent literals | User preview | **Genericity counterfactual** | — | Maintainer decision |

## Architectural form factors observed

### 1. Thin wrapper over a reusable primitive

Examples: `grill-me`, `grill-with-docs`.

Strength: tiny hot path and one source of methodology truth.

Failure: source authors explicitly report that naming another Skill does not reliably prove it loaded. A one-line Skill is only robust when the loader/runtime makes delegation observable or mechanically enforced.

### 2. Thin discovery Skill over executable/versioned runtime

Example: `agent-browser`.

Strength: tiny stable entry point, runtime-coupled instructions never drift from installed binary, and evals test that models actually load/select them.

This is materially stronger than prose-only delegation.

### 3. Method/reference Skill used by a separate driver

Examples: `tdd`, `codebase-design`.

Strength: method stays reusable and orchestration stays elsewhere.

Failure: instruction compliance such as red-before-green is not automatically execution proof.

### 4. Stateful workflow driver

Examples: `triage`, `improve-codebase-architecture`, `setup-matt-pocock-skills`.

Strength: phases/roles define user interaction and durable state transitions.

Failure: semantic decisions remain model/human judgement unless state guards are mechanical.

### 5. Creative operating method

Example: `frontend-design`.

Strength: rich quality heuristics and self-bias critique.

Failure: same actor generates and grades its own aesthetic output; dedicated eval evidence is weak.

### 6. Context transport Skill

Example: `handoff`.

Strength: very small, pointer-over-copy compaction.

Failure: summary completeness/staleness is not mechanically bound to task/version/authority.

## Recurring cross-Skill lessons

1. **Short Skill length is not the goal by itself.** Good short Skills work because behavior has somewhere stronger to live: shared primitive, runtime, workflow, references or Harness.
2. **Prose delegation without loading/execution evidence is fragile.** `grill-with-docs` documents this explicitly.
3. **The strongest architecture in this set is not the longest prompt; it is thin entry + executable runtime + progressive reference + eval.** `agent-browser` is the clearest example.
4. **Human questions should be reserved for decisions, not retrievable facts.** `grilling`, `setup`, `triage` independently reinforce this.
5. **Durability must be selective.** Glossaries, ADRs, Agent Briefs, out-of-scope records, setup config and handoffs each store different knowledge classes.
6. **Negative knowledge is valuable.** Rejected architecture, out-of-scope features, anti-patterns, known AI design defaults and failure semantics prevent repeated mistakes.
7. **Verification quality varies sharply across the leaderboard.** Popularity does not predict Harness maturity: `agent-browser` has live/eval infrastructure while several prompt methods have none.
8. **Context cost is an architecture variable.** Thin routers, dynamic runtime skills, snapshot refs, pointers instead of copies and conditional setup all attack context growth differently.
9. **Do not collapse method into enforcement.** TDD/grilling/frontend-design contain useful methods, but a statement in SKILL.md is not proof the behavior occurred.
10. **Stateful workflows outperform chat memory when work spans time/actors.** Triage and browser sessions make state explicit; handoff/grill-me expose the limits of conversation-only state.
