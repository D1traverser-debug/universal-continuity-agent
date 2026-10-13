# 跨对话继承系统建设与维护｜Handoff

- task_id: `continuity:universal-continuity-maintenance`
- owner: `UNIVERSAL_CONTINUITY_HARNESS`
- status: `ACTIVE`
- manifest_version: `107`
- resume_epoch: `9`
- active lease: `lease-350c8bbe-08cf-47e7-8116-0537f9c9ad67`
- requirements baseline: `FROZEN_V1_0`
- current controller: `main-mutation-mechanical-enforcement-v70-2026-10-13`
- controller status: `BLOCKED revision 12 / M7_IMPLEMENTATION_AND_SUPERSESSION`

## 当前权威需求

clean-slate v4 需求规格已完成并冻结：

- `research/clean_slate_v4/03_frozen_requirements_spec_v1_0.md` — 权威需求规格；
- `research/clean_slate_v4/04_final_requirements_stress_validation.md` — 最终横向压力反查；
- `01_normalized_functional_requirements.md` 与 `02_real_workflow_reverse_validation.md` 保留为需求形成历史，不再是当前权威规格。

v1.0 包含：
- 10 个一级能力 A–J；
- 15 个跨域约束 X01–X15；
- 20 个冻结验收场景；
- 每个关键二级要求的触发、必须行为、必留状态/证据、失败语义。

## 冻结规则

后续架构设计不能为了实现方便自行改需求。只有以下情况才允许建立新需求版本：
1. 用户明确新增/删除/修改需求；
2. 真实业务或故障证据证明 v1.0 有遗漏、矛盾或不可验收条款；
3. 外部能力边界变化导致原需求客观不可实现，需要用户重新决策。

任何变化必须版本化，不能静默覆盖 v1.0。

## 最终需求压力反查结果

没有发现需要新增第 11 个一级能力的独立用户需求。并发、要求中途变化、跨窗口、多 Agent 部分失败、未知副作用、数据冲突、provider/runtime 变化、旧任务迁移、父子系统变更、后台维护竞争、成本/质量、权限/HITL、上下文压缩、多故障、观察信号与权威真值、writer topology 变化、候选知识晋升和真实产物交付等问题均有明确落点。

旧控制面风险也已映射：G27→F10；G29→D12/F08/X07；G30/G22→I01-I06/G09；G24→E10；G03→D06-D10/E02/E07；G04→D03/D12/X14；G23→H07；G20/G21→I08/X08；G14→J01/J05/X09。

## 当前授权边界

用户本轮要求的是“需求规格做好并且不再修改后告知”。该目标现在已经完成。当前**没有**自动获得生产架构重构授权，也没有自动进入实现。

如用户下一步明确要求设计新架构，应从 frozen v1.0 A–J/X01–X15 推导架构，并把实现困难记录为设计约束，而不是反改需求。

## material-main 机械 enforcement 仍未关闭

历史 direct-main mutation 失败类仍是 `RECURRED_AFTER_FIX`，prevention 仍 OPEN/BLOCKED。需求规格中的 X11 已明确“高影响不变量优先机械化”，但文档本身不构成机械封堵。

本轮需求冻结过程中也出现了数次对不存在分支的 Contents API 调用，均被 GitHub 404 或安全检查拒绝，没有产生 main commit/文件；这进一步说明危险原语仍可调用，不能把提示语当作 enforcement。

当前批准写模型仍是：active lease + observed-HEAD CAS + CI + authoritative reread。

## v65 direct-main / PR-first 回归锚点

当前模型不是 PR-first。

当前 `SINGLE_ACTIVE_CHAT` writer model 的批准发布路径仍是 active lease + observed-HEAD CAS + CI + authoritative reread。PR-first 实验没有成为 authoritative implementation；这不影响需求 v1.0 冻结状态。

## next_action

等待用户明确指令。若用户要求继续新架构设计，则：
1. 只以 frozen requirements v1.0 为需求 authority；
2. 重新观察版本敏感 runtime/tool/provider 能力；
3. 从需求 + 风险推导最小架构；
4. 不允许为了架构便利篡改需求；
5. 生产 refactor 仍需明确授权。