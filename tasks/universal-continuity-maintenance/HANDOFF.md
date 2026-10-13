# 跨对话继承系统建设与维护｜Handoff

- task_id: `continuity:universal-continuity-maintenance`
- task_class: `SYSTEM_INFRA`
- owner: `UNIVERSAL_CONTINUITY_HARNESS`
- status: `ACTIVE`
- contract: `CONTINUITY_V3_7`
- current writer lease: `lease-350c8bbe-08cf-47e7-8116-0537f9c9ad67`
- resume_epoch: `9`
- manifest_version: `101`
- human revision: `UC-20261013-r101` (derived presentation only)
- completed controller: `architecture-reliability-benchmark-library-gap-audit-v69-2026-10-13`
- controller status: `COMPLETE revision 37 / FINAL M11 PASS`
- final review: `audits/ARCHITECTURE_APPLICABILITY_V69_FINAL_2026-10-13.json`

## 本轮已完成

用户要求的两件事已经完成：

1. **删出/降级无法可靠研究的内容。** RTCA DO-178C 与 IEC 61508 的付费规范正文不再计入“完整深研框架”；FAA/IEC 公开资料只作为 bounded evidence lens。历史研究痕迹保留用于 provenance，但不再参与当前“完整研究过”的计数。UVM 不删除，因为 Accellera 有足够公开资料做架构级研究。
2. **判断已研究知识哪些能用。** 当前适用性权威研究视图为 `research/system_architecture_library/22_applicability_screen.md`；结论是几乎所有保留知识都有作用，但多数应该成为共享 invariant、failure model、verification question 或少量共用原语，而不是逐个框架落成模块。

六类共享原语：

1. Derived System / Authority Model；
2. Runtime Semantics + Execution Lineage + Effect Contract；
3. Assurance / Coverage / Evaluation Trace；
4. Supervision / FDIR / Hazard Control；
5. Measured Reliability + Progressive Rollout / Resilience；
6. Formal Writer / Commit Protocol。

明确不采用：当前单 writer 模型下的 Raft/共识、字面 UVM phase/class、把有限用户任务 Kubernetes 化、中央 MAPE-K Knowledge DB、永久 LLM supervisor、抹平 substrate replay/state 差异的 generic runtime abstraction、无必要 blanket multi-agent、认证流程模仿、无观测分母的虚构 SLO。

## 本轮附带闭环的复发性可靠性问题

创建 applicability screen 时再次出现 material `main` 使用 GitHub Contents API、没有 expected-HEAD CAS 的操作偏差。该失败类属于 `RECURRED_AFTER_FIX`，已按维护规则上升到 mandatory bootstrap 层处理，而不是再加一条冷路径提醒。

现在 `ENTRYPOINT.md` 明确：HEAD-CAS 可用时，Universal material `main` 不得使用 Contents API；必须 active lease + reread HEAD + commit-on-HEAD + expected_sha CAS + authoritative reread。详细合同仍唯一归 `PROGRESS_OBSERVABILITY_POLICY.json`，没有切换为 PR-first。

首版 guard 因 ENTRYPOINT reserved-headroom 被 M8 正确打回；压缩期间保留了所有历史回归锚点，最终 material commit `8ac05af3b009c7bfc323286ba6e1c85faf72cd54` 全绿：control-plane PASS、Agent architecture PASS、pytest `323 passed`。随后 M7/M8 durable checkpoint `a1354776960735f3d1f26074b4f5527202e50fc3` 也通过 continuity-ci。

M9 propagation：guard 作为 Universal kernel 通过 mandatory ENTRYPOINT 自动继承，不复制到四个 BUSINESS owner；针对 owner 的 shadow/override 扫描未发现冲突副本；研究库继续 cold-path/non-authority。

M10 second-order review：没有新增 root authority、PR-first、永久 Agent、owner 规则副本或 framework zoo；没有生产架构重构。剩余 assurance 边界包括：不能物理阻止故意违规的授权外部 writer；本地 CI 不证明 private owner 的实时状态或业务结果；付费规范不做认证/规范符合性主张。

M11 durable learning 已落到 ENTRYPOINT、回归测试、research README/CATALOG/22、controller、manifest、handoff 与 final audit。

## 当前真实 next_action

本轮“研究集裁剪 + 适用性筛选”已经闭环。**生产架构仍未重构。** 下一步只有在用户另行明确下达“开始架构调整/重构”的命令后，才重新读取当时 current authority、重新观察版本敏感 Agent runtime 事实，并从六类原语里选择最小高收益组合实施；不得自动把今天的候选升级为 production design。

## v65 direct-main / PR-first 回归锚点

当前模型不是 PR-first。

active lease + observed-HEAD CAS + CI + authoritative reread

实验分支 `continuity/pr-first-mutation-gate-v65` 没有 merge，也不是 authoritative implementation。

Universal 合规 material main write 继续以该链路为准；`main protected=false` 本身不是当前 `SINGLE_ACTIVE_CHAT` 威胁模型下的 HIGH defect；若 writer topology/权限威胁模型改变，必须重新评估。
