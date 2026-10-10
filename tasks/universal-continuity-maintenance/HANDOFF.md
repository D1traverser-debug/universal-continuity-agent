# 跨对话继承系统建设与维护｜Handoff

- task_id: `continuity:universal-continuity-maintenance`
- task_class: `SYSTEM_INFRA`
- display_name_zh: `跨对话继承系统建设与维护`
- owner: `UNIVERSAL_CONTINUITY_HARNESS`
- status: `ACTIVE`
- contract: `CONTINUITY_V3_7`
- system-maintenance policy: `1.4`
- artifact/context governance: `1.1`
- execution-readiness contract: `1.0`

## Current truth
- 工程真源：`D1traverser-debug/universal-continuity-agent@main`。同聊天 active lease 仍为 `lease-f266a907-aaf1-4b6a-a283-0e64b979d652`，`resume_epoch=1`；本轮没有 takeover。
- Universal 已从“用户指出一个刺 -> 新增 policy/prompt/role”的逐症状补丁方式收敛为 architecture-first + operational-hygiene：新增 root authority surface 受 admission gate 约束，重复 owner 故障进入 scoped reliability incident，文件/缓存/外部引用由现有 artifact governance 管理。
- 本轮又暴露了更深一层缺口：现有 Continuous Learning 虽要求比较当前 contract、拒绝不合适 guidance，但真实对话中仍会先把用户提出的 UVM/extends 类比当作主要架构方向，直到用户再次指出“我的视角不一定对”。这说明过去的学习系统缺少机械的 epistemic-independence gate，容易把用户或助手的第一方案高质量工程化，而不是先独立验证问题和候选。
- 已修，不新建平行 policy：
  - `CONTINUOUS_LEARNING_POLICY.md` 新增 `Epistemic independence and candidate-adoption gate`。用户对目标/约束/其独有外部事实仍是 authority；用户提出的实现机制/类比、助手自己的第一方案、其他 Agent 建议、热门框架或网页观点都只是 candidate。
  - 非平凡架构/进化候选必须先分离目标与方案、读当前 authority、比较至少一个可信替代方案、主动找反例/失败条件，并按 correctness、failure containment、coupling、maintainability、observability、migration/hot-path cost、reversibility、owner boundary 等适用维度比较；未经 eval/regression 不能声称更好。
  - `SYSTEM_MAINTENANCE_POLICY.json` v1.4 增加 `PREMATURE_SOLUTION_CANONICALIZATION_OR_USER_CORRECTION_SIGNAL`、`CHALLENGE_INITIAL_SOLUTION_CANDIDATES` 和对应 reliability/failure semantics。用户反复需要纠正系统“把我的建议当 canonical architecture”现在本身就是 reliability signal。
  - `OWNER_ADAPTER_CONTRACT.json` 要求 durable owner 把用户/助手/其他 Agent 的 solution proposal 当 candidate，不当 authority；domain-specific evolution 可以覆盖具体方法，但不能绕过跨 owner 的 evidence、reliability、authority/ownership invariants。
- 这次修复明确否定“类比就是架构”。UVM、Kubernetes、OS、组织结构、生物进化等只能作为 candidate generator；不能因类比漂亮就决定系统结构。
- 当前判断：Universal 尚未结构性失控，但已经接近“方法学膨胀”临界点。`SYSTEM_BLUEPRINT.md` 已有 11 个 architecture layers，而 `OWNER_ADAPTER_CONTRACT` 正不断吸收 artifact、maintenance、learning、GC、reliability 等横切要求。继续把所有共享方法学直接塞进一个巨型父 contract、再让每个 owner 复制实现，会造成 control-plane/owner 双向臃肿。
- 下一架构问题必须独立评估，不预设 UVM inheritance 为答案：跨 Agent 通用能力更可能需要 `small stable kernel + composable methodology modules/bundles + owner hooks/overrides + central conformance/evidence` 一类组合式结构，但这仍是待比较的候选，不是当前生产 authority。
- 外部模式提供了可比较证据而不是答案：Kubernetes 倾向多个窄 controller/自定义 controller 编码 domain knowledge，而不是单个 monolithic control loop；OPA 将通用 policy 与执行解耦，并强调 bundle roots/namespaces 以避免多来源冲突；OpenAI Agents SDK 建议从单 specialist 起步，按需要增加 orchestration、guardrails、state、observability/eval，而不是先建立巨型继承体系。

