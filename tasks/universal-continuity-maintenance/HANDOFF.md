# 跨对话继承系统建设与维护｜Handoff

- task_id: `continuity:universal-continuity-maintenance`
- task_class: `SYSTEM_INFRA`
- owner: `UNIVERSAL_CONTINUITY_HARNESS`
- status: `ACTIVE`
- contract: `CONTINUITY_V3_7`
- current writer: `lease-2c5946fb-3d78-4a23-9440-2df7d41817ec`
- resume_epoch: `5`
- manifest_version: `46`
- system maintenance policy: `1.6`
- meta-maintenance harness: `1.1`
- Agent architecture contract: `1.1`
- control signal contract: `1.0`

## 当前阶段

`V3_7_AGENT_CONTROL_PLANE_V1_1_INTEGRATION_VALIDATION_PENDING__FINANCIAL_THIN_ROUTER_PASS__LIVE_DRIFT_SIGNAL_TRAJECTORY_PROVEN__A_SHARE_NOVEL_VIDEO_OWNER_DRIFT_SIGNALS_OPEN`

本聊天由用户明确要求接管 SYSTEM_INFRA；takeover 已从 epoch 4 合法推进到 epoch 5，并回读确认当前 lease。不得再次在同聊天伪造 takeover。

## 本轮不是继续堆规则

目标仍是 GitHub Agent 产品化，而不是把 Library/聊天里的大段文字搬成仓库 Markdown：

`Skill/router -> Runtime/executor -> Workflow/state -> Harness/eval -> References -> Continuity`

Universal 是 control plane：Registry / Router / shared Architecture Harness / Monitor / Signal Plane。它不应成为跨仓万能业务 writer。

## 独立复核上一位 writer 的结果

上一位 writer 建立的方向成立：

- `AGENT_ARCHITECTURE_CONTRACT.json` / root `AGENT_MANIFEST.json`；
- thin bootstrap budget；
- centralized architecture harness；
- State Plane vs Signal Plane；
- daily remote Architecture Watch；
- BUSINESS owner `agent_manifest_ref` admission。

但本轮重新观察后发现 rollout 后所有四个 BUSINESS owner HEAD 都已前进，旧 `OWNER_ARCHITECTURE_OBSERVATIONS.json` 全部 stale。说明 remote freshness 不是一次性 rollout receipt。

## Agent Architecture Contract 1.1

A-share 与 Video 两个独立 owner 在 rollout 后都引入了 owner-local `architecture_contract_version=1.1` 与新 vocabulary。简单把它们打回 1.0 会掩盖 Universal v1.0 表达能力不足；允许各 owner 自己定义共享语义则会造成 contract fork。

因此 Universal 中央 contract 升级到 backward-compatible `1.1`：

- 显式支持 manifest `1.0` 与 `1.1`；
- 未知未来版本 fail closed；
- Skill 仍以 router 为核心，但 1.1 可表达 compact hard-boundary anchors；
- A-share / Video 已出现的 owner vocabulary 只有在 Universal 显式 alias 下才合法；
- A-share 的 `public_entrypoint + internal_components`、scalar `canonical_root` 只作为被中央 contract 明确列出的 1.1 field-shape compatibility；
- 未知 alias/shape 不能借“兼容”绕过 schema；
- Skill >8192 bytes 仍是 `PASS_WITH_DRIFT`，缺 runtime/workflow/harness 仍是 structural FAIL。

Tests 已覆盖 v1.0 compatibility、A-share/Video aliases、approved field shapes、unknown alias、future 9.9 version、oversize drift 与 missing-layer negatives。

## Financial thin router 已完成

Financial 当前 owner head：

`a76c83c917ae6c81ec398ef99749125131e6be2c`

`skills/financial-writing-agent/SKILL.md` 已从约 20KB 压缩到 `5540` bytes，同时保留 compact hard-boundary anchors；详细研究/写作/标题/Word/QA 规则继续由 `references/*`、policy、runtime、guards 负责。

最终 owner CI：`38108186593` SUCCESS。

旧 static audit 首轮曾因要求 Skill 复制业务规则而红；没有把 20KB 手册塞回去，而是保留必要 hard-boundary anchors，使 thin router 与现有 contract regression 同时成立。

