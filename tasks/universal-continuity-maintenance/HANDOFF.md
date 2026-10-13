# 跨对话继承系统建设与维护｜Handoff

- task_id: `continuity:universal-continuity-maintenance`
- task_class: `SYSTEM_INFRA`
- owner: `UNIVERSAL_CONTINUITY_HARNESS`
- status: `ACTIVE`
- contract: `CONTINUITY_V3_7`
- current writer lease: `lease-350c8bbe-08cf-47e7-8116-0537f9c9ad67`
- resume_epoch: `9`
- manifest_version: `98`
- human revision: `UC-20261013-r98` (derived presentation only)
- current controller: `architecture-reliability-benchmark-library-gap-audit-v69-2026-10-13`
- controller status: `ACTIVE revision 31 @ M8_MULTI_LAYER_VALIDATION`
- M7 implementation receipt: `audits/ARCHITECTURE_APPLICABILITY_AND_MAIN_MUTATION_ROUTE_V69_M7_IMPLEMENTATION_2026-10-13.json`

## 本轮用户授权与研究结果

用户授权的是：删除/降级核心资料无法可靠获取的研究项，并用保留下来的知识做适用性筛选；**不是**直接进行 Universal 生产架构重构。

当前有效研究集已经裁剪：

- RTCA DO-178C 付费规范正文、IEC 61508 付费规范系列已从“完整深研框架集合”移除；
- FAA/IEC 公开一手资料仅保留为 bounded evidence lens，不产生规范符合性/认证主张；
- UVM 保留，因为 Accellera 公开资料足以做架构级研究；
- 其余成熟体系和 2026 Agent runtime 继续保留。

`research/system_architecture_library/22_applicability_screen.md` 是当前适用性结果，压缩为六类共享原语：

1. Derived System / Authority Model；
2. Runtime Semantics + Execution Lineage + Effect Contract；
3. Assurance / Coverage / Evaluation Trace；
4. Supervision / FDIR / Hazard Control；
5. Measured Reliability + Progressive Rollout / Resilience；
6. Formal Writer / Commit Protocol。

结论：大部分保留知识**都能用上**，但主要作为共享 invariant、failure model、verification question 或少量共用原语，而不是每个框架变成一个模块。框架动物园、无条件 multi-agent、Raft、字面 UVM/Kubernetes/MAPE-K 移植等均不采用。

## 复发性 main 写入流程缺陷

适用性文件首次写入时再次发生 Contents API material-main write，提交 `2ec72f478ce225ec0a9619a3d70a516e89bb0da0`。没有观察到内容冲突，但属于 `RECURRED_AFTER_FIX`。

controller 已 reopen 到 M2A，重新完成 M2A–M6A，并在 M7 做了更高抽象层修复：

- `ENTRYPOINT.md` 现在在 mandatory bootstrap 中明确：有 branch-head CAS primitive 时，material `main` **MUST NOT use GitHub Contents API create/update/delete**；
- 必须 active lease + reread current HEAD + commit parent=current HEAD + `expected_sha=OBSERVED_CURRENT_MAIN_HEAD` + authoritative reread；
- 详细合同仍只由 `PROGRESS_OBSERVABILITY_POLICY.json` 持有；
- `tests/test_user_proposal_and_main_mutation_integrity.py` 新增 bootstrap 回归；
- 没有切成 PR-first，也没有新增 parallel mutation policy。

M7 material patch 使用的合规发布链：

`0ba190c05f1b14913d873695bb63c75598098d30 -> 6a8cc347c942d0589acbde0971b427f6e0893708`

`update_ref(expected_sha=0ba190c05f1b14913d873695bb63c75598098d30)` 成功，且已 reread `main` 验证 `6a8cc347...` 为 authority。

## 当前下一步

当前进入 M8：观察 `6a8cc347...` 及本 M7 checkpoint 的 CI，验证 bootstrap guard、回归测试、controller structural validity、研究库 catalog/README 一致性。若绿则继续 M9 propagation → M10 second-order review → M11 durable checkpoint；若失败则按 controller reopen。

生产架构重构仍未授权。

## v65 direct-main / PR-first 回归锚点

当前模型不是 PR-first。

active lease + observed-HEAD CAS + CI + authoritative reread

实验分支 `continuity/pr-first-mutation-gate-v65` 没有 merge，也不是 authoritative implementation。

Universal 合规 material main write 继续以该链路为准；`main protected=false` 本身不是当前 `SINGLE_ACTIVE_CHAT` 威胁模型下的 HIGH defect；若 writer topology/权限威胁模型改变，必须重新评估。
