# Source Index and Research Boundary

Accessed: 2026-10-13. Prefer first-party/original sources. URLs are evidence pointers, not production authority.

## Systems engineering / lifecycle / assurance

- NASA Systems Engineering Handbook: https://www.nasa.gov/reference/systems-engineering-handbook/
- NASA SE Fundamentals: https://www.nasa.gov/reference/2-0-fundamentals-of-systems-engineering/
- NASA SE Appendix / requirement and V&V matrices: https://www.nasa.gov/reference/system-engineering-handbook-appendix/
- RTCA DO-178 family landing page: https://www.rtca.org/do-178/
- FAA AC 20-115D: https://www.faa.gov/regulations_policies/advisory_circulars/index.cfm/go/document.information/documentID/1032046
- IEC 61508-1:2010 official catalog: https://webstore.iec.ch/en/publication/5515
- IEC 61508-3:2010 official catalog: https://webstore.iec.ch/en/publication/5517
- IEC 61508-1:2026 pre-release status: https://webstore.iec.ch/en/publication/117296

## Evolution / topology / environment

- Thoughtworks, Building Evolutionary Architectures free chapter: https://www.thoughtworks.com/content/dam/thoughtworks/documents/books/bk_building_evolutionary_architectures_second_edition_free_chapter.pdf
- Thoughtworks fitness-function material: https://www.thoughtworks.com/en-au/insights/articles/fitness-function-driven-development
- Team Topologies key concepts: https://teamtopologies.com/key-concepts
- Team Topologies interaction modes: https://teamtopologies.com/key-concepts-content/team-interaction-modeling-with-team-topologies
- Twelve-Factor dev/prod parity: https://12factor.net/dev-prod-parity

## Autonomic control / reconciliation / authority

- IBM Research, An architectural approach to autonomic computing: https://research.ibm.com/publications/an-architectural-approach-to-autonomic-computing
- IBM Redbook MAPE-K description: https://www.redbooks.ibm.com/redbooks/pdfs/sg246665.pdf
- Kubernetes Controllers: https://kubernetes.io/docs/concepts/architecture/controller/
- Kubernetes Custom Resources / controllers: https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/
- Kubernetes Operator pattern: https://kubernetes.io/docs/concepts/extend-kubernetes/operator/
- OpenGitOps principles: https://opengitops.dev/

## Supervision / fault management

- Erlang/OTP supervisor documentation: https://www.erlang.org/doc/apps/stdlib/supervisor.html
- Erlang supervisor design principles: https://www.erlang.org/doc/system/sup_princ.html
- NASA Software Safety Analysis / FDIR: https://swehb.nasa.gov/spaces/SWEHBVD/pages/102695725/8.09+-+Software+Safety+Analysis
- NASA Software Architecture Description / Fault Management: https://swehb.nasa.gov/spaces/7150/pages/16450571/7.07+-+Software+Architecture+Description

## Reliability / operations

- Google SRE, Embracing Risk / error budgets: https://sre.google/sre-book/embracing-risk/
- Google SRE, Monitoring Distributed Systems / four golden signals: https://sre.google/sre-book/monitoring-distributed-systems/
- Google SRE, Eliminating Toil: https://sre.google/sre-book/eliminating-toil/
- AWS Well-Architected Operational Excellence: https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/operational-excellence.html
- AWS Design for operations: https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/design-for-operations.html

## Verification / formal methods / resilience

- Accellera UVM current releases: https://www.accellera.org/downloads/standards/uvm
- Accellera UVM User Guide 1.1 (architecture concepts remain useful; older guide): https://www.accellera.org/images/downloads/standards/uvm/uvm_users_guide_1.1.pdf
- Leslie Lamport TLA+ home: https://lamport.azurewebsites.net/tla/tla.html
- TLA+ tools / TLC: https://lamport.azurewebsites.net/tla/tools.html
- Raft paper: https://raft.github.io/raft.pdf
- USENIX Raft page: https://www.usenix.org/conference/atc14/technical-sessions/presentation/ongaro
- AWS idempotent retries: https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/
- AWS retry control / backoff / jitter: https://docs.aws.amazon.com/wellarchitected/latest/framework/rel_mitigate_interaction_failure_limit_retries.html
- Knight & Leveson correlated multi-version failures (bibliographic/abstract access): https://www.sciencedirect.com/science/article/pii/S1474667017601009
- MIT PSASS STPA handbooks: https://psas.scripts.mit.edu/home/books-and-handbooks/
- Principles of Chaos Engineering: https://principlesofchaos.org/

## Source limitations

1. DO-178C and IEC 61508 normative standards are not reproduced here. Public RTCA/FAA/IEC pages establish scope, status and selected lifecycle/assurance facts only.
2. UVM's current release is IEEE 1800.2-related UVM 2020 reference implementation; the freely accessible UVM 1.1 guide is used only for stable testbench concepts such as agent/driver/monitor/coverage, not as a statement of the newest standard text.
3. Team Topologies and Evolutionary Architecture are organizational/software-architecture practices, not safety standards.
4. Chaos Engineering is an experimental discipline, not permission to inject destructive faults into authoritative user/business state.
5. N-version programming is included partly as a warning: separate implementations/models do not automatically imply statistically independent failures.