## Operational hygiene / owner status
- 重复持久要求、已修 defect 复发、mandatory gate 被重复绕过、stale rule/state/artifact 重复驱动执行，都属于 reliability signal；affected owner/capability 在根因修复 + regression/eval + authority reread 前冻结无关扩张，其他健康 owner 不受影响。
- 自清洁仅限 owner/dependency/retention-aware GC；不能因为旧就删 checkpoint、accepted/published business evidence 或 active next_action 依赖。
- Financial Writing：真实 `record_writing_learning_sample` 已接入 material user feedback durable-learning claim，profile v2 `learning_evidence_capture = SESSION_EXECUTABLE`。final CI run `38032299542` / job `114155603504` / head `a6e69993787394f1abeef4b5da6e5bb3cb0b5e9d`，50 tests + SDK/MCP/contract/static/wheel/DOCX smokes PASS。
- Video Growth：旧 LEARN 阶段声明 `production_methodologist` / `evolution_engineer` 却未调度，已改为 `Production Methodologist -> Evolution Engineer candidate -> Red Team -> Showrunner`。scheduled learning evidence = `SESSION_EXECUTABLE`；mid-stage/repeated-failure sidecar 仍仅 `HARNESS_WIRED`。final CI run `38032673305` / job `114156701436` / head `81f3f96e168128de42b9d1661f25f8189c93dc3a`，84 tests + installed CLI/AgenticStudio smoke PASS。isolated reviewer / enforced quality-critical generation gateway 仍是精确硬阻塞。
- Novel 合法 `NOVEL_OS -> NOVEL_WRITING_AGENT` / v3.7 cutover 后的 6 个 stale tests 已 reconcile 到当前 canonical authority；没有为测试回滚真实 owner。

## Epistemic-independence validation
- code/policy head validated: `04aebdaa09e80d105f12d2c1d3cfe4c87dca0caf`
- GitHub Actions run: `38034208661`
- job: `114161174157`
- package: `universal-continuity-agent 3.7.0`
- pytest: `94 passed in 0.14s`
- 新 regression 机械验证：用户方案/助手第一方案不是 architecture authority；非平凡候选必须有 alternative comparison + failure-mode search；owner-specific evolution 允许特化方法但不得绕过 evidence/owner boundaries。

## Product/external boundaries
- 没有 scheduler/event-watch infrastructure 时，self-maintenance / self-cleaning / incident / evolution loop 发生在 active material/maintenance turn；不得声称聊天关闭后仍持续后台运行。
- GitHub 不是旧聊天 push channel。账户级 Custom Instructions 的旧 Continuity hook 已确认存在，但 execution-readiness + autonomous-maintenance 最新增量仍未得到用户明确保存确认；existing-chat refresh/handshake 与 fresh-chat Continuity product E2E 仍待真实产品验收。
- A股与 Novel 仍需在合法 owner maintenance/writer turn 补 operational-hygiene/evolution conformance；Universal 不抢业务 lease、不直接改写 business truth。

## Current stage
`V3_7_EPISTEMIC_INDEPENDENCE_GATE_ACTIVE__CROSS_AGENT_METHODOLOGY_COMPOSITION_REVIEW_PENDING`

## Next action
1. 继续独立审计 Universal control-plane bloat：区分真正 kernel invariant、按需 methodology capability、owner-specific domain method、纯 audit/evidence；找可删除/合并/下沉的内容，而不是继续横向加 policy。
2. 比较跨 Agent 复用候选：composition/module/bundle、controller/operator、hook/override、policy namespace、capability package、schema/conformance 等；以 coupling、升级传播、owner autonomy、failure containment、context cost、versioning、testability 为准，不预设 inheritance。
3. 只有在候选比较 + regression/eval 后才决定是否做最小架构重构；目标是让 owner 复用通用清洁/读写/可靠性/学习方法学，同时只覆盖 domain-specific 部分，不复制整套总控，也不让 Universal 变成巨型父 Agent。
4. 同时继续 A股/Novel owner conformance、Financial real feedback receipt、Video LEARN receipt、existing/fresh-chat product E2E。

## Recovery rule
本任务是 `EXPLICIT_ONLY` 系统基础设施维护任务。恢复先读本 Handoff、manifest、`SYSTEM_MAINTENANCE_POLICY.json` v1.4、`CONTINUOUS_LEARNING_POLICY.md`、`OWNER_ADAPTER_CONTRACT.json`、`ARTIFACT_CONTEXT_GOVERNANCE_POLICY.json`；不要从聊天记忆重建执行真相。