Financial business task stage / article state / business lease 未被 Universal 改写。

## 第一条真实 post-rollout Signal Plane trajectory

本轮真实 remote sweep：

- Financial `a76c83c...` — architecture `PASS`, Skill 5540, CI `38108186593` SUCCESS。
- A-share `666c77a...` — `PASS_WITH_DRIFT`, Skill 8272, CI `38108315217` SUCCESS。
- Novel `df9be9a...` — `PASS_WITH_DRIFT`, Skill 19540, CI `38108317227` SUCCESS；CHAT_BRIDGED assurance 仍保持边界。
- Video `ee029fee...` — `PASS_WITH_DRIFT`, Skill 9310, CI `38088627844` SUCCESS；strict isolated review 仍保持 OPEN。

Durable audit：`audits/AGENT_ARCHITECTURE_LIVE_DRIFT_REVALIDATION_2026-10-11.json`。

已创建非权威 control signals：

- #2 A-share Skill budget drift；
- #3 Novel Skill budget drift；
- #4 Video Skill budget drift。

Universal 没有为解决这些 drift 去抢 owner business lease。Signal 不是 task authority、不是 checkpoint、不是业务状态。

这证明了 Signal Plane 的一条真实闭环到：

`remote detection -> durable GitHub control signal emission`

还没有证明 automatic owner repair 或未知 failure-class completeness。

## Architecture Watch 的真实边界

Automation `Agent Architecture Watch` id `6acab16812248191b9f8c8ab52803491` 仍 enabled daily condition watch。

但产品状态显示 `notifications_enabled=false`、`email_enabled=false`。因此不能宣称“已可靠主动通知用户”。Prompt 已改为 durable-signal-first：发现 meaningful drift 时优先 create/update `[CONTROL_SIGNAL]`，只有产品通知能力实际 enabled 时才表述为通知。

当前可证明：daily check infrastructure + durable GitHub signal path。

当前不可证明：用户通知投递、自动 owner 修复、未来未知 drift recall。

## CI 失败证据保留

Universal CI `38108771603`：

- risk-tiered local audit PASS；
- HIGH -> FULL_CONTROL_PLANE + SYNTHETIC_FAULT_INJECTION；
- 24 synthetic fault cases 全 PASS；
- Agent architecture harness PASS；
- full pytest 195 PASS / 2 FAIL。

两个失败都来自 takeover 后 meta-run/manifest binding stale：Meta-run 仍 target v44，而当前 manifest 已 v45；HARNESS latest meta-run 与 manifest ref 也不一致。

没有放宽测试。当前 checkpoint 将 Meta-run + manifest v46 + Handoff + Generic cache 原子绑定，随后再跑 clean high-risk CI。

## 当前 assurance ceiling

本轮已经证明：

- shared Agent Architecture Contract 1.1 compatibility/normalization 已实现并有 regression；
- current four-owner remote re-observation 已完成；
- Financial thin router owner CI PASS；
- Signal Plane 已产生真实 post-rollout durable signals；
- architecture monitor notification boundary 已校准。

尚未证明：

- 最终 Universal 1.1 integration clean CI（当前 next action）；
- A-share / Novel / Video Skill drift 已关闭；
- Watch 的用户通知 delivery；
- automatic owner repair；
- Universal operator-dependence independent heldout/live grader；
- real newly admitted BUSINESS owner + genuinely fresh product chat cold-start E2E；
- universal pre-write `WRITE_PATH_ENFORCED`；
- owner live quality/isolation gates。

## Next action

运行并验证当前 Agent Architecture Contract 1.1 高风险整合的 clean Universal CI。若 PASS：

1. 将本轮 architecture stack 升为 `REGRESSION_VERIFIED`；
2. 保持 Financial `PASS`；
3. A-share/Novel/Video 继续由各 owner engineering context 消费 #2-#4，再由 Universal remote revalidation 关闭；
4. Architecture Watch 持续 cold-path 检查，无 drift 时不制造维护工作；
5. prior independent/live evidence gates 保持 OPEN，不用 CI 冒充。

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

恢复时先读 manifest + 本 Handoff。不要把 architecture PASS、owner CI、control signal、watch task 或 COMMITTED 外推成 live business quality、independent semantic correctness、notification delivery 或 global flawlessness。
