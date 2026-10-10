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
- 工程真源：`D1traverser-debug/universal-continuity-agent@main`；顶层架构权威为 `SYSTEM_BLUEPRINT.md`。
- 当前活动协议只有 v3.7；旧 executable protocol 不并行保留，历史由 Git history 承担，业务历史由各 owner authority 保留。
- 全系统回归已完成，详见 `audits/SYSTEM_REGRESSION_AUDIT_2026-10-10.md`。
- 回归发现并已修复核心版本漂移：`BARE_INHERIT_DISCOVERY.json`、`CONTEXT_RECOVERY_POLICY.json`、`OWNER_REGISTRY.json`、`NEW_CHAT_BOOTSTRAP.json` 均已对齐 v3.7；版本一致性测试已扩展到核心启动/恢复策略面。
- 旧聊天原地协议升级不再只是 policy 承诺：已新增 `runtime/protocol_reconciliation.py`，机械验证当前 lease/epoch，只允许协议元数据 additive patch，并禁止协议迁移改写业务 stage/next_action/artifacts/lease/epoch；未知或不支持状态 fail closed。
- 最新 GitHub Actions：run `38014845513` / job `114102722190`，validated executable head `f785db3e0828190f9a8f53422bbe0548760708a2`，package `3.7.0`，`66 passed`。
- 裸 `继承` 5-source quorum 已重新回归通过：5/5 required owner sources 可查询，权威 default USER candidate count 为 4；具体实时任务名称不复制进公共 Universal harness。
- A股长期入口已安全 reconcile 到 v3.7；Financial Writing、Video Growth、NOVEL_OS 的活跃任务不由维护任务抢 lease/改 checkpoint，而由各自合法 writer 在下一次 durable turn lazy reconcile。
- Financial Writing 已生成 owner-side handoff compaction plan；Video Growth 已生成 owner-side checkpoint compaction plan。两者都要求在合法 writer turn 中精简重复规则/历史后回读验证。
- Video Growth 回归发现一项缺少视频域权威支撑的跨域工具偏好污染风险；已在 compaction plan 中标记为不得自动晋升为视频 durable rule，除非合法 writer 找到视频域持久 provenance。
- `继承前进度` 与每轮 `进度提交` 已进入 v3.7 协议和测试；真正 fresh-chat 产品级 E2E 仍需要一个全新 ChatGPT 对话触发，仓库 CI 无法替代账户级启动链路。

## Current stage
`V3_7_FULL_SYSTEM_REGRESSION_PASS__PRODUCT_E2E_AND_LAZY_OWNER_RECONCILIATION_PENDING`

## Next action
1. 用户在账户 Personalization / Custom Instructions 中确保存在当前 Continuity startup/backstop 规则后，新开一个真正的新聊天，仅发送 `继承`，验收 5-source discovery 与候选展示；这一步不应 takeover 任何任务。
2. 为低风险验收完整 takeover UX，在该新聊天明确恢复 `跨对话继承系统建设与维护`，验证 `继承前进度 -> compatibility -> takeover -> 进度提交`。这会使当前聊天成为 stale writer，属于预期行为。
3. Financial Writing / Video Growth / NOVEL_OS 各自旧聊天下一次发生 material durable turn 时，由当前合法 writer 执行已 staged 的 v3.7 same-chat reconciliation；不得由维护任务越权抢写。
4. 按 `CONTINUOUS_LEARNING_POLICY.md` 继续维护期主动学习，仅把经验证且属于 Continuity scope 的原则沉淀到最小 authority + tests。

## Exact artifacts for next action
- `SYSTEM_BLUEPRINT.md`
- `CURRENT_PROTOCOL.json`
- `VERSION_LIFECYCLE_POLICY.json`
- `LIVE_CHAT_RECONCILIATION_POLICY.json`
- `PROGRESS_OBSERVABILITY_POLICY.json`
- `OWNER_PROTOCOL_ADAPTATION_REGISTRY.json`
- `HARNESS_STATUS.json`
- `runtime/protocol_reconciliation.py`
- `audits/SYSTEM_REGRESSION_AUDIT_2026-10-10.md`

## Recovery rule
本任务是系统基础设施维护任务，不进入普通裸 `继承` 默认 USER 候选。仅在用户明确要求继续、维护或升级 Universal Continuity / 继承系统 / 跨对话继承系统时恢复。
