# 跨对话继承系统建设与维护｜Handoff

- task_id: `continuity:universal-continuity-maintenance`
- task_class: `SYSTEM_INFRA`
- owner: `UNIVERSAL_CONTINUITY_HARNESS`
- status: `ACTIVE`
- contract: `CONTINUITY_V3_7`
- current writer: `lease-2c5946fb-3d78-4a23-9440-2df7d41817ec`
- resume_epoch: `5`
- manifest_version: `50`
- system maintenance policy: `1.7`
- meta-maintenance harness: `1.2`
- artifact/context governance: `1.2`
- Agent architecture contract: `1.1`
- control signal contract: `1.0`

## 当前阶段

`V3_7_AGENT_CONTROL_PLANE_V1_1_REGRESSION_VERIFIED__TOP10_SELECTED_PRIMITIVES_PRODUCTION_PROMOTION_REGRESSION_VERIFIED__META_HARNESS_1_2_REGRESSION_VERIFIED__MUTATION_OUTCOME_UNKNOWN_REGRESSION_VERIFIED__CONTEXT_FOOTPRINT_REGRESSION_VERIFIED__TRACER_BULLET_ADMISSION_REGRESSION_VERIFIED__SIGNAL_VERIFY_FIRST_AND_AGENT_READY_BRIEF_REGRESSION_VERIFIED__EXPECTED_TRUTH_EVIDENCE_SEAM_REGRESSION_VERIFIED__NEGATIVE_DECISION_MEMORY_REGRESSION_VERIFIED__OWNER_DRIFT_SIGNALS_OPEN__OPERATOR_DEPENDENCE_LIVE_EVIDENCE_OPEN__PRIOR_LIVE_EVIDENCE_GATES_OPEN`

同聊天继续维护；保持 epoch `5` 与当前 lease，不伪造 takeover。

## 本轮完成：selected primitives 真正晋升生产

Top10 Skill 学习库仍位于 `research/skill-library/2026-global-ai-skills-top10/`。本轮没有复制 whole Skill，也没有新增 `Top10 Policy`、Triage Agent、TDD root policy、decision database authority 或 supervisory Agent，而是把净新增机制放入现有 semantics owner。

1. **reuse-before-build**：`SYSTEM_MAINTENANCE_POLICY.json` + Meta Harness 1.2 对 systemic maintenance 强制先检查平台/插件/owner/runtime/policy/harness/Skill 等可复用能力，再决定是否自建。
2. **facts-vs-decisions / decision frontier**：系统必须区分已验证事实、未解决事实、真正用户决策、自主 next steps；可检索事实不能冒充用户选择题。
3. **architecture payoff + deletion test**：非平凡架构变更必须比较 failure cost / change cost / payoff，并显式考虑删除、简化、合并、no-change；现有 authority 能承载时拒绝新 root surface。
4. **non-idempotent mutation `OUTCOME_UNKNOWN`**：`ARTIFACT_CONTEXT_GOVERNANCE_POLICY.json` 1.2 + `runtime/mutation_outcome.py` 区分 `CONFIRMED_SUCCESS / CONFIRMED_FAILURE / OUTCOME_UNKNOWN`；可能已 dispatch 但未验证 final state 的非幂等写禁止盲重试，必须 reconcile。幂等性只影响 retry safety，不等于 commit proof。
5. **measured context-footprint**：`runtime/context_footprint.py` + `AGENT_ARCHITECTURE_CONTRACT.json` 把“thin”从形容词变成 UTF-8 byte budget。token 仅是明确标注的近似值，不冒充真实 tokenizer。
6. **tracer-bullet admission**：新 owner / 不确定 runtime integration 在 broad rollout 前先证明一条窄的真实或 production-equivalent E2E 路径；只证明该窄路径，不外推为 owner 全局质量。
7. **verify-before-clarify + Agent-ready brief**：`runtime/control_signal.py` 先 re-observe，再自主补 retrievable facts；只有不可获取事实或真实 human judgment 才打断用户。委派前必须生成稳定 brief，而不是扔 raw chat/history。
8. **expected-truth evidence seam**：`runtime/maintenance_decision_eval.py` + corpus 1.1 为 expected truth 冻结独立 identity；live product `trace_ref` 不能与 expected-truth ref 相同。同仓 oracle 作者身份仍不等于独立语义正确性。
9. **searchable negative decision memory**：`runtime/decision_memory.py` 从 durable meta-audit 的 REJECTED alternatives 提取 `concept_key / rationale / rejection_horizon / reconsider_when`，可按概念检索；audit history 仍是 source，不新建第二 authority DB。

## 明确未全局化

- P4 inline crystallization：不新建机制；现有 chat-only material change / durable record 规则更强。
- P6 runtime-served versioned operating knowledge：保留 owner-optional，不以当前证据强推 Universal。
- P11 inspect-default / ask-only-choices：已被 decision frontier + Signal verify-first 覆盖。
- P12 evidence-gated complexity：已被 payoff/deletion + authority admission 覆盖。
- frontend-design：留给 Video/UI 等 owner-local quality harness，不污染 Universal kernel。

## 验证证据

闭环证据：`audits/TOP10_PRODUCTION_PROMOTION_CLOSURE_2026-10-11.md`。

### 原始行为整合高风险验证

