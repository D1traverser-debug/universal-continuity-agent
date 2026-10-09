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
- 用户已在真正的新聊天中只发送 `继承` 做端到端验收：5 个 required owner 全部查询成功，返回 4 个默认 USER 候选；因此 account startup hook 的真实 E2E 已通过。
- v3.6 新增 `CONTEXT_RECOVERY_POLICY.json`：恢复链从“尽量加载更多”改成渐进式披露：metadata → 短 handoff → next_action 需要的精确 artifact refs → selective search → old chat history 最后兜底。
- Handoff 现在明确是“当前执行真相”，不是聊天 transcript 的压缩副本；spec/plan/issue/commit/diff/research 等已有 artifact 优先引用，不重复复制。
- v3.6 新增任务拓扑：同目标继续/同目标 fresh handoff/side query/fork child task/new task，避免旁支污染主任务或因换聊天误建新 task。
- 不采用固定 150K 等 token 阈值作为硬规则；上下文健康根据漂移、矛盾分支、authority 变化和恢复成本判断。
- 验证改为 risk-matched verification：低风险局部变更只做定向检查，contract/router/authority 变更才扩大测试。
- 新增 `MEDIA_DISTILLATION_PROTOCOL.md`：媒体学习严格区分原始音轨/字幕、视觉、作者同源长文、页面元数据、第三方整理；禁止把完整 transcript 冒充“完整看过所有画面”。
- 当前参考媒体（杰森的效率工坊 GPT-6 Codex 核心技巧）已完成同一性核验、完整 20:14 YouTube transcript 阅读、作者同源长文完整阅读，并对影响系统的关键产品原则用 OpenAI 当前一手文档做了交叉验证。
- 当前参考媒体的视觉层尚未完成 full-stream review：Opera Browser Connector 断开，YouTube/微信均未提供可直接提取的完整视频流；此缺口已被明确记录，不冒充完成。

## Current stage
`V3_6_PROGRESSIVE_CONTEXT_RECOVERY_ACTIVE`

## Next action
继续维护并验收 v3.6 渐进式恢复策略；若获得原视频流、浏览器连接或可逐场景视觉访问，则补齐参考媒体的完整视觉层学习，并仅在发现新的、经验证且适合 Continuity scope 的原则时再升级系统。

## Recovery rule
本任务是系统基础设施维护任务，禁止进入普通裸“继承”业务候选。仅在用户明确说 `继承：跨对话继承系统建设与维护`、`继续跨对话继承系统建设与维护`，或明确要求继续维护/升级 Universal Continuity Agent 时恢复。

成功在新聊天接管后，旧聊天退役。
