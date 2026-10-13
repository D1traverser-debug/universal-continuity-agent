# 跨对话继承系统建设与维护｜Handoff

- task_id: `continuity:universal-continuity-maintenance`
- task_class: `SYSTEM_INFRA`
- owner: `UNIVERSAL_CONTINUITY_HARNESS`
- status: `ACTIVE`
- contract: `CONTINUITY_V3_7`
- current writer lease: `lease-350c8bbe-08cf-47e7-8116-0537f9c9ad67`
- resume_epoch: `9`
- manifest_version: `99`
- human revision: `UC-20261013-r99` (derived presentation only)
- current controller: `architecture-reliability-benchmark-library-gap-audit-v69-2026-10-13`
- controller status: `ACTIVE revision 32 @ M7_IMPLEMENTATION_AND_SUPERSESSION`
- M8 failure receipt: `audits/ARCHITECTURE_APPLICABILITY_V69_M8_HEADROOM_FAILURE_2026-10-13.json`

## 研究裁剪与适用性结论

用户授权：删除/降级核心资料无法可靠获取的研究项，并用保留下来的知识做适用性筛选；未授权 Universal 生产架构重构。

当前有效研究集：
- RTCA DO-178C 与 IEC 61508 的付费规范正文已从“完整深研框架集合”移除；FAA/IEC 公开一手资料只作为 bounded evidence lens；
- UVM 保留，Accellera 公开资料足够做架构级比较；
- 其余成熟体系与当前 OpenAI/Microsoft/Google/LangGraph Agent runtime 保留。

当前适用性权威研究视图：`research/system_architecture_library/22_applicability_screen.md`。

六类共享原语：
1. Derived System / Authority Model；
2. Runtime Semantics + Execution Lineage + Effect Contract；
3. Assurance / Coverage / Evaluation Trace；
4. Supervision / FDIR / Hazard Control；
5. Measured Reliability + Progressive Rollout / Resilience；
6. Formal Writer / Commit Protocol。

结论：大部分保留知识都能用上，但主要作为共享 invariant、failure model、verification question 或少量共用原语，不按框架逐个建模块。Raft、字面 UVM/Kubernetes/MAPE-K 移植、永久 LLM supervisor、抹平 runtime 差异的 generic abstraction、无证据 SLO 等明确不采用。

## main 写入流程复发与修复状态

创建 `22_applicability_screen.md` 时发生 Contents API material-main write `2ec72f...`，属于 `RECURRED_AFTER_FIX`。controller 已升级根因并在 mandatory `ENTRYPOINT.md` 增加 HEAD-CAS bootstrap guard，同时加回归测试；详细合同继续由 `PROGRESS_OBSERVABILITY_POLICY.json` 唯一持有，不切换 PR-first。

第一版 M7 material patch `6a8cc347...` 使用合规 `active lease + observed HEAD + expected_sha CAS + reread` 发布，逻辑方向没有被 M8 否定。

## M8 唯一失败与当前 reopen

CI `38397187483 / 115295288959`：
- control-plane audit PASS；
- Agent architecture PASS；
- pytest `322 passed / 1 failed`；
- 唯一失败：`ENTRYPOINT.md` 8142 bytes，只剩 50 bytes headroom，而合同要求至少 512 bytes（因此 ENTRYPOINT 必须 <=7680 bytes）。

controller 已按失败证据从 M8 reopen 到 M7。**不得放宽 512-byte headroom**。当前动作只允许把同一 bootstrap invariant 等价压缩，并同步回归测试；研究裁剪与六原语适用性结论不受该文本预算失败影响。

## 下一步

压缩 `ENTRYPOINT.md` 到 <=7680 bytes 并保留 main mutation guard 的核心语义；通过 Git Data tree/commit + `update_ref(expected_sha=current observed main)` 发布；重新完成 M7，进入 M8 重跑 CI。若绿，再走 M9 → M10 → M11。

生产架构重构仍未授权。

## v65 direct-main / PR-first 回归锚点

当前模型不是 PR-first。

active lease + observed-HEAD CAS + CI + authoritative reread

实验分支 `continuity/pr-first-mutation-gate-v65` 没有 merge，也不是 authoritative implementation。

Universal 合规 material main write 继续以该链路为准；`main protected=false` 本身不是当前 `SINGLE_ACTIVE_CHAT` 威胁模型下的 HIGH defect；若 writer topology/权限威胁模型改变，必须重新评估。
