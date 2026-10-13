# 跨对话继承系统建设与维护｜Handoff

- task_id: `continuity:universal-continuity-maintenance`
- owner: `UNIVERSAL_CONTINUITY_HARNESS`
- status: `ACTIVE`
- manifest_version: `105`
- resume_epoch: `9`
- active lease: `lease-350c8bbe-08cf-47e7-8116-0537f9c9ad67`
- current controller: `main-mutation-mechanical-enforcement-v70-2026-10-13`
- controller status: `BLOCKED revision 12 / M7_IMPLEMENTATION_AND_SUPERSESSION`

## 当前设计任务

用户已把 clean-slate v4 的重点拉回到“先把真正想要的功能说清楚，再从功能推导架构”。当前已完成第一轮需求归一化，不再把上层能力、下层细节、异常案例和验收场景平铺成 40 个同级 REQ。

新需求树：
`research/clean_slate_v4/01_normalized_functional_requirements.md`

当前归一化结果：
- 9 个一级能力：目标驱动自主完成；自主知识获取/提炼/决策；任务规划调度与多 Agent 协作；系统结构理解与精准变更；持久状态/统一知识/跨会话连续性；运行监测/诊断/恢复；子系统与 Agent 生态治理；自我进化/主动维护/复杂度控制；质量验证/完成证明/用户交付。
- 10 个跨域约束：用户负担最小、不臃肿、不拆东墙补西墙、真值与来源可辨、自主有边界、故障隔离、兼容迁移、成本意识、可追溯、禁止虚假完成。
- 12 个代表性场景：普通“做XX”、当前资料研究、视频多 Agent、小说蒸馏原创、新增长期要求、聊天上限继承、未知工具结果、子系统重复故障、空闲维护、多任务竞争、新 Agent/工具引入、升级后继承旧任务。

下一步设计工作不是立即选框架，而是用真实业务场景继续反查这棵需求树：如果发现遗漏，先判断它是新的一级能力、已有能力的二级行为、跨域约束还是场景；只有无法归类的独立用户能力才新增一级能力。然后为稳定需求建立验收条件，再进入 clean-slate 架构推导。

## 既有功能覆盖结论

此前功能覆盖审计已经完成：共归纳 18 个当前总控功能域；G01–G30 已触及所有主要功能域，没有发现一个完整的大功能从未被审视过。

旧 `research/system_architecture_library/23_refactor_execution_plan.md` 不能原样作为实施清单。其九项显式补齐要求仍是后续架构设计必须吸收的风险输入：G27 context compaction、G29 runtime/protocol/provider compatibility、G30/G22 evaluation-promotion lifecycle、G24 writer-model transition trigger、G03 inter-owner interaction、G04 environment/substrate、G23 multiple-fault、G20/G21 coupling/toil、G14 fitness-function map。

详细证据：`audits/ARCHITECTURE_FUNCTION_COVERAGE_CROSSCHECK_V70_2026-10-13.md`。

## material-main 机械 enforcement 仍未关闭

上一轮 direct file mutation 复发产生 commit `b0dd89ffdc43876951cfb430d57ea6b0eb1e4792`；随后已通过 Git Data + `expected_sha` CAS 恢复 README，并保留审计，恢复 commit 为 `240029ddf6168d6a55a9af05357330a3a49cf167`。

该失败类为 `RECURRED_AFTER_FIX`。v69 的 ENTRYPOINT 文字 guard 已被事实证明不能机械阻止错误工具路径。prevention 仍为 OPEN/BLOCKED，必须由 tool/repository permission 等机械层解决；新增需求文档或更多提示语不构成关闭证据。

事故状态：`audits/MAIN_MUTATION_RECURRENCE_V70_2026-10-13.json`。

## v65 direct-main / PR-first 回归锚点

当前模型不是 PR-first。

active lease + observed-HEAD CAS + CI + authoritative reread

实验分支 `continuity/pr-first-mutation-gate-v65` 没有 merge，也不是 authoritative implementation。

这些锚点描述当前 authority 与历史实验边界；它们不表示 convention-only PR-first、提示语或回归文案可以替代已证明缺失的机械 enforcement。

## authorization

当前只授权 clean-slate v4 **需求设计**。生产架构重构尚未开始，也不得因需求文档完成而视为已授权。

## next_action

1. 用金融文章/A股/视频/小说/系统维护等真实工作流逐个反查需求树；
2. 合并重复场景，补真正缺失的功能；
3. 为一级/关键二级能力写可验收的行为标准；
4. 在需求稳定后，再从需求与风险反推 clean-slate 架构；
5. 任何生产实现前仍需处理或明确重新决策 material-main 机械 enforcement 阻塞。
