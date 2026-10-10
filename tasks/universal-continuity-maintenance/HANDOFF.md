# 跨对话继承系统建设与维护｜Handoff

- task_id: `continuity:universal-continuity-maintenance`
- task_class: `SYSTEM_INFRA`
- display_name_zh: `跨对话继承系统建设与维护`
- owner: `UNIVERSAL_CONTINUITY_HARNESS`
- status: `ACTIVE`
- contract: `CONTINUITY_V3_7`
- system-maintenance policy: `1.2`
- artifact/context governance: `1.1`

## Current truth
- 工程真源：`D1traverser-debug/universal-continuity-agent@main`。
- 本轮纠正了一个维护方式本身的缺陷：不能继续采用“用户指出一个问题 -> 新增一个 policy/prompt/role”的逐症状补丁模式。`SYSTEM_MAINTENANCE_POLICY.json` v1.2 新增 `authority_surface_admission_gate`：创建新的 root policy/contract/registry/permanent agent/active compatibility layer 前，必须先证明现有 authority 不能无歧义承载、不会制造重复、不是更应该用 runtime code/test/schema/owner adapter 解决，并说明 owner/load trigger/deprecation path；否则默认拒绝新增。
- 本轮最初新建了 `FILE_OPERATION_GOVERNANCE_POLICY.json`，随后在架构审查中判定它与现有 artifact/context governance 重叠。其有效语义已合并进 `ARTIFACT_CONTEXT_GOVERNANCE_POLICY.json` v1.1，原文件已经删除；测试明确禁止该平行 root policy 回归。
- `ARTIFACT_CONTEXT_GOVERNANCE_POLICY.json` v1.1 现在统一管理：工程权威、持久任务状态、业务证据、学习证据、cache、scratch、外部引用、个性化上下文，以及文件读/写/改/搬/删/发布的 stable identity、freshness、version/conflict、postcondition verification、invalidation、cleanup。
- Material file mutation 的工具返回成功不等于提交成功；需要 reread/provider metadata 验证后置条件。破坏性修改/删除在 identity 或依赖未知时必须阻塞。弱 identity（仅文件名、聊天描述位置、跨 session local path）不能用于可解析 stable identity 的 destructive/conflict-sensitive mutation。
- Library / Notion / connected apps 默认不是 control-plane authority。系统正确性不能依赖用户先清空它们；即使旧资料仍存在，也不能覆盖当前 owner/GitHub authority。用户可自行清理这些外部 surface，但这只是卫生/降噪，不是正确性的前提。
- Google Drive 被定义为 `OPTIONAL_ARTIFACT_VAULT_OR_EXPLICIT_REFERENCE`：适合最终 Word/PDF/slides/spreadsheets、显式来源、owner 指定业务证据；不允许充当隐式 runtime checkpoint 或工程规则真源。若作为 artifact vault，必须记录 stable provider ref、owner/task、artifact kind、版本/更新时间（可得时）以及验证后的写入回执。
- `OWNER_ADAPTER_CONTRACT.json` 已要求 durable owner 暴露 canonical artifact/file stores、stable identity、read freshness、mutation conflict、post-write verification、invalidation、delete/retention、superseded cleanup、external artifact vault 等 conformance 信息。Universal 只管跨 owner invariant，具体业务 retention 和 business truth 仍由 owner 管。
- 外部学习对照：OpenAI Agents 的 session/trace/eval 强调可观察执行和证据驱动改进；LangGraph 将 checkpoint 作为显式持久状态；Temporal 用 event history + workflow versioning 保障长期 workflow 的 durable execution/兼容升级；OpenAI agent improvement loop采用 trace/feedback -> eval -> harness change，而不是想法直接晋升为规则。完整记录见 `audits/CONTROL_PLANE_ARCHITECTURE_REVIEW_2026-10-10.md`。
- 用户提出的风险类型基本成立：stale read、错文件/错版本、写后未验证、重复/废旧 active artifact、chat-only learning、外部 source 漂移、owner 与总控理解分叉，均属于真实系统风险。但“把外部资料全部删除”不是系统正确性的必要条件；正确架构必须在它们存在时仍 fail-safe。
- CI 中间 run `38021429230` 为 `87 passed / 1 failed`，暴露 `HARNESS_STATUS` 的 canonical acceptance key 漂移。没有放宽测试；已恢复 canonical key。最终 run `38021590796` / job `114123561213` / head `44c9af2d05752df5be35ec279d6fb8458591bbef`：`89 passed in 0.20s`。
- 更广义“自我进化系统”仍按用户要求暂缓单独设计。本轮只固定一个前提：学习/反馈/聊天想法不能无证据自动晋升成生产规则。

## Current stage
`V3_7_CONTROL_PLANE_GOVERNANCE_CONSOLIDATED__OWNER_CONFORMANCE_AND_PRODUCT_E2E_PENDING`

## Next action
1. 后续维护默认 architecture-first；新增 authority surface 前执行 admission gate，优先修改既有 authority、增加 runtime/test/schema、合并/删除 superseded mechanism。
2. 各合法 owner writer/maintenance turn 逐步补齐 artifact/file conformance，不抢其他 active lease、不从 Universal 重写业务真相。
3. 最终 Word/PDF 等如需长期存储，允许 owner 采用 Google Drive artifact vault，但必须以 stable ref + verified write receipt 接入；是否启用由对应 owner/用户具体任务决定，不让 Drive 成为 control-plane dependency。
4. 账户级 Custom Instructions execution-readiness/autonomous-maintenance 增量以及 existing-chat/fresh-chat 产品 E2E 仍是产品层待验收项。
5. broader self-evolution 留待下一轮单独设计。

## Recovery rule
本任务是系统基础设施维护任务，`EXPLICIT_ONLY`。恢复后先读本 Handoff、manifest、`SYSTEM_MAINTENANCE_POLICY.json`、`ARTIFACT_CONTEXT_GOVERNANCE_POLICY.json`；不要从聊天记忆重建执行真相。
