# 跨对话继承系统建设与维护｜Handoff

- task_id: `continuity:universal-continuity-maintenance`
- task_class: `SYSTEM_INFRA`
- owner: `UNIVERSAL_CONTINUITY_HARNESS`
- status: `ACTIVE`
- contract: `CONTINUITY_V3_7`
- methodology profile contract: `1.0`
- system-maintenance policy: `1.5`
- artifact/context governance: `1.1`
- execution-readiness contract: `1.0`

## Current truth

- 工程真源：`D1traverser-debug/universal-continuity-agent@main`。
- 当前 maintenance chat 仍持有原 lease：`lease-f266a907-aaf1-4b6a-a283-0e64b979d652`；`resume_epoch=1`；本轮没有 takeover。
- 产品传播链 existing-chat / fresh-chat 双路径 E2E 均已 PASS。
- risk-tiered global audit 已常驻 CI preflight。
- 新增的 operator-dependence reliability incident 仍为 `PARTIALLY_REMEDIATED__PRODUCT_BEHAVIOR_EVAL_PENDING`；不能因为代码层 hardening 已完成就宣称总控已经能稳定自主识别所有 systemic signal。

## Operator-dependence reliability incident

真实故障：用户再次需要提醒 Universal，不应等待用户提出架构机制或枚举后续内部问题，而应自己诊断、反驳初始方案、识别系统性/重复失败并推进修复。

这不是缺少 policy 文案。`SYSTEM_MAINTENANCE_POLICY.json` 原本已经写明：用户不是系统维护员、重复纠正属于 reliability signal、非平凡方案必须挑战初始候选、内部维护不应等待用户枚举。

因此根因属于 enforcement / product behavior，而不是“再补一句提示词”。详细 incident：`audits/UNIVERSAL_OPERATOR_DEPENDENCE_RELIABILITY_INCIDENT_2026-10-10.md`。

## Verified remediation completed this turn

### 1. Declaration conformance 与 operational conformance 已在 runtime 分离

`runtime/methodology_conformance.py` 当前有两个不同层级：

- `evaluate_methodology_conformance(...)`：只证明 owner 声明的 profile/version/hooks/overrides 结构合法；
- `evaluate_operational_methodology_conformance(...)`：证明当前 action 激活的 profile 有实际 profile-run、required hooks 被观察到，并且 evidence refs 经过 caller-supplied independent verifier 验证。

硬边界：

- declaration PASS 不等于 operational PASS；
- receipt 本身只是 evidence index，不是 evidence；
- 没有 independent verifier 时 operational 必须 FAIL；
- evidence ref 验证失败必须 FAIL；
- 声明了 hook 但运行证据没有观察到 required hook 必须 FAIL；
- 只要求本次 action 激活的 profile，不能为了“统一”每次运行全部 profiles。

### 2. 该边界已进入 CORE_ALWAYS CI preflight

`runtime/system_audit.py` 新增核心不变量：

`methodology_declaration_operational_separation`

每次 CI 在 pytest 前都会跑 synthetic negative check，证明：

- declaration-only owner 不能被当成 operational；
- self-reported receipt 没有 independent verifier 不能 operational PASS。

Fault inventory 也新增：

- `declared_methodology_is_treated_as_operational_proof`
- `self_reported_methodology_receipt_lacks_independent_evidence_verification`

### 3. CI evidence

当前 behavioral head：`0692cd6929370507e8a4d09b2715515520618af5`

- GitHub Actions run: `38042185203`
- job: `114184468600`
- `runtime.system_audit`: PASS
- pytest: `116 passed in 0.20s`

所以这一部分是实际 executable evidence，不是管理文字。

## Enforcement assurance boundary

当前必须区分三件事：

1. **Owner business runtime gate**：当 owner 的所有相关业务 mutation 都经过 controller/dispatcher 时，可以达到真正的 write-path enforcement。
2. **Universal repository CI gate**：Universal 当前 GitHub Actions 会在 branch write 后运行 `system_audit + pytest`，因此当前可信等级是 `CI_ENFORCED_POST_WRITE`。
3. **Arbitrary ChatGPT GitHub maintenance write**：当前 GitHub connector 写操作并不先经过 Universal-owned pre-write dispatcher，所以 Universal 现在不能声称 arbitrary maintenance mutation 已 `WRITE_PATH_ENFORCED`。

