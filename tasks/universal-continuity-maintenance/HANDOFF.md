# 跨对话继承系统建设与维护｜Handoff

- task_id: `continuity:universal-continuity-maintenance`
- task_class: `SYSTEM_INFRA`
- owner: `UNIVERSAL_CONTINUITY_HARNESS`
- status: `ACTIVE`
- contract: `CONTINUITY_V3_7`
- current writer: `lease-2c5946fb-3d78-4a23-9440-2df7d41817ec`
- resume_epoch: `5`
- manifest_version: `48`
- system maintenance policy: `1.6`
- meta-maintenance harness: `1.1`
- Agent architecture contract: `1.1`
- control signal contract: `1.0`

## 当前阶段

`V3_7_AGENT_CONTROL_PLANE_V1_1_REGRESSION_VERIFIED__TOP10_SKILL_LIBRARY_10_OF_10_COMPLETE__CROSS_SKILL_SELECTION_COMPLETE__PRODUCTION_PROMOTION_PENDING_REGRESSION_BACKED_CHANGE__OWNER_DRIFT_SIGNALS_OPEN__PRIOR_LIVE_EVIDENCE_GATES_OPEN`

本聊天经用户明确要求已合法接管 SYSTEM_INFRA：epoch `4 -> 5`，当前 lease 为 `lease-2c5946fb-3d78-4a23-9440-2df7d41817ec`。同聊天继续维护时保持该 lease/epoch，不再伪造 takeover。

## 2026 Global AI Skills Top10 完整蒸馏库

用户纠正了最初“只看 rank #1 就先选择”的做法，要求先完整蒸馏十个 Skill，再统一比较选型。该要求现已闭环。

Library root：`research/skill-library/2026-global-ai-skills-top10/`

包含：

- `README.md` — 完成/证据边界；
- `SCHEMA.md` — 统一完整蒸馏 schema；
- `INDEX.json` — 10/10 source pin + 最终 disposition；
- `01-find-skills.md` ... `10-triage.md`；
- `CROSS_SKILL_PRIMITIVE_MATRIX.md`；
- `PHASE_B_SELECTION.md`。

固定上游 revision：

- `vercel-labs/skills@13e4063a1cf913f5606d57d42ab83a86f5001e04`
- `mattpocock/skills@49dd158d1076134a641b33efb035946536778336`
- `vercel-labs/agent-browser@d9570915f4dd6504dee4070379d2c4f79d81dbb2`
- `anthropics/skills@dbd4588f9e1033efb41dad4bef2f7947c8993d44`

完整蒸馏不只看主 `SKILL.md`；对 thin wrapper 继续追 delegated primitive，对 executable Skill 继续追 runtime/tests/evals/workflows/reference，记录 source-author 已知投诉、失败模式、out-of-scope 和证据上限。

`tests/test_top10_skill_distillation_library.py` 强制 10/10 完整后才允许最终 selection；GitHub Actions run `38110768456` SUCCESS。

Durable audit：

- `audits/META_MAINTENANCE_TOP10_SKILL_LIBRARY_2026-10-11.json`
- `audits/TOP10_SKILL_LIBRARY_CLOSURE_2026-10-11.md`

## Top10 横向选择结果

没有按安装榜名次选，也没有 whole-sale copy。

### 选中的跨 Agent 原子机制

- `find-skills`：reuse-before-build capability acquisition funnel；
- `grill-me/grilling`：facts-vs-decisions + bounded dependency frontier；
- `grill-with-docs`：inline crystallization / sparse durable admission，**不接受 prose-only cross-Skill invocation 当执行证明**；
- `improve-codebase-architecture`：payoff-weighted scan + deletion test；
- `agent-browser`：最强架构参考——thin discovery Skill + runtime-versioned instruction + context-footprint eval + session isolation + mutating `outcome_unknown` + final-state verification；
- `tdd`：evidence seam / independent expected truth / tracer bullet；
- `setup-matt-pocock-skills`：inspect → default → only ask genuine choices + evidence-gated complexity；
- `triage`：verify-before-clarify + durable agent-ready brief + negative institutional memory。

### owner-local only

`frontend-design` 只作为 Video/视觉/UI owner 的质量方法候选，不进入 Universal kernel。

### 不新增的机制

`handoff` 仅作参考：当前 `CONTEXT_RECOVERY_POLICY` 已更强，包含 task/owner/stage/next_action/blocker/version/artifact refs/lease epoch 与 pointer-over-copy。

### 明确拒绝

- install/stars 固定阈值作为质量 gate；
- global install 默认；
- 一行 Skill/跨 Skill 文案调用被当作实际执行证明；
- chat-only durable state；
- prompt-only red-before-green/角色执行宣称；
- same-actor self-review 冒充独立质量证明；
- 所有 Top10 方法复制进 Universal startup/Skill；
- 因榜单流行度直接推广进生产。

