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
- controller cutover audit: `audits/MAINTENANCE_EXECUTION_CONTROLLER_CUTOVER_2026-10-12.md`
- controller regression evidence: GitHub Actions `38268950814` / job `114878120772` / `298 passed`

## 当前权威状态

1. V61 已把系统性维护升级为：先建 parent-system outline，再做 root cause/failure class、历史同类检索、recurrence 判定与 abstraction escalation，最后回落 `class_level_prevention + concrete instance fix` 后验证；该结构仍有效。
2. 本轮进一步确认一个更直接的缺陷：**进入维护入口以后，旧系统仍主要是“policy 定义 SOP + meta harness 最后审记录”，不是 during-execution execution control**。因此模型理论上可以先 patch，最后再补齐大纲/历史检索记录。该 failure class 记为 `declarative-SOP-without-execution-control`。
3. 已新增 `runtime/maintenance_controller.py`，但它不拥有第二套流程。canonical stage 仍由 `SYSTEM_MAINTENANCE_POLICY.json.meta_maintenance_outline.stages` 唯一定义；controller 只负责当前 stage、顺序、action authorization、BLOCKED/resume、re-open/downstream invalidation 和 closure gate。
4. 三态入口现在固定为 `NO_DEFECT / INVESTIGATE / CONFIRMED_DEFECT`。`NO_DEFECT` 保持正常业务热路径；`INVESTIGATE` 只查证据且不能 material patch；systemic/non-trivial `CONFIRMED_DEFECT` 进入 controller。入口只负责分流，不复制完整 SOP。
5. Controller 已机械覆盖：禁止 stage skip；禁止 M7 前 material patch；`INVESTIGATE` 未确认不能 patch；validation/propagation/second-order review 只能在对应 stage；validation/second-order 新发现可 reopen 更早 stage 并使下游 receipt 失效；全部 canonical stages 未完成不能 CLOSE。
6. `AGENT_MANIFEST.json` 已把 controller 声明为 runtime entrypoint + workflow transition guard；`SYSTEM_BLUEPRINT.md` 已明确区分 `maintenance_controller.py`（during-execution controller）与 `meta_maintenance.py`（post-hoc closure verifier）。
7. 第一版 wiring 因把太多 SOP 塞进入口而真实 CI 失败；没有调大预算，而是压缩入口，把详细流程移回 cold-path policy/runtime。随后压缩又删掉部分已有 takeover/progress invariant，CI 再次失败；这些稳定边界已经恢复。最终 current verified sizes：`ENTRYPOINT.md` 8,013 B、`CURRENT_PROTOCOL.json` 454 B、两文件合计 8,467 B / 9,216 B；`STARTUP_HOOK.md` 3,464 B / 4,096 B。
8. 最终真实 CI run `38268950814` / job `114878120772`：risk-tiered audit PASS、selected synthetic faults PASS、Agent architecture harness PASS（仅既有 owner drift warnings）、pytest `298 passed`。因此当前 controller/ingress wiring 达到 `REGRESSION_VERIFIED`。
9. **不要把这写成 controller-native live proof。** 本轮 repair 在 controller 存在之前已经开始，所以没有伪造ย้อนหลัง stage trace。第一条真正“从入口开始就由 controller 驱动”的 systemic maintenance trajectory 仍 OPEN。
10. 还有一个更硬的产品边界：当前 ChatGPT GitHub connector 可以直接调用 repository mutation；repo 内 Python controller 不能物理拦截外部 tool call。因此当前保证是“路由 + deterministic authorization + CI/regression”，不是不可绕过的 mutation middleware。若真实 trajectory 仍出现绕过，下一层应该是 controller-aware mutation gateway 或 GitHub protection/required-check 级执行约束，不得再靠提醒 prose。
11. Financial 最新 `main` 仍为 `ce7bac183e0ca57be1cbc1591e7e124f209055e0`；其 fresh-chat DUAL 3-output retest 与 ce7bac fresh architecture revalidation 继续 OPEN。本轮 Universal maintenance 不获取任何 BUSINESS lease、不修改 BUSINESS truth。

## 当前开放门

- **controller-native live trajectory**：OPEN。下一次真实 systemic/non-trivial maintenance 必须从三态入口开始，并在用户不提醒 SOP 的情况下按 controller stage 推进。
- **tool-level hard enforcement**：OPEN。当前 repo controller 不能物理拦截 ChatGPT GitHub connector 的直接 mutation；如 live evidence 证明仍可绕过，必须升到 mutation gateway / repository protection，而不是继续堆 prompt。
- **semantic analogue completeness / live no-reminder proof**：OPEN。结构门仍不能证明 failure-class 语义匹配永远完整。
- **independent semantic review / live outcome**：OPEN。298 tests 不等于独立语义审查或未来结果保证。
- **Financial fresh-chat DUAL 3-output retest**：OPEN。
- **Financial ce7bac architecture revalidation**：OPEN。
- **monitor disable provenance issue #12**：OPEN。

## 下一步

1. 后续任何 material 输入先走轻量三态 triage；健康业务 `NO_DEFECT` 不加载全维护栈。
2. 一旦进入 systemic/non-trivial maintenance，controller current stage 是 SOP 执行导航；禁止先 patch 再补记录。
3. 第一条 controller-native live trajectory 是当前最高价值验证；若仍发生 controller bypass，直接把问题升级为 `execution-controller-not-on-mutation-path`，评估真正 mutation gateway / GitHub enforcement。
4. 保持入口薄，不因可靠性需求把完整治理文本塞回 STARTUP/ENTRYPOINT。
5. 不获取任何 BUSINESS lease，不修改 BUSINESS truth；共享方法传播只走 Universal control-plane authority。