因此本轮明确拒绝先造一个 `maintenance_admission.py` 然后假装所有 GitHub writes 都会经过它。

如果以后需要 hard pre-write enforcement，必须先建立真实 choke point，例如受控 maintenance dispatcher / PR gate / equivalent mutation path，然后再做绕过测试。

## Product-behavior gap still open

代码层 hardening 没有自动证明下面这个行为：

> 当用户只暴露症状、重复失败或给出一个可能错误的机制时，live Universal 是否会自己识别 systemic signal、检查 authority、生成替代方案并升级到 maintenance，而不是等待用户再次提醒。

当前 repo 没有 live-agent trace/eval runner。不能用关键词 detector 或静态 JSON fixture 冒充这个能力已经验证。

本 incident 的下一关闭条件必须包含真实 agent trajectory / product run：

- signal classification 不依赖固定关键词；
- 能区分普通一次性 revision 与 repeated/systemic defect；
- user / assistant / framework 的机制只作为 candidate；
- 会主动检查当前 authority；
- 至少比较可信替代方案并找反例；
- 不让用户承担内部迁移/recordkeeping；
- 不越过 owner lease 改写业务 truth；
- 最终 evidence 能被独立 grader / human calibration 复核。

外部 agent-eval 实践也支持这个方向：真正的 agent harness 应看 end-to-end trace、tool calls、handoffs 和最终环境状态，而不是只读自述 receipt；但外部资料只是 candidate evidence，不能代替本仓库实际验证。

## Financial Writing implication

Financial Writing 的判断中有三点已被当前代码事实证实：

- 当前 Universal methodology validator 过去确实只有 declaration-level semantics；本轮已修中央 validator；
- Financial 当前 `continuity/UNIVERSAL_PROTOCOL_ADAPTER.json` 尚未声明 methodology profile bindings；
- Financial 自己的 runtime business workflow 已有 controller choke point，因此其文章 stage/gate 比系统工程 maintenance write 更接近真正 hard enforcement。

但本轮没有从 Universal 直接重写 Financial 的 task state、checkpoint、active lease，也没有为了“看起来接入了”立刻给 Financial 塞 profile fields。

Financial 将作为严格 operational-conformance rollout 的重点 owner，但只有在合法 owner maintenance/writer 边界下，且必须同时有 owner-local executable evidence / quality eval；不能把 declaration PASS 叫 integration complete。

## Global audit baseline remains active

- `CORE_ALWAYS`
- `IMPACT_SCOPED`
- `OWNER_SENTINEL_ROTATION`
- `FULL_CONTROL_PLANE`
- `SYNTHETIC_FAULT_INJECTION`

普通维护不机械执行所有业务流水线；协议、authority、startup/storage/methodology/execution contract 等横切变化才升级 full sweep。

## Current stage

`V3_7_PRODUCT_E2E_PASS__OPERATIONAL_CONFORMANCE_CI_ENFORCED__OPERATOR_DEPENDENCE_INCIDENT_ACTIVE__OWNER_PROFILE_MIGRATION_IN_PROGRESS`

## Next action

1. 不新增 root management policy；保持当前 incident OPEN。
2. 在可获得真实 live-agent trajectory / product-run harness 时，建立并运行 maintenance-decision/escalation eval；没有真实 runner 前不伪造“自动 eval PASS”。
3. 保持 declaration-vs-operational separation 为 CI `CORE_ALWAYS`。
4. 下一 owner rollout 时优先验证 Video 当前绑定能否达到 operational conformance，而不只 declaration conformance。
5. Financial Writing / A股 / Novel 只在各自合法 owner turn 做 thin binding + owner-local regression/eval；不能从 Universal 抢 lease 或重写业务状态。
6. 若未来要求 GitHub maintenance pre-write hard enforcement，先建立真实 mutation choke point，再谈 `WRITE_PATH_ENFORCED`。
7. 无 scheduler/event-watch infrastructure 时，不声称聊天关闭后的离线持续自维护。

## Recovery rule

恢复本系统任务时先读 `TASK_MANIFEST.json` + 本 Handoff，再按 `ENTRYPOINT.md` 的 event-driven matrix 加载所需 authority。不要从旧聊天记忆重建执行真相，也不要因为看到 profile declaration 就假定 operational integration 已成立。
