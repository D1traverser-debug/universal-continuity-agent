# 跨对话继承系统建设与维护｜Handoff

- task_id: `continuity:universal-continuity-maintenance`
- task_class: `SYSTEM_INFRA`
- owner: `UNIVERSAL_CONTINUITY_HARNESS`
- status: `ACTIVE`
- contract: `CONTINUITY_V3_7`
- current writer: `lease-4b4bc507-0949-4b2e-aed4-c0186dd07566`
- resume_epoch: `2`

## 当前总状态

- **本轮完整系统审计大纲已实际执行**：authority refresh → 全控制面 inventory → contract/runtime/registry/recovery/execution/learning/status 攻击 → negative-space/replay/self-attestation/bypass → 根因聚类 → 最小修复 → regression/CI → remote owner sweep → second-order challenge → learning distillation → checkpoint。
- Universal 当前内部可执行审计尾项：**COMPLETE**。不能把剩余 live/independent-evidence gate 误写成“内部还有没做的实现”。
- Known-topology existing/fresh-chat Continuity E2E：历史真实证据 PASS；**real new-owner cold-start product E2E 仍 OPEN**。
- Dynamic owner membership：REGRESSION_VERIFIED；`OWNER_REGISTRY.json` 仍是唯一 membership authority。
- Universal operator-dependence incident：仍 OPEN；代码/CI/同会话 self-grading 不能替代 independently graded live/held-out trajectories。
- Methodology declaration rollout：COMPLETE；action receipt contract = **1.3**；current operational PASS 仍必须逐 action 提供 exact action binding + external expectation + independent evidence/semantic verification。
- `COMMITTED`：只表示 durable persistence + authoritative reread；不提升 execution / methodology / review / quality / outcome assurance。

## 这次全量审计抓出的母漏洞

1. **Untrusted verifier input**：expectation、replay history、session observation 本身也可能是不完整/自报控制输入；不能默认可信。
2. **Plan-execution disconnect**：audit mode/fault list 写在计划里，不等于检查真的执行。
3. **Schema-coercion privilege escalation**：`"false"` 等错误类型不能被宽松转换成更高权限/可恢复性。
4. **Complete-discovery / incomplete-presentation split**：全量发现不能在 resolver/UI helper 被静默截断，partial discovery 不能 autoresume。
5. **Historical-proof version laundering**：真实旧 receipt 在合同升级后仍是历史证据，但不能自动升级成当前 assurance。
6. **Suite/history amnesia**：重写 verifier/fault suite 时不能静默忘掉已经防住的旧 failure class。

Durable learning artifact：`audits/FULL_CONTROL_PLANE_EXECUTION_AND_LEARNING_AUDIT_2026-10-11.md`。能机械化的模式已进入 regression/synthetic fault；不是聊天提醒。

## 核心修复

### Execution proof / readiness

- execution receipt：exact expectation mandatory；subject/input/output/result/action/task/stage/capability/executor 不允许靠缺省减少验证。
- receipt anti-replay：receipt-id 检查不能由 caller 关闭；claim anti-replay 时 replay-history completeness 需要 verifier。
- `ATTESTED_ISOLATED`：不能靠 caller 自填 `executor_identity + proof_ref` 晋升；需要独立 attestation verifier。
- duplicate session observations：fail closed。
- `side_channel_allowed=false`：中央 evaluator 现在实际参与 route enforcement，不再只是声明字段。
- permission/recovery boolean：strict typing；禁止 truthy-string 提权。

### Methodology receipt 1.3

- 1.2 → **1.3**；profile hook/version 没变，action-receipt contract 变严。
- receipt 必须有 exact `task_id / stage / action_id / subject_bindings / input_bindings`。
- external action expectation 与 owner receipt 分离，避免 receipt 自己定义自己要证明的 subject。
- duplicate same-profile runs fail closed。
- pre-1.3 historical receipts 不可重放为 current operational PASS。

### Continuity / recovery