- behavioral integration commit: `aa0d6da1a8e36fcaba6559770d0bf621f506ea22`
- Actions run: `38126896565`
- job: `114433021349`
- risk: `HIGH`
- modes: `FULL_CONTROL_PLANE + SYNTHETIC_FAULT_INJECTION`
- all current BUSINESS owner metadata in scope
- synthetic fault suite: PASS, zero failed
- Agent Architecture harness: PASS（保留既有 A-share / Novel / Video drift warnings）
- pytest: `234 passed`

### v50 closure 过程中发现并修复的真实反证

第一次 v50 HIGH-risk closure：

- HEAD: `713e242c87b0bf978a12defe9581036427537234`
- Actions run: `38128049693`
- job: `114436418691`
- system audit: PASS
- synthetic fault suite: PASS
- Agent Architecture harness: PASS
- pytest: `233 passed, 1 failed`
- 失败原因：`latest_meta_maintenance_run_ref` 仍指向 target_manifest_version `49` 的历史 run，而当前 manifest 已是 `50`。

没有放宽测试，也没有把旧 v49 run post-hoc 改写成 v50。新增独立 current run：

`audits/META_MAINTENANCE_TOP10_PRODUCTION_PROMOTION_V50_CLOSURE_2026-10-11.json`

旧 run `audits/META_MAINTENANCE_TOP10_PRODUCTION_PROMOTION_2026-10-11.json` 保留为历史生产晋升轨迹。

### 最终 v50 HIGH-risk closure

- HEAD: `2c101244a7399c7c75ebe56e09ab3aa3443175c7`
- Actions run: `38128234320`
- job: `114436961188`
- risk: `HIGH`
- modes: `FULL_CONTROL_PLANE + SYNTHETIC_FAULT_INJECTION`
- system audit: PASS
- synthetic fault suite: PASS, zero failed
- Agent Architecture harness: PASS，仍仅有已承认的 A-share / Novel / Video drift warnings
- all current BUSINESS owner metadata in scope
- pytest: `234 passed in 0.59s`

`OUTCOME_UNKNOWN` 有专门 deterministic regression，并包含在上述 234-test integrated suite 中。当前 system synthetic-fault collection 没有再复制一个同义 mutation classifier scenario；因此 fault-suite PASS 不被计作该项的独立第二份证明。

## 当前 assurance

Selected Universal production-promotion primitives：**REGRESSION_VERIFIED**。

这不等于：

- `ACTION_LEVEL_INDEPENDENTLY_VERIFIED`；
- `LIVE_OUTCOME_VERIFIED`；
- 四个 BUSINESS owner 每条真实动作路径都已经接入；
- operator-dependence 已经长期解决；
- 全系统无缺陷。

## 仍 OPEN

1. **real new-owner fresh-chat product E2E**：必须自然出现一个新 admitted BUSINESS owner + genuinely fresh ChatGPT product chat；不能用 synthetic fixture 冒充。
2. **Universal operator-dependence**：仍需 independent heldout/live trajectory grader；本轮结构门和 regression 不能替代真实效果证据。
3. **owner-local action adoption**：共享语义只能在真实 owner action 到来时，在该 owner lease 与 exact evidence gate 下接入；Universal 不偷 business lease。
4. **owner architecture drift signals**：A-share / Novel / Video 的已记录 drift 继续 OPEN。
5. **pre-write enforcement**：任意 ChatGPT→GitHub mutation 仍不是通用 `WRITE_PATH_ENFORCED`。
6. **各业务 owner 原有 live gates**：Novel publication/CH9/independent attestation，Financial action-level methodology/blind pairwise/heldout diversity，A-share replay/live adapters/durability，Video generation gateway/trusted reviewer/live provider proof 等继续 owner-local OPEN。

## Next action

以后只在真实事件上继续：

- 新 owner 自然出现时自动拿它做 cold-start live validation；
- owner 真实 material action 出现时按 shared invariant 做 action-level adoption，不制造假样本；
- operator-dependence 有真实 heldout/live trajectory 时再升级 assurance；
- owner drift signal 有新证据时处理对应 owner，不把 metadata maintenance 变成业务 lease takeover；
- 若没有新的可执行证据或真实 defect，遵守 stop rule，不为了“持续优化”制造额外层。

## Recovery refs

- `tasks/universal-continuity-maintenance/TASK_MANIFEST.json`
- `audits/META_MAINTENANCE_TOP10_PRODUCTION_PROMOTION_V50_CLOSURE_2026-10-11.json`
- `audits/META_MAINTENANCE_TOP10_PRODUCTION_PROMOTION_2026-10-11.json`（historical v49 run）
- `audits/TOP10_PRODUCTION_PROMOTION_CLOSURE_2026-10-11.md`
- `SYSTEM_MAINTENANCE_POLICY.json`
- `ARTIFACT_CONTEXT_GOVERNANCE_POLICY.json`
- `AGENT_ARCHITECTURE_CONTRACT.json`
- `CONTROL_SIGNAL_CONTRACT.json`
- `runtime/meta_maintenance.py`
- `runtime/mutation_outcome.py`
- `runtime/context_footprint.py`
- `runtime/control_signal.py`
- `runtime/maintenance_decision_eval.py`
- `runtime/decision_memory.py`
- `HARNESS_STATUS.json`
- `OWNER_ARCHITECTURE_OBSERVATIONS.json`

不要把 `COMMITTED`、CI、结构化 Harness、Skill 热度或 REGRESSION_VERIFIED 外推成 live quality、independent semantic correctness 或 global flawlessness。
