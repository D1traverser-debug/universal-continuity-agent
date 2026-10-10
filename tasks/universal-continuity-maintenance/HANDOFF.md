# 跨对话继承系统建设与维护｜Handoff

- task_id: `continuity:universal-continuity-maintenance`
- task_class: `SYSTEM_INFRA`
- owner: `UNIVERSAL_CONTINUITY_HARNESS`
- status: `ACTIVE`
- contract: `CONTINUITY_V3_7`
- current writer: `lease-4b4bc507-0949-4b2e-aed4-c0186dd07566`
- resume_epoch: `2`

## 当前结论

Universal v3.7 的 existing-chat / fresh-chat Continuity 产品传播 E2E 已通过。四个业务 owner 的 methodology **声明级** rollout 已完成；但声明、hook binding 和 owner CI 都不是 action-level operational proof。

本轮纠正了上一轮维护误判：Financial Writing 的 Word 生成、render、持久 WritingState、知识写回和外部引用行为实际会触发 `artifact_io@1.0`。此前只绑定 `operational_hygiene@1.0 + evolution@1.0` 不完整，不能用“只声明当前实际需要的 profile”解释。

## Financial Writing 修复

### 1. artifact_io 已补齐

当前 Financial adapter：`D1traverser-debug/financial-writing-agent@main:continuity/UNIVERSAL_PROTOCOL_ADAPTER.json`

现在精确绑定：
- `artifact_io@1.0`
- `operational_hygiene@1.0`
- `evolution@1.0`

`artifact_io` 的 12 个 owner-local hooks 已映射到 Financial 自己现有的 WritingState / Word / render / hash / downstream invalidation / knowledge-writeback / external-reference 机制，没有复制 Universal 大段规则，也没有增加平行业务状态机。

回归测试新增在 Financial `tests/test_execution_capability_entrypoint.py`，防止 `artifact_io` 或必需 hooks 后续被静默移除。

验证：
- behavioral/test head: `07a05bf2dc93db25b9514f3c66807bc967a3d3bf`
- Actions run `38062102017`
- job `114242271276`
- SDK surface / MCP smoke / unit+trajectory / executable contract eval / static ownership+bundle / wheel isolated install / DOCX render 全 PASS。
- adapter evidence metadata commit: `91724371b7281024ff52bfac2c28b914104d06b2`
- corresponding Actions run `38062215617`: PASS。

Financial 的业务 durable task `financial-writing:main` 有独立 active lease；本次 SYSTEM_INFRA maintenance 没有修改它的 manifest/Handoff、文章 stage、文章内容或业务 lease。

### 2. action-level operational methodology gate 已提升为总控硬步骤

Universal 原本已有 `runtime/methodology_conformance.py:evaluate_operational_methodology_conformance`，它明确要求：
- event-activated `profile_runs`；
- profile version；
- activation id / trigger；
- 实际 observed hooks；
- stable evidence refs；
- independent evidence verifier。

但上一轮 `ENTRYPOINT.md` 没把这条 evaluator 明确放进 material owner action 的强制执行链，导致“声明接线正确，但这一轮可能没触发”的 operator-dependence 风险仍存在。

现已修复：
- `ENTRYPOINT.md` commit `119b0197e7b659219d627aac155830ab802bb650`
- `tests/test_methodology_conformance.py` commit `3be40d76819109bd38a0cf02ca5ec9415c438ad8`
- Universal Actions run `38062342604`: PASS。

当前规则：只验证本次动作实际激活的 profile；但凡该 profile 支撑/约束 material action，在宣称相应 gate 完成或 `COMMITTED` 前，必须拿真实 profile run + 独立可验证 evidence。缺 receipt/verifier 只阻塞对应 gate，不能用 declaration、owner regression 或 CI 替代。

## 精确未闭环项

1. **Financial action-level operational proof**：控制面硬门已接好，但尚未用一篇新的真实 Financial material article run 产生并独立验证完整 profile receipt。因此只能说 enforcement contract 已修，不能说 live article trajectory 已验证。
2. **Financial prose quality improvement**：仍缺 independently verifiable blind pairwise judge + evidence verifier。已知 offshore-wind rejection 必须改善，rutile held-out 不得退化；CI 不能证明文章质量提升。
3. **Personalized Writing DNA**：仍需要自然产生的真实 user acceptance/edit 或 post-publication performance evidence。
4. **Universal operator-dependence incident**：仍需真实 live maintenance-decision/escalation product trajectories + independent grading/evidence verification 才能关闭。

## Current stage

`V3_7_PRODUCT_E2E_PASS__OPERATOR_DEPENDENCE_INCIDENT_ACTIVE__FINANCIAL_THREE_PROFILES_BOUND_AND_REGRESSION_PASS__ACTION_LEVEL_CONFORMANCE_PENDING__LIVE_QUALITY_EVIDENCE_PENDING__OWNER_DECLARATION_MIGRATION_COMPLETE`

## Next action

- 下一次真实 Financial material action：按事件只激活需要的 methodology profiles，收集 `profile_runs` 与独立可验证 refs，运行 operational methodology conformance；只有真实 PASS 才能把 Financial action-level gate 标为已验证。
- 有独立 Financial blind pairwise judge + verifier 时，跑 quality promotion evidence。
- 有独立 product-run/grader path 时，跑 Universal maintenance-decision held-out trajectories。
- 在这些能力未出现前保持精确 OPEN，不伪造后台执行或 operational PASS。

## Recovery refs

- `tasks/universal-continuity-maintenance/TASK_MANIFEST.json`
- `OWNER_REGISTRY.json`
- `OWNER_PROTOCOL_ADAPTATION_REGISTRY.json`
- `ENTRYPOINT.md`
- `OWNER_ADAPTER_CONTRACT.json`
- `runtime/methodology_conformance.py`
- Financial: `D1traverser-debug/financial-writing-agent@main:continuity/UNIVERSAL_PROTOCOL_ADAPTER.json`
- Financial: `D1traverser-debug/financial-writing-agent@main:continuity/EXECUTION_CAPABILITIES.json`

恢复时读取 manifest + 本 Handoff，再按 `ENTRYPOINT.md` 事件矩阵加载当前动作需要的 authority；不要从旧聊天重建执行真相。