- bare authoritative candidate set 默认不再硬截 5 个。
- incomplete discovery 永远不能 autoresume。
- paused/terminal task 不能直接拿 writer lease；需要 owner-authoritative reactivation。
- cross-owner duplicate task_id fail closed，不再静默 dedupe。
- checkpoint 有 task_id 时必须匹配；legacy short checkpoint 缺 task_id 可依赖已经选中的 authoritative task context，不能伪造冲突 identity。
- domain `contract_version` 不再盲目当成 Continuity protocol version。

### System audit / CI

旧问题最严重的一点：`runtime.system_audit` 原来会计算 FULL_CONTROL_PLANE / SYNTHETIC_FAULT_INJECTION 计划，但 CI 固定 `routine_change` 且不传 changed paths；计划存在不等于执行。

已修：
- CI 从真实 commit diff 取得 changed paths；
- high-risk contract/runtime/workflow 变更自动升级；
- selected synthetic faults **真实执行**；
- audit 输出明确 assurance ceiling：local CI ≠ remote owner sweep ≠ live product evidence；
- 重写 fault suite 时保留历史 counterexamples，并追加新 failure classes。

## Remote owner sweep

本轮 maintenance runner 只读当前 4 个 BUSINESS owner 的 adapter / execution capability / discovery metadata；只修派生工程 metadata，不偷业务 lease、不改业务事实。

### Financial Writing

- receipt emitter + MCP public schema + capability metadata 已迁到 1.3 exact-action binding。
- stale task-index v0.6 → v0.7 已同步。
- current owner validation: head `464c7aae2aa94ec61dd6da286aab1107b709629a`; Actions `38074834696`; job `114279535922`; **PASS, 71 tests + SDK/MCP/contract/static/wheel/DOCX render**。
- owner-generated 1.3 receipt 仍是 `UNVERIFIED_OWNER_RECEIPT`；independent operational verification OPEN。
- live prose-quality promotion仍 OPEN；CI 不证明文章变好。

### A-share

- 发现 `audits/2026-10-10_FULL_CONTROL_PLANE_SELF_AUDIT.json` 是真实历史证据，但产生于 receipt 1.3 exact-action 之前。
- 已降级为 `HISTORICAL_ONLY`；不能作为 current v1.3 action-level operational PASS。
- adapter repair head `5d259ac62ee5c0636ae30af5fab3364b904e4f9f`; Actions `38074881268`: **PASS**。
- market-day task state / lease 未改。

### Novel

- current Skill = `2.1.1-github`, runtime = `github-owner-2.2.1`；TASK_INDEX 原来仍镜像旧版本。
- 只修 discovery metadata；business task 仍 `WAITING`，stage 仍 `CH0008_FINAL_ACCEPTED_PUBLISH_READY_AWAITING_EXTERNAL_PUBLICATION_CONFIRMATION`。
- repair head `44a7a83b7327d5ec650d192650fffb7c473df863`; Actions `38074843270`: **PASS**。
- 不把 CHAT_BRIDGED reviewer 描述成 true independent attestation。

### Video

- adapter / capability / task-index 当前指针可达且一致；未发现新的派生 metadata drift。
- 当前业务 stage 仍 `VISUAL_PREVIEW_PROCESS_REENTRY`。
- strict isolated multimodal review / unique quality-critical generation gateway 的已知 blockers 保持 OPEN；不角色扮演成已执行。

## Regression / counterevidence

- Universal recovery hardening current-main regression：run `38074724886`, job `114279195145`, **149 passed**。
- 中间 CI 红灯被保留作 counterevidence：
  - checkpoint identity 第一版收得过严，破坏合法 legacy short checkpoint；改为“存在则必须匹配，缺失由 exact selected authority 提供 identity”。
  - Financial 1.3 emitter 第一版与 MCP 1.2 public schema 冲突；同步 public contract 后再回归。
  - Financial 后续旧测试仍断言 profile 6 / receipt 1.2；更新 stale expectation，而不是回滚 1.3。