Production promotion **尚未发生**。下一轮如继续进化，只通过现有 authority/runtime/harness 晋升确实补缺口的机制，并单独加 regression；不新建 `Top10 Policy` 或永久 supervisory Agent。

## Agent Control Plane 1.1 既有状态保持

共享架构仍是：

`Skill/router -> Runtime/executor -> Workflow/state -> Harness/eval -> References -> Continuity`

Universal 是 Registry / Router / shared Architecture Harness / Monitor / Signal Plane，不是跨仓万能业务 writer。

Financial thin router 已完成：Skill `5540` bytes，owner CI `38108186593` SUCCESS，未改 Financial business state/lease。

当前 remote owner observation：

- Financial `a76c83c...` — `PASS`；
- A-share `666c77a...` — `PASS_WITH_DRIFT`，Skill 8272；
- Novel `df9be9a...` — `PASS_WITH_DRIFT`，Skill 19540，CHAT_BRIDGED assurance 不变；
- Video `ee029fee...` — `PASS_WITH_DRIFT`，Skill 9310，strict isolated review 仍 OPEN。

Open signals：#2 A-share、#3 Novel、#4 Video。Universal 不抢 owner business lease。

## Architecture Watch 边界

Automation `Agent Architecture Watch` id `6acab16812248191b9f8c8ab52803491` daily condition watch 仍启用。

已证明：remote drift observation 可写 durable GitHub control signal。

未证明：用户通知投递；产品状态为 `notifications_enabled=false` / `email_enabled=false`。不能宣传成可靠主动通知用户。

## 既有关键验证证据

- Agent Architecture 1.1 high-risk run `38109071587`：`FULL_CONTROL_PLANE + SYNTHETIC_FAULT_INJECTION`，24 fault cases PASS，full pytest `197 passed`。
- negative compatibility run `38109089931` SUCCESS。
- Top10 library completeness regression run `38110768456` SUCCESS。

这些最多支持对应的 `REGRESSION_VERIFIED`，不外推为 live business quality 或 independent semantic correctness。

## 当前 OPEN

1. Top10 选中跨 Agent primitives 的 production promotion 尚未进行；必须分别走现有 authority + regression，不允许 chat-only adoption。
2. A-share / Novel / Video Skill-router signals #2-#4 等 owner engineering context 修复 + owner CI + Universal remote revalidation。
3. Architecture Watch 用户通知 delivery disabled/unproven。
4. Automatic owner repair 与未知未来 failure-class completeness 未证明。
5. Universal operator-dependence 仍需 independent held-out/live maintenance trajectory grader + distinct verifier。
6. real newly admitted BUSINESS owner + genuinely fresh ChatGPT product chat cold-start E2E 仍 OPEN。
7. owner methodology receipt 1.3 的真实 action independent semantic verification 继续 event-gated。
8. Financial live prose quality / Personalized Writing DNA outcome、Novel provider-attested isolation、Video strict isolated reviewer 等 owner live assurance 保持 OPEN。
9. arbitrary ChatGPT -> GitHub mutation 仍不是 universal pre-write `WRITE_PATH_ENFORCED`。

## Next action

如果继续 production evolution：只晋升 Top10 selection 中**确实补现有缺口**的原子机制，优先候选为 capability reuse-before-build、facts-vs-decisions、architecture payoff/deletion test、context-footprint/evidence-seam 与 non-idempotent mutation `outcome_unknown`；每个都进入已有 authority/runtime/harness 并加回归，禁止新增 Top10 root policy/supervisor。

并行保持 daily Architecture Watch / Signal Plane 和 #2-#4 owner drift；没有新 signal 时不制造无价值维护。

## Recovery refs

- `tasks/universal-continuity-maintenance/TASK_MANIFEST.json`
- `research/skill-library/2026-global-ai-skills-top10/README.md`
- `research/skill-library/2026-global-ai-skills-top10/INDEX.json`
- `research/skill-library/2026-global-ai-skills-top10/PHASE_B_SELECTION.md`
- `audits/TOP10_SKILL_LIBRARY_CLOSURE_2026-10-11.md`
- `audits/META_MAINTENANCE_TOP10_SKILL_LIBRARY_2026-10-11.json`
- `AGENT_ARCHITECTURE_CONTRACT.json`
- `OWNER_ARCHITECTURE_OBSERVATIONS.json`
- `CONTROL_SIGNAL_CONTRACT.json`
- `SIGNAL_PLANE.md`

不要把 Skill 榜单安装量、研究库完整性、selection、owner CI、architecture PASS、control signal、watch task 或 COMMITTED 外推成 live quality、独立语义正确性、notification delivery 或 global flawlessness。
