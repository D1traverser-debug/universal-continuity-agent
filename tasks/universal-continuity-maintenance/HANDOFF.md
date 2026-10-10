# 跨对话继承系统建设与维护｜Handoff

- task_id: `continuity:universal-continuity-maintenance`
- task_class: `SYSTEM_INFRA`
- owner: `UNIVERSAL_CONTINUITY_HARNESS`
- status: `ACTIVE`
- contract: `CONTINUITY_V3_7`
- current writer: `lease-4b4bc507-0949-4b2e-aed4-c0186dd07566`
- resume_epoch: `2`

## 当前总状态

- Universal v3.7 existing-chat / fresh-chat Continuity 产品传播 E2E：PASS。
- Methodology profile applicability negative-space guard：PASS。任何 current-contract profile 都必须显式 `APPLIES / NOT_APPLICABLE + reason + evidence_refs`；适用 profile 静默漏绑会 FAIL。
- Financial：`artifact_io + operational_hygiene + evolution` 已绑定并 owner regression PASS；真实文章 action-level methodology conformance 与 prose-quality blind pairwise evidence仍 OPEN。
- Novel：Release Execution Evidence 已完成二次挑刺/加固；domain business stage/Canon/lease 未改。
- Universal operator-dependence incident：仍 OPEN，需真实 independently graded maintenance-decision trajectories 才能关闭。

## Novel owner 独立核验与二次挑刺

用户提供 Novel owner 自审回复后，本 maintenance writer 独立读取了 Novel `SKILL.md`、`continuity/EXECUTION_CAPABILITIES.json`、`runtime/release_evidence_guard.py`、tests、checkpoint、evolution audit 与 CI。

原回复的核心事实成立：
- Skill 已进入 2.1 系列；
- CH9+ 有 release-evidence hard gate；
- CH8 明确 `LEGACY_AGGREGATE_MIGRATED`，不补造历史 receipts；
- normal review = `CHAT_BRIDGED / ROLE_SEPARATED_NOT_ATTESTED_ISOLATED`；
- `strict_attested_isolated_reviewer` 仍 `DECLARED_ONLY`；
- CH8/CH9 business stage、Canon v12、external publication fact、resume_epoch/lease 未被系统进化改写；
- owner CI 的 Recovery Guard / Release Evidence Guard / owner contract tests 均可执行。

但原自审还有第二阶证据强度缺口：一个最终聚合 `CHxxxx_EXECUTION_EVIDENCE.json` 仍可能由同一 CHAT_BRIDGED session 事后一次性补写。更多角色名、timestamp 或文件数量不能把这种 self-attested receipt 变成独立 execution attestation。

同时原 guard 还存在可机械修复的绑定弱点：
- Project Profile / Canon refs / recent FINAL refs 没有逐项验证文件存在与 hash；
- CHAT_BRIDGED receipts 没有统一强制 Context Pack binding 与非空 result summary；
- final-body pipeline roles 没有统一绑定 FINAL source hash；
- blind reviewer receipt 的自身 source/context binding 不够严格。

## Novel 二次加固

采用最小修法：强化能机械验证的 binding，同时明确降级不能证明的 assurance；不新增更多假 Agent，也不伪造 isolated executor。

Novel owner 现在要求：
- 所有本地 Project Profile / Canon / recent FINAL Context Pack ref 必须存在并 SHA-256 匹配；
- 每个 receipt 必须有唯一 id；
- CHAT_BRIDGED receipt 必须绑定 frozen Context Pack；
- 每个 receipt 必须有非空 role result summary；
- `COPYEDITOR_PROOFREADER / ARTIFACT_RELEASE_ENGINEER / CANON_COMMITTER` 必须绑定 FINAL source hash；
- blinded reviewer evidence 本身必须有有效 source hash + Context Pack binding；
- deterministic guard 输出 evidence strength：`STRUCTURED_SELF_ATTESTED_CHAT_BRIDGED_UNLESS_EXTERNAL_TRACE_PRESENT`；
- Skill / execution capabilities 明确：CHAT_BRIDGED receipt 是结构化自证，不是 independent proof of cognition or chronology；真正 attestation 需要 distinct execution identity/provider trace。

Novel versions after hardening:
- Skill: `2.1.1-github`
- runtime metadata: `github-owner-2.2.1`
- execution-capability profile_version: `3`
- release_evidence_contract: `1.0`（兼容加固，首次真实 CH9 尚未发生）

