# 跨对话继承系统建设与维护｜Handoff

- task_id: `continuity:universal-continuity-maintenance`
- task_class: `SYSTEM_INFRA`
- owner: `UNIVERSAL_CONTINUITY_HARNESS`
- status: `ACTIVE`
- contract: `CONTINUITY_V3_7`
- current writer: `lease-4b4bc507-0949-4b2e-aed4-c0186dd07566`
- resume_epoch: `2`

## 当前总状态

- Known-topology existing/fresh-chat Continuity E2E：历史真实证据 PASS；**real new-owner cold-start product E2E 仍 OPEN**。
- Dynamic owner membership：REGRESSION_VERIFIED；`OWNER_REGISTRY.json` 是唯一 membership authority。
- **Cross-owner execution proof binding：REGRESSION_VERIFIED。** Video / A-share / Financial 三次自检的共同母漏洞已从 owner-specific 症状蒸馏为 `unbound-proof replay / wrong-subject evidence` 与 `shadow obligation list / configured-obligation drift`。
- **Persistence / assurance separation：PASS at contract/regression level。** `COMMITTED` 只表示权威状态已持久化并回读，不表示 execution / methodology / review / quality / outcome 已通过；OPEN/BLOCKED gate 本身允许被可靠 checkpoint。
- Universal operator-dependence incident：仍 OPEN；本轮不能用代码/CI 代替 independently graded live trajectories。
- Operational methodology receipt contract = 1.2；独立 evidence-ref verification 与独立 hook-assessment semantic verification 仍是 action-level 高保证要求。
- Novel：真实 CH9 production proof / true independent execution attestation 仍 OPEN。
- Financial：真实 action-level methodology conformance / independent blind-pairwise prose-quality promotion 仍 OPEN。

## 本轮触发

用户提供了 Video Growth、A-share Market、Financial Writing 三份使用总控“挑刺→蒸馏→学习→进化”完成的 owner 自检，要求总控继续检查自己，而不是把三个 owner 的局部修复分别当作终点。

## 跨-owner 根因

三份 owner 自检表面不同：

- Video：角色/PASS/计划任务存在，但执行证明可能缺失或未绑定 exact brief；硬编码 stage subset 会漏掉新增计划任务。
- A-share：ReplayEval/结构化 GateDecision 存在，但未必证明机械 replay 或独立 audit 真执行。
- Financial：judge/evidence refs 存在，但若未绑定 exact candidate/change/run，旧或无关 trace 可以被重放。

共同母漏洞：

1. **Proof presence != proof for this exact claim.** 真实性、精确绑定、语义支持、独立性是不同问题。
2. **Canonical configured obligation != shadow allowlist.** 如果 machine-readable plan 已声明任务，runtime 必须从 canonical plan 派生 proof obligation，不能再维护一份容易漏项的阶段/角色名单。

## 总控自身挑出的三个缺陷

### 1. Execution contract 有原则，但缺通用机械门

旧 `EXECUTION_READINESS_CONTRACT.json` 已写“receipt 必须绑定 task/stage/capability/executor/input/output/result”，但 `runtime/execution_readiness.py` 只负责执行前 readiness，没有通用 post-execution exact-binding validator。

修复：新增 `runtime/execution_receipt.py` + `tests/test_execution_receipt.py`。

可机械拒绝：
- wrong task / stage / capability / action；
- wrong candidate/change/brief/replay subject binding；
- wrong input/artifact digest；
- reused receipt id；
- owner 显式要求时 reused execution/provider/work-order identity；
- incomplete output evidence。

证据上限：这个 validator 只证明 **binding + configured anti-replay**；不证明 provider issuance、executor trust、chronology、reviewer independence 或 semantic quality。

### 2. Execution-readiness regression 仍有四 owner 硬编码

`tests/test_execution_readiness.py` 仍直接列出 Financial / A-share / Novel / Video。已改为从 `OWNER_REGISTRY` 动态推导 business owner set，消除最后一份已发现的 closed-world execution topology allowlist。

### 3. `COMMITTED` 与 operational methodology assurance 被错误耦合

`PROGRESS_OBSERVABILITY_POLICY.json` 原本把 COMMITTED 定义为 persistence success；后续 `ENTRYPOINT.md` 又出现把 operational methodology conformance 与 COMMITTED 绑定的语义。

已拆开：
- `COMMITTED = DURABLE_PERSISTENCE_ONLY`；
- 高 assurance gate 未过 -> gate 保持 OPEN/BLOCKED；
- 但“这个 gate 仍 OPEN/BLOCKED”必须能够被 COMMITTED 到 checkpoint；
- verified commit 不会提升所提交内容的 assurance level。

这防止另一种证据偷换：`commit succeeded` ≠ `review/quality/methodology succeeded`。

