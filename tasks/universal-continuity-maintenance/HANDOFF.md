# 跨对话继承系统建设与维护｜Handoff

- task_id: `continuity:universal-continuity-maintenance`
- task_class: `SYSTEM_INFRA`
- owner: `UNIVERSAL_CONTINUITY_HARNESS`
- status: `ACTIVE`
- contract: `CONTINUITY_V3_7`
- methodology profile contract: `1.0`
- system-maintenance policy: `1.5`
- artifact/context governance: `1.1`
- execution-readiness contract: `1.0`

## Current truth

- 工程真源：`D1traverser-debug/universal-continuity-agent@main`。
- 当前 maintenance chat 已完成 new-chat takeover：`lease-4b4bc507-0949-4b2e-aed4-c0186dd07566`；`resume_epoch=2`；supersedes `lease-f266a907-aaf1-4b6a-a283-0e64b979d652`。
- 产品传播链 existing-chat / fresh-chat 双路径 E2E 均已 PASS。
- risk-tiered global audit 已常驻 CI preflight。
- operator-dependence reliability incident 仍为 `PARTIALLY_REMEDIATED__PRODUCT_BEHAVIOR_EVAL_PENDING`；不能因为代码层 hardening 已完成就宣称总控已经能稳定自主识别所有 systemic signal。
- 用户本轮要求优先修 Financial Writing；已在不改写 Financial 业务 task state / checkpoint / lease 的前提下完成 owner-system repair、质量回归 harness 与 owner regression。

## Operator-dependence reliability incident

真实故障：用户再次需要提醒 Universal，不应等待用户提出架构机制或枚举后续内部问题，而应自己诊断、反驳初始方案、识别系统性/重复失败并推进修复。

这不是缺少 policy 文案。`SYSTEM_MAINTENANCE_POLICY.json` 已写明：用户不是系统维护员、重复纠正属于 reliability signal、非平凡方案必须挑战初始候选、内部维护不应等待用户枚举。

因此根因属于 enforcement / product behavior，而不是“再补一句提示词”。详细 incident：`audits/UNIVERSAL_OPERATOR_DEPENDENCE_RELIABILITY_INCIDENT_2026-10-10.md`。

## Central operational-conformance hardening remains active

`runtime/methodology_conformance.py` 继续区分：

- `evaluate_methodology_conformance(...)`：声明级 profile/version/hooks/overrides 合法性；
- `evaluate_operational_methodology_conformance(...)`：实际 profile-run、required hooks、caller-supplied independent verifier、evidence refs。

硬边界不变：declaration PASS 不等于 operational PASS；self-reported receipt 不是 evidence；缺 independent verifier 或 evidence ref 验证失败必须 fail closed。

`runtime/system_audit.py` 的 `methodology_declaration_operational_separation` 仍属于 CORE_ALWAYS CI invariant。

## Financial Writing first-owner repair completed at engineering/harness level

### 1. 不是“再加一条少编号规则”，而是修冲突机制

真实海风失败稿被从 ChatGPT Library 找回，并固化成 owner-local regression artifact：

- `financial-writing-agent/evals/artifacts/offshore-wind-2026-10-10-rejected-deep-v071.md`

根因审计发现：Financial 的 `style.md` 已经反对机械对称，但 runtime 曾同时存在三层相反压力：

- Writer prompt 要求 `Use visible numbered hierarchy aggressively`；
- deterministic `check_payload_navigation` 把文章长度、股票数、H1 数映射成最低 H2/H3 配额；
- Word mechanical QA 对长 Deep 文再次要求至少 3 个低级编号。

这会把“可导航”错误等价成“编号越多越好”，直接制造报告腔/机械分组。

本轮已收敛为：

- H1 保留宏观导航；
- H2/H3 只在真实并行分析分支、类别、步骤时使用；
- 不再由篇幅、股票数量、H1 数量或视觉配额触发；
- deterministic guard 只保留极端 `monolithic body block` 可读性保护，不再设编号最低数量；
- company-universe/material coverage、stock-grounded monitoring、template cluster、Reader Funnel、Authorial Prose、factual/compliance/state/artifact gates 均保留。

因此这不是降低门槛，而是把错误的格式 proxy 从质量门槛中删除。

### 2. General editorial quality 与 Personalized Writing DNA 已拆开

新增 owner-local：

- `financial_writing_agent/quality_regression.py`
- `evals/quality_regression.json`
- `tests/test_quality_regression.py`

质量 promotion 需要：

- hard invariants 零退化；
- blind pairwise candidate-vs-baseline；
- candidate A/B 位置交换；
- position-swap 结果稳定；
- caller-supplied evidence verifier；
- 已知真实失败必须改善；
- held-out 不退化并至少有一个 candidate win。

`GENERAL_EDITORIAL_QUALITY` 不再要求用户先给正向点赞/范文；系统不能把用户变成 optimizer。

`PERSONALIZED_WRITING_DNA` 若声称“这是用户个人偏好”，才额外要求真实 user acceptance/edit 或 post-publication performance evidence。

