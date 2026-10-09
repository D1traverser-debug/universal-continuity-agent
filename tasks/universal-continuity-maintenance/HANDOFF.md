# 跨对话继承系统建设与维护｜Handoff

- task_id: `continuity:universal-continuity-maintenance`
- task_class: `SYSTEM_INFRA`
- display_name_zh: `跨对话继承系统建设与维护`
- domain: `CONTINUITY`
- owner: `UNIVERSAL_CONTINUITY_HARNESS`
- status: `ACTIVE`
- resume_visibility: `EXPLICIT_ONLY`
- contract: `CONTINUITY_V3_4`

## Current truth
- Universal Continuity 工程真源：`D1traverser-debug/universal-continuity-agent@main`。
- ChatGPT Library 只保留根级薄 bootstrap 指针；完整 Continuity 工程目录已删除。
- v3.4 在 v3.3 的 `display_name_zh` 基础上新增 bare-inherit deterministic discovery quorum：裸“继承”必须完整查询所有 required owner source 后才能报告总任务数。
- 若任一 required source 缺失，必须返回 `INCOMPLETE_DISCOVERY`；不得把部分结果说成“全部/一共 N 个”。
- Financial Writing、A-share、Video Growth 的 live task state 留在各自 owner；Novel 由 NOVEL_OS durable recovery chain 管理。
- 当前默认 USER 候选的业务索引已纠正：历史 AI 制药文章已归档隐藏；Financial Writing Site Runtime Gate A2 为 SYSTEM_INFRA / EXPLICIT_ONLY；新增长期 USER 入口“金融文章写作”和“A股荐股”。
- 最新 Universal CI：27/27 pytest PASS。

## Current stage
`V3_4_DETERMINISTIC_DISCOVERY_ACTIVE`

## Next action
继续接入现有聊天/任务；对每个业务任务由对应 owner 保存真实 checkpoint，并维护全 owner discovery 完整性、候选去重和恢复一致性。Continuity 自身修改前必须先读取 `main` 最新 HEAD。

## Recovery rule
本任务是系统基础设施维护任务，禁止进入普通裸“继承”业务候选。仅在用户明确说 `继承：跨对话继承系统建设与维护`、`继续跨对话继承系统建设与维护`，或明确要求继续维护/升级 Universal Continuity Agent 时恢复。

成功在新聊天接管后，旧聊天退役。
