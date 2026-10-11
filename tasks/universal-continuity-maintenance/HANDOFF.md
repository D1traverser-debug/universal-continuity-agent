# 跨对话继承系统建设与维护｜Handoff

- task_id: `continuity:universal-continuity-maintenance`
- task_class: `SYSTEM_INFRA`
- owner: `UNIVERSAL_CONTINUITY_HARNESS`
- status: `ACTIVE`
- contract: `CONTINUITY_V3_7`
- current writer: `lease-2c5946fb-3d78-4a23-9440-2df7d41817ec`
- resume_epoch: `5`
- manifest_version: `47`
- system maintenance policy: `1.6`
- meta-maintenance harness: `1.1`
- Agent architecture contract: `1.1`
- control signal contract: `1.0`

## 当前阶段

`V3_7_AGENT_CONTROL_PLANE_V1_1_REGRESSION_VERIFIED__FINANCIAL_THIN_ROUTER_PASS__LIVE_DRIFT_SIGNAL_TRAJECTORY_VERIFIED__A_SHARE_NOVEL_VIDEO_OWNER_DRIFT_SIGNALS_OPEN__MONITOR_NOTIFICATION_BOUNDARY_CALIBRATED__PRIOR_LIVE_EVIDENCE_GATES_OPEN`

本聊天经用户明确要求已合法接管 SYSTEM_INFRA：epoch `4 -> 5`，当前 lease 为 `lease-2c5946fb-3d78-4a23-9440-2df7d41817ec`。同聊天继续维护时保持该 lease/epoch，不再伪造 takeover。

## 这轮完成的主控改造

GitHub Agent 产品化现在由共享架构约束：

`Skill/router -> Runtime/executor -> Workflow/state -> Harness/eval -> References -> Continuity`

Universal 是 Registry / Router / shared Architecture Harness / Monitor / Signal Plane，而不是跨仓万能业务 writer。

### Agent Architecture Contract 1.1

Universal `AGENT_ARCHITECTURE_CONTRACT.json` 已从 1.0 升到 backward-compatible 1.1：

- owner manifest 1.0 与 1.1 显式支持；
- 未知未来版本 fail closed；
- Skill 允许 `ROUTER` 或 compact hard-boundary router class；
- A-share/Video 已出现的 1.1 owner vocabulary 只有被 Universal alias 显式接纳后才合法；
- A-share 的 `public_entrypoint + internal_components` 与 scalar `canonical_root` 只作为 contract 显式声明的 field-shape compatibility；
- runtime 不再硬编码 1.1 field-shape 特例，而是从 contract 的 `field_shapes_by_manifest_version` 决定是否允许；
- 删除对应 contract declaration 时，负向 regression 必须 FAIL；
- Skill >8192 bytes = `PASS_WITH_DRIFT`，缺 runtime/workflow/harness = structural FAIL。

## Financial thin router

Financial 当前 head：`a76c83c917ae6c81ec398ef99749125131e6be2c`。

`skills/financial-writing-agent/SKILL.md` 已从约 20KB 缩到 `5540` bytes；详细研究/写作/标题/Word/QA 规则仍由 references/policy/runtime/guards 持有，Skill 只保留路由、执行边界与 compact hard-boundary anchors。

Financial owner CI `38108186593` SUCCESS。没有改 Financial business task stage、article state 或 business lease。

## 第一条真实 post-rollout Signal Plane trajectory

所有四个 BUSINESS owner 在初始 rollout 后 HEAD 均发生变化，旧 observation cache 全部 stale。本轮重新观察后：

- Financial `a76c83c...` — `PASS`, Skill 5540, CI `38108186593` SUCCESS。
- A-share `666c77a...` — `PASS_WITH_DRIFT`, Skill 8272, CI `38108315217` SUCCESS。
- Novel `df9be9a...` — `PASS_WITH_DRIFT`, Skill 19540, CI `38108317227` SUCCESS；CHAT_BRIDGED assurance 不变。
- Video `ee029fee...` — `PASS_WITH_DRIFT`, Skill 9310, CI `38088627844` SUCCESS；strict isolated review 仍 OPEN。