- 最终中央 high-risk status/registry/checkpoint sync 仍必须由最新 GitHub Actions 再验证后才可对用户报告 `COMMITTED`。

## Second-order challenge

- plan 是否真的执行？→ selected synthetic faults 现在会执行，且 CI 输入真实 changed paths。
- 验证器输入是不是自己伪造的？→ expectation/replay-history/attestation 增加独立边界。
- 是否只修 triggering example？→ 保留历史 fault corpus + 新 fault class；跨 owner 推广。
- 是否有逃逸路径？→ side-channel、partial discovery autoresume、terminal lease、truthy-string、duplicate observation/task-id、stale derived metadata 都被检查。
- 是否用 CI 冒充 live proof？→ 明确否；remote sweep 与 product/outcome evidence 独立。
- 是否用历史 receipt 冒充新合同？→ 明确禁止；A-share 实际完成了一次降级重分类。
- 是否过度设计？→ 不新增巨型 parent agent / parallel root policy；继续 small kernel + owner-local hooks。

## Assurance ceiling

本轮内部 hardening 最高为：`REGRESSION_VERIFIED`；远端 owner metadata sweep 证明当前读取/派生 metadata 的一致性。

不能因此升级为：
- `ACTION_LEVEL_INDEPENDENTLY_VERIFIED`；
- `LIVE_OUTCOME_VERIFIED`；
- universal pre-write `WRITE_PATH_ENFORCED`。

## Current stage

`V3_7_FULL_CONTROL_PLANE_EXECUTION_HARDENED__REMOTE_OWNER_SWEEP_COMPLETE__METHODOLOGY_RECEIPT_V1_3_ACTIVE__INTERNAL_AUDIT_AND_LEARNING_TAIL_COMPLETE__LIVE_EVIDENCE_GATES_OPEN`

## Next action

1. **没有新 maintenance signal / 新能力时，不再发明内部工作。**
2. 新 BUSINESS owner 真正 admission 后，跑 real new-owner + genuinely fresh-chat product E2E。
3. distinct grader/evidence verifier 可用时，跑 Universal operator-dependence heldout/live trajectories。
4. Financial heldout diversity + independent blind pairwise judge + semantic verifier 满足时，才跑 live quality promotion。
5. Personalized Writing DNA 等待真实 user acceptance/edit 或 post-publication outcome evidence；不要求用户为了验证系统制造正样本。
6. Video strict isolated review / generation gateway、各 owner 1.3 action-level methodology operational gate 继续按各自真实证据推进。
7. arbitrary ChatGPT GitHub mutation 仍只有 repository CI post-write enforcement；不得宣称 pre-write enforcement 已解决。

## Recovery refs

- `tasks/universal-continuity-maintenance/TASK_MANIFEST.json`
- `audits/FULL_CONTROL_PLANE_EXECUTION_AND_LEARNING_AUDIT_2026-10-11.md`
- `HARNESS_STATUS.json`
- `OWNER_REGISTRY.json`
- `OWNER_PROTOCOL_ADAPTATION_REGISTRY.json`
- `runtime/system_audit.py`
- `runtime/execution_receipt.py`
- `runtime/execution_readiness.py`
- `runtime/methodology_conformance.py`
- `runtime/universal_continuity.py`
- `OWNER_ADAPTER_CONTRACT.json`
- `PROGRESS_OBSERVABILITY_POLICY.json`
- `CONTINUOUS_LEARNING_POLICY.md`
- `audits/UNIVERSAL_OPERATOR_DEPENDENCE_RELIABILITY_INCIDENT_2026-10-10.md`

恢复时先读 manifest + 本 Handoff，再按 `ENTRYPOINT.md` 事件矩阵加载当前动作需要的 authority。不要把 CI、receipt existence、COMMITTED、remote metadata sweep 或历史 topology PASS 外推成更高 assurance。
