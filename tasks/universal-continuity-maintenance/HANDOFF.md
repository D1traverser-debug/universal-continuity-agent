# 跨对话继承系统建设与维护｜Handoff

- task_id: `continuity:universal-continuity-maintenance`
- task_class: `SYSTEM_INFRA`
- display_name_zh: `跨对话继承系统建设与维护`
- domain: `CONTINUITY`
- owner: `UNIVERSAL_CONTINUITY_HARNESS`
- status: `ACTIVE`
- resume_visibility: `EXPLICIT_ONLY`
- contract: `CONTINUITY_V3_6`

## Current truth
- Universal Continuity 工程真源：`D1traverser-debug/universal-continuity-agent@main`。
- ChatGPT Library 只保留根级薄 bootstrap 指针；完整 Continuity 工程目录已删除。
- v3.4 已实现 bare-inherit deterministic discovery quorum。
- v3.5 增加账户级 `STARTUP_HOOK.md`，解决新聊天裸“继承”没有真正启动 GitHub Continuity 的问题。
- 用户已在真正的新聊天中只发送 `继承` 做端到端验收：5 个 required owner 全部查询成功，返回 4 个默认 USER 候选；account startup hook 的真实 E2E 已通过。
- v3.6 新增 `CONTEXT_RECOVERY_POLICY.json`：恢复链采用渐进式披露：metadata → 短 handoff → next_action 需要的精确 artifact refs → selective search → old chat history 最后兜底。
- Handoff 是“当前执行真相”，不是 transcript 压缩副本；spec/plan/issue/commit/diff/research 等已有 artifact 优先引用，不重复复制。
- v3.6 新增任务拓扑：同目标继续/同目标 fresh handoff/side query/fork child task/new task，避免旁支污染主任务或因换聊天误建新 task。
- 不采用固定 150K 等 token 阈值作为硬规则；验证采用 risk-matched verification。
- `MEDIA_DISTILLATION_PROTOCOL.md` 已成为正式媒体学习方法：L1 原始媒体、L2 作者同源材料、L3 平台元数据、L4 第三方整理分层取证，禁止跨证据层夸大完成度。
- 当前参考媒体《4 个必须学习的 GPT-6 核心技巧：让你把 Codex 发挥到极致》已完成：原微信页解析、同作者同版 YouTube 身份核验、完整 20:14 transcript 阅读、作者同源长文完整阅读、00:00–20:14 全时段视觉 scene-by-scene 分析。
- 视觉层实际覆盖：Obsidian Canvas、官方文档/来源列表、上下文评测与定价表、compact/side/fork/new 决策树、handoff skill、实验配置/Issue、模型矩阵、ChatGPT-Codex 三层集成图、Prompt/AGENTS.md/Skills 示例、Subagent/Testing/Approval 指南以及最终迁移 Checklist。
- 取其精华：已吸收短 handoff、artifact 引用优先、渐进加载、side/fork/new 任务拓扑、目标/上下文/约束/完成条件式契约、风险匹配验证、可逆操作自主推进等原则。
- 去其糟粕/易过时部分：不把固定 150K smart-zone、固定 long-context 价格阈值、模型价格/模型梯队、第三方桥接工具、账号封禁个案、实验功能开关状态写成 Continuity 硬规则。

## Current stage
`V3_6_PROGRESSIVE_CONTEXT_RECOVERY_ACTIVE`

## Next action
继续维护 v3.6，并用真实跨聊天恢复案例审计 owner handoff 是否足够短、权威、引用化；只有出现新的、经一手证据验证且属于 Continuity scope 的改进点时才升级协议。

## Recovery rule
本任务是系统基础设施维护任务，禁止进入普通裸“继承”业务候选。仅在用户明确说 `继承：跨对话继承系统建设与维护`、`继续跨对话继承系统建设与维护`，或明确要求继续维护/升级 Universal Continuity Agent 时恢复。

成功在新聊天接管后，旧聊天退役。
