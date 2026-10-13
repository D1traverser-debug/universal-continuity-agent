# 跨对话继承系统建设与维护｜Handoff

- task_id: `continuity:universal-continuity-maintenance`
- task_class: `SYSTEM_INFRA`
- owner: `UNIVERSAL_CONTINUITY_HARNESS`
- status: `ACTIVE`
- contract: `CONTINUITY_V3_7`
- current writer lease: `lease-350c8bbe-08cf-47e7-8116-0537f9c9ad67`
- resume_epoch: `9`
- manifest_version: `97`
- human revision: `UC-20261013-r97` (derived presentation only)
- current controller: `architecture-reliability-benchmark-library-gap-audit-v69-2026-10-13`
- controller status: `ACTIVE revision 30 @ M7_IMPLEMENTATION_AND_SUPERSESSION / PREPATCH CHECKPOINTED`
- prepatch checkpoint: `audits/ARCHITECTURE_APPLICABILITY_AND_MAIN_MUTATION_ROUTE_V69_PREPATCH_2026-10-13.json`

## 用户本轮授权边界

用户明确要求：

1. 对核心资料无法可靠获取的架构/规范研究进行删除或降级，不再装作“完整研究过”；
2. 用剩余已研究且可验证的知识重新判断哪些能用于 Universal。

这授权了**研究集清理 + 适用性筛选**，没有授权把全部候选直接改进生产架构。

## 研究集裁剪结果

- RTCA DO-178C 付费规范正文：从“已深研完整框架”计数中移除；只保留 FAA 公开软件保证资料能够直接支持的生命周期、追踪、独立性等思想。
- IEC 61508 付费规范系列：从“已深研完整框架”计数中移除；只保留 IEC 公开资料能直接支持的功能安全生命周期/变更/危险控制思想。
- UVM：保留。Accellera 有公开 User Guide、Class Reference、reference implementation，足够进行架构级比较。
- 其他 Pass-2 成熟体系与 OpenAI/Microsoft/Google/LangGraph 当前 Agent runtime 继续保留为公开/原始资料可验证的研究对象。

适用性筛选已经落在：`research/system_architecture_library/22_applicability_screen.md`。

核心结论不是建立“框架动物园”，而是把可用知识压缩成六类共享原语：

1. Derived System / Authority Model；
2. Runtime Semantics + Execution Lineage + Effect Contract；
3. Assurance / Coverage / Evaluation Trace；
4. Supervision / FDIR / Hazard Control；
5. Measured Reliability + Progressive Rollout / Resilience；
6. Formal Writer / Commit Protocol。

Raft、字面 UVM phase/class、Kubernetes 化所有有限任务、中央 MAPE-K Knowledge DB、永久 LLM supervisor、抹平 substrate 差异的 generic runtime abstraction、无证据的 SLO 数字等均明确不采用。

## 本轮发现的复发性系统缺陷

在创建 `22_applicability_screen.md` 时，再次发生了 material `main` 写入使用 GitHub Contents API、没有显式 `observed HEAD + expected-HEAD CAS` 的操作偏差；提交为 `2ec72f478ce225ec0a9619a3d70a516e89bb0da0`。没有观察到冲突，研究内容本身有效，但写入路径不合规。

这属于 `RECURRED_AFTER_FIX`，不能再用同层提醒修补。controller 已 reopen 到 M2A 完成抽象升级分析，然后重新走完 M2A–M6A，并在 M7 重新建立 prepatch checkpoint。

根因：详细 direct-main 规则存在于 `PROGRESS_OBSERVABILITY_POLICY.json` 和旧 Handoff，但关键禁止项没有进入每次 Continuity 都强制加载的 bootstrap authority，仍依赖操作者记忆。

选定的最小高层修复：

- 在 `ENTRYPOINT.md` 增加极短 material-main mutation invariant：有 HEAD-CAS primitive 时禁止 Contents API material write；必须 active lease + observed HEAD + expected-HEAD CAS；
- 详细语义继续由现有 `PROGRESS_OBSERVABILITY_POLICY.json` 唯一拥有，避免复制整套规则；
- 增加回归测试绑定该 bootstrap invariant；
- 不切换为 PR-first，不新增 mutation policy，不声称能物理阻止一个故意违规的授权外部 writer。

## 当前下一步

当前已到 M7 implementation admission。下一步仅实施上述最小 bootstrap + regression 修复，同时把 README/CATALOG/Pass-2 当前研究表述同步为“付费规范正文不计入完整深研、六原语适用性筛选完成”。之后跑 CI，若失败按 controller reopen；若通过再继续 M8–M11。

生产架构重构仍未授权。

## v65 direct-main / PR-first 回归锚点

当前模型不是 PR-first。

active lease + observed-HEAD CAS + CI + authoritative reread

实验分支 `continuity/pr-first-mutation-gate-v65` 没有 merge，也不是 authoritative implementation。

Universal 合规 material main write 继续以该链路为准；`main protected=false` 本身不是当前 `SINGLE_ACTIVE_CHAT` 威胁模型下的 HIGH defect；若 writer topology/权限威胁模型改变，必须重新评估。
