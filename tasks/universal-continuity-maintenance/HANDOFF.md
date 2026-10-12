# 跨对话继承系统建设与维护｜Handoff

- task_id: `continuity:universal-continuity-maintenance`
- task_class: `SYSTEM_INFRA`
- owner: `UNIVERSAL_CONTINUITY_HARNESS`
- status: `ACTIVE`
- contract: `CONTINUITY_V3_7`
- current_stage: `SYSTEM_MAINTENANCE_ACTIVE`
- current writer lease: `lease-d5136fdf-0661-4cd9-aeba-74db63c4dc3f`
- resume_epoch: `7`
- manifest_version: `61`
- system-maintenance policy: `1.8`
- meta-maintenance: `1.3`
- latest formal meta-run: `audits/META_MAINTENANCE_FAILURE_CLASS_ESCALATION_V61_2026-10-12.json`
- controller state: `tasks/universal-continuity-maintenance/MAINTENANCE_CONTROLLER_STATE.json`
- controller run: `maintenance-execution-sop-v62-selfhost-2026-10-12`
- controller state status: `COMPLETE` revision `21`
- controller continuation audit: `audits/MAINTENANCE_CONTROLLER_SELF_HOSTED_CONTINUATION_V62_2026-10-12.md`
- latest controller validation: GitHub Actions `38271641398` / job `114887058655` / `295 passed`

## 当前权威状态

1. 当前协议仍为 v3.7。系统性维护的 canonical semantics 仍由 `SYSTEM_MAINTENANCE_POLICY.json` 唯一拥有；没有新增第二套 root policy。
2. 本轮确认的根因不是“历史 recall 不够”，而是**进入维护后仍可能靠模型记忆 SOP**。旧架构是强 policy + post-hoc meta verifier，但缺少 during-execution transition control，因此理论上可能先 patch、后补大纲/历史记录。
3. 当前入口固定为轻量三态：`NO_DEFECT / INVESTIGATE / CONFIRMED_DEFECT`。`NO_DEFECT` 走正常业务；`INVESTIGATE` 只核证且不能 material patch；systemic/non-trivial `CONFIRMED_DEFECT` 进入 `runtime/maintenance_controller.py`。
4. `runtime/maintenance_controller.py` 是唯一 during-execution controller，但不拥有第二套阶段表；它从 `SYSTEM_MAINTENANCE_POLICY.json.meta_maintenance_outline.stages` 读取 canonical stages。`runtime/meta_maintenance.py` 继续只做 post-hoc closure/conformance verifier，两者职责分开。
5. Controller 已机械禁止：stage skip、未确认 INVESTIGATE 的 material patch、未到 M7 的 material patch、没有 authoritative-reread prepatch checkpoint 的 patch、未完成所有 canonical stages 的 CLOSE。reopen 会截断旧 downstream receipts，BLOCKED 保留精确恢复点。
6. 重复的 `runtime/maintenance_sop.py` 与对应重复测试已经删除；没有新增 Supervisor/Reflection Agent、failure database、root registry 或另一套 startup SOP。
7. `AGENT_MANIFEST.json` 已把 `runtime/maintenance_controller.py` 声明为 runtime/transition guard，并把 `MAINTENANCE_CONTROLLER_STATE.json` 声明为 workflow/continuity state surface。
8. M10 二阶审查真实发现过一个遗漏：此前只测试 controller 逻辑，没有在 CI 中直接读取并验证当前 durable controller state。Controller 因此实际 reopen 回 M7，而不是继续假 PASS；随后新增 `tests/test_current_maintenance_controller_state.py`，现在 full pytest 会从 `AGENT_MANIFEST` 找到真实 state ref 并按当前 policy 验证它。
9. 第二轮 hosted validation：run `38271641398` / job `114887058655`，risk-tiered audit PASS、Agent architecture harness PASS、pytest `295 passed`。因此当前内部保证达到 `REGRESSION_VERIFIED`。
10. 当前 durable controller state 已完成到 M11，revision `21`。但本轮事故在 controller 出现之前已经开始，所以只能诚实称为 **`SELF_HOSTED_CONTROLLER_CONTINUATION_M7_TO_M11`**；M0-M6A 是证据绑定的历史 receipts，不能倒称 controller-native pre-action execution。
11. 因此第一条真正**从 material input → triage → M0…M11** 全程由 controller 驱动、且不靠用户提醒 SOP 的 fresh systemic trajectory 仍是 OPEN 的最高价值 live gate。禁止为了关门而倒造历史轨迹。
12. `recall/history` 现在只承担诊断输入：帮助识别 failure class/历史修复；真正保证“进入后不漏步”的是 persisted controller state + action authorization + reopen/invalidation + CI/meta closure。
13. 所有当前 BUSINESS owner 继续通过 Universal contract/routing 继承共享维护方法；没有复制 controller 到 owner repo，没有获取 BUSINESS lease，也没有修改 BUSINESS truth。
14. 工具层硬边界仍 OPEN：ChatGPT GitHub connector 可以直接 mutation，repo 内 Python controller 无法物理拦截外部 tool call；当前 `main` 也没有 branch protection。若 fresh live trajectory 仍出现绕过，下一层应评估 controller-aware mutation gateway 或 GitHub protection/required checks，而不是继续加 prompt/Agent。
15. `TASK_MANIFEST.json` 的 latest formal meta-run 仍保持 V61。本轮没有把一个“事故中途才引入 controller”的轨迹伪装成完整 M0 controller-native formal meta-run。已有 closure-binding regression 会在未来正式启用 controller contract 时要求 COMPLETE controller trace；正式 promotion 应绑定第一条真正 fresh ingress-native 完整轨迹。

## 当前开放门

- **fresh ingress-native controller trajectory**：OPEN。下一次真实 systemic/non-trivial maintenance 必须从三态入口开始，全程由 controller stage 推进。
- **tool-level unbypassable enforcement**：OPEN。当前 repo controller 不能物理拦截外部 GitHub mutation；如出现 live bypass，升级到 mutation gateway / branch protection 层。
- **formal controller-meta promotion**：OPEN，必须绑定第一条真正从入口开始的 COMPLETE controller trace，不能用本轮中途接管轨迹倒填。
- **semantic analogue completeness**：OPEN。failure-class 历史匹配仍可能有语义漏配；这是诊断质量问题，不是 SOP execution 问题。
- **independent semantic review / live outcome**：OPEN。295 tests 不等于独立语义正确性或未来结果保证。
- **Financial fresh-chat DUAL 3-output retest**：OPEN。
- **Financial current-head architecture revalidation**：OPEN。
- **monitor disable provenance issue #12**：OPEN。

## 下一步

1. 后续任何 material 输入先执行薄 triage；只有 `INVESTIGATE / CONFIRMED_DEFECT` 才进入维护路径。
2. 一旦确认 systemic/non-trivial defect，读取/创建 durable controller state，后续动作必须由 current stage + action authorization 驱动，禁止先 patch 再补记录。
3. 下一条真实 fresh systemic trajectory 是关键验收：必须自动从入口进入 controller，并在没有用户提醒 SOP 的情况下完成或精确 BLOCK。
4. 若 controller 在真实工具 mutation 前仍可被绕过，不再增加 reminder/Agent；直接把 failure class 升级为 `execution-controller-not-on-mutation-path` 并评估工具/仓库级硬约束。
5. 保持入口薄、业务热路径轻；共享方法传播，不传播 owner-local BUSINESS truth。
6. 文档/状态收口后的 GitHub CI 仍必须正常通过，但不为了记录“最后一次 CI 的 run id”再制造递归状态提交。
