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

## Current truth
- 工程真源：`D1traverser-debug/universal-continuity-agent@main`；Continuity 总架构权威为 `SYSTEM_BLUEPRINT.md`，跨 Agent 调度权威为 `ORCHESTRATION_BLUEPRINT.md` / `EXECUTION_READINESS_CONTRACT.json`。
- Continuity 当前活动协议仍只有 v3.7；Universal Execution Harness 与 Continuity 并列，不把业务执行逻辑塞进恢复系统。
- 执行保证等级为 `DECLARED_ONLY -> HARNESS_WIRED -> SESSION_EXECUTABLE -> ATTESTED_ISOLATED`；Agent/Prompt/Skill/config/code stub 本身不是执行证明。
- GitHub 仓库是 durable engineering authority，但**不是聊天推送/事件监听器**。仅把规则写进 GitHub 不能保证已经打开、且不重新读取仓库的旧聊天自动获知更新。
- 为避免 owner 侧遗漏，Financial Writing、A股、Video Growth 三个 GitHub business owner 都已建立 `continuity/EXECUTION_CAPABILITIES.json`，且各自最新 `SKILL.md` 与 `continuity/TASK_INDEX.md` 已要求：任何 material stage/next_action/work order 前重新读取 capability manifest，并只对当前步骤所需能力做 session handshake。
- Owner 入口已加 regression guard，防止未来 Skill/TASK_INDEX 重写时静默删掉 execution-capability wiring。A股 wiring CI 已 PASS（run `38016854800`, head `650cba169c46246d431b0176d219867e92ebd051`）。Video wiring test 已修正两个错误测试层级：不再要求业务 next_action 含字面 `receipt`，能力模式断言改为语义/大小写无关；最新 run `38017210573` 正在验证。Financial Writing 当前 main Skill/Task Index 已回读确认 wiring 存在，但 owner 全 CI 目前被独立的 MCP Streamable HTTP smoke failure 阻塞，不能把该 owner 宣称 full-CI PASS。
- 账户级 `STARTUP_HOOK.md` 已包含同一 execution-readiness refresh 规则，并明确承担旧聊天的 routing/UX backstop：GitHub-backed durable business task 在 material action 前必须刷新 owner Skill + `continuity/EXECUTION_CAPABILITIES.json`；同一聊天角色切换不能冒充 `ATTESTED_ISOLATED`。
- Repository 无权限替用户编辑 ChatGPT Personalization / Custom Instructions。当前 OpenAI 官方文档说明 Custom Instructions 更新会立即应用到所有聊天，包括已有对话；因此**覆盖已经打开但可能不主动刷新 GitHub 的旧聊天，仍需要账户级 Custom Instructions 存在**。未得到用户明确确认前，不得声称该广播层已安装。
- 无部署时可以使用 owner contract 明确允许的 `CHAT_BRIDGED` 路径；缺失 hard capability 只阻塞精确 gate，不能绕过，也不应把整个 Agent 判死。
- 原有 single-writer 边界保持：本维护任务不抢 Financial Writing / Video Growth / NOVEL_OS 活跃业务 lease，不因 execution metadata 更新改写业务 checkpoint。
- Universal executable control plane 最近一次已验证 CI：run `38016256163` / job `114107069402`，head `ca865a831120d61039ffc347ede50aabd8899741`，`77 passed`。Owner 入口传播属于各 owner 仓库独立 wiring/CI，不把其结果伪装成 Universal executable CI。

## Current stage
`V3_7_EXECUTION_PROPAGATION_WIRED__ACCOUNT_BROADCAST_CONFIRMATION_AND_OWNER_HANDSHAKES_PENDING`

## Next action
1. 用户只需执行一次账户级动作：在 ChatGPT Settings -> Personalization -> Custom Instructions 中保存/确认当前 `STARTUP_HOOK.md` 所定义的 Continuity + execution-readiness 广播语义，并保持 customization enabled。不要要求用户逐个旧聊天迁移或粘贴规则。
2. 保存后，在任一已经打开的 GitHub-backed durable business chat 下一次 material turn 验收：它应先刷新当前 owner Skill / `continuity/EXECUTION_CAPABILITIES.json`，再做 targeted session handshake；不应仅依赖旧上下文。
3. 继续完成 owner-level runtime handshake E2E：Financial Writing 验 SDK/runtime path，A股验 live source + owner runtime，Video Growth 验普通 work-packet path并保持 isolated reviewer / generation gateway hard blockers fail-closed。
4. Continuity 仍需一次真正 fresh-chat 产品级 E2E：裸 `继承` 完成 required-source discovery，再明确恢复本任务，验证 `继承前进度 -> compatibility/takeover -> 进度提交`。
5. 不继续为“看起来完善”新增 permanent agents；优先把 declared/partially-wired capability 接成 invocation + executor + receipt，或降级为 on-demand sidecar/删除冗余机制。

## Exact artifacts for next action
- `STARTUP_HOOK.md`
- `ENTRYPOINT.md`
- `SYSTEM_BLUEPRINT.md`
- `ORCHESTRATION_BLUEPRINT.md`
- `EXECUTION_READINESS_CONTRACT.json`
- `OWNER_EXECUTION_REGISTRY.json`
- `OWNER_REGISTRY.json`
- `runtime/execution_readiness.py`
- `HARNESS_STATUS.json`
- `audits/CROSS_AGENT_EXECUTION_READINESS_2026-10-10.md`

## Recovery rule
本任务是系统基础设施维护任务，不进入普通裸 `继承` 默认 USER 候选。仅在用户明确要求继续、维护或升级 Universal Continuity / 总调度 / GitHub Agent harness / 跨对话继承系统时恢复。
