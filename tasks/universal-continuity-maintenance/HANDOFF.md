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
- pause checkpoint: `tasks/universal-continuity-maintenance/PAUSE_CHECKPOINT_2026-10-13.md`

## 用户当前明确边界

先把之前浅学的体系都学深，并加入当前主流 Agent runtime：OpenAI Agents API/SDK、Microsoft Agent Framework、Google ADK/Agents CLI、LangGraph/LangSmith。建立独立库、重新找出 Universal 的问题。**不调整、不重构，等待用户后续明确命令。**

用户现在要求暂停当前窗口并把进度完整留存，准备之后从新窗口继续本任务。不得在暂停后自行进入 M7 implementation。

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

## 当前验证状态

- `38382360943 / 115245654728`：control-plane PASS、Agent architecture PASS、pytest `320 passed / 2 failed`。
- `38382648214 / 115246616835`：control-plane PASS、Agent architecture PASS、pytest `321 passed / 1 failed`。
- `38384381827 / 115252412136`：control-plane PASS、Agent architecture PASS、pytest `321 passed / 1 failed`。

当前唯一已知 pytest failure 是 Handoff 回归保护要求保留精确 v65 锚点 `没有 merge，也不是 authoritative implementation`。本 Handoff 已恢复该精确短语；新窗口恢复后应先检查本次/后续 CI 是否全绿，再决定是否需要仅做 checkpoint-correction。研究内容本身没有因此失效。

## M7 冻结

`21_pass2_candidate_map.md` 是 `CANDIDATE_ONLY`。以后用户下达重构命令时，必须先重读当时 current authority，再重新比较候选；今天的研究不能自动升级为设计决定。

## 本轮过程异常（不得隐藏）

Pass 2 前两个新研究文件曾通过 GitHub Contents API 直接提交，未显式走 `observed HEAD + expected_sha CAS`。随后创建本暂停 checkpoint 时又发生一次同类 operator-side Contents API 写入；另有一次误创建临时 probe 文件。它们没有改 BUSINESS 真值，但都是违反当前 direct-main 合规写入流程的操作偏差。后续修正必须使用 current main reread + active lease + expected-HEAD CAS，并把临时 probe 从 authority tree 清理掉；不得把这些异常从恢复上下文里省略。

## 仍开放但不是本轮重构授权

G01–G30 都只是 diagnosis/candidate input；Novel #3、Video #4 owner-local drift 仍由其 owner 管；Financial fresh-chat DUAL 三输出实测仍 owner-scoped OPEN；private owner CI 未执行处不能称 PASS；independent semantic/live-outcome assurance 仍 OPEN；monitor #12 仍 `HISTORICAL_OPEN`；`__noop*` / 旧 maintenance branch 仍非权威 cleanup debt。

## 新窗口恢复指令

本任务是 `SYSTEM_INFRA / EXPLICIT_ONLY`。按当前 Continuity 规则，裸 `继承` 不应自动把 SYSTEM_INFRA 当默认候选。为了保证新窗口准确恢复当前任务，请使用：

`继承，继续架构可靠性深研任务（continuity:universal-continuity-maintenance）`

新窗口必须先读 `ENTRYPOINT.md` + `CURRENT_PROTOCOL.json`，再读当前 `TASK_MANIFEST.json`、本 `HANDOFF.md` 和 `PAUSE_CHECKPOINT_2026-10-13.md`，先展示继承前进度，再合法 takeover（新 resume_epoch / lease），然后从 authoritative next_action 继续；不得凭聊天记忆重建任务。

## v65 direct-main / PR-first 回归锚点

当前模型不是 PR-first。

active lease + observed-HEAD CAS + CI + authoritative reread

实验分支 `continuity/pr-first-mutation-gate-v65` 没有 merge，也不是 authoritative implementation。

Universal 合规 material main write 继续以该链路为准；`main protected=false` 本身不是当前 `SINGLE_ACTIVE_CHAT` 威胁模型下的 HIGH defect；若 writer topology/权限威胁模型改变，必须重新评估。

## 下一步

暂停。新窗口恢复后第一件事是确认 current main、清理误创建临时 probe、检查/重跑 checkpoint CI，并保持 M7 blocked，除非用户随后明确下达重构命令。