## 二阶反攻与真实红灯

不是第一次局部 PASS 就收口。

Intermediate head `58c330697b74e9638a592321ac2a92708fa34d11`：
- `runtime.system_audit` PASS
- full pytest **FAIL**：148 passed / 1 failed
- 失败测试仍要求 `COMMITTED` 与 `operational conformance` 耦合。

没有为绿灯回滚新分离模型；改为保留“operational conformance 才能宣称 gate/action 完成”，同时让 persistence status 独立。

Validated behavioral head `563a10476e889b132ef66dcd4cc186ef0ad5fe1f`：
- Actions run `38071270624`
- job `114269000183`
- system_audit PASS
- full pytest PASS

## 本轮新增 / 修改 authority

- `runtime/execution_receipt.py`
- `tests/test_execution_receipt.py`
- `EXECUTION_READINESS_CONTRACT.json`
- `tests/test_execution_readiness.py`
- `CONTINUOUS_LEARNING_POLICY.md`
- `tests/test_system_maintenance_policy.py`
- `PROGRESS_OBSERVABILITY_POLICY.json`
- `tests/test_progress_observability.py`
- `ENTRYPOINT.md`
- `audits/CROSS_OWNER_EXECUTION_EVIDENCE_BINDING_DISTILLATION_2026-10-11.md`

## Assurance ceiling

本轮 cross-owner hardening 当前最多是：

`REGRESSION_VERIFIED`

不能升级为：
- ACTION_LEVEL_INDEPENDENTLY_VERIFIED；
- LIVE_OUTCOME_VERIFIED。

原因：GitHub CI 是代码/测试的独立执行证据，不是对本轮所有 maintenance reasoning / hook assessment 的独立语义 grader。

## Current stage

`V3_7_KNOWN_TOPOLOGY_PRODUCT_E2E_PASS__NEW_OWNER_COLD_START_PRODUCT_E2E_PENDING__DYNAMIC_OWNER_MEMBERSHIP_REGRESSION_PASS__CROSS_OWNER_EXECUTION_PROOF_BINDING_REGRESSION_PASS__PERSISTENCE_ASSURANCE_SEPARATION_PASS__OPERATOR_DEPENDENCE_INCIDENT_ACTIVE__OWNER_PROFILE_APPLICABILITY_GUARD_PASS__SECOND_ORDER_EVOLUTION_METHOD_DISTILLED__NOVEL_RELEASE_EVIDENCE_BINDING_HARDENED__FINANCIAL_THREE_PROFILES_BOUND_AND_REGRESSION_PASS__ACTION_LEVEL_CONFORMANCE_PENDING__LIVE_QUALITY_EVIDENCE_PENDING`

## Next action

1. 把 exact-action proof binding 作为跨-owner invariant；owner 只保留自己的 subject/input identity 与业务 gate 语义，不再复制母规则。
2. Existing owners 在真实 gate 上逐步采用 central validator 或等价 owner-native exact-binding；Universal 不偷 business lease、不替 owner 改业务状态。
3. 需要独立 reviewer/methodology semantic verification 的 gate，缺 distinct verifier/trace 时继续 OPEN；不要拿 CI 或 COMMITTED 冒充。
4. Real new-owner fresh-chat product E2E 继续 OPEN，直到真实新 BUSINESS owner + 真新 ChatGPT chat 形成产品轨迹。
5. Universal operator-dependence incident 继续 OPEN，直到 independently graded held-out/live product trajectories 通过。
6. Novel / Financial 继续各自现有 live-evidence gates；不要求用户继续制造内部例子或正样本。

## Recovery refs

- `tasks/universal-continuity-maintenance/TASK_MANIFEST.json`
- `ENTRYPOINT.md`
- `EXECUTION_READINESS_CONTRACT.json`
- `runtime/execution_receipt.py`
- `tests/test_execution_receipt.py`
- `PROGRESS_OBSERVABILITY_POLICY.json`
- `CONTINUOUS_LEARNING_POLICY.md`
- `OWNER_REGISTRY.json`
- `runtime/owner_topology.py`
- `audits/CROSS_OWNER_EXECUTION_EVIDENCE_BINDING_DISTILLATION_2026-10-11.md`
- `audits/COLD_START_NEW_OWNER_TOPOLOGY_INCIDENT_2026-10-11.md`
- `audits/UNIVERSAL_OPERATOR_DEPENDENCE_RELIABILITY_INCIDENT_2026-10-10.md`

恢复时先读 manifest + 本 Handoff，再按 `ENTRYPOINT.md` 事件矩阵加载当前动作需要的 authority。不要把 CI、receipt existence、COMMITTED 或历史 topology PASS 外推成更高 assurance。
