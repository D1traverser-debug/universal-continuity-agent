# 跨对话继承系统建设与维护｜Handoff

- task_id: `continuity:universal-continuity-maintenance`
- task_class: `SYSTEM_INFRA`
- owner: `UNIVERSAL_CONTINUITY_HARNESS`
- status: `ACTIVE`
- contract: `CONTINUITY_V3_7`
- current writer: `lease-2c5946fb-3d78-4a23-9440-2df7d41817ec`
- resume_epoch: `5`
- manifest_version: `49`
- system maintenance policy: `1.7`
- meta-maintenance harness: `1.2`
- artifact/context governance: `1.2`
- Agent architecture contract: `1.1`
- control signal contract: `1.0`

## 当前阶段

`V3_7_AGENT_CONTROL_PLANE_V1_1_REGRESSION_VERIFIED__TOP10_CORE_PRIMITIVES_PRODUCTION_PROMOTION_IN_PROGRESS__META_HARNESS_1_2_WIRED__MUTATION_OUTCOME_UNKNOWN_WIRED__FINAL_CI_PENDING__OWNER_DRIFT_SIGNALS_OPEN__PRIOR_LIVE_EVIDENCE_GATES_OPEN`

同聊天继续维护；保持 epoch `5` 与当前 lease，不伪造 takeover。

## Top10 Skill 研究与选择

完整库仍位于 `research/skill-library/2026-global-ai-skills-top10/`，10/10 source normalization 和 Phase B selection 已完成。该库是 cold-path learning evidence，不进入启动热路径。

本轮开始把选中机制真正晋升生产；不是 whole-skill copy，也没有新增 `Top10 Policy` 或 supervisory Agent。

## 第一批 production promotion

### 1. reuse-before-build

`SYSTEM_MAINTENANCE_POLICY.json` 与 Meta Harness 1.2 现在要求 systemic maintenance 在自建新 capability 前显式检查已有：平台能力、工具/插件、owner/runtime primitive、已有 policy/harness/Skill。`BUILD_NEW` 必须留下已检查且被拒绝的候选。

### 2. facts-vs-decisions / decision frontier

Systemic run 必须区分：

- 已验证事实；
- 尚未解决的事实；
- 真正需要用户决定的事项；
- 可以自主继续的 next steps。

`facts_resolved_before_user_decision=true` 是结构门。可检索/可验证事实不能冒充“需要用户选择”的架构问题。

### 3. architecture payoff + deletion test

任何 systemic architecture maintenance 必须记录 current failure cost、change cost、expected payoff，并显式检查 deletion/simplification/consolidation/no-change。净复杂度增加必须给出理由；现有 authority 能承载时，不新建平行 root surface。

### 4. non-idempotent mutation `OUTCOME_UNKNOWN`

`ARTIFACT_CONTEXT_GOVERNANCE_POLICY.json` 1.2 + `runtime/mutation_outcome.py` 已建立三态：

- `CONFIRMED_SUCCESS`
- `CONFIRMED_FAILURE`
- `OUTCOME_UNKNOWN`

请求可能已 dispatch、但 timeout/ack 丢失且最终状态未验证时，不能假装明确失败。非幂等 `OUTCOME_UNKNOWN` 禁止盲重试；必须 reconcile final state，或依赖真实幂等语义/idempotency key。即使 retry-safe，也不等于 commit proof。

## Meta-Governance 1.2

`runtime/meta_maintenance.py` 从 1.1 升到 1.2，仅对 SYSTEMIC/ARCHITECTURE/FULL_CONTROL_PLANE 强制新增：

- capability reuse scan；
- fact/decision frontier；
- architecture payoff/deletion test。

LOCAL、低耦合、可逆维护仍可走轻量路径；1.0/1.1 run 保持历史可读，不自动提升 assurance。

真实本轮 run：`audits/META_MAINTENANCE_TOP10_PRODUCTION_PROMOTION_2026-10-11.json`。

## 当前验证状态

已添加/更新：

- `tests/test_meta_maintenance.py`
- `tests/test_mutation_outcome.py`
- `tests/test_artifact_context_governance.py`
- `AGENT_MANIFEST.json` runtime/harness 声明。

当前只可称 `WIRED`；最终 current-main 高风险 CI 尚未验收。CI 绿后才允许把第一批提升到 `REGRESSION_VERIFIED`。

## 不外推的边界

- Meta Harness 的结构 PASS 不证明语义判断独立正确；operator-dependence live/heldout grader 仍 OPEN。
- Universal mutation classifier 已有机械语义，不等于四个 BUSINESS owner 每条真实外部写路径都已接入；owner-local adoption 必须由真实 action/event 驱动。
- Top10 其余候选（context-footprint、evidence seam / tracer bullet、frontend-design owner-local 方法等）尚未完成生产晋升。
- A-share / Novel / Video architecture drift signals #2–#4 继续 OPEN。
- real newly admitted BUSINESS owner fresh-chat E2E、methodology action-level independent proof、各 owner live quality/outcome gates 均保持 OPEN。
- arbitrary ChatGPT → GitHub mutation 仍不是通用 pre-write `WRITE_PATH_ENFORCED`。

## Next action

1. 修齐 v49 cache/version-alignment tests；
2. 跑 current-main HIGH-risk CI，要求 risk-tiered audit + Agent architecture harness + full pytest；
3. 红灯按根因修，不降低门；
4. 绿后更新 final manifest/Harness/Handoff/cache 与本轮 meta-run CI evidence；
5. 再评估剩余选中 primitives，按归属层逐个晋升，不批量污染 Universal kernel。

## Recovery refs

- `tasks/universal-continuity-maintenance/TASK_MANIFEST.json`
- `audits/META_MAINTENANCE_TOP10_PRODUCTION_PROMOTION_2026-10-11.json`
- `SYSTEM_MAINTENANCE_POLICY.json`
- `runtime/meta_maintenance.py`
- `ARTIFACT_CONTEXT_GOVERNANCE_POLICY.json`
- `runtime/mutation_outcome.py`
- `research/skill-library/2026-global-ai-skills-top10/PHASE_B_SELECTION.md`
- `OWNER_ARCHITECTURE_OBSERVATIONS.json`
- `SIGNAL_PLANE.md`

不要把 WIRED、CI、Skill 榜单热度或结构化 meta-run 外推成 live quality、独立语义正确性或 global flawlessness。
