# 01 — Systems Engineering, V-model Reasoning, DO-178C and IEC 61508

## Core problem addressed

Large systems fail when local implementation outruns mission definition, requirement decomposition, interface control, lifecycle change management, verification/validation planning, or hazard-derived assurance. NASA systems engineering, aviation design-assurance practice and IEC functional-safety lifecycle thinking all attack this from different domains.

## NASA systems-engineering structure

NASA's handbook treats systems engineering as a lifecycle discipline spanning design, realization, technical management, operations and retirement. Its useful architecture lesson is the **two-direction structure**:

- top-down: stakeholder expectations → technical requirements → logical/behavioral decomposition → design solution;
- bottom-up: implementation/integration → verification → validation → transition to the next system level.

That symmetry is more important here than copying a literal drawing of a V. Verification asks whether the realized item complies with the approved requirements; validation asks whether it fulfills intended use in the intended environment. NASA also emphasizes interface management, baselines, configuration/change authority, requirement quality, verification matrices and validation matrices.

### Universal mapping

Universal has pieces of this already: protocol and owner contracts, state-machine guards, CI, action receipts, owner checkpoints and live-outcome assurance ceilings. What is not yet first-class is a **bidirectional trace** from user/system objective → invariant/requirement → owning surface → executable guard → test/eval → live evidence → residual risk.

## V-model reasoning

Use the V-model as a reasoning pattern, not as a mandated delivery process:

- each decomposition decision should have a corresponding integration/verification obligation;
- each interface should have an integration test or observation strategy;
- each requirement should define how it will be verified;
- each intended-use claim should define how it will be validated in the real execution environment.

Universal currently has strong local tests but weaker explicit pairing between every architecture requirement and its verification/validation evidence.

## DO-178C public guidance boundary

RTCA identifies DO-178C as the current core airborne-software design/product-assurance document (published 2011), and FAA AC 20-115D recognizes DO-178C together with DO-330/331/332/333 as an acceptable means for airborne software assurance. Public material is enough to extract several general lessons:

- assurance objectives must be explicit rather than inferred from process ceremony;
- verification evidence must be tied to development artifacts and objectives;
- tool confidence matters when a tool can create or verify assurance evidence;
- independence requirements depend on criticality;
- configuration management and change impact matter throughout the lifecycle;
- formal methods can supplement conventional verification but do not erase evidence obligations.

**Important correction:** DO-178C does not simply equal “the V-model,” nor should this system claim DO-178C compliance. The full standard is not freely reproduced and Universal is not an airborne certification program. The useful lesson is rigorous objective/evidence traceability proportional to consequence.

## IEC 61508 functional-safety lifecycle

IEC 61508-1:2010 is the current valid Edition 2 general standard as of this study; IEC 61508-3:2010 covers safety-related software lifecycle requirements. IEC's public framework explicitly spans:

concept/scope → hazard and risk analysis → safety requirements/allocation → realization → installation/commissioning → validation → operation/maintenance/repair → modification/retrofit → decommissioning/disposal.

IEC also separates required safety integrity from systematic capability and treats functional-safety management, assessment, competence and lifecycle modification as part of assurance. A 2026 Edition 3 pre-release exists, but the official page still marks Edition 2 (2010) valid and Edition 3 under development with forecast publication in 2027; therefore this library does not treat the pre-release as current normative authority.

### Universal mapping

Useful candidate questions:

- Which Universal operations are merely reliability-sensitive, and which could create high-impact user/business harm if wrong?
- Is criticality reflected in review independence, test depth and mutation permission?
- When a maintenance change modifies an invariant, is change impact traced across every dependent verification obligation?
- Is retirement/decommissioning of obsolete mechanisms explicit, or can stale paths remain live?
- Is the maintainer/tool evidence trusted beyond what has actually been qualified?

## What not to transplant

Do not impose certification paperwork or safety-integrity levels on ordinary writing/business workflows. The value is structural: lifecycle completeness, traceability, criticality-proportional assurance, independent verification where warranted, and controlled modification. Excess ceremony on low-risk paths would violate Universal's hot-path and bounded-complexity principles.

## Current assessment

- Lifecycle/change thinking: **PARTIAL / STRONGER THAN AVERAGE**.
- Explicit requirement-to-evidence trace matrix: **CURRENT GAP**.
- Criticality-proportional assurance taxonomy: **PARTIAL** (assurance ladder exists; hazard criticality is less explicit).
- Controlled retirement/supersession: **PARTIAL / PRESENT**, but cross-surface completeness is not formally traced.
