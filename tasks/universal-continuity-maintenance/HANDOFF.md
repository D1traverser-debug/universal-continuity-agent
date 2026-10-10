# 跨对话继承系统建设与维护｜Handoff

- task_id: `continuity:universal-continuity-maintenance`
- task_class: `SYSTEM_INFRA`
- display_name_zh: `跨对话继承系统建设与维护`
- domain: `CONTINUITY`
- owner: `UNIVERSAL_CONTINUITY_HARNESS`
- status: `ACTIVE`
- resume_visibility: `EXPLICIT_ONLY`
- contract: `CONTINUITY_V3_7`
- execution-readiness contract: `1.0`
- system-maintenance policy: `1.1`
- artifact/context governance: `1.0`

## Current truth
- 工程真源：`D1traverser-debug/universal-continuity-agent@main`。Continuity 总架构权威是 `SYSTEM_BLUEPRINT.md`；系统维护自治权威是 `SYSTEM_MAINTENANCE_POLICY.json`；跨 Agent 文件/缓存/上下文治理权威是 `ARTIFACT_CONTEXT_GOVERNANCE_POLICY.json`；跨 Agent 执行真实性由 `ORCHESTRATION_BLUEPRINT.md` / `EXECUTION_READINESS_CONTRACT.json` 管。
- Continuity 当前活动协议仍只有 v3.7。本轮属于 compatible hardening，不滥升协议版本。
- 用户不是系统维护 operator。系统性缺口、传播/执行真实性问题、CI 回归、authority drift、重复/废旧机制、artifact/cache/context 漂移、chat-only material change 未持久化，均会触发自治维护闭环：`检测 -> 定位 authority -> 读取真源 -> 根因 -> 最小修复 -> regression guard -> CI/验证 -> 维护记录 -> task/status -> 权威回读 -> 精确报告`。
- 新增 `ARTIFACT_CONTEXT_GOVERNANCE_POLICY.json` v1.0，将跨 Agent 信息分成 8 类：`ENGINEERING_AUTHORITY`、`DURABLE_TASK_STATE`、`BUSINESS_EVIDENCE`、`LEARNING_EVIDENCE`、`REBUILDABLE_CACHE`、`SESSION_SCRATCH`、`EXTERNAL_REFERENCE`、`CHAT_PERSONALIZATION_CONTEXT`。只有前两类天然可直接驱动执行；其他类别必须通过 owner contract / provenance / promotion 才能升级 authority。
- 缓存、索引镜像、派生摘要、render/search cache、临时 extraction 都是 `REBUILDABLE_CACHE`：可删可重建，不是 checkpoint authority，不是 COMMITTED 证据。聊天中的临时想法和未持久化工具输出属于 `SESSION_SCRATCH`，不应被下一聊天当作已经进化的系统规则。
- Library、Google Drive、Notion、Slack、Project sources 和其他 connected apps 默认属于 `EXTERNAL_REFERENCE`：可做资料/证据，但“存在/能搜到”不等于 owner authority。只有 owner contract 明确指定或用户在当前任务显式提供并保留 provenance 时，才进入业务证据路径。
- Custom Instructions、Project instructions、Memory、past chats 属于 behavioral/personalization context，不是业务 checkpoint。当前官方产品资料表明：Custom Instructions 更新会应用到现有聊天；Project instructions 在项目内会覆盖 global Custom Instructions；Memory 可能使用过去聊天、Custom Instructions、Library 文件和 connected app 内容；Library 会自动保存上传/生成文件且删除聊天不等于删除 Library 文件。这些是产品事实，不固化成永久协议真理，需要在相关维护决策时重验。
- 因 Project instructions 可以覆盖 global Custom Instructions，Project 内存在一个产品级 bootstrap 风险：若 Project instructions 与 Continuity 路由冲突，global hook 不能被当成绝对强制层。当前治理规则要求把 Project instruction precedence 与业务数据 authority 分开；真实冲突出现时再做 project-specific compatibility，不要求用户现在逐项目迁移。
- `OWNER_ADAPTER_CONTRACT.json` 已要求 durable owners 暴露：durable task state 放哪里、哪些是 authoritative business evidence、哪些 store 只是 cache/reference、上游变化如何 invalidate 下游 artifact、superseded artifact 如何退出 active path。Universal 可以 stage conformance，但不能抢 active owner lease 或从总控直接重写 owner business truth。
- 旧实现/旧文件的总原则：superseded engineering implementation 在 replacement authority 存在且无 migration edge 依赖时退出 active tree，Git history 是实现档案；stale cache 删除/重建；duplicate active docs 合并为一份 authority；task checkpoint、accepted/published business evidence、audit causality 不因“清爽”而删除。
- 更广义“进化系统”暂不展开，按用户要求保留到后续单独讨论。本轮只把 learning 的 evidence/promotion 边界固化：`LEARNING_EVIDENCE` 不能静默变成 rule；一个想法若只存在聊天里，就不算 durable evolution。
- Financial Writing v0.6 的“更像可维护软件系统”有实证：其 architecture 有 deterministic outer runtime、upstream revision invalidation、stale render 清理、`RAW_EVIDENCE_ONLY` learning sample、旧 `mcp_server.py` / `CHAT_TEXT` / visual-sticker contracts / canned structure-pattern library 明确删除且禁止回归；当前 main v0.6 regression run `38018238323` 在 head `5d5e2493de1ff6b940366b133611cd3cd929244d` 成功。它确实具备一部分自维护机制，但不能据此夸大成“未来所有问题都能自己发现并修好”。
- Universal 本轮 artifact/context governance 完整 CI：run `38019817158` / job `114118106198` / validated head `8c02cea278a4009c848d6d3430ea411d25bc9e85`，package `3.7.0`，`84 passed in 0.23s`。后续 audit/checkpoint/status 写入为 metadata-only。
- 完整审计：`audits/CROSS_AGENT_ARTIFACT_CONTEXT_GOVERNANCE_2026-10-10.md`。

