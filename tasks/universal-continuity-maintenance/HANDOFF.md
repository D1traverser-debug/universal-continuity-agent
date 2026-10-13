# 跨对话继承系统建设与维护｜Handoff

- task_id: `continuity:universal-continuity-maintenance`
- task_class: `SYSTEM_INFRA`
- owner: `UNIVERSAL_CONTINUITY_HARNESS`
- status: `ACTIVE`
- contract: `CONTINUITY_V3_7`
- current writer lease: `lease-8ecdf71e-46b3-4e7d-b2ea-61ee05c6d654`
- resume_epoch: `8`
- manifest_version: `95`
- human revision: `UC-20261013-r95` (derived presentation only)
- current controller: `architecture-reliability-benchmark-library-gap-audit-v69-2026-10-13`
- controller status: `BLOCKED revision 20 @ M7_IMPLEMENTATION_AND_SUPERSESSION`

## 用户当前明确边界

先把之前浅学的体系都学深，并加入当前主流 Agent runtime：OpenAI Agents API/SDK、Microsoft Agent Framework、Google ADK/Agents CLI、LangGraph/LangSmith。建立独立库、重新找出 Universal 的问题。**不调整、不重构，等待用户后续明确命令。**

## Pass 2 已完成

独立冷库：`research/system_architecture_library/`。

状态：`COLD_PATH_ONLY / NON_AUTHORITY / NO_REFACTOR_APPLIED`。正常 ChatGPT/业务执行不加载整库；版本敏感的框架事实在真正依赖前必须重新观察。

深化的旧框架包括 NASA SE/V模型、Evolutionary Architecture、Team Topologies、分布式系统/Raft边界/幂等重试、UVM、MAPE-K、Kubernetes Controller/Operator、OTP supervision、GitOps、Google SRE、AWS Operational Excellence、Twelve-Factor、DO-178C公开保证思想、IEC 61508公开安全生命周期、TLA+、N-version/common-mode、NASA FDIR、STPA、Chaos Engineering。

深化标准不再是“知道概念”，而是至少覆盖：目的、runtime/control model、state/authority、failure semantics、recovery/resume、verification/observability、lifecycle/change、限制/误用、Universal映射。

新增当前 Agent runtime 深研：
- OpenAI Agents API：managed harness / Agent / Environment / Session / events-items / hosted-self-hosted lifecycle；
- OpenAI Agents SDK：Runner、Session、RunState、HITL、handoff/nested agent、tool lifecycle、tracing/MCP，以及 lost-ACK/session-write reconciliation/exclusive resume；
- Microsoft Agent Framework current 1.x：Harness Agent、AgentSession、workflow/checkpoint、RequestPort/HITL、Sequential/Concurrent/Handoff/GroupChat/Magentic、OpenTelemetry/evaluation，以及 compaction/checkpoint replay/session lineage；
- Google ADK current 2.x + Agents CLI：graph/dynamic workflow、Session/Event/State/Memory/Artifacts、HITL/resume、plugins/callbacks、eval/deploy lifecycle，以及 failed-node rerun/redelivery/state races/provenance；
- LangGraph current 1.2.x + LangSmith：StateGraph/Pregel、Command、thread/checkpointer/Store、interrupt、durability modes、subgraphs、offline/online eval与deployment reconciliation，以及 interrupted-node replay/side-effect idempotency。

Pass-2 files：`15_prior_frameworks_deep_pass.md`、`16_agent_runtime_frameworks_2026.md`、`17_state_resume_side_effect_matrix.md`、`18_agent_runtime_failure_case_matrix.md`、`19_pass2_sources.md`、`20_pass2_current_universal_gap_audit.md`、`21_pass2_candidate_map.md`。原 01–14 保留为历史 Pass-1 证据。

## 新增诊断 G25–G30

- G25：没有统一 durable execution-lineage 模型；
- G26：HITL/approval exact-occurrence binding 不是共享 invariant；
- G27：context compaction 尚未作为执行状态变换治理；
- G28：各 runtime 的 session/workflow/memory/artifact/live-state 与 replay granularity 未统一声明；
- G29：协议/runtime/provider version compatibility 尚不是一等 assurance 维度；
- G30：live failure/user correction → reproducible eval → regression → promotion → online observation 的闭环碎片化。

核心共同结论：**checkpoint/persistence ≠ exactly-once external effect**。当前成熟框架仍需显式处理 replay、幂等、lost ACK、approval identity、session/workflow lineage 和外部结果 reconciliation。

## 第一次 Pass-2 checkpoint CI 的真实失败

CI `38382360943` / job `115245654728`：control-plane audit PASS、Agent architecture PASS，但 full pytest 为 `320 passed / 2 failed`。两项均是现有回归保护而不是研究内容错误：
1. BLOCKED controller 的 `investigation_resolution` 必须保持 null；
2. Handoff 必须保留 v65 精确回归锚点 `当前模型不是 PR-first`。

第二次 corrective CI `38382648214` / job `115246616835`：control-plane audit PASS、Agent architecture PASS，full pytest `321 passed / 1 failed`；剩余失败是 Handoff 还缺另一个 v65 精确锚点。该锚点已在本次纠正中恢复，不能用语义近似替代回归合同。

## 不应误读

- 不代表采用任何一个框架；
- 不代表要把 Universal 改成 Kubernetes/UVM/OTP；
- 不代表增加 supervisor Agent；
- 不代表当前需要 Raft；
- 不代表 DO-178C/IEC 61508 合规；
- 不代表已经读完每个项目每一行源码或未来版本；当前完成的是足以做架构比较的深度。

## M7 冻结

`21_pass2_candidate_map.md` 是 `CANDIDATE_ONLY`。以后用户下达重构命令时，必须先重读当时 current authority，再重新比较候选；今天的研究不能自动升级为设计决定。

## 本轮过程异常（不得隐藏）

Pass 2 前两个新研究文件曾通过 GitHub Contents API 直接提交，未显式走 `observed HEAD + expected_sha CAS`。在当前 single active writer 下未观察到冲突，且只改 NON_AUTHORITY research 文件，没有改 BUSINESS/production behavior，但它违反了 v65 后的合规写入流程。已停止；后续 checkpoint 从重新读取 current main 使用 expected-HEAD CAS。controller/manifest 保留此事实。

## 仍开放但不是本轮重构授权

G01–G30 都只是 diagnosis/candidate input；Novel #3、Video #4 owner-local drift 仍由其 owner 管；Financial fresh-chat DUAL 三输出实测仍 owner-scoped OPEN；private owner CI 未执行处不能称 PASS；independent semantic/live-outcome assurance 仍 OPEN；monitor #12 仍 `HISTORICAL_OPEN`；`__noop*` / 旧 maintenance branch 仍非权威 cleanup debt。

## v65 direct-main / PR-first 回归锚点

当前模型不是 PR-first。

active lease + observed-HEAD CAS + CI + authoritative reread

Universal 合规 material main write 继续以该链路为准；`main protected=false` 本身不是当前 `SINGLE_ACTIVE_CHAT` 威胁模型下的 HIGH defect；若 writer topology/权限威胁模型改变，必须重新评估。

## 下一步

**等待用户明确重构命令。** 在此之前只允许研究证据维护/事实纠正，不进入 M7 production implementation。
