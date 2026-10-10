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
- system-maintenance policy: `1.0`

## Current truth
- 工程真源：`D1traverser-debug/universal-continuity-agent@main`；Continuity 总架构权威为 `SYSTEM_BLUEPRINT.md`，系统维护自治权威为 `SYSTEM_MAINTENANCE_POLICY.json`，跨 Agent 调度权威为 `ORCHESTRATION_BLUEPRINT.md` / `EXECUTION_READINESS_CONTRACT.json`。
- Continuity 当前活动协议仍只有 v3.7；本轮属于 compatible hardening，不因维护自治增强滥升协议版本。
- 用户不是系统维护 operator。发现系统性缺口、传播/执行真实性问题、CI 回归、版本/authority drift、重复机制或 owner wiring 漂移时，当前合法 maintenance writer 默认必须自行完成：`检测 -> 定位 authority -> 读取当前真源 -> 根因诊断 -> 最小安全修复 -> regression guard -> CI/验证 -> 升级/维护记录 -> task/status 更新 -> 权威回读 -> 精确报告`。除非遇到账户/UI动作、新权限/凭证、不可逆高影响选择或无法安全推断的外部事实，不等待用户逐项提醒。
- 本轮用户指出“系统维护工作不应等我提醒”后，新增 `SYSTEM_MAINTENANCE_POLICY.json`，并把 maintenance autonomy 写进 `SYSTEM_BLUEPRINT.md`、`CONTINUOUS_LEARNING_POLICY.md`、`STARTUP_HOOK.md`；新增 `tests/test_system_maintenance_policy.py` 机械防回退。
- 本轮 CI 首跑 run `38018174945` 在新维护测试之外暴露一个**旧漂移**：现有 `tests/test_startup_hook.py` 要求 `STARTUP_HOOK.md` 保留精确 fail-closed marker `CONTINUITY_BOOTSTRAP_UNAVAILABLE`，但文档此前被弱化成普通不可访问说明。没有降低旧测试门槛，而是修复 `STARTUP_HOOK.md` 并把维护自治一并接入 startup semantics。
- 修复后 run `38018225600` / job `114113204158` / validated head `afa7bac8ad0cbe3b02a35955cb60f28dd3f2d6ee` 全绿：package `3.7.0`，`81 passed in 0.19s`。
- 完整审计记录：`audits/SYSTEM_MAINTENANCE_AUTONOMY_2026-10-10.md`。该记录包含问题、根因、authority surfaces、首轮失败、修复、验证、行为效果和剩余边界。
- 用户已明确确认：ChatGPT Custom Instructions 中已有旧版 Continuity 总入口，覆盖显式继续路由、Universal repo bootstrap、完整 discovery、exact owner routing、compatibility/takeover、进度提交、协议/owner/checkpoint 自动迁移与 lease/resume_epoch 边界；无需重装，也无需逐聊迁移。
- 现有账户指令仍属于 execution-readiness / autonomous-maintenance 上线前版本。GitHub 不能主动推送给已打开且不刷新仓库的旧聊天，因此账户级仍需保存最新增量语义：material action 前刷新 owner Skill + `continuity/EXECUTION_CAPABILITIES.json`、targeted session handshake、声明不等于执行证据、`ATTESTED_ISOLATED` 不得由同聊天角色切换冒充，以及系统维护默认自治闭环。Repository 无权代替用户编辑该账户设置。
- Financial Writing、A股、Video Growth 三个 GitHub business owner 已有 `continuity/EXECUTION_CAPABILITIES.json`，且 owner Skill/TASK_INDEX 已接线。A股 wiring CI PASS（run `38016854800`）；Video wiring CI PASS（run `38017210573`）；Financial Writing 入口回读 PASS，但完整 owner CI 仍被独立 MCP Streamable HTTP smoke 阻塞，不能虚报 full PASS。
- 执行保证仍固定为 `DECLARED_ONLY -> HARNESS_WIRED -> SESSION_EXECUTABLE -> ATTESTED_ISOLATED`；role/Prompt/Skill/config/stub 不是执行证明。缺失 hard capability 只阻塞精确 gate。
- 系统维护自治不越权：不能抢其他 active owner lease，不能从维护任务改写 domain business truth，不能伪造 product-level E2E，不能用新增 permanent agent 代替真实 invocation/executor/evidence。

## Current stage
`V3_7_AUTONOMOUS_SYSTEM_MAINTENANCE_ACTIVE__ACCOUNT_EXECUTION_EXTENSION_AND_OWNER_HANDSHAKES_PENDING`

## Next action
1. 以后任何 Universal Continuity / cross-agent control-plane 维护缺陷，默认直接执行 `SYSTEM_MAINTENANCE_POLICY.json` 完整闭环；不再等用户逐项指出升级记录、回归、状态同步等内部动作。
2. 当前唯一账户级外部边界：用户将最新 `STARTUP_HOOK.md` / 完整账户指令中的 execution-readiness + autonomous-maintenance 增量保存进 ChatGPT Custom Instructions；无需重装旧 Continuity，也无需逐聊迁移。
3. 保存后，在已经打开的 GitHub-backed durable business chat 的下一次 material turn 验收 owner Skill / `continuity/EXECUTION_CAPABILITIES.json` refresh + targeted session handshake。
4. 继续 owner-level runtime E2E：Financial Writing 验 SDK/runtime path；A股验 live source + owner runtime；Video Growth 验普通 work-packet path，同时 critical isolated reviewer / generation gateway blocker 保持 fail-closed。
5. Continuity 产品层仍需真正 fresh-chat E2E：裸 `继承` 完整 discovery，再恢复本维护任务，验证 `继承前进度 -> compatibility/takeover -> 进度提交`。

## Exact artifacts for next action
- `SYSTEM_MAINTENANCE_POLICY.json`
- `SYSTEM_BLUEPRINT.md`
- `STARTUP_HOOK.md`
- `CONTINUOUS_LEARNING_POLICY.md`
- `tests/test_system_maintenance_policy.py`
- `audits/SYSTEM_MAINTENANCE_AUTONOMY_2026-10-10.md`
- `ORCHESTRATION_BLUEPRINT.md`
- `EXECUTION_READINESS_CONTRACT.json`
- `HARNESS_STATUS.json`

## Recovery rule
本任务是系统基础设施维护任务，不进入普通裸 `继承` 默认 USER 候选。仅在用户明确要求继续、维护或升级 Universal Continuity / 总调度 / GitHub Agent harness / 跨对话继承系统时恢复。恢复后系统维护闭环本身默认自治，不要求用户枚举内部维护步骤。
