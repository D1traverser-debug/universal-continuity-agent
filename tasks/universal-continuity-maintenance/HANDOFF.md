# 跨对话继承系统建设与维护｜Handoff

- task_id: `continuity:universal-continuity-maintenance`
- task_class: `SYSTEM_INFRA`
- display_name_zh: `跨对话继承系统建设与维护`
- domain: `CONTINUITY`
- owner: `UNIVERSAL_CONTINUITY_HARNESS`
- status: `ACTIVE`
- resume_visibility: `EXPLICIT_ONLY`
- contract: `CONTINUITY_V3_5`

## Current truth
- Universal Continuity 工程真源：`D1traverser-debug/universal-continuity-agent@main`。
- ChatGPT Library 只保留根级薄 bootstrap 指针；完整 Continuity 工程目录已删除。
- v3.4 已实现 bare-inherit deterministic discovery quorum：裸“继承”必须完整查询所有 required owner source 后才能报告总任务数。
- 真实新聊天验收暴露启动链缺口：单独输入“继承”时，新聊天可能只命中长期 Memory 中的“学习继承，任务不继承”，完全没有调用 Library/GitHub。
- 因此 v3.5 新增 `STARTUP_HOOK.md`：GitHub/Library 只是存储与发现面，不是新聊天自动事件监听器；裸“继承/继续/恢复”必须由账户级 Custom Instructions 或等价全局指令先路由到 Universal Continuity。
- `学习继承，任务不继承` 仅适用于 NEW_TASK；明确 continuation 命令必须优先分类为 CONTINUE。
- 未触发 Universal Continuity 的泛化回复定义为 `CONTINUITY_BOOTSTRAP_NOT_TRIGGERED`，不得宣称继承成功。
- 当前核心 discovery/owner/index 逻辑保持有效；待完成的是账户级启动钩子配置后的真正新聊天端到端验收。

## Current stage
`V3_5_STARTUP_HOOK_REQUIRED`

## Next action
配置账户级 Custom Instructions 启动钩子，然后打开真正新聊天，只发送 `继承`。PASS 必须是：完整候选发现/一致候选数，或 required source 不可用时明确 `INCOMPLETE_DISCOVERY`；若仍只回复“学习继承、任务不继承”，则启动钩子仍未生效。

## Recovery rule
本任务是系统基础设施维护任务，禁止进入普通裸“继承”业务候选。仅在用户明确说 `继承：跨对话继承系统建设与维护`、`继续跨对话继承系统建设与维护`，或明确要求继续维护/升级 Universal Continuity Agent 时恢复。

成功在新聊天接管后，旧聊天退役。
