# Clean-Slate v4 — 需求最终压力反查

Status: `FINAL_REQUIREMENTS_VALIDATION / NO_NEW_TOP_LEVEL_GAP / FROZEN_V1_0`
Date: 2026-10-13

## 结论

对 v0.2 进行最终横向压力反查后，没有发现需要新增第 11 个一级能力的独立用户需求。发现的剩余问题均能归入 A–J 的二级条款或 X 跨域约束，已写入 `03_frozen_requirements_spec_v1_0.md`。

## 压力维度与落点

| 压力 | 规格落点 | 结果 |
|---|---|---|
| 多任务并发/资源竞争 | A05/A06, D02/D09, F07 | COVERED |
| 用户中途改目标/撤销要求 | A03-A05/A09, B04 | COVERED |
| 长任务跨多窗口 | F01-F10 | COVERED |
| 多 Agent 部分失败 | D06-D10, H01-H09 | COVERED |
| 工具结果未知/丢 ACK | H04-H05, G05 | COVERED |
| 数据源冲突/缺关键数据 | C03, G03-G06, X12 | COVERED |
| 模型/provider/runtime 临时或版本变化 | D03-D05/D12, F08, X07 | COVERED |
| 子系统升级时旧任务仍在执行 | E05/E09, F08, G02/G05 | COVERED |
| 父系统和子系统同时修改 | E02-E05, D09, X06/X11 | COVERED |
| 后台维护撞前台业务 | D13, I09-I10 | COVERED |
| 质量与成本冲突 | C05, D05, I08, X08 | COVERED |
| 权限/HITL/高影响操作 | B05, D03, X05/X14 | COVERED |
| 上下文压缩丢义务 | F10, X09 | COVERED |
| 多故障同时发生 | H07 | COVERED |
| 观察信号误当权威真值 | X04/X15 | COVERED |
| 写者拓扑变化导致旧一致性假设失效 | E10, D09 | COVERED |
| 学习候选污染生产 | I04-I06, D11, X13 | COVERED |
| 反复错误继续打补丁 | H03/H09, I02/I06-I08 | COVERED |
| 交付状态与真实文件不一致 | G08, J03 | COVERED |
| 角色/审核声明冒充真实执行 | D03, J02/J04/J06, X10 | COVERED |

## 对旧控制面风险的吸收

- G27 context compaction → F10；
- G29 runtime/protocol/provider compatibility → D12 + F08 + X07；
- G30/G22 evaluation/promotion lifecycle → I01-I06 + G09；
- G24 writer-model transition trigger → E10；
- G03 inter-owner interaction → D06-D10 + E02/E07；
- G04 environment/substrate → D03/D12 + X14；
- G23 multiple-fault → H07；
- G20/G21 coupling/toil → I08 + X08；
- G14 fitness/assurance map → J01/J05 + X09。

## 冻结判定

- `NO_NEW_TOP_LEVEL_CAPABILITY_GAP`
- `NO_UNRESOLVED_LAYERING_CONFLICT`
- `KEY_BEHAVIORS_ACCEPTANCE_SPECIFIED`
- `REAL_WORKFLOW_AND_CROSS_CUTTING_STRESS_VALIDATED`
- `REQUIREMENTS_FROZEN_V1_0`

后续架构设计如果发现实现困难，不得直接修改需求；必须把困难记录为架构/实现约束。只有用户显式需求变化或新的真实证据证明规格本身有缺陷，才允许创建新需求版本。