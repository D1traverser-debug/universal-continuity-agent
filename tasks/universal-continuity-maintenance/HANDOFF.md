# 跨对话继承系统建设与维护｜Handoff

- task_id: `continuity:universal-continuity-maintenance`
- task_class: `SYSTEM_INFRA`
- owner: `UNIVERSAL_CONTINUITY_HARNESS`
- status: `ACTIVE`
- contract: `CONTINUITY_V3_7`
- current writer: `lease-d5136fdf-0661-4cd9-aeba-74db63c4dc3f`
- resume_epoch: `7`
- manifest_version: `58`
- meta-maintenance: `1.2`
- latest meta-run: `audits/META_MAINTENANCE_CONTEXT_CAPACITY_V58_2026-10-11.json`

## 当前阶段

`V3_7_AGENT_CONTROL_PLANE_V1_1_REGRESSION_VERIFIED__GLOBAL_LIVE_OWNER_REOBSERVATION_V51_PASS__VIDEO_SHARED_ARCHITECTURE_VERSION_DRIFT_REPAIRED__OWNER_REGISTRY_MEMBERSHIP_OBSERVATION_SEPARATION_REGRESSION_VERIFIED__ARCHITECTURE_WATCH_HOURLY__TOP10_SELECTED_PRIMITIVES_REGRESSION_VERIFIED__OWNER_DRIFT_SIGNALS_OPEN__OPERATOR_DEPENDENCE_LIVE_EVIDENCE_OPEN__PRIOR_LIVE_EVIDENCE_GATES_OPEN__CONTEXT_CAPACITY_PREFLIGHT_REGRESSION_VERIFIED`

## 本轮闭环

1. 真实新聊天 takeover 已完成：`resume_epoch 6 -> 7`，旧 lease 被 supersede；当前聊天持有上面的 lease。
2. V55 已把 turn-entry context-capacity preflight 写入既有 `CONTEXT_RECOVERY_POLICY.json`，不新增 token estimator、daemon 或第二套恢复 authority。
3. 预检采用 `GREEN / AMBER / RED` 风险等级；显式产品 conversation-length warning 可作为 RED 证据。没有可靠产品遥测时，不声称精确剩余 token/context 数字。
4. RED 时必须在开始新的 substantive work 前先 durable checkpoint / fresh-chat handoff；background/hourly monitors 不是 per-turn capacity guard。
5. 原始 CI `38138790729` 的唯一 pytest 失败来自 stale meta-run target，不是 capacity-preflight tests。
6. V57 首次 self-audit run `38139581465` 随后发现 `GENERIC_TASK_REGISTRY` 的 rebuildable cache 仍缓存旧 `current_stage`；严格 invariant 保留，未特殊放宽。
7. 同步 cache 后的 V57 preclosure CI `38139715061`：control-plane audit PASS、Agent architecture harness PASS、pytest `247 passed`。
8. V58 以单个 Git tree commit 同步 meta-run、TASK_MANIFEST、HARNESS_STATUS、GENERIC_TASK_REGISTRY 与本 Handoff；最终 regression-clean 以该 V58 closure commit 自身的 unchanged CI 成功为 acceptance condition。若该 CI 失败，按失败范围继续修复，不把本 Handoff 当作绿色证明。

## 当前 Next action

保持 turn-entry capacity preflight 与 safe-checkpoint/fresh-chat handoff 语义。出现显式产品长度警告或其他 RED evidence 时，不再开启新的实质工作，先 checkpoint。不要制造精确剩余上下文数字，也不要把后台 monitor 当成本回合容量守门器。

其余维护保持 signal-driven stop rule：没有新的 drift/evidence 时不制造新层；有新 signal 时再进入对应 authority。

## 仍然 OPEN

1. real new-owner fresh-chat product E2E；
2. operator-dependence independent heldout/live trajectory grader；
3. A-share / Novel / Video 已确认的 architecture / assurance drift；
4. owner-local action-level methodology/evidence 与业务 live quality/outcome gates；
5. recurring mechanisms 的长期运行质量与未来 remote-owner freshness；
6. 不得把结构/CI 通过外推成全局 flawless 或 live business outcome 证明。

## Recovery refs

- `tasks/universal-continuity-maintenance/TASK_MANIFEST.json`
- `tasks/universal-continuity-maintenance/HANDOFF.md`
- `CONTEXT_RECOVERY_POLICY.json`
- `tests/test_context_recovery_policy.py`
- `SYSTEM_MAINTENANCE_POLICY.json`
- `PROGRESS_OBSERVABILITY_POLICY.json`
- `OWNER_REGISTRY.json`
- `GENERIC_TASK_REGISTRY.json`
- `HARNESS_STATUS.json`
- `audits/META_MAINTENANCE_CONTEXT_CAPACITY_V58_2026-10-11.json`
- `tasks/universal-continuity-maintenance/CHECKPOINT_CONTEXT_CAPACITY_V55.md`
