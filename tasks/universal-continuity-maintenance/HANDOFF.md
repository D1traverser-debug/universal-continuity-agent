# 跨对话继承系统建设与维护｜Handoff

- task_id: `continuity:universal-continuity-maintenance`
- task_class: `SYSTEM_INFRA`
- display_name_zh: `跨对话继承系统建设与维护`
- owner: `UNIVERSAL_CONTINUITY_HARNESS`
- status: `ACTIVE`
- contract: `CONTINUITY_V3_7`
- system-maintenance policy: `1.3`
- artifact/context governance: `1.1`
- execution-readiness contract: `1.0`

## Current truth
- 工程真源：`D1traverser-debug/universal-continuity-agent@main`。同聊天 active lease 仍为 `lease-f266a907-aaf1-4b6a-a283-0e64b979d652`，`resume_epoch=1`；本轮没有 takeover。
- 维护系统已经从“用户指出一个刺 -> 再补一个 policy/prompt/role”收敛为 architecture-first + operational-hygiene 模式。新 root authority surface 仍受 `authority_surface_admission_gate` 约束，现有 authority 能承载时默认合并/修改/删除旧机制，不新增平行规则面。
- 本轮进一步确认：用户反复重申同一个持久要求、同类故障在已接受修复后再次出现、mandatory gate 重复被绕过/虚报、owner 重复从 stale rule/state/artifact 执行，都不能再视为“模型偶尔忘了”，而要视为 owner reliability signal。
- `SYSTEM_MAINTENANCE_POLICY.json` v1.3 已增加 scoped `reliability_guard`。重复故障闭环为：`持久化 incident/failure evidence -> 根因层分类 -> 检查 refresh/execution path -> 修 true owner -> 加/改 regression/eval -> 删除/降级冲突或 superseded mechanism -> fresh evidence 验证`。受影响 owner/capability 的无关功能扩张在可靠性恢复前冻结；冻结不扩散到其他健康 owner。聊天里的道歉、提醒、人格切换或“以后注意”不算修复。
- `OWNER_ADAPTER_CONTRACT.json` 已增加 `operational_hygiene_and_learning` conformance：owner 应暴露 incident/observability evidence location、self-maintenance trigger path、learning evidence、eval/regression promotion path、owner-aware GC/dependency rule、reliability/change-freeze guard、superseded cleanup。Universal 只验证跨 owner 不变量，不抢业务 writer、不改写 domain truth。
- “自清洁”被限定为 owner/dependency/retention-aware GC：只自动清 stale/rebuildable/superseded artifact；不能因为旧就删 durable checkpoint、accepted/published business evidence 或仍被 active next_action 依赖的文件。
- 外部成熟模式的学习结论记录在 `audits/CROSS_AGENT_OPERATIONAL_HYGIENE_REVIEW_2026-10-10.md`：reconciler/controller、observability/eval、owner-aware garbage collection、incident/postmortem、reliability/error-budget style change freeze、durable workflow history/versioning、evidence-gated evolution。它们共同支持“先可靠、再扩张；证据驱动晋升；失败必须形成可重复回归”。

## Financial Writing audit
- 财经系统不是结构性崩溃。它已有真实 Python state machine、persisted task state、learning-sample runtime、trajectory/regression、executable contract eval、static ownership/version audit、wheel smoke、DOCX render smoke。
- 真正遗忘缺口：虽然 runtime 已有 `record_writing_learning_sample`，Skill 过去没有强制 material user edit/feedback/rejection/acceptance 在 durable-learning claim 或相关 revision loop 关闭前持久化；capability manifest 也未暴露该执行路径。这允许“当前聊天改对了，但下一聊天并没有真正学会”。
- 已修：Skill + maintenance reference 规定 persisted writing task 上的 material explicit feedback 必须通过 `record_writing_learning_sample` 或等价 owner receipt 持久化；若当前 executor 不可用，仍执行本轮修改，但必须明确 durable learning 未持久化，不能声称未来聊天已学会。
- `continuity/EXECUTION_CAPABILITIES.json` profile v2 增加 `learning_evidence_capture = SESSION_EXECUTABLE`，绑定真实 plugin/runtime invocation + persisted sample receipt。
- Financial final CI：run `38032299542` / job `114155603504` / head `a6e69993787394f1abeef4b5da6e5bb3cb0b5e9d`；`50 passed`；OpenAI Agents SDK smoke PASS；MCP Streamable HTTP smoke PASS（17 typed/annotated tools）；contract eval 无 failing case；static audit PASS；isolated wheel install PASS；DOCX render smoke PASS。