## Current stage
`V3_7_CROSS_AGENT_ARTIFACT_GOVERNANCE_ACTIVE__OWNER_CONFORMANCE_AND_PRODUCT_E2E_PENDING`

## Next action
1. 系统维护继续默认自治，不等待用户逐项指出缓存、废旧文件、漂移、升级记录、回归等内部 follow-up。
2. 在 Financial Writing、A股、Video Growth 等 durable owners 的合法 writer/maintenance turn，逐步补齐 storage/evidence/cache/invalidation/cleanup conformance；不抢 lease、不重写业务真相。
3. 当前账户级外部边界仍是保存最新 Custom Instructions 增量，使已有聊天获得 execution-readiness + autonomous-maintenance 语义；Project instructions 若将来发生真实冲突，再做 project-specific compatibility，而不是现在要求逐项目改配置。
4. 继续 existing-chat targeted session handshake 和 fresh-chat Continuity E2E。
5. 更广义自我进化系统留到用户下一轮专门讨论；不要把本轮 artifact lifecycle patch 偷偷扩展成 unrestricted self-modification。

## Exact artifacts for next action
- `SYSTEM_BLUEPRINT.md`
- `SYSTEM_MAINTENANCE_POLICY.json`
- `ARTIFACT_CONTEXT_GOVERNANCE_POLICY.json`
- `OWNER_ADAPTER_CONTRACT.json`
- `CONTINUOUS_LEARNING_POLICY.md`
- `VERSION_LIFECYCLE_POLICY.json`
- `CONTEXT_RECOVERY_POLICY.json`
- `tests/test_artifact_context_governance.py`
- `audits/CROSS_AGENT_ARTIFACT_CONTEXT_GOVERNANCE_2026-10-10.md`
- `HARNESS_STATUS.json`

## Recovery rule
本任务是系统基础设施维护任务，不进入普通裸 `继承` 默认 USER 候选。仅在用户明确要求继续、维护或升级 Universal Continuity / 总调度 / GitHub Agent harness / 跨对话继承系统时恢复。恢复后系统维护闭环默认自治，不要求用户枚举内部维护步骤。
