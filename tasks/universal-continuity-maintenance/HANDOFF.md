# 跨对话继承系统建设与维护｜Handoff

- task_id: `continuity:universal-continuity-maintenance`
- task_class: `SYSTEM_INFRA`
- display_name_zh: `跨对话继承系统建设与维护`
- domain: `CONTINUITY`
- owner: `UNIVERSAL_CONTINUITY_HARNESS`
- status: `ACTIVE`
- resume_visibility: `EXPLICIT_ONLY`
- contract: `CONTINUITY_V3_3`

## Current truth
- Universal Continuity 工程真源：`D1traverser-debug/universal-continuity-agent@main`。
- ChatGPT Library 只保留根级薄 bootstrap 指针；完整 Continuity 工程目录已删除。
- v3.3 已加入 `display_name_zh`，并通过中文 continuation phrase resolver 回归。
- Financial Writing、A-share、Video Growth 的 live task state 留在各自 owner；Novel 由 NOVEL_OS durable recovery chain 管理。
- 用户正在把仍有执行价值的现有聊天逐个接入 Continuity。

## Current stage
`V3_3_GITHUB_CUTOVER_ACTIVE`

## Next action
继续接入现有聊天/任务；对每个业务任务由对应 owner 保存真实 checkpoint，并执行 compatibility/recovery 验收。Continuity 自身修改前必须先读取 `main` 最新 HEAD。

## Recovery rule
本任务是系统基础设施维护任务，禁止进入普通裸“继承”业务候选。仅在用户明确说 `继承：跨对话继承系统建设与维护`、`继续跨对话继承系统建设与维护`，或明确要求继续维护/升级 Universal Continuity Agent 时恢复。

成功在新聊天接管后，旧聊天退役。