## Video Growth audit
- 视频的进化链存在真实结构断点：`agents.json` 已声明 `production_methodologist` / `evolution_engineer`，`self-learning.md` 也写了学习闭环，但旧 `execution-plan.json` 的 `LEARN` 阶段没有真正调度这两个角色；旧 learning tests 也没有证明它们被调用，更没有区分 learning artifact 与 GitHub production authority mutation。因此此前“会自我进化”的实现程度被文档描述夸大了。
- 已修工程面但没有触碰 Video business checkpoint/lease：
  - `agents.json` v0.5.1：Evolution Engineer 只生成 candidate change package，不得把 candidate 冒充 production change；durable promotion 仍需 owner maintenance apply/test/verify。
  - `LEARN` stage 现在真实调度 `Production Methodologist -> Evolution Engineer candidate -> Red Team -> Showrunner`，产出 `learning_candidate` / proposed `learning_receipt` / review receipts。
  - `continuity/EXECUTION_CAPABILITIES.json` profile v2：post-performance `scheduled_learning_evidence_pipeline = SESSION_EXECUTABLE`；mid-stage/repeated-failure `learning_evolution_sidecar = HARNESS_WIRED`，不得夸大为全自动 event-driven self-healing。
  - learning tests 现在机械验证 role sequence、candidate/promotion boundary 和 assurance truthfulness。
- 两轮安装 smoke 还顺手暴露了 CI 自身的 stale exact-version assertions（agents 0.5.0、planner 0.4.0）；没有回滚新实现，而是改成当前契约语义检查并直接验证 LEARN agent sequence。
- Video final CI：run `38032673305` / job `114156701436` / head `81f3f96e168128de42b9d1661f25f8189c93dc3a`；`84 passed in 1.26s`；installed CLI / packaged `AgenticStudio` smoke PASS。
- Video 仍有精确硬阻塞：production trusted isolated-review executors 为空，因此 critical blind multimodal review 不能满足 `ATTESTED_ISOLATED`；generation preflight 有，但 single enforced quality-critical generation gateway 尚未实现；mid-stage/repeated-failure learning sidecar 仍只有 `HARNESS_WIRED`。这些不能靠聊天角色扮演冒充已解决。

## Adjacent hygiene evidence
- Universal 新 reliability/owner-conformance 规则首轮 CI 暴露了 Novel 已完成合法 `NOVEL_OS -> NOVEL_WRITING_AGENT` / v3.7 GitHub owner cutover，但 6 个旧测试仍钉在 legacy owner/protocol。没有回滚真实 authority，也没有忽略失败；已把测试 reconcile 到当前 canonical owner + alias + manifest + execution registry 不变量。
- Universal final CI：run `38032272822` / job `114155522633` / head `0651195c95e7697dd57700bdad6ce193b6a8a5ff`；package `3.7.0`；`93 passed in 0.26s`。
- 这类“维护 A 暴露验证 B 已漂移 -> 核对真实 authority -> 修验证而不是回滚 authority”就是当前 operational hygiene 的目标行为。

## Product/external boundaries
- 没有 scheduler/event-watch infrastructure 时，当前“自管理/自清洁/incident loop”发生在 active material/maintenance turn，不得声称聊天关闭后仍持续后台运行。
- A股与 Novel 仍需在各自合法 owner maintenance/writer turn 补齐 operational-hygiene conformance；Universal 不抢它们的 active business lease。
- 账户级 Custom Instructions 中旧 Continuity 总入口已由用户确认存在；execution-readiness + autonomous-maintenance 最新增量仍未得到用户明确保存确认。GitHub 不是旧聊天 push channel；existing-chat refresh/handshake 与 fresh-chat Continuity 产品 E2E 仍待真实产品验收。
- broader unrestricted self-evolution 仍是后续独立设计，不把这轮 reliability/hygiene hardening 偷换成无限制自修改。

## Current stage
`V3_7_OPERATIONAL_HYGIENE_BASELINE_ACTIVE__OWNER_EVOLUTION_CONFORMANCE_AND_PRODUCT_E2E_PENDING`

## Next action
1. 在 A股、Novel 等合法 owner maintenance/writer turn 补齐 incident/observability、self-maintenance trigger、learning evidence、eval promotion、owner-aware GC、reliability freeze、superseded cleanup conformance；不抢 lease、不改写业务真相。
2. Financial Writing 下一次真实 material user correction / accept-reject turn 验 `learning_evidence_capture` 的 session handshake + persisted receipt，确认聊天纠错确实进入 durable evidence。
3. Video 下一次合法 LEARN/work-packet 路径验 Methodologist/Evolution candidate/Red Team/Showrunner receipts；mid-stage sidecar 仍需未来补 event trigger 才能提升 assurance。
4. 继续 existing-chat owner refresh/targeted handshake 与 fresh-chat Continuity E2E。
5. 若任何 owner 再重复已修复的核心故障，直接进入 scoped reliability incident/freeze，不再让用户重述规则后继续加功能。

## Recovery rule
本任务是 `EXPLICIT_ONLY` 系统基础设施维护任务。恢复先读本 Handoff、manifest、`SYSTEM_MAINTENANCE_POLICY.json` v1.3、`OWNER_ADAPTER_CONTRACT.json`、`ARTIFACT_CONTEXT_GOVERNANCE_POLICY.json` 与最新 operational-hygiene audit；不要从聊天记忆重建执行真相。
