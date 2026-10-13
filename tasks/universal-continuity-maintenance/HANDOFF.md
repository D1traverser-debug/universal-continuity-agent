# 跨对话继承系统建设与维护｜Handoff

- task_id: `continuity:universal-continuity-maintenance`
- task_class: `SYSTEM_INFRA`
- owner: `UNIVERSAL_CONTINUITY_HARNESS`
- status: `ACTIVE`
- current_stage: `SYSTEM_MAINTENANCE_ACTIVE`
- current writer lease: `lease-8ecdf71e-46b3-4e7d-b2ea-61ee05c6d654`
- resume_epoch: `8`
- manifest_version: `92`
- Human Durable Revision: `UC-20261013-r92`
- current controller run: `architecture-reliability-benchmark-library-gap-audit-v69-2026-10-13`
- controller status: `BLOCKED` at `M7_IMPLEMENTATION_AND_SUPERSESSION`, revision `11`

## v69 当前停点：学习库和诊断完成，重构未授权

用户明确要求：至少完整学习其列出的架构/可靠性体系，做成独立库，先找出现有问题，**然后等用户命令再调整重构**。

因此本轮严格停在 M7 之前：

- 已完成学习/诊断阶段 `M0 -> M6A`；
- 已建立冷路径、非权威独立研究库：`research/system_architecture_library/`；
- 已完成跨框架矩阵：`research/system_architecture_library/12_cross_framework_matrix.md`；
- 已完成当前 Universal gap audit：`research/system_architecture_library/13_current_universal_gap_audit.md`；
- 已保存候选重构问题/方案，但它们不是决定：`research/system_architecture_library/14_refactor_candidate_map.md`；
- **没有修改** `ENTRYPOINT.md`、`SYSTEM_BLUEPRINT.md`、`ORCHESTRATION_BLUEPRINT.md`、owner contracts、runtime behavior、tests、BUSINESS state 或任何 BUSINESS repo；
- 下一步只能在用户明确下令调整/重构后，重新读取当时最新 authority，再从 M7 继续；不能把当前候选直接当成批准方案。

## 独立学习库覆盖

研究库不是简单罗列框架名称，而是先建立 12 个父系统维度，再映射框架：

1. purpose / lifecycle / decomposition
2. control / reconciliation
3. authority / change
4. topology / interaction
5. execution / environment
6. supervision / recovery
7. reliability governance
8. verification / assurance
9. formal correctness
10. safety / hazard control
11. evolution / learning
12. resilience experiments

已学习并入库的体系至少包括：

- NASA Systems Engineering / V-model-style decomposition-realization reasoning
- Evolutionary Architecture / fitness functions
- Team Topologies / 组间交互、流、平台认知负担
- distributed systems / Raft / idempotency / retries / ambiguous outcomes
- UVM verification architecture
- IBM MAPE-K autonomic control
- Kubernetes Controller / Operator
- Erlang/OTP Supervision Tree
- OpenGitOps
- Google SRE
- AWS Well-Architected Operational Excellence
- environment parity / Twelve-Factor
- DO-178C public assurance guidance + FAA AC 20-115D
- TLA+ / TLC model checking
- N-version programming / correlated failure
- IEC 61508 public functional-safety lifecycle material
- NASA FDIR / fault management
- STPA
- Chaos Engineering

DO-178C、IEC 61508 等付费规范没有被伪装成“已经掌握全部规范正文”，研究库明确记录：这里只能基于公开官方资料做架构学习，不能宣称 certification / normative conformance。

## v69 当前发现

Gap audit 共保存 24 个 finding。高影响类别主要集中在：

