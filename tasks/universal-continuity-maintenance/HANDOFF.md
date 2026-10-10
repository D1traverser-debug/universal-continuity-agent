# 跨对话继承系统建设与维护｜Handoff

- task_id: `continuity:universal-continuity-maintenance`
- task_class: `SYSTEM_INFRA`
- owner: `UNIVERSAL_CONTINUITY_HARNESS`
- status: `ACTIVE`
- contract: `CONTINUITY_V3_7`
- system-maintenance policy: `1.5`
- execution-readiness contract: `1.0`

## 当前权威状态

- 工程真源：`D1traverser-debug/universal-continuity-agent@main`。
- 当前 writer：`lease-4b4bc507-0949-4b2e-aed4-c0186dd07566`，`resume_epoch=2`。
- existing-chat / fresh-chat Continuity 产品传播 E2E 均已 PASS。
- operator-dependence reliability incident 仍为 OPEN；不能用代码/CI 代替真实 live product trajectory evidence。
- Financial Writing 的结构性格式冲突、质量回归 harness 与 owner regression 已修复并通过；但“文章质量实证提升”仍缺独立 blind pairwise live evidence。

## 本轮新增进度

### Financial 当前 session handshake

`quality_regression_promotion_gate` 的 owner ceiling 为 `HARNESS_WIRED`。本会话缺：

- independently verifiable pairwise judge execution identity / trace；
- 对应 evidence verifier。

因此只阻塞 Financial 的 live quality promotion gate；不得用当前聊天自行切换评审角色冒充独立证据，也不得改写 Financial 业务 task state / lease。

### Universal operator-dependence eval harness

已新增：

- `runtime/maintenance_decision_eval.py`
- `evals/maintenance_decision_cases.json`
- `tests/test_maintenance_decision_eval.py`

设计边界：

- 不做关键词匹配；真实 product trace 必须由独立/分离 grader 转成结构化 criteria；
- 要求 grader id/run id、trace/evidence refs 与 caller-supplied evidence verifier；
- 同时覆盖 under-escalation 与 over-escalation；
- same-run/self-reported grade 不能作为独立证据；
- 该 harness 是 eval/runtime surface，不新增 root policy、registry 或 permanent Agent。

验证：

- isolated local eval regression：`7 passed`；
- final harness head：`61641696ca580061dd8a156b126a0fb438e984d8`；
- GitHub Actions run `38054693980` / job `114220641319`：`runtime.system_audit` PASS，完整 pytest PASS。

这只证明 eval harness 可执行，不证明 live Universal 已经稳定自主升级 systemic signal。

## 仍未证明

- Financial prose quality improvement：PENDING independent live blind pairwise evidence。
- Personalized Writing DNA：PENDING real accepted/edit/performance evidence。
- Universal operator-dependence incident closure：PENDING real product trajectories + independent grading/evidence verification。
- arbitrary ChatGPT GitHub maintenance mutation：仍不是 `WRITE_PATH_ENFORCED`；当前保证仅到 repository CI post-write。

## Current stage

`V3_7_PRODUCT_E2E_PASS__OPERATOR_DEPENDENCE_INCIDENT_ACTIVE__FINANCIAL_OWNER_HARNESS_REPAIRED_AND_REGRESSION_PASS__LIVE_QUALITY_EVIDENCE_PENDING__OWNER_PROFILE_MIGRATION_IN_PROGRESS`

## Next action

1. 若获得独立可验证的 product-run / judge path，先跑 Universal maintenance-decision held-out suite；incident 只有 suite 真实 PASS 才能关闭。
2. 若获得 Financial 独立 pairwise judge + evidence verifier，跑 offshore-wind rejection 与 rutile held-out：已知失败必须改善，held-out 不得退化。
3. 两个 live-evidence gate 都缺当前 session capability 时，不伪造 PASS；继续可独立推进的 owner profile migration / control-plane maintenance，并保持 owner authority 与 lease 边界。
4. 不要求用户为了内部维护额外制造正向样本或充当 evaluator。

## Recovery refs

- `tasks/universal-continuity-maintenance/TASK_MANIFEST.json`
- `audits/UNIVERSAL_OPERATOR_DEPENDENCE_RELIABILITY_INCIDENT_2026-10-10.md`
- `SYSTEM_MAINTENANCE_POLICY.json`
- `EXECUTION_READINESS_CONTRACT.json`
- `runtime/maintenance_decision_eval.py`
- `evals/maintenance_decision_cases.json`
- Financial: `D1traverser-debug/financial-writing-agent@main:continuity/EXECUTION_CAPABILITIES.json`

恢复时先读 manifest + 本 Handoff，再按 `ENTRYPOINT.md` 事件矩阵加载本次动作需要的 authority；不要从旧聊天重建执行真相。
