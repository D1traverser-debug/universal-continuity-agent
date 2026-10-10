# 跨对话继承系统建设与维护｜Handoff

- task_id: `continuity:universal-continuity-maintenance`
- task_class: `SYSTEM_INFRA`
- display_name_zh: `跨对话继承系统建设与维护`
- domain: `CONTINUITY`
- owner: `UNIVERSAL_CONTINUITY_HARNESS`
- status: `ACTIVE`
- resume_visibility: `EXPLICIT_ONLY`
- contract: `CONTINUITY_V3_7`

## Current truth
- 工程真源：`D1traverser-debug/universal-continuity-agent@main`；总架构权威新增 `SYSTEM_BLUEPRINT.md`。
- 当前只保留一个活动协议：v3.7。协议升级不再为每个 hardening 小改动递增版本；版本规则见 `VERSION_LIFECYCLE_POLICY.json`。
- 已新增 `LIVE_CHAT_RECONCILIATION_POLICY.json`：旧聊天不锁死在创建时协议版本；同一有效 writer 的原地协议升级不增加 `resume_epoch`、不更换 lease，真正新聊天 takeover 才会。
- 用户不是迁移操作员。旧 owner/checkpoint 的兼容、迁移与 adaptation 由 Continuity/owner 自动处理；不要求用户逐对话迁移。
- 已清理活动根目录中的完成态 `MIGRATION_MANIFEST.json` / `MIGRATION_STATUS.json` / `MIGRATION_CHECKPOINT.md` / `ENGINEERING_HOME_STATUS.json`；审计事实合并到 `archive/migrations/2026-10-09-library-to-github.md`，原文件仍可由 Git history 恢复。
- `tasks/_TASK_MANIFEST_TEMPLATE.json` 已对齐 3.7，并新增 `continuity_protocol_version` / `domain_contract_version` / `last_protocol_reconciled_at`，避免 Universal 协议和业务 contract 混用。
- Owner 协议适配状态见 `OWNER_PROTOCOL_ADAPTATION_REGISTRY.json`：A股长期入口因无 active lease 已直接迁至 v3.7；Financial Writing / Video Growth / NOVEL_OS 因存在有效 lease，已分别放置 owner/routing adapter，等待各自当前有效 writer 下一次 durable turn 原地 reconcile，维护任务不抢写它们的 task manifest。
- 账户级 `STARTUP_HOOK.md` 已整合新旧聊天规则：fresh resume 要先报告 `继承前进度`；所有已纳入 Continuity 的持久任务（包括旧对话）每次最终答复都要报告 `进度提交`。
- 最新 CI：run `38013131965` / job `114097414804`，package `3.7.0`，`57 passed`。详见 `HARNESS_STATUS.json`。
- v3.7 `继承前进度` 的真正 fresh-chat 产品级 E2E 仍需下一次真实新聊天验收；CI 不能替代。

## Current stage
`V3_7_ARCHITECTURE_LIFECYCLE_AND_LIVE_CHAT_RECONCILIATION_ACTIVE`

## Next action
1. 下一次真实新聊天继承时验收 `继承前进度 -> compatibility/protocol reconciliation -> takeover -> 进度提交` 产品级 UX。
2. 当 Financial Writing / Video Growth / NOVEL_OS 的旧聊天下一次发生 durable turn 时，验证 owner adapter 能在不抢 lease、不重放业务工作的前提下把 task-level protocol metadata 原地 reconcile 到 v3.7，并输出当前 `进度提交`。
3. 继续 owner conformance：Financial Writing handoff 瘦身、Video Growth checkpoint 瘦身；A股 authority ref 缺口已通过 `config/cutover_status.json` 等稳定 refs 修复。
4. 按 `CONTINUOUS_LEARNING_POLICY.md` 主动学习并只吸收经证据验证、属于 Continuity scope 的改进。

## Exact artifacts for next action
- `SYSTEM_BLUEPRINT.md`
- `CURRENT_PROTOCOL.json`
- `VERSION_LIFECYCLE_POLICY.json`
- `LIVE_CHAT_RECONCILIATION_POLICY.json`
- `OWNER_PROTOCOL_ADAPTATION_REGISTRY.json`
- `PROGRESS_OBSERVABILITY_POLICY.json`
- `STARTUP_HOOK.md`
- `HARNESS_STATUS.json`
- `audits/OWNER_HANDOFF_AUDIT_2026-10-09.md`

## Recovery rule
本任务是系统基础设施维护任务，不进入普通裸 `继承` 默认 USER 候选。仅在用户明确要求继续、维护或升级 Universal Continuity / 继承系统 / 跨对话继承系统时恢复。
