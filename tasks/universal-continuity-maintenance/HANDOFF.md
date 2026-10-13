# 跨对话继承系统建设与维护｜Handoff

- task_id: `continuity:universal-continuity-maintenance`
- task_class: `SYSTEM_INFRA`
- owner: `UNIVERSAL_CONTINUITY_HARNESS`
- status: `ACTIVE`
- contract: `CONTINUITY_V3_7`
- current writer lease: `lease-8ecdf71e-46b3-4e7d-b2ea-61ee05c6d654`
- resume_epoch: `8`
- manifest_version: `94`
- human revision: `UC-20261013-r94` (derived presentation only)
- current controller: `architecture-reliability-benchmark-library-gap-audit-v69-2026-10-13`
- controller status: `BLOCKED revision 19 @ M7_IMPLEMENTATION_AND_SUPERSESSION`

## 用户当前明确边界

先把之前浅学的体系都学深，并加入当前主流 Agent runtime：OpenAI Agents API/SDK、Microsoft Agent Framework、Google ADK/Agents CLI、LangGraph/LangSmith。建立独立库、重新找出 Universal 的问题。**不调整、不重构，等待用户后续明确命令。**

## Pass 2 已完成

独立冷库仍为：`research/system_architecture_library/`。

它现在明确是：
- `COLD_PATH_ONLY`
- `NON_AUTHORITY`
- `NO_REFACTOR_APPLIED`
- 正常 ChatGPT/业务执行不读取整库
- 版本敏感的框架事实在真正依赖前必须重新观察

### 深化的旧框架

NASA SE/V模型、Evolutionary Architecture、Team Topologies、分布式系统/Raft边界/幂等重试、UVM、MAPE-K、Kubernetes Controller/Operator、OTP supervision、GitOps、Google SRE、AWS Operational Excellence、Twelve-Factor环境一致性、DO-178C公开保证思想、IEC 61508公开安全生命周期、TLA+、N-version/common-mode、NASA FDIR、STPA、Chaos Engineering。

深化标准不再是“知道概念”，而是至少覆盖：目的、runtime/control model、state/authority、failure semantics、recovery/resume、verification/observability、lifecycle/change、限制/误用、Universal映射。

### 新增当前 Agent runtime 深研

- OpenAI Agents API：managed harness / Agent / Environment / Session / events-items / hosted-self-hosted environment lifecycle。
- OpenAI Agents SDK：Runner、Session、RunState、HITL、nested agent/handoff、tool lifecycle、tracing/MCP；特别关注 session append lost-ACK、exclusive resume、pending-write reconciliation。
- Microsoft Agent Framework current 1.x：Harness Agent、AgentSession、workflow/checkpoint、RequestPort/HITL、Sequential/Concurrent/Handoff/GroupChat/Magentic、OpenTelemetry、evaluation；特别关注 compaction、checkpoint replay、approval/session lineage。
- Google ADK current 2.x + Agents CLI：graph/dynamic workflow、Session/Event/State/Memory/Artifacts、HITL/resume、plugins/callbacks、eval/deploy lifecycle；特别关注 failed-node rerun、redelivery duplicate effects、state races/provenance。
- LangGraph current 1.2.x + LangSmith：StateGraph/Pregel、Command、checkpointer/thread, Store、interrupt、durability modes、subgraph namespace、offline/online eval和desired/current deployment reconciliation；特别关注 interrupted-node replay和side-effect idempotency。

## Pass-2 durable files

- `15_prior_frameworks_deep_pass.md`
- `16_agent_runtime_frameworks_2026.md`
- `17_state_resume_side_effect_matrix.md`
- `18_agent_runtime_failure_case_matrix.md`
- `19_pass2_sources.md`
- `20_pass2_current_universal_gap_audit.md`
- `21_pass2_candidate_map.md`

`CATALOG.json` 是当前研究目录索引；原 01–14 文件保留为 Pass-1 历史证据。

## Pass-2 新增诊断

在原 G01–G24 基础上增加：

- `G25`：不同 runtime adapter 间没有统一 durable execution-lineage 模型；
- `G26`：HITL/approval 的 exact-occurrence binding 不是共享控制面 invariant；
- `G27`：context compaction 尚未作为执行状态变换治理；
- `G28`：各 substrate 的 session/workflow/memory/artifact/live-state 和 replay granularity 未统一声明；
- `G29`：MCP/A2A/provider/runtime version compatibility 尚不是一等 assurance 维度；
- `G30`：live failure/user correction → reproducible eval → regression → promotion → online observation 的闭环仍碎片化。

最重要的新共同结论：**checkpoint/persistence ≠ exactly-once external effect**。成熟框架都仍需要应用层处理 replay、幂等、lost ACK、approval identity、session/workflow lineage 和外部结果 reconciliation。

## 不应误读的结论

- 不代表要采用任何一个框架。
- 不代表要把 Universal 改成 Kubernetes/UVM/OTP。
- 不代表要增加 supervisor Agent。
- 不代表 Raft/共识现在有必要。
- 不代表 DO-178C/IEC 61508 合规或认证。
- 不代表已经读完这些项目的每一行源码或未来版本；当前完成的是足以做架构比较的深度。

## M7 冻结

`21_pass2_candidate_map.md` 仍是 `CANDIDATE_ONLY`。以后用户下达重构命令时，必须先重读当时 current authority，再重新比较候选；今天的研究不能自动升级为设计决定。

候选方向目前只保留为：derived system model、assurance/coverage trace、reliability objectives、environment/runtime semantics、execution lineage/effect contract、supervision/FDIR、hazard/UCA、formal writer model、independence/eval promotion、progressive rollout/chaos contract。

## 本轮过程异常（不得隐藏）

Pass 2 前两个新研究文件曾通过 GitHub Contents API 直接提交，未显式走 `observed HEAD + expected_sha CAS`。在当前 single active writer 下未观察到冲突，且只改 NON_AUTHORITY research 文件，没有改 BUSINESS/production behavior，但它违反了 v65 后的合规写入流程。已停止该做法；后续 checkpoint batch 从重新读取的 current main 使用 expected-HEAD CAS 发布。这个事实已写入 controller/manifest，不当作没发生。

## 仍然开放但不是本轮重构授权

- G01–G30 都只是 diagnosis/candidate input；
- Novel #3、Video #4 owner-local drift 仍由其 owner 管；
- Financial fresh-chat DUAL 三输出实测仍 owner-scoped OPEN；
- private owner CI 未执行处不能称 PASS；
- independent semantic/live-outcome assurance 仍 OPEN；
- monitor #12 仍 `HISTORICAL_OPEN`，不是当前 monitor 重建授权；
- `__noop*` / 旧 maintenance branch 仍非权威 cleanup debt。

## 下一步

**等待用户明确重构命令。** 在此之前只允许研究证据维护/事实纠正，不进入 M7 production implementation。
