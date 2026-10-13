# 跨对话继承系统建设与维护｜Handoff

- task_id: `continuity:universal-continuity-maintenance`
- owner: `UNIVERSAL_CONTINUITY_HARNESS`
- status: `ACTIVE`
- manifest_version: `106`
- resume_epoch: `9`
- active lease: `lease-350c8bbe-08cf-47e7-8116-0537f9c9ad67`
- current controller: `main-mutation-mechanical-enforcement-v70-2026-10-13`
- controller status: `BLOCKED revision 12 / M7_IMPLEMENTATION_AND_SUPERSESSION`

## 当前设计任务

用户要求先从真实功能反推 clean-slate v4，而不是从架构框架倒推需求。本轮已完成真实业务反查，并修订需求树。

权威设计输入：
- `research/clean_slate_v4/01_normalized_functional_requirements.md` — v0.2 归一化功能需求；
- `research/clean_slate_v4/02_real_workflow_reverse_validation.md` — 财经写作、A 股、视频、小说、总控维护五类真实工作流反推审计。

## 真实工作流反查后的结构变化

v0.1 的 9 个一级能力不再机械保留。本轮发现：

1. 用户意图、用户要求和作用域生命周期此前分散在目标理解、变更定位、调度和继承中；真实错误已证明它应该成为独立一级能力。
2. “任务规划与多 Agent 协作”不足以表达真实执行：视频/写作需要确认 Agent、工具、模型、provider、connector、Runtime、额度和产物依赖的当前可执行性，因此扩展为执行编排与资源协调。
3. “持久状态 + 统一知识”混入了生命周期完全不同的对象；现拆为“持久任务状态与连续性”和“数据/产物/知识治理”。
4. 原“系统结构理解与精准变更”和“子系统/Agent 生态治理”高度重叠，合并为“系统/子系统拓扑与变更治理”。

v0.2 因此得到 10 个一级能力：
A 用户意图/要求/作用域治理；B 自主任务完成；C 知识/证据获取、提炼与最适配决策；D 执行编排与资源协调；E 系统/子系统拓扑与变更治理；F 持久任务状态与跨会话连续性；G 数据/产物/知识治理；H 运行监测/故障诊断/可靠恢复；I 自我进化/主动维护/复杂度控制；J 质量验证/完成证明/用户交付。

同时新增三条通用约束：关键高影响约束优先机械化；关键前置数据/能力/授权/证据缺失时不得静默降级；探索/候选状态不得未经验证污染权威生产状态。

## 五类真实工作流的主要新发现

- 财经写作：NEW_TASK、CONTINUE、SYSTEM_AUDIT 必须区分；规则/Agent 声明不能替代当前 capability；当前交付 Word 必须做真实产物验真；生产和审核需要适当独立证据。
- A 股：需要交易日/时间语义、冻结快照、数据血缘、来源冲突 reconciliation、完整性门禁；盘后真实结果只能按证据逐步晋升为方法改进。
- 视频：需要模型/工具/额度/质量路由、工作流 producer→artifact→consumer 可达性、批准资产身份/版本/连续性、探索轨/生产轨隔离和真实 reviewer receipt。
- 小说：需要“整本”为完成单位、coverage/hash/next-location 可恢复游标、单书结论适用范围/anti-overfit、单书证据到跨作品方法论的分层晋升。
- 总控维护：D/G 合并合理；文字规则存在不等于关键 invariant 已机械封堵；失败修复必须提升到正确抽象层并有晋升/退役闭环。

## 下一步设计工作

不立即选框架。下一步为 A–J 的关键二级能力建立可验收行为标准：触发条件、必须行为、状态变化、异常处理、完成证据、真实回归场景。验收标准稳定以后，再从需求 + 风险反推 clean-slate 架构。

## 既有功能覆盖结论

此前功能覆盖审计已经完成：G01–G30 已触及所有主要当前控制面功能域；旧 `research/system_architecture_library/23_refactor_execution_plan.md` 仍不能原样作为新架构实施清单。旧九项风险输入仍需在未来架构推导时逐项映射，而不是丢弃。

## material-main 机械 enforcement 仍未关闭

上一轮 direct file mutation 复发产生 commit `b0dd89ffdc43876951cfb430d57ea6b0eb1e4792`，恢复 commit 为 `240029ddf6168d6a55a9af05357330a3a49cf167`。该失败类仍为 `RECURRED_AFTER_FIX`，prevention 仍 OPEN/BLOCKED。

本轮反查把“关键约束优先机械化”提升为通用需求；这不等于当前 GitHub 工具/仓库层已经完成机械封堵。

本轮还发生了数次对不存在分支的 Contents API 调用，均被 GitHub 404 拒绝、未产生 commit 或文件。这没有造成 main mutation，但进一步说明危险原语仍然可调用；不能把提示语视为物理 enforcement。

事故状态仍由 `audits/MAIN_MUTATION_RECURRENCE_V70_2026-10-13.json` 约束。

## v65 direct-main / PR-first 回归锚点

当前模型不是 PR-first。

active lease + observed-HEAD CAS + CI + authoritative reread

实验分支 `continuity/pr-first-mutation-gate-v65` 没有 merge，也不是 authoritative implementation。

这些锚点只描述当前 authority 与历史实验边界；convention-only PR-first、提示语或回归文案不能替代已经证明缺失的机械 enforcement。

## authorization

当前只授权 clean-slate v4 **需求设计**。生产架构重构尚未开始。

## next_action

1. 为 A–J 的关键二级能力建立可验收行为标准；
2. 用五类真实业务 + 并发/故障/升级/要求变更等横向场景形成验收矩阵；
3. 需求与验收稳定后，再从它们反推 clean-slate 架构；
4. 任何生产实现前仍需处理或明确重新决策 material-main 机械 enforcement 阻塞。