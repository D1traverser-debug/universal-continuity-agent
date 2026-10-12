# 跨对话继承系统建设与维护｜Handoff

- task_id: `continuity:universal-continuity-maintenance`
- task_class: `SYSTEM_INFRA`
- owner: `UNIVERSAL_CONTINUITY_HARNESS`
- status: `ACTIVE`
- contract: `CONTINUITY_V3_7`
- current_stage: `SYSTEM_MAINTENANCE_ACTIVE`
- current writer lease: `lease-8ecdf71e-46b3-4e7d-b2ea-61ee05c6d654`
- resume_epoch: `8`
- manifest_version: `64`
- system-maintenance policy: `1.8`
- meta-maintenance: `1.3`
- latest completed formal meta-run: `audits/META_MAINTENANCE_FAILURE_CLASS_ESCALATION_V61_2026-10-12.json`
- latest completed controller state: `tasks/universal-continuity-maintenance/MAINTENANCE_CONTROLLER_STATE.json`
- latest controller run: `monitor-external-state-authority-v63-2026-10-12`
- latest controller status: `COMPLETE` revision `33`
- latest hosted validation: GitHub Actions `38277130974` / job `114905234417` — risk-tiered audit PASS, Agent architecture harness PASS, full pytest PASS

## 本轮缺陷审计结论

本轮不是风险清单式审查，而是一次真实 fresh systemic maintenance trajectory。用户提出“检查总控是否有缺陷隐患”后先做 triage；用户随后澄清当前核心监控是其主动删除，系统没有把该删除误当作新的静默失活事故。确认的缺陷进入 `runtime/maintenance_controller.py`，完整走过 M0→M11；期间两次真实 CI failure 都触发 reopen，而不是被忽略。

### 已确认并修复 1：外部产品状态被旧仓库观测冒充当前事实

此前 task/status surfaces 仍携带 monitor enabled/hourly 的现时语义，但 ChatGPT automation product state 已因用户主动删除发生变化。根因不是“用户删了监控”，而是外部产品状态可以脱离 GitHub 变化，仓库过去缺少足够严格的 freshness/authority 边界。

现在的架构规则：ChatGPT automation/task 是否存在、是否 enabled、scheduler 是否存活属于 **external product state**。GitHub 可以保存期望策略与带时间戳的 last-observed evidence，但任何依赖“现在是否存在/启用”的判断都必须在产品面可用时 live reread。显式用户删除/禁用不得被自动逆转，除非之后获得新授权。

当前 2026-10-13T00:27:13+08:00 的产品面 reread：没有核心 Continuity monitor tasks；用户已明确确认这是主动删除，因此 `monitor_recreation_authorized=false`。历史 issue #12 仍只保留其原始未解问题：此前那次 silent enabled→disabled 的 provenance 未知；当前主动删除不是该历史事故复发证据。

### 已确认并修复 2：task manifest mutation version 与 formal meta-proof version 错误耦合

合法 new-chat takeover 会由 `runtime/universal_continuity.py::acquire_resume_lease()` 增加 `manifest_version`。旧 regression 同时要求 `latest_meta_maintenance_run_ref.target_manifest_version == current manifest_version`。这意味着普通 takeover/任务 checkpoint 也会迫使系统制造一份“当前版本 formal meta-run”，否则 CI 失败。

该 failure class 在 V53 已出现并以“每次 takeover 补当前版本 formal meta-run”修过；本轮同类再次发生，而且当前 controller contract 已明确禁止为了关门倒造未完成轨迹。因此按 policy 1.8 做 abstraction escalation，不再重复 V53 同层补丁。

新的架构模型：
- `manifest_version` = durable task mutation / CAS lineage；合法 takeover/checkpoint 可独立增长；
- `latest_meta_maintenance_run_ref` = **最近一条真正完成的 formal maintenance proof**；
- completed formal run 的 `target_manifest_version` 不能晚于 current manifest，但普通 task mutation 不要求 exact equality；
- ACTIVE/BLOCKED trajectory 不能为了追版本号而被伪装成 completed formal proof；
- exact-current proof binding 只应由另一个明确的 promotion/freshness gate 在确实需要时要求。

