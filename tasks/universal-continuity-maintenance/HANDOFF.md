# 跨对话继承系统建设与维护｜Handoff

- task_id: `continuity:universal-continuity-maintenance`
- task_class: `SYSTEM_INFRA`
- owner: `UNIVERSAL_CONTINUITY_HARNESS`
- status: `ACTIVE`
- contract: `CONTINUITY_V3_7`
- methodology profile contract: `1.0`
- system-maintenance policy: `1.4`
- artifact/context governance: `1.1`
- execution-readiness contract: `1.0`

## Current truth
- 工程真源：`D1traverser-debug/universal-continuity-agent@main`。同聊天 lease 仍是 `lease-f266a907-aaf1-4b6a-a283-0e64b979d652`，`resume_epoch=1`；本轮没有 takeover。
- Universal 已完成 composable methodology self-pilot：`artifact_io@1.0`、`operational_hygiene@1.0`、`evolution@1.0` 通过 exact-version profile + owner-local hooks 复用公共不变量，`runtime/methodology_conformance.py` 机械拒绝 floating version、missing hook 和 forbidden override。
- canonical bootstrap 已瘦身为 `ENTRYPOINT.md -> CURRENT_PROTOCOL.json -> event-specific authority -> exact owner state`；无关 policy、audits、owners、旧聊天历史默认 cold path。
- 用户已于 2026-10-10 明确确认：旧 Continuity Custom Instructions 段已直接删除，并完整保存当前 `STARTUP_HOOK.md` 提供的最新版账户级指令。因此账户层 minimal-bootstrap、execution-readiness、autonomous-maintenance 传播状态从 pending 改为 confirmed。
- 这个确认只证明用户完成账户 UI 保存；**不证明** existing-chat refresh/handshake 或 fresh-chat bare-inherit E2E 已成功。产品验收仍需真实对话证据。

## Composable methodology self-pilot
- `OWNER_ADAPTER_CONTRACT.json` 内 methodology composition v1.0 是共享方法学 contract，没有新增平行 `METHODOLOGY_POLICY.json`。
- `artifact_io@1.0`：stable identity、freshness/conflict、verified mutation、invalidation、retention/cleanup、artifact-vault hooks。
- `operational_hygiene@1.0`：incident evidence、self-maintenance trigger、owner-aware GC、scoped reliability freeze。
- `evolution@1.0`：learning evidence、independent candidate critique、eval/regression promotion、superseded cleanup。
- domain owner 可以替换本地 implementation/taxonomy/threshold/evaluator/安全 retention，但不得覆盖 authority precedence、single-writer lease、authoritative-reread commit、candidate != production、promotion requires evidence、destructive mutation safety。
- Financial Writing / Video Growth 的领域进化方法继续留在 owner 本地；Universal 只复用跨领域 invariants，不接管领域算法。

## Validation history
- Universal methodology/hot-path engineering validation：run `38036023965` / job `114166494334` / head `f07c3b5a6a746f0adb70ed1878093d659c60b7c9`，`102 passed in 0.20s`。
- final main 在 checkpoint/status/cache 同步后又验证：run `38036340774` / job `114167444776` / head `8e913eb091eb2592fdd2488fd3e1d08db25ab4e6`，`102 passed in 0.15s`。
- 中间三次 `101 passed / 1 failed` 分别保护 existing-chat coverage、mandatory `进度提交`、version-lifecycle ownership pointer；没有通过删测试掩盖瘦身回归。

## Product / account boundary
- `account_continuity_instruction_confirmed_by_user = true`。
- `account_execution_readiness_extension_confirmed = true`。
- `account_autonomous_maintenance_extension_confirmed = true`。
- `account_minimal_bootstrap_extension_confirmed = true`。
- confirmation evidence：2026-10-10 用户在当前 maintenance chat 明确回复“已保存最新版 Custom Instructions。旧的直接删掉了，用的你给的这个”。
- GitHub 仍不是 UI push channel；上述状态来自用户真实保存确认，不来自 repo 推断。
- existing-chat product E2E：PENDING。
- fresh-chat bare-inherit product E2E：PENDING。
- 产品验收原则：repo CI 不能替代真实聊天；fresh-chat 首轮只发 `继承` 并检查完整 discovery，不选择业务任务，避免为测试无意义 takeover。

## Business-owner boundary
- Financial Writing：durable feedback capture 已 wired；methodology profile binding 待合法 owner turn。
- Video Growth：`Production Methodologist -> Evolution Engineer candidate -> Red Team -> Showrunner` 保持 owner-local；methodology profile binding 待合法 owner turn。
- A股、Novel profile/operational-hygiene conformance 也只在合法 maintenance/writer turn 完成；Universal 不抢业务 lease、不直接改写 business truth。
- legacy `owner_must_expose` compatibility mirrors 暂保留，直到支持的 owners 全迁移且 regression 证明无旧 reader。

## Current stage
`V3_7_COMPOSABLE_METHODOLOGY_KERNEL_ACTIVE__ACCOUNT_HOOK_CONFIRMED__OWNER_PROFILE_MIGRATION_AND_PRODUCT_E2E_PENDING`

## Next action
1. 真实 existing-chat E2E：在一个升级前已经存在、已纳入 Continuity 的持久任务聊天中触发一次不需要推进业务的 continuation/refresh；PASS 要求读取 current protocol/owner capability/profile，原地刷新，不能仅因 contract/profile 更新而更换 lease 或增加 `resume_epoch`。
2. 真实 fresh-chat E2E：新建普通聊天，仅发送 `继承`；PASS 要求 minimal bootstrap、完整 discovery 或明确 `INCOMPLETE_DISCOVERY/CONTINUITY_BOOTSTRAP_UNAVAILABLE`，不得从记忆猜测。首轮不要选择业务任务。
3. 收到产品 E2E 证据后，Universal 负责验收并写回，不要求用户自己判断 pass/fail。
4. 并行在 Financial Writing / Video Growth / A股 / Novel 的合法 owner turn 做 thin profile binding + methodology conformance + owner-specific regression/eval；如果只是新增重复配置、没有减少复制/漂移，则拒绝推广或回退。
5. 无 scheduler/event-watch infrastructure 时，不声称聊天关闭后的离线持续自维护。

## Recovery rule
恢复本系统任务时先读 `TASK_MANIFEST.json` + 本 Handoff，再按 `ENTRYPOINT.md` 的事件驱动矩阵加载所需 authority；不要机械预读全部 policy，也不要从聊天记忆重建执行真相。
