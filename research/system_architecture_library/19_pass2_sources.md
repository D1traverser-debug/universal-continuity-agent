# 19 — Pass-2 Source Index and Epistemic Boundary

Accessed: 2026-10-13. Prefer first-party/current official documentation, original papers and current public repositories. URLs are evidence pointers only; they do not become production authority.

## OpenAI Agents API / Agents SDK

Official current documentation:
- https://developers.openai.com/api/docs/guides/agents
- https://developers.openai.com/api/docs/guides/agents-api/overview
- https://developers.openai.com/api/docs/guides/agents-api/architecture
- https://developers.openai.com/api/docs/guides/agents-api/sessions
- https://developers.openai.com/api/docs/guides/agents-api/environments/self-hosted
- https://developers.openai.com/api/docs/guides/agents-api/environments/lifecycle
- https://openai.github.io/openai-agents-python/
- https://openai.github.io/openai-agents-python/ref/run_state/

Implementation evidence (descriptive, not normative):
- https://github.com/openai/openai-agents-python/issues/4775 — lost acknowledgement / pending input duplication class; closed after reconciliation work.

Key boundary learned: OpenAI-managed session/harness durability does not make arbitrary application function tools or external systems transactional. Agents API session state and environment lifecycle are separate.

## Microsoft Agent Framework

Official current documentation:
- https://learn.microsoft.com/agent-framework/get-started/harness
- https://learn.microsoft.com/en-us/agent-framework/concepts/harness
- https://learn.microsoft.com/en-us/agent-framework/journey/workflows
- https://learn.microsoft.com/en-us/agent-framework/workflows/
- https://learn.microsoft.com/en-us/agent-framework/workflows/human-in-the-loop
- https://learn.microsoft.com/en-us/agent-framework/workflows/orchestrations/
- https://learn.microsoft.com/agent-framework/agents/observability
- https://github.com/microsoft/agent-framework/releases

Current release evidence observed: Python 1.19.0 dated 2026-09-18. The research treats Agent Framework as a moving 1.x line, not a frozen “1.0 feature set.”

Implementation issue families were reviewed in the public repository for approval/session restore, checkpoint replay, compaction/control-history integrity and protocol-version compatibility. Issue evidence is used only to identify failure classes.

## Google ADK 2.x / Agents CLI

Official/current sources:
- https://developers.googleblog.com/why-we-built-adk-20/
- https://developers.googleblog.com/announcing-adk-go-20/
- https://developers.googleblog.com/build-long-running-ai-agents-that-pause-resume-and-never-lose-context-with-adk/
- https://google.github.io/adk-docs/
- https://google.github.io/agents-cli/cli/
- https://google.github.io/agents-cli/guide/evaluation/
- https://github.com/google/adk-python/releases

Current release evidence observed: `google/adk-python` v2.10.0, dated 2026-09-24. Current 2.x research therefore includes post-2.0 replay/evaluation evolution rather than assuming initial GA behavior is frozen.

## LangGraph / LangSmith

Official/current sources:
- https://docs.langchain.com/oss/python/langgraph/overview
- https://docs.langchain.com/oss/python/langgraph/persistence
- https://docs.langchain.com/oss/python/langgraph/interrupts
- https://docs.langchain.com/oss/python/langgraph/durable-execution
- https://docs.langchain.com/oss/python/langgraph/subgraphs
- https://docs.langchain.com/oss/python/langgraph/
- https://docs.langchain.com/langsmith/evaluation-types
- https://docs.langchain.com/langsmith/data-plane
- https://github.com/langchain-ai/langgraph/releases

Current release evidence observed: LangGraph 1.2.13 dated 2026-10-05.

## Prior deep-pass source families

Retain and deepen the Pass-1 source set in `SOURCES.md`:
- NASA Systems Engineering Handbook, appendices, V&V/requirements material;
- Thoughtworks evolutionary architecture/fitness functions;
- Team Topologies official concepts and interaction modes;
- Raft original paper plus AWS Builders Library idempotency/retry guidance;
- Accellera UVM reference implementation/guides;
- IBM autonomic computing/MAPE-K original material;
- Kubernetes controller/operator/custom-resource docs;
- Erlang/OTP supervisor principles/docs;
- OpenGitOps principles;
- Google SRE book (risk/error budgets, monitoring, toil);
- AWS Well-Architected Operational Excellence;
- Twelve-Factor dev/prod parity;
- FAA/RTCA public DO-178C recognition material;
- IEC public 61508 catalog/lifecycle material;
- Lamport TLA+/TLC material;
- Knight & Leveson multi-version common-mode research;
- MIT STPA handbooks;
- Principles of Chaos Engineering;
- NASA software safety/FDIR guidance.

## Depth criterion used in Pass 2

A framework is considered “deep-studied for architecture comparison” only after the research can answer, at minimum:
1. What problem is it designed to solve?
2. What is its runtime/control/execution model?
3. What state exists, and who owns authority over it?
4. What are its key failure semantics?
5. How does it recover/resume/reconcile?
6. What verification/observability/evaluation evidence does it expose?
7. How does change/version/promotion work?
8. What does it explicitly *not* guarantee?
9. Which parts map to Universal, and which would be cargo-cult transplantation?

Passing this criterion is **not** a claim of exhaustive mastery of every API, every source file, every paid normative clause, every historical version or every future release.

## Standards/copyright boundary

- DO-178C and IEC 61508 paid normative text is not reproduced; no certification/compliance claim is made.
- UVM concepts use public Accellera/IEEE-related materials; no IEEE 1800.2 conformance claim is made.
- GitHub issues are implementation observations, not intended framework contracts.
- Current-version facts are timestamped research evidence and can age; production architecture must re-observe them before relying on version-specific behavior.