该规则已写入 `SYSTEM_BLUEPRINT.md`，并由 `tests/test_meta_maintenance.py` 与 `tests/test_meta_governance_status_alignment.py` 回归保护。

## 本轮真实验证

1. 首次实现后的 CI `38275331371` 真实失败：manifest compaction 漏掉 `methodology_owner_declaration_contract_version`；controller reopen M7 并修复。
2. 第二次 CI `38275584909`：risk-tiered audit PASS、architecture PASS，但 pytest 294 pass / 1 fail，暴露上述 manifest/meta-proof 版本耦合；controller reopen 到 M2A，查到 V53 同类历史并升级到 system-architecture repair。
3. 生命周期解耦实现后的 CI `38276628670` 全绿。
4. M10 二阶审查发现 repair semantics 还没有进入 architecture map，于是再次 reopen M7，将两条不变量写入 `SYSTEM_BLUEPRINT.md` 并增加 regression anchor。
5. 最终 hosted validation `38277130974` / `114905234417`：risk-tiered audit PASS、Agent architecture harness PASS、full pytest PASS。

这因此是当前任务中第一条可诚实记录为 **fresh / no-user-reminder / M0→M11 complete** 的 controller trajectory；不是把旧事故中途接管的历史倒称为 ingress-native proof。

## 仍然 OPEN 的真实缺陷/边界

### A. Tool-level unbypassable enforcement — HIGH / OPEN

GitHub `main` 目前仍 `protected=false`，没有 required status checks enforcement。repo 内 `maintenance_controller.py` 可以规定和验证顺序，但不能物理阻止一个外部 GitHub connector/API 直接 mutation。因此当前保证仍是 **repo/controller + CI level enforcement**，不是 unbypassable mutation-path enforcement。

下一层如果要关闭此门，应评估 controller-aware mutation gateway 或 GitHub branch protection / required checks。不要再通过增加 prompt、Supervisor Agent 或更多提醒文本来伪装硬约束。本聊天当前可用 GitHub connector 没有 branch-protection 写动作，因此本轮未冒充已经关闭。

### B. HARNESS_STATUS historical monitor cache — LOWER-AUTHORITY DRIFT / OPEN FOR CONVERGENCE

`HARNESS_STATUS.json` 是明确标注的 rebuildable cache，内部仍可能含本轮之前的 monitor-enabled historical observations。它现在不能覆盖 task manifest 与 live product reread，也不能再作为 present-tense liveness evidence。后续重建该 cache 时应收敛到新模型；该缓存漂移不再是当前 liveness authority。

### C. Independent semantic / live outcome proof — OPEN

最终 CI 证明 scoped regression/structure 通过，不证明独立语义判断无误，也不证明未来外部产品变化或实际业务结果。`independent_meta_semantic_review` 继续 OPEN。

### D. Formal controller-meta promotion — OPEN but now eligible

当前最新 formal meta-run 仍是 V61，没有为了本轮追 `manifest_version` 而伪造新 formal proof。现在 controller trajectory 已 genuinely COMPLETE，可在下一次维护动作中评估是否把这条完整 trace 正式 promotion/bind 到 meta-governance proof。

### E. 既有业务侧开放门

Financial current-head architecture revalidation 与 fresh-chat DUAL 3-output retest 仍 OPEN；本 SYSTEM_INFRA 审计没有取得 Financial BUSINESS lease，也没有修改其业务真值。

## 下一步

优先级建议：
1. 评估并关闭 **tool-level mutation bypass**（mutation gateway 或 GitHub protection/required checks）；
2. 用这条 COMPLETE controller trace 做 **formal controller-meta promotion**，但只在 proof schema/contract 真正满足时推进，不能倒填；
3. 下次 HARNESS_STATUS rebuild 时收敛 monitor cache；
4. 继续 Financial 已登记的 current-head architecture revalidation / fresh-chat DUAL 3-output retest；
5. 保持所有 BUSINESS owner lease/business truth 边界不变。
