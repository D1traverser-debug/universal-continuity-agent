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
- 工程真源：`D1traverser-debug/universal-continuity-agent@main`；Continuity 总架构权威为 `SYSTEM_BLUEPRINT.md`。
- Continuity 当前活动协议仍只有 v3.7；本轮新增的是与 Continuity 并列的 Universal Execution Harness，不因执行层 hardening 把 Continuity 协议滥升到 3.8。
- 跨 Agent 执行控制面已经落地：`ORCHESTRATION_BLUEPRINT.md` + `EXECUTION_READINESS_CONTRACT.json` + `OWNER_EXECUTION_REGISTRY.json` + `runtime/execution_readiness.py`。
- `OWNER_REGISTRY.json` 与 `ENTRYPOINT.md` 已把 GitHub-backed business owner 接入执行层：Continuity 先解决 exact task/owner/lease，之后总调度器才对当前 `next_action` 做 capability handshake。
- 执行保证等级固定区分：`DECLARED_ONLY -> HARNESS_WIRED -> SESSION_EXECUTABLE -> ATTESTED_ISOLATED`。Skill/角色名/Prompt/config/code stub 本身不再计作“Agent 已执行”。
- 当前 session 能力与 repo 能力分开：owner manifest 只给 assurance ceiling；真正执行前必须观察本聊天/运行环境是否具备相应工具、runtime、credential、modality。缺少 hard capability 时只阻塞精确 gate，不把整个 owner 判死。
- 无部署模式允许 `CHAT_BRIDGED`，但只能用于 owner contract 明确允许且不要求真实隔离的能力；一个聊天切换多个角色不能满足 `ATTESTED_ISOLATED`。
- 三个现有 GitHub business owner 已统一增加 `continuity/EXECUTION_CAPABILITIES.json`：Financial Writing、A股、Video Growth。它们不复制业务 task state，也不抢 active lease。
- Financial Writing 当前是 state machine + OpenAI Agents SDK executor + deterministic checks 的较完整 executor-wired 形态；当前 session SDK/runtime availability 仍需 handshake。
- A股当前是 market-day state machine + runtime service/plugin contract 的 owner-runtime-wired 形态；live source/data 与当前 session binding 每个交易日单独 handshake。
- Video Growth 明确暴露真实缺口：work-order/governance 有，critical blind multimodal reviewer 的 production trusted executors 仍为空，generation preflight 有但 single enforced generation gateway 尚未实现。Production Methodologist / Evolution Engineer 不再因“有角色名”就视为 steady-state agent，默认按 capability-gap sidecar 管理。
- Anti-bloat 已进入执行合同：失败优先判断是 existing role responsibility / deterministic gate / stage capability / on-demand sidecar / permanent agent；永久 Agent 必须同时有 invocation/event path + executor/evidence contract，否则保持 `DECLARED_ONLY`。
- 本轮 CI 初次 run `38016204633` 失败，原因是此前状态文件误删旧 startup acceptance evidence；恢复证据后重跑成功，没有降低测试门槛。
- 最新 GitHub Actions：run `38016256163` / job `114107069402`，validated executable head `ca865a831120d61039ffc347ede50aabd8899741`，package `3.7.0`，`77 passed`。
- 全系统/跨 Agent 审计见 `audits/SYSTEM_REGRESSION_AUDIT_2026-10-10.md` 与 `audits/CROSS_AGENT_EXECUTION_READINESS_2026-10-10.md`。
- 原有 Continuity 边界保持：真正 fresh-chat 的 `继承前进度 -> compatibility/takeover -> 进度提交` 产品级 E2E 仍需真实新聊天触发；其他业务 active writer 不由维护任务抢 lease。

## Current stage
`V3_7_UNIVERSAL_EXECUTION_CONTROL_PLANE_ACTIVE__PRODUCT_E2E_AND_OWNER_RUNTIME_HANDSHAKES_PENDING`

## Next action
1. 后续任何 GitHub-backed business Agent 的 material `next_action`，总调度器先读取 owner `continuity/EXECUTION_CAPABILITIES.json`，只 handshake 当前步骤需要的能力，再选择 OWNER_NATIVE / CHAT_BRIDGED / DETERMINISTIC_TOOL / ISOLATED_EXTERNAL / BLOCKED；禁止把 repository declaration 当执行证据。
2. 在各业务真实下一轮执行中做 owner-level end-to-end 验收：Financial Writing 验 executor/runtime handshake；A股验 live-source + owner runtime handshake；Video Growth 验普通 work packet 可执行路径，同时保持 critical isolated reviewer / generation gateway blocker fail-closed，直到真实 executor/gateway 接通。
3. 不为“看起来完善”继续新增 permanent agents；优先把已有 declared-only/partially-wired capability 变成真实 invocation + executor + receipt，或降级为 on-demand sidecar/删除冗余机制。
4. Continuity 产品层仍需一次真正 fresh-chat 验收：裸 `继承` 5-source discovery，然后明确恢复本维护任务，验证 `继承前进度 -> takeover -> 进度提交`。
5. Financial Writing / Video Growth / NOVEL_OS 的 v3.7 lazy protocol reconciliation 仍由各自合法 writer 在下一次 durable turn 完成；维护任务不越权改业务 checkpoint。

## Exact artifacts for next action
- `SYSTEM_BLUEPRINT.md`
- `ENTRYPOINT.md`
- `ORCHESTRATION_BLUEPRINT.md`
- `EXECUTION_READINESS_CONTRACT.json`
- `OWNER_EXECUTION_REGISTRY.json`
- `OWNER_REGISTRY.json`
- `runtime/execution_readiness.py`
- `HARNESS_STATUS.json`
- `audits/CROSS_AGENT_EXECUTION_READINESS_2026-10-10.md`
- `audits/SYSTEM_REGRESSION_AUDIT_2026-10-10.md`

## Recovery rule
本任务是系统基础设施维护任务，不进入普通裸 `继承` 默认 USER 候选。仅在用户明确要求继续、维护或升级 Universal Continuity / 总调度 / GitHub Agent harness / 跨对话继承系统时恢复。