### 3. Corpus 已由系统主动回收，不依赖用户手工找文件

真实海风拒绝稿已完整固化；另从历史 Library 找到不同题材的 Financial 输出：

- `financial-writing-agent/evals/artifacts/rutile-2026-10-06-heldout-baseline.md`

它仅作为 cross-topic historical owner baseline，不被标成“用户喜欢的范文”。

因此当前：

- `GENERAL_EDITORIAL_QUALITY = PROMOTION_READY_CORPUS_ONLY`
- `PERSONALIZED_WRITING_DNA = NOT_READY_POSITIVE_USER_OR_PERFORMANCE_EVIDENCE_MISSING`

一般质量 corpus 不再依赖用户继续反馈才能启动；但具体“质量提升”仍必须有独立盲评证据。

### 4. Financial owner regression = PASS

Financial behavioral head：`a52249967db7745ebf322e3c9696ef5a03c85f37`

GitHub Actions：

- run `38045054149`
- job `114192795282`
- OpenAI Agents SDK surface smoke = PASS
- MCP Streamable HTTP smoke = PASS
- unit + trajectory = PASS
- executable contract eval = PASS
- static rule ownership / bundle audit = PASS
- wheel + isolated install = PASS
- DOCX render smoke = PASS

随后只追加 methodology assurance metadata commit `a65a6955e7fc40c59b78d782d4671fcf548921c7`，记录上述已验证 behavioral head；不要把 metadata receipt 自己当新的 prose-quality proof。

## What is proven vs not proven

### Proven

- Financial methodology declaration 已 exact-version bound：`operational_hygiene@1.0 + evolution@1.0`。
- quality-regression promotion harness 已可执行并有 regression tests。
- 海风真实失败已进入 durable regression evidence，不再依赖 Library 留存。
- cross-topic held-out 已存在，一般质量 corpus 组成已足够。
- 机械编号 quota 的 runtime/QA 冲突已经移除，同时保留材料完整性和可读性 hard guards。
- Financial owner engineering regression 全绿。

### Not yet proven

- 不能说“财经文章质量已经实证变好”。当前缺的是**具体候选输出的独立 blind pairwise live evidence**。
- 不能说 Personalized Writing DNA 已学会用户偏好；还没有足够真实 positive user/performance evidence。
- 不能说 Universal operator-dependence incident 已关闭；还缺 real maintenance-decision/escalation product trajectory eval。
- 不能说 arbitrary ChatGPT GitHub maintenance write 已 `WRITE_PATH_ENFORCED`；当前仍只有 Universal repository `CI_ENFORCED_POST_WRITE`，除非未来先建立真实 mutation choke point。

## Infrastructure answer to the user's broader question

- 不需要先部署服务器才能修 Financial。repo/runtime/CI/eval 足以完成当前这类结构性修复。
- 服务器/scheduler/event worker 只在需要**聊天关闭后持续运行、在线 trace 采集、定期自动评测/优化**时才成为必要基础设施。
- Custom Instructions/个性化只能改善启动、路由和行为倾向，不能替代 owner runtime gate、eval corpus、promotion evidence、artifact authority 或 CI。
- 用户必须提供的只应是不可替代的外部事实/价值信号，例如：真正的个人审美确认、发布后的真实表现、账号权限/产品 UI 操作；内部诊断、方案比较、文件迁移、回归、状态同步不应转嫁给用户。

## Current stage

`V3_7_PRODUCT_E2E_PASS__OPERATOR_DEPENDENCE_INCIDENT_ACTIVE__FINANCIAL_OWNER_HARNESS_REPAIRED_AND_REGRESSION_PASS__LIVE_QUALITY_EVIDENCE_PENDING__OWNER_PROFILE_MIGRATION_IN_PROGRESS`

## Next action

1. 继续以 Financial Writing 为第一优先 owner。
2. 当存在可验证 independent judge / live owner execution path 时，对具体 candidate 执行真实 blind pairwise：海风 rejection 必须改善；金红石 held-out 不得退化。
3. 只有上述 live evidence PASS 后，才能说这次方法改动“文章质量被证明提升”；CI 本身不能替代该证据。
4. Personalized Writing DNA 只在自然积累到真实 accepted/edit/performance evidence 后 promotion，不要求用户为了系统维护额外造样本。
5. Universal operator-dependence incident 保持 OPEN，直到 real product trajectory eval 证明 live Universal 会主动升级 systemic signal，而非等待用户再次提醒。
6. A股 / Novel 等 owner 后续 thin binding 仍须守 owner authority，不从 Universal 改写其业务 truth 或抢 lease。
7. 无 scheduler/event-watch infrastructure 时，不声称聊天关闭后的离线持续自维护。

## Recovery rule

恢复本系统任务时先读 `TASK_MANIFEST.json` + 本 Handoff，再按 `ENTRYPOINT.md` 的 event-driven matrix 加载所需 authority。不要从旧聊天记忆重建执行真相，也不要因为 profile declaration 或 owner CI PASS 就假定 live quality 已被证明。
