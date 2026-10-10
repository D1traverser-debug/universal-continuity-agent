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
- 本轮按“看实际怎么做，不看怎么描述”完成 Universal 自身 self-pilot，而不是先要求子 Agent 服从一个尚未验证的方法学。
- 独立比较了 controller-runtime/Kubernetes reconciliation、Backstage service/extension-point/module、OPA bundle roots、Temporal durable workflow versioning、OpenAI trace/eval improvement loop。共同实战约束是：共享窄不变量/接口，domain behavior 本地化；明确 ownership；运行中 durable state 不能漂浮到 latest；进化必须由执行证据/eval 驱动。
- 拒绝三类候选：巨型 parent-Agent inheritance tree、把公共 policy 全复制到每个 owner、让 Universal 接管每个 domain 的进化算法。UVM `extends` 只保留为“公共不变量 + 受控特化”的启发，不作为生产架构。

## Composable methodology self-pilot
- `OWNER_ADAPTER_CONTRACT.json` 现有 authority 内增加 methodology composition v1.0，没有新增 `METHODOLOGY_POLICY.json`。
- 当前 profiles：
  - `artifact_io@1.0`：stable identity、freshness/conflict、verified mutation、invalidation、retention/cleanup、artifact-vault hooks；语义 owner 为 `ARTIFACT_CONTEXT_GOVERNANCE_POLICY.json`。
  - `operational_hygiene@1.0`：incident evidence、self-maintenance trigger、owner-aware GC、scoped reliability freeze；语义 owner 为 `SYSTEM_MAINTENANCE_POLICY.json`。
  - `evolution@1.0`：learning evidence、independent candidate critique、eval/regression promotion、superseded cleanup；语义 owner 为 `CONTINUOUS_LEARNING_POLICY.md`。
- owner 只 pin exact profile version + bind domain-local hooks；不复制共享 profile prose，不允许 floating `latest`。
- domain owner 可以覆盖 implementation/taxonomy/threshold/evaluator/安全 retention 等本地方法，但不得覆盖：authority precedence、single-writer lease、authoritative-reread commit、candidate != production、promotion requires evidence、destructive mutation safety。
- `runtime/methodology_conformance.py` 是真实 validator，不是文档承诺。它会 FAIL profile version mismatch、missing hooks 和 forbidden override。
- `tests/test_methodology_conformance.py` 已验证：三 profile 可薄绑定组合；`latest` 被拒；缺 post-write verify 被拒；owner 想把 candidate 直接当 production 被拒；平行 methodology root policy 被禁止。

## Universal hot-path slimming
- 审计发现旧 `ENTRYPOINT.md` 一边说“按需加载”，一边末尾又要求 11-file `Read next`；旧 `STARTUP_HOOK.md` 也会诱导每次启动预读大量 control-plane 文档。这是实际 bloat，不只是文档审美问题。
- 现在 canonical bootstrap 改为：`ENTRYPOINT.md -> CURRENT_PROTOCOL.json -> event-specific authority -> exact owner state`。
- `SYSTEM_BLUEPRINT.md`、audits/research、无关 owner、inactive profiles、旧聊天 transcript 默认是 cold path。
- 条件加载：bare discovery 才读 discovery；protocol mismatch 才读 lifecycle/reconciliation；material owner execution 才读 execution contract + exact Skill/capabilities；文件操作才激活 `artifact_io`；维护才激活 `operational_hygiene`；durable learning/evolution 才激活 `evolution`。
- Blueprint 从原来的 11-layer 展示收敛为 7 个架构域：bootstrap edge、continuity kernel、execution kernel、methodology composition、domain owner boundary、artifact/context boundary、maintenance/evolution boundary。生命周期/进度/恢复的 ownership pointer 仍显式保留，但不再等于固定 preload。

## “瘦身不能删语义”的实战证据
三次中间 CI 失败都被保留并用于纠错，而不是改测试糊绿：
1. run `38035776737`：`101 passed / 1 failed`，发现瘦身误删“包括升级前已经打开/继承的旧对话”；恢复。
2. run `38035840541`：`101 passed / 1 failed`，发现 mandatory `每次最终答复末尾必须报告“进度提交”` 语义被弱化；恢复。
3. run `38035972287`：`101 passed / 1 failed`，发现 Blueprint 删掉 `VERSION_LIFECYCLE_POLICY.json` ownership pointer；确认这是架构指针而非热路径负担，恢复。
- 最终工程验证：run `38036023965` / job `114166494334` / head `f07c3b5a6a746f0adb70ed1878093d659c60b7c9`，package `3.7.0`，`102 passed in 0.20s`。
- 详细审计：`audits/CROSS_AGENT_METHODOLOGY_COMPOSITION_REVIEW_2026-10-10.md`。

## Business-owner boundary
- Financial Writing 与 Video Growth 已有各自真实进化实现，不应被 Universal 替换成一个通用“学习算法”。后续它们只绑定 shared `evolution` invariants，再保留 domain-specific eval/roles/runtime。
- Financial Writing：durable feedback capture 已真实 wired；其写作样本、structure/style/trajectory eval 继续归财经 owner。
- Video Growth：`Production Methodologist -> Evolution Engineer candidate -> Red Team -> Showrunner` 继续归视频 owner；scheduled learning evidence 已 `SESSION_EXECUTABLE`，mid-stage sidecar 仍只有 `HARNESS_WIRED`，不能夸大。
- A股、Novel 以及 Financial/Video profile migration 都必须在各自合法 maintenance/writer turn 进行；Universal 不抢业务 lease，不重写 business truth。
- legacy `owner_must_expose` 列表暂时作为 compatibility mirror；只有支持的 owners 全部迁到 profile declarations、回归证明无旧 reader 后才能删。

## Product / execution boundaries
- 账户级旧 Continuity hook 已由用户确认存在；但 GitHub 更新不会自动修改 Custom Instructions。最新 minimal-bootstrap / execution-readiness / autonomous-maintenance 增量仍未得到用户明确保存确认。
- existing-chat refresh/handshake 和 fresh-chat product E2E 仍需真实产品证据；repo CI 不能替代。
- 没有 scheduler/event-watch infrastructure 时，maintenance/reconciliation/evolution 发生在 active material/maintenance turn；不得声称离线持续后台自治。

## Current stage
`V3_7_COMPOSABLE_METHODOLOGY_KERNEL_ACTIVE__OWNER_PROFILE_MIGRATION_AND_PRODUCT_E2E_PENDING`

## Next action
1. 先用 Universal 作为 reference implementation；不因为 contract 已存在就声称所有 owner 已“继承”。
2. 在合法 owner turn 中逐个迁移 Financial Writing / Video Growth / A股 / Novel：只声明实际需要的 profiles、pin exact version、绑定现有 hooks，跑 `methodology_conformance` + owner-specific regression/eval；如果只是新增一层重复配置而没有减少复制/漂移，则拒绝推广或回退设计。
3. Financial/Video 保留各自 domain evolution methods，仅共享 authority/evidence/reliability/promotion/cleanup invariants。
4. 后续继续审计 root authority surfaces；能合并/下沉 runtime/test 的不要横向新增 policy。
5. 产品层继续等待最新账户语义保存确认，并做 existing-chat/fresh-chat E2E。

## Recovery rule
恢复本系统任务时先读 `TASK_MANIFEST.json` + 本 Handoff，再按 `ENTRYPOINT.md` 的事件驱动矩阵加载需要的 authority；不要再机械预读全部 policy，也不要从聊天记忆重建执行真相。