- 维护 meta-method 缺少稳定的架构 benchmark taxonomy；
- 没有统一的**派生**系统模型/架构图，把 owner、authority、environment、control loop、dependency、evidence、recovery 放到同一分析视图；
- 组间 owner ownership 清楚，但 interaction mode / dependency / backpressure / escalation 不够一等化；
- ChatGPT / GitHub / CI / owner runtime / MCP-plugin / external product / independent verifier 的环境架构和 parity/promotion 仍碎片化；
- 没有 Universal 自身的 quantitative SLI/SLO/error budget；
- 没有完整的 requirement/invariant -> runtime guard -> test/eval -> live evidence 双向 trace；
- lease/resume_epoch/HEAD-CAS 等核心并发不变量没有 TLA+/等价 formal model checking；
- 没有通用 supervision tree、restart/retry intensity、escalation、degraded/safe-hold recovery model；
- FDIR 的 detection 有，但 isolation/recovery/concurrent-fault 不是统一架构；
- 没有 STPA 风格的 losses/hazards/unsafe-control-action 层；
- synthetic fault injection 已经存在，但没有 UVM 式 coverage closure，也没有 Chaos 式 steady-state/blast-radius contract；
- 独立审查边界比一般系统强，但多模型/多 Agent 仍缺 common-mode failure independence matrix；
- GitOps 的 authority 判断正确，但缺 resource-by-resource desired/observed/reconciler inventory；
- external mutation 已有 unknown-outcome classification，但 idempotency/retry/backoff/jitter 还不是共享 contract；
- shared control-plane rollout/canary、toil、platform cognitive-load、architecture fitness map 仍非一等化。

这些 finding 是“当前缺口/保证边界”，**不是 24 个必须各自新增模块的命令**。候选合并假设认为，真正重构时应优先寻找 5–7 个跨框架 primitive，而不是造一个 UVM Agent、一个 MAPE-K Agent、一个 STPA Agent 等框架动物园。

## 当前已有能力不能被推翻

v69 同时确认了一批当前结构是强项，不应因为学习新框架就推倒：

- 最小 bootstrap / cold-path maintenance；
- `OWNER_REGISTRY.json` 单一 owner membership authority；
- BUSINESS owner truth 与 Universal control plane 边界；
- active lease + resume_epoch + stale-writer fail-closed；
- observed-HEAD CAS；
- state plane / signal plane 分离；
- declared vs session-executable capability 分离；
- action-bound receipt / anti-replay；
- self-attested vs isolated/independent assurance 分离；
- deterministic maintenance controller + reopen；
- existing synthetic fault injection；
- authority-surface admission / anti-bloat；
- candidate learning evidence 不等于 production authority；
- bounded closure，不声称全局完美。

## 下一步的唯一合法动作

等待用户明确下令“调整 / 重构 / 开始实施”。收到后：

1. 重新读当时最新 `ENTRYPOINT.md + CURRENT_PROTOCOL.json + TASK_MANIFEST + controller state`；
2. 验证当前 writer/lease/head；
3. 从 v69 gap audit 和 candidate map 恢复，但重新评估候选，不把旧候选自动视为批准；
4. M7 前先建立 prepatch checkpoint；
5. 只做最小高收益设计，优先合并、派生、复用，避免新增平行 authority；
6. 再走 M8/M9/M10/M11 和 CI/reread。

## v68 Human Durable Revision 保留规则

用户正常可读 revision 仍是：`UC-YYYYMMDD-rN`，从 `updated_at + manifest_version` 派生，不存第二份权威。Git SHA、protocol、manifest version、controller revision 各自保留不同技术语义。

不建中央 revision registry；不建 daily counter；不遍历 Git history 算号；不为每个 checkpoint 打 Git tag；不增加启动 preload。

## v65 direct-main / PR-first regression anchor

当前模型不是 PR-first。

Universal material compliant writes continue to use active lease + observed-HEAD CAS + CI + authoritative reread. PR-first and branch protection are not default requirements under the current `SINGLE_ACTIVE_CHAT` threat model; unprotected `main` alone is not a HIGH defect.

实验分支 `continuity/pr-first-mutation-gate-v65` **没有 merge，也不是 authoritative implementation**；它仍是 unmerged / no-PR / non-authoritative experimental branch。

## 既有 OPEN 边界继续保留

v69 研究不会掩盖 v67/v68 既有 OPEN：

- formal controller-meta promotion；
- independent meta semantic / live held-out assurance；
- HARNESS_STATUS lower-authority monitor cache cleanup；
- historical issue #12 provenance；
- Novel/Video owner-local drift；
- Financial fresh-chat DUAL 3-output retest；
- private owner CI runner 未执行；
- tool-limited non-authoritative branch cleanup。

## Assurance ceiling

本 checkpoint 能证明的是：用户点名的主要架构/可靠性体系已经按公开 primary/original sources 建成冷路径知识库，并与当前 Universal authority 做了系统 gap crosswalk；它**不能**证明所有可能的工程体系、所有未来故障类、付费标准全文、或未来重构方案已经穷尽。

当前实施 gate：`BLOCKED_PENDING_EXPLICIT_USER_REFACTOR_COMMAND`。
