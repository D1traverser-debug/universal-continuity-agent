# System Architecture & Reliability Benchmark Library

Status: `PASS2_PRUNED_AND_APPLICABILITY_SCREENED / NON_AUTHORITY / NO_PRODUCTION_REFACTOR`  
Created: 2026-10-13  
Scope: Universal Continuity architecture/maintenance benchmark research  
Load policy: **cold-path only**; never part of normal bootstrap or ordinary BUSINESS execution.

## Why this library exists

A user challenge exposed a maintenance meta-method gap: an audit can be mechanically correct against its checklist while the checklist itself omits a mature family of architecture, control, verification, recovery or reliability questions. A second challenge correctly identified that the first research pass was still too shallow to be called “deep learning.”

Pass 2 therefore raised the research bar. A studied framework is counted in the current deep-study set only when publicly accessible first-party/original material is sufficient to compare, at minimum:

1. purpose/problem boundary;
2. runtime/control/execution model;
3. state and authority;
4. failure semantics;
5. recovery/resume/reconciliation;
6. verification/observability/evaluation;
7. lifecycle/change/versioning;
8. explicit non-guarantees and misuse boundaries;
9. mapping to Universal without cargo-cult adoption.

This is not a claim of exhaustive mastery of every API, source file, paid normative clause or future version.

## Current deep-study scope after source pruning

Retained architecture/reliability subjects:

- NASA Systems Engineering / V-model reasoning;
- Evolutionary Architecture / fitness functions;
- Team Topologies / inter-group interaction;
- distributed-systems consistency, retries and idempotency;
- UVM verification architecture using public Accellera material;
- MAPE-K;
- Kubernetes controller/operator reconciliation;
- Erlang/OTP supervision;
- GitOps/OpenGitOps;
- Google SRE;
- AWS Well-Architected Operational Excellence;
- environment parity / Twelve-Factor;
- TLA+ / model checking;
- N-version/common-mode failure research;
- NASA FDIR/fault management;
- STPA;
- Chaos Engineering.

Current agent-runtime subjects:

- OpenAI Agents API;
- OpenAI Agents SDK;
- Microsoft Agent Framework current 1.x;
- Google ADK current 2.x;
- Google Agents CLI/evaluation lifecycle;
- LangGraph current 1.2.x;
- LangSmith tracing/evaluation/deployment lifecycle.

### Public evidence lenses, not “fully deep-studied frameworks”

- FAA public airborne-software assurance material related to DO-178C;
- IEC public functional-safety lifecycle material related to IEC 61508.

The paid/copyrighted normative DO-178C and IEC 61508 standards are **not** counted as fully studied framework corpora because the complete normative texts are not reliably available here. Their public first-party material may support bounded lifecycle/traceability/hazard questions only; no certification or normative-conformance claim is made.

UVM is not removed: Accellera publicly provides sufficient guides, class references and reference implementation material for architecture-level study, while IEEE 1800.2 conformance is not claimed.

## Parent dimensions

The research is organized around architecture questions rather than product names:

1. Purpose / lifecycle / decomposition
2. Control / reconciliation
3. Authority / change
4. Topology / interaction
5. Execution / environment
6. Supervision / recovery
7. Reliability governance
8. Verification / assurance
9. Formal correctness
10. Safety / hazard control
11. Evolution / learning
12. Resilience experiments
13. Durable execution lineage
14. HITL / approval / replay semantics
15. Evaluation feedback lifecycle

## Current applicability result

`22_applicability_screen.md` supersedes `21_pass2_candidate_map.md` as the current applicability view. It concludes that the retained knowledge is broadly useful, but should be consolidated into six cross-cutting primitive families rather than implemented as one subsystem per named framework:

1. **Derived System / Authority Model**
2. **Runtime Semantics + Execution Lineage + Effect Contract**
3. **Assurance / Coverage / Evaluation Trace**
4. **Supervision / FDIR / Hazard Control**
5. **Measured Reliability + Progressive Rollout / Resilience**
6. **Formal Writer / Commit Protocol**

Explicit non-adoptions include Raft under the current single-writer threat model, literal UVM phase/class transplantation, Kubernetes-ifying finite user tasks, a centralized MAPE-K knowledge database, permanent LLM supervisor agents, a generic runtime abstraction that hides substrate replay/state differences, blanket multi-agent orchestration, certification-style process imitation, and fabricated SLO targets.

## Reading order

For the current deep pass and applicability result:

1. `15_prior_frameworks_deep_pass.md`
2. `16_agent_runtime_frameworks_2026.md`
3. `17_state_resume_side_effect_matrix.md`
4. `18_agent_runtime_failure_case_matrix.md`
5. `19_pass2_sources.md`
6. `20_pass2_current_universal_gap_audit.md`
7. `21_pass2_candidate_map.md` — historical/frozen candidate map
8. `22_applicability_screen.md` — current source-pruned applicability decision

The original `01`–`14` notes remain historical Pass-1 evidence and should not be mistaken for the current depth claim. Historical notes are preserved rather than rewritten to fabricate provenance; current scope and supersession are controlled by this README and `CATALOG.json`.

## Authority boundary

This directory is **learning/evidence, not corrective architecture**. It does not change owner BUSINESS truth or automatically promote architecture candidates. The user authorized source pruning/demotion and applicability screening; production architecture refactor still requires a separate explicit command.

No framework name is authority. The six primitive families are a screened design input, not a production roadmap.

## Freshness boundary

- GitHub issue evidence is implementation failure evidence, not normative behavior.
- OpenAI/Microsoft/Google/LangGraph facts are version-sensitive and were re-observed on 2026-10-13 for this applicability screen; re-observe again before a later implementation depends on version-specific behavior.
- Public FAA/IEC material is evidence-lens only; paid normative standards are outside the complete research corpus.
