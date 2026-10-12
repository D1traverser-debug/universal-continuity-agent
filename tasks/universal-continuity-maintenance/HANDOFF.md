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
- latest meta-run: `audits/META_MAINTENANCE_FAILURE_CLASS_ESCALATION_V61_2026-10-12.json`
- regression evidence: GitHub Actions `38253314936` / job `114824858476` / `275 passed`

## 当前权威状态

1. 本轮修复对象不是 Financial 单点 bug，而是 Universal 自进化方法的复发性缺陷：过去已经要求 parent-system reframe、failure-class distillation、主动学习和 second-order review，但旧 `runtime/meta_maintenance.py` 仍允许系统只填写 `failure_classes`，不证明检索过历史同类事件，也不强制“修过又复发”时上升抽象层。因此同族故障仍可能再次等用户提醒。
2. `SYSTEM_MAINTENANCE_POLICY.json` v1.8 现在明确把**大纲放在下钻之前**。系统性问题的 canonical 顺序是：`信号/约束分类 → 读取 authority → BUILD_FULL_SYSTEM_IMPACT_MAP → 详细 root cause + failure class → 历史同类检索 → recurrence 判定与 abstraction escalation → 学习/备选/设计 → 高层/类型机制修复 → 回落 class_level_prevention + concrete instance fix → validation → cross-surface/propagation → second-order review → durable learning`。
3. 纵向抽象梯由同一 policy owner 定义：`INSTANCE → FAILURE_CLASS → OWNER_OR_COMPONENT_MECHANISM → SYSTEM_ARCHITECTURE → META_METHOD`。第一次问题优先最低充分层；同类问题在 accepted fix 后再次发生，必须高于上次修复层级；若已在 `META_METHOD` 仍复发，则必须显式进入 `MAX_LEVEL_REDESIGN`，不能伪造不存在的更高层。
4. `runtime/meta_maintenance.py` schema 1.3 把上述方法变成 fail-closed 结构门：当前 systemic run 必须搜索全部已分类 failure class；known/recurrent class 必须绑定历史 ref；`RECURRED_AFTER_FIX` / `CROSS_OWNER_RECURRENT` 必须记录 prior repair level 并升级；高层修复后必须同时记录 `class_level_prevention` 与 `instance_fix`。runtime 的枚举只是 executable mirror，并对 canonical policy 做 parity 检查，防止形成 shadow rule。
5. `runtime/self_maintenance_trajectory.py` 也已同步，不再只验证抽象政策：reference trajectory 现在包含 `PARENT_SYSTEM_REFRAME → DIAGNOSE_ROOT_CAUSE → SEARCH_FAILURE_HISTORY → ABSTRACTION_ESCALATION_DECISION → ... → PATCH → RETURN_TO_CLASS_PREVENTION_AND_INSTANCE_FIX → VALIDATION`。
6. V59 已明确记录 `symptom-first-repair-without-parent-system-reframe` 与 `owner-maintenance-waits-for-user-signal...`；V60 又记录 confirmed defect 发 signal 后仍需用户催着真正修；Financial live trajectory又暴露 task/output negative-space omission。本轮因此正式分类为 `RECURRED_AFTER_FIX`，prior level=`SYSTEM_ARCHITECTURE`，current level=`META_METHOD`，不是另一次局部补丁。
7. 第一次 V61 真实 CI 并没有直接绿：run `38252468487` / job `114822012392` 为真实 runner，结果 `271 passed, 4 failed`。失败暴露两类 stale consumer：旧 self-maintenance reference simulation 仍编码旧顺序，以及 `tests/test_system_audit.py` 硬编码 policy `1.7`。没有降低新 gate，而是把影响面扩大到这些 consumer 并修正。
8. 修复 consumer 后，run `38253314936` / job `114824858476` 真实执行并通过：risk-tiered control-plane audit `PASS`、Agent architecture harness `PASS_WITH_ACKNOWLEDGED_OWNER_DRIFT_WARNINGS`、pytest `275 passed`。因此 V61 可到 `REGRESSION_VERIFIED`；仍不能升级为 independent semantic/live outcome proof。
9. 没有新增 Reflection/Supervisor Agent、root policy、failure database 或业务热路径 preload。现有 audit artifacts 继续保存历史证据；如果未来真实运行证明 free-form failure class 名称导致明显同类问题仍匹配失败，再在 `META_METHOD` 层评估 normalized concept key / semantic retrieval，而不是现在预先堆系统。
10. Financial 最新 `main` 仍为 `ce7bac183e0ca57be1cbc1591e7e124f209055e0`。其 fresh-chat default DUAL 轨迹之前暴露应交付 Deep+Broad+Audit 三份而实际只交两份；Financial owner 已做 TaskContract/output parity repair，但 fresh-chat 3-output retest 与 ce7bac fresh architecture revalidation 仍 OPEN。Universal 不改写其 BUSINESS truth/lease。

## 当前开放门

- **live no-reminder proof**：OPEN。下一次真实 systemic incident 必须在没有用户再次指出“这是同类问题”的情况下，自己先建 parent-system outline，再检索历史 failure class、判断 recurrence、正确上升 abstraction level，并回落修 class + 当前实例。
- **semantic analogue completeness**：OPEN。结构门不能证明模型找全所有语义同类历史事件；若未来明显漏配，需在 `META_METHOD` 层重新设计 retrieval/concept normalization。
- **independent semantic review / live outcome**：OPEN。275 tests 证明当前结构与回归，不证明语义诊断永远正确，也不证明用户以后绝不会再提醒。
- **Financial fresh-chat DUAL 3-output retest**：OPEN。
- **Financial ce7bac architecture revalidation**：OPEN。
- **monitor disable provenance issue #12**：OPEN。

## 下一步

1. 后续任何 material/systemic 问题先执行：`信号 → authority → parent-system outline → root cause/failure class → historical match → recurrence → abstraction level`，禁止先 patch 再补大纲。
2. 如果是 `RECURRED_AFTER_FIX/CROSS_OWNER_RECURRENT`，不得在原层继续打补丁；必须上升至少一级，再回落完成 `class_level_prevention + concrete instance fix` 后才能验证关闭。
3. 下一次真实无提醒轨迹作为 V61 live proof；若仍漏掉明显历史同类，继续在 `META_METHOD` 层修“学习/检索机制”，而不是回到局部 guard 堆叠。
4. 不获取任何 BUSINESS lease，不修改 BUSINESS truth；共享方法传播只走现有 Universal profile/maintenance contract。
