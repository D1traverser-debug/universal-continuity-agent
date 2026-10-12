# Universal architecture drift root-cause repair — 2026-10-12

## Classification

`CONFIRMED_DEFECT`.

The prior architecture-watch pass correctly detected and emitted non-authoritative control signals, but stopping at signal emission was not closure. The current maintenance policy requires a confirmed material SYSTEM_INFRA defect to enter repair/evolution in the same maintenance turn when the authoritative writer and write surface are available.

## Why the user had to remind the system

The immediate operator-dependence failure was not lack of detection. Detection worked. The gap was between **signal emission** and **maintenance consumption**:

1. the architecture watch was intentionally a non-authoritative remote detector and could not take BUSINESS leases or rewrite business state;
2. its prompt emphasized create/update control signals, but did not encode the new architecture-delta semantics and could repeatedly report whole-HEAD drift;
3. the active Universal maintenance writer did not consume those confirmed SYSTEM_INFRA signals before the user asked whether they were actually repaired;
4. the assistant therefore treated `signal persisted` as a stopping point even though the system's own unified maintenance/evolution loop says confirmed defects must proceed to root cause, repair, validation, second-order review and durable learning.

This is classified as `OPERATOR_DEPENDENCE / SIGNAL_TO_REPAIR_HANDOFF_GAP` rather than a failure of GitHub signal persistence.

## Root cause 1 — volatile maintenance stage duplicated as cache truth

### Symptom

Universal CI failed with:

`GENERIC_TASK_REGISTRY maintenance current_stage is stale`

### Parent-system cause

`TASK_MANIFEST.current_stage` had evolved into a cumulative changelog containing many completed milestone labels. `GENERIC_TASK_REGISTRY`, although declared rebuildable/non-authoritative, duplicated that volatile string and CI required exact equality. Every new milestone therefore created a manual two-surface synchronization obligation.

### Repair

- Stabilize the SYSTEM_INFRA lifecycle stage to `SYSTEM_MAINTENANCE_ACTIVE`.
- Record detailed progress, evidence and next work in manifest status/evidence fields and HANDOFF rather than encoding history into `current_stage`.
- Keep the discovery cache thin and explicitly delegate detailed continuation to the authoritative TASK_MANIFEST/HANDOFF.
- Add regression tests bounding stage size and requiring stable-stage cache alignment.

This removes the failure class rather than merely copying the latest long string into both files.

## Root cause 2 — Universal Skill retained a shadow bootstrap order

### Symptom

`ENTRYPOINT.md` and `STARTUP_HOOK.md` require exactly `ENTRYPOINT.md + CURRENT_PROTOCOL.json` first, then event-driven authority loading, while `skills/universal-continuity/SKILL.md` retained an older fixed list and omitted `CURRENT_PROTOCOL.json` as the second mandatory bootstrap file.

### Parent-system cause

The thin Skill still contained a second evolving authority list. Internal control-plane evolution therefore required coordinated edits in both root authority and Skill prose.

### Repair

The Skill now contains only the two-file bootstrap and delegates every later load to current ENTRYPOINT event routing. Regression rejects reintroduction of the old fixed list.

## Root cause 3 — whole repository HEAD was misused as architecture identity

### Symptom

Financial GITHUB_CHAT legitimately writes article state/artifacts under `workspaces/articles/{task_id}` on `main`. Universal previously marked architecture stale whenever the repository HEAD moved, so normal article progression could repeatedly invalidate architecture validation without any architecture change.

### Parent-system cause

One identity (`owner repository HEAD`) was serving two different purposes:

- exact observation of the repository's latest state;
- identity of architecture-relevant surfaces.

That conflated business persistence with architecture evolution.

### Repair

Architecture freshness is now fail-closed but delta-aware:

- exact HEAD equality remains sufficient;
- when HEAD differs, a current remote compare must bind exactly from `architecture_validation_head` to `observed_owner_head`;
- only an explicitly evidenced `architecture_relevant_change=false` delta preserves freshness;
- missing/incomplete/mismatched evidence or any architecture-relevant path change remains stale and requires revalidation.

A live Financial example validated the distinction: after structural validation at `98063362...`, the owner advanced to `2c71944b...`; the exact compare contains only article `STATE`, Delivery, Mechanical Audit and Final Audit artifacts.

## Root cause 4 — Skill byte target was semantically under-specified

### Symptom

The architecture watch described A-share/Novel/Video as over an 8,192-byte Skill target, which could be read as a capacity limit on the owner system or its knowledge corpus.

### Parent-system cause

The contract had a `target_max_bytes` but did not state strongly enough that its scope is only the **always-loaded hot-path Skill router**. That allowed a performance heuristic to be interpreted as a repository/knowledge-size constraint.

### Repair

The shared contract now states mechanically:

- byte target scope = `HOT_PATH_SKILL_ROUTER_FILE_ONLY`;
- it is not a hard repository or knowledge cap;
- oversize is `PASS_WITH_DRIFT`, not an execution blocker;
- large references, research/distillation corpora, novel canon, market/company data, project artifacts and audit history are explicitly allowed and expected when the domain requires them;
- large corpora should be indexed and progressively disclosed: metadata/index first, exact current-action material second.

Thus Novel's masterwork distillation library and A-share research/data stores can continue to grow. The remaining Novel/A-share/Video warning means only that too much always-hot routing/policy prose may be loaded every invocation.

## Revalidation performed

- Financial structural architecture revalidated at `98063362b4716eaed4b222e40493eebe8b612524`; subsequent observed HEAD `2c71944bb22d04899773efbf8622e4b1ebf56609` is supported by an exact business-artifact-only delta.
- Novel structural architecture revalidated at `349879601b3114c7caee999ef4079088666c1d90` as `PASS_WITH_DRIFT`; all manifest refs are present. The 19,540-byte Skill warning is router-only; the large `research/masterworks`, `protocols`, `projects/canon` and manuscript corpus is not penalized for size.
- A-share and Video retain current validated HEADs and successful owner CI; their Skill-size findings remain performance/architecture warnings only.

## Assurance boundaries

This repair does not upgrade:

- owner runtime/live business correctness;
- Financial owner-native or provider-attested semantic certification;
- Novel current owner CI (runner did not execute steps);
- writing/investment/video output quality;
- BUSINESS task leases or state.

Universal did not mutate BUSINESS owner state during this repair.

## Prevention

1. Regression tests cover two-file Skill bootstrap, stable maintenance stage semantics, router-budget scope, and delta-aware freshness.
2. The existing hourly architecture-watch automation was updated to classify exact HEAD deltas and to treat the byte target as router-only.
3. Future architecture observation must fail closed when delta evidence is missing or architecture-relevant changes are present.
4. Signal persistence is not closure; confirmed SYSTEM_INFRA signals must be consumed by the active maintenance loop when the required authority/write surface is available.
