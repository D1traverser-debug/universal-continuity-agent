# 10 — N-Version Programming, Multi-Model Review and Common-Mode Failure

## Original idea

N-version programming attempts fault tolerance by independently developing multiple implementations from the same specification, executing them on the same input and combining/voting on outputs. Its reliability promise depends heavily on failure independence.

Knight and Leveson's classic experiment found that independently produced program versions exhibited more correlated failures than an independence assumption predicted. Separate implementations can share difficult inputs, ambiguous requirements, human reasoning patterns, libraries, design assumptions or specification defects.

## Direct relevance to multi-agent / multi-model systems

“Five models reviewed it” is not automatically five independent evidence sources.

Models may share:

- training-data distributions;
- prompts and task framing;
- the same incomplete source set;
- the same upstream specification error;
- the same tool outputs;
- the same conversation/context;
- the same executor/runtime;
- the same evaluator rubric;
- the same sampling or orchestration layer;
- the same blind spot induced by the architecture itself.

Therefore diversity of names, providers or roles does not equal statistical or epistemic independence.

## Independence dimensions that should be distinguished

For a critical review, the useful question is *what failure dependencies were actually separated?*

Candidate dimensions:

1. **execution context** — same conversation/process vs isolated run;
2. **model/provider** — same underlying model family vs different;
3. **prompt/specification** — same framing vs independently derived interpretation;
4. **evidence source** — same references vs independently collected/validated evidence;
5. **tool/runtime** — same connector/runtime vs distinct implementation path;
6. **reference model/evaluator** — same rubric/checker vs independent oracle;
7. **temporal/provenance** — post-hoc generated role records vs separately timestamped execution traces;
8. **failure domain** — whether a shared authority/specification defect would make all versions agree on the same wrong answer.

## Universal current state

Universal already rejects several dangerous shortcuts:

- same-session self-review is not called independent verification;
- role names do not prove distinct execution;
- structured receipts do not automatically prove independence;
- exact action/subject/input binding is required;
- provider-attested isolation is treated as a stronger evidence class.

This is materially better than naive majority voting.

## Remaining gap

There is no single **common-mode failure / independence matrix** for high-assurance multi-model or multi-agent review. As a result, a future system could accidentally overvalue “N reviewers” without recording which dependence dimensions differ.

## Voting is not always the right combiner

Majority voting assumes a crisp comparable output and tolerable minority error. For architecture/safety diagnosis, minority dissent may be the most valuable signal. Better patterns can include:

- independent proposals + explicit disagreement analysis;
- red-team search for counterexamples;
- deterministic oracle/checker where available;
- evidence-weighted adjudication;
- fail-closed on unresolved high-impact disagreement rather than forced majority consensus.

## What not to transplant

Do not create redundant models just to increase reviewer count. Extra agents add latency, cost and correlated ceremony. Independence should be purchased only where the failure cost warrants it, and the exact independence dimension must be evidenced.

## Current assessment

- Self-attestation / independence distinction: **STRONG**.
- Exact proof binding: **STRONG**.
- Common-mode failure taxonomy: **CURRENT GAP**.
- Model diversity metrics: **CURRENT GAP**.
- Default majority-vote architecture: **REJECTED as generally unsafe/underspecified**.