Durable audit：`audits/AGENT_ARCHITECTURE_LIVE_DRIFT_REVALIDATION_2026-10-11.json`。

非权威 signals：

- #2 A-share Skill budget drift；
- #3 Novel Skill budget drift；
- #4 Video Skill budget drift。

这些 signal 不改变 owner business truth，也不授予 Universal business lease。

已证明 Signal Plane：`remote detection -> durable GitHub control signal emission`。

未证明：automatic owner repair、未知 failure-class completeness、用户通知投递。

## Architecture Watch 边界

Automation `Agent Architecture Watch` id `6acab16812248191b9f8c8ab52803491` 保持 daily condition watch。

产品状态显示 `notifications_enabled=false` / `email_enabled=false`，因此不能说“已可靠主动通知用户”。当前 prompt 为 durable-signal-first：meaningful drift 优先 create/update `[CONTROL_SIGNAL]`; 只有产品通知能力实际 enabled 才允许声称通知。

## 验证证据

中间并非一路绿：

- takeover 后 Meta-run/manifest binding stale，CI 正确红；没有放宽测试，而是把 Meta-run + manifest + Handoff + Generic cache 原子重绑。
- Universal atomic checkpoint run `38109034408`：system audit、architecture harness、full pytest PASS。
- Universal high-risk runtime run `38109071587` / job `114380651443`：变更被识别为 `HIGH`，实际进入 `FULL_CONTROL_PLANE + SYNTHETIC_FAULT_INJECTION`；24 个 synthetic fault case 全 PASS；architecture harness PASS；full pytest `197 passed`。
- Universal negative compatibility run `38109089931` SUCCESS：field-shape compatibility 未在 contract 声明时 fail closed。

因此 Agent Architecture 1.1 当前 assurance = `REGRESSION_VERIFIED`，不是 independent semantic correctness 或 live business quality。

## 当前 OPEN

1. A-share / Novel / Video Skill-router signals #2-#4，等待各 owner engineering context 安全 slimming + owner CI，再由 Universal remote revalidation 关闭。
2. Architecture Watch 用户通知 delivery disabled/unproven；durable GitHub signal emission 是已证明 transport。
3. Automatic owner repair 与未知未来 failure-class completeness 未证明。
4. Universal operator-dependence 仍需 independent held-out/live maintenance trajectory grader + distinct verifier。
5. real newly admitted BUSINESS owner + genuinely fresh ChatGPT product chat cold-start E2E 仍 OPEN。
6. owner methodology receipt 1.3 的真实 action independent semantic verification 继续 event-gated。
7. Financial live prose quality / Personalized Writing DNA outcome、Novel provider-attested isolation、Video strict isolated reviewer 等 owner live assurance 保持 OPEN。
8. arbitrary ChatGPT -> GitHub mutation 仍不是 universal pre-write `WRITE_PATH_ENFORCED`。

## Next action

保持 daily Architecture Watch 与 Signal Plane。A-share/Novel/Video 在各自 owner engineering context 消费 #2-#4；Universal 只在 owner 修复完成后重新观察 HEAD/Skill/manifest/CI 并关闭相应 signal。没有新 signal 时不制造维护 mutation。

## Recovery refs

- `tasks/universal-continuity-maintenance/TASK_MANIFEST.json`
- `audits/META_MAINTENANCE_SYSTEM_SELF_AUDIT_2026-10-11.json`
- `audits/AGENT_ARCHITECTURE_LIVE_DRIFT_REVALIDATION_2026-10-11.json`
- `AGENT_ARCHITECTURE_CONTRACT.json`
- `AGENT_MANIFEST.json`
- `OWNER_ARCHITECTURE_OBSERVATIONS.json`
- `CONTROL_SIGNAL_CONTRACT.json`
- `SIGNAL_PLANE.md`
- `runtime/agent_architecture.py`
- `runtime/agent_architecture_audit.py`
- `tests/test_agent_architecture.py`

不要把 architecture PASS、owner CI、control signal、watch task 或 COMMITTED 外推成 live quality、独立语义正确性、notification delivery 或 global flawlessness。
