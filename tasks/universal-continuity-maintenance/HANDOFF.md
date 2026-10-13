# 跨对话继承系统建设与维护｜Handoff

- task_id: `continuity:universal-continuity-maintenance`
- task_class: `SYSTEM_INFRA`
- owner: `UNIVERSAL_CONTINUITY_HARNESS`
- status: `ACTIVE`
- contract: `CONTINUITY_V3_7`
- current writer lease: `lease-350c8bbe-08cf-47e7-8116-0537f9c9ad67`
- resume_epoch: `9`
- manifest_version: `100`
- human revision: `UC-20261013-r100` (derived presentation only)
- current controller: `architecture-reliability-benchmark-library-gap-audit-v69-2026-10-13`
- controller status: `ACTIVE revision 34 @ M9_CROSS_SUBSYSTEM_INHERITANCE_AND_PROPAGATION`
- M7/M8 correction receipt: `audits/ARCHITECTURE_APPLICABILITY_V69_M7_CORRECTION_AND_M8_VALIDATION_2026-10-13.json`

## 用户授权与当前研究结论

用户本轮授权：删除/降级核心资料无法可靠获取的研究项，并用保留知识判断哪些可用于 Universal；**没有授权生产架构重构**。

研究集已裁剪：
- RTCA DO-178C、IEC 61508 的付费规范正文不再计入“完整深研框架”；
- FAA/IEC 公开资料只作为 bounded evidence lens；
- UVM 保留，因为 Accellera 公开资料足够做架构级研究；
- 其余成熟体系与 OpenAI/Microsoft/Google/LangGraph 当前 Agent runtime 保留。

当前适用性视图：`research/system_architecture_library/22_applicability_screen.md`。

可用知识压缩为六类共享原语，而不是一个框架一个模块：
1. Derived System / Authority Model；
2. Runtime Semantics + Execution Lineage + Effect Contract；
3. Assurance / Coverage / Evaluation Trace；
4. Supervision / FDIR / Hazard Control；
5. Measured Reliability + Progressive Rollout / Resilience；
6. Formal Writer / Commit Protocol。

明确不采用：当前单 writer 模型下的 Raft/共识、字面 UVM phase/class、把有限用户任务 Kubernetes 化、中央 MAPE-K Knowledge DB、永久 LLM supervisor、抹平 substrate replay/state 差异的 generic runtime abstraction、无必要的 blanket multi-agent、认证流程模仿、无观测分母的虚构 SLO。

## direct-main 写入复发修复

创建 `22_applicability_screen.md` 时发生一次 material Contents-API main write，提交 `2ec72f...`，属于 `RECURRED_AFTER_FIX`。controller 已提升修复层级：mandatory `ENTRYPOINT.md` 现在明确 material `main` 在 HEAD-CAS 可用时不得使用 Contents API，必须 active lease + reread HEAD + commit-on-HEAD + expected_sha CAS + reread authority；详细合同仍唯一归 `PROGRESS_OBSERVABILITY_POLICY.json` 所有，不切换 PR-first。

首版 guard 因 ENTRYPOINT headroom 回归被 M8 正确打回 M7；压缩过程逐步恢复历史精确回归锚点。最终 material commit：`8ac05af3b009c7bfc323286ba6e1c85faf72cd54`。

最终 CI `38398927554 / 115301225424`：
- risk-tiered control-plane audit PASS；
- Agent architecture PASS；
- full pytest `323 passed`。

因此 corrected M7 与 M8 已完成，当前进入 M9 propagation review。

## 当前下一步

验证共享 bootstrap invariant 是否通过 mandatory ENTRYPOINT 自动覆盖未来 Universal maintenance writer，而无需复制到 BUSINESS owner；确认研究库继续保持 cold-path/non-authority、没有向业务 owner 传播框架模块。然后执行 M10 second-order review 与 M11 durable checkpoint。

生产架构重构仍未授权；六原语是筛选后的设计输入，不是已实施 production roadmap。

## v65 direct-main / PR-first 回归锚点

当前模型不是 PR-first。

active lease + observed-HEAD CAS + CI + authoritative reread

实验分支 `continuity/pr-first-mutation-gate-v65` 没有 merge，也不是 authoritative implementation。

Universal 合规 material main write 继续以该链路为准；`main protected=false` 本身不是当前 `SINGLE_ACTIVE_CHAT` 威胁模型下的 HIGH defect；若 writer topology/权限威胁模型改变，必须重新评估。