Key owner evidence:
- hardened behavioral/test head: `ced06cec1a2201135d32c7f9d8c8c32c43b83507`
- CI run `38065144178` / job `114251164978`: Recovery Guard PASS, Release Evidence Guard PASS, full owner tests PASS
- owner metadata/audit head: `2ebc4dea8c5b6c083ad1db5d0c88b8839b6a6f95`
- CI run `38065230141`: PASS

第一次 hardened CI `38065104562` 曾 FAIL，因为旧 recovery-contract test 对 pre-hardening evidence-contract 字符串做了精确断言；guards 本身均 PASS。旧断言随后被更新，没有绕过失败。

Novel current business truth remains owner-owned:
- current_stage: `CH0008_FINAL_ACCEPTED_PUBLISH_READY_AWAITING_EXTERNAL_PUBLICATION_CONFIRMATION`
- Canon v12
- last FINAL = CH8
- CH8 external publication = not confirmed
- CH9 = READY
- 新 evidence contract 从 CH9 首次生产正式接受 action-level 验证

## Central cache reconciliation

Novel owner 自审指出 Universal `OWNER_PROTOCOL_ADAPTATION_REGISTRY` 仍缓存旧 regression head。当前 SYSTEM_INFRA chat 持有合法 Universal maintenance lease，因此本轮已同步：
- `OWNER_REGISTRY.json` Novel status -> release-evidence binding hardened + CHAT_BRIDGED self-attested + CH9 production proof pending；
- `OWNER_PROTOCOL_ADAPTATION_REGISTRY.json` -> novel behavioral head / owner metadata head / CI refs / skill/runtime version / evidence-strength boundary。

这些是 rebuildable conformance metadata；没有修改 Novel business task manifest/checkpoint/Canon/正文/发布事实/lease。

## 仍未闭环

1. **Novel CH9 real production proof**：代码/negative tests/CI 已证明 enforcement mechanics；尚未有真实 CH9 Context Pack + role receipts trajectory。只有首次生产 PASS 后才能说 domain release-evidence gate 在真实章节上工作。
2. **Novel true execution attestation**：CHAT_BRIDGED receipt 仍是 self-attested。不同 execution identity/provider trace 未提供前，不得说真正 isolated / independently attested reviewer 已执行。
3. **Financial action-level operational proof**：下一次真实 material article 仍需 event-activated `profile_runs` + independent verifier + operational methodology conformance。
4. **Financial prose-quality promotion**：仍需 independently verifiable blind pairwise evidence；offshore-wind rejection 必须改善，rutile held-out 不退化。
5. **Universal operator-dependence incident**：仍需 independently graded held-out product trajectories。

## Current stage

`V3_7_PRODUCT_E2E_PASS__OPERATOR_DEPENDENCE_INCIDENT_ACTIVE__OWNER_PROFILE_APPLICABILITY_GUARD_PASS__NOVEL_RELEASE_EVIDENCE_BINDING_HARDENED__FINANCIAL_THREE_PROFILES_BOUND_AND_REGRESSION_PASS__ACTION_LEVEL_CONFORMANCE_PENDING__LIVE_QUALITY_EVIDENCE_PENDING`

## Next action

- Novel：等 CH8 外部发布确认后，业务 owner 进入 CH9；首次 CH9 必须真实生成/验证 release-evidence artifacts，不得由 maintenance task 代跑或补造。
- Financial：下一次真实 article material action 做 action-level methodology conformance；有独立 pairwise judge/verifier 后跑质量 promotion。
- Universal：有真实 product-run/grader path 后跑 maintenance-decision held-out suite。
- 缺真实能力/证据时保持 OPEN，不用 CI、角色名或自报 receipt 冒充更高 assurance。

## Recovery refs

- `tasks/universal-continuity-maintenance/TASK_MANIFEST.json`
- `OWNER_REGISTRY.json`
- `OWNER_PROTOCOL_ADAPTATION_REGISTRY.json`
- `OWNER_ADAPTER_CONTRACT.json`
- `ENTRYPOINT.md`
- Novel: `D1traverser-debug/novel-writing-agent@main:SKILL.md`
- Novel: `continuity/EXECUTION_CAPABILITIES.json`
- Novel: `runtime/release_evidence_guard.py`
- Novel: `audits/NOVEL_SYSTEM_EVOLUTION_AUDIT_2026-10-10.md`

恢复时先读 manifest + 本 Handoff，再按 ENTRYPOINT 事件矩阵加载当前动作所需 authority；不要从旧聊天重建执行真相。
