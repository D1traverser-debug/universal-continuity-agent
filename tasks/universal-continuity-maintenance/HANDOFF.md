# 跨对话继承系统建设与维护｜Handoff

- task_id: `continuity:universal-continuity-maintenance`
- task_class: `SYSTEM_INFRA`
- owner: `UNIVERSAL_CONTINUITY_HARNESS`
- status: `ACTIVE`
- contract: `CONTINUITY_V3_7`
- current_stage: `SYSTEM_MAINTENANCE_ACTIVE`
- current writer lease: `lease-8ecdf71e-46b3-4e7d-b2ea-61ee05c6d654`
- resume_epoch: `8`
- manifest_version: `79`
- current controller run: `universal-global-control-plane-audit-v67-2026-10-13`
- controller status: `ACTIVE` revision `14`, reopened to `M7_IMPLEMENTATION_AND_SUPERSESSION`
- prepatch audit: `audits/UNIVERSAL_GLOBAL_CONTROL_PLANE_AUDIT_V67_PREPATCH_2026-10-13.json`

## v67 全局总控审计

范围：入口、执行、工作流、竞争/并发、冲突、遗忘、废旧、覆盖/绕过、调用、继承、状态权威、CI/测试、跨 Agent 边界和恢复。

M7 第一版已修：
- continuation bootstrap 与全局轻量 defect preflight 的 scope 冲突；
- OWNER_REGISTRY 混入动态 assurance；
- active/resolved control-signal 生命周期含混，并在 live reobserve 后关闭 stale A-share #2；
- ENTRYPOINT 过窄 headroom；
- TASK_MANIFEST 的 control-signal contract version 指针滞后。

## M8 第一次验证结果与真实 reopen

CI `38357483978` / job `115163633645`：risk-tiered/full control-plane audit PASS、Agent architecture PASS，但 full pytest `303 passed / 7 failed`。

失败不是忽略项：
1. ENTRYPOINT 压缩删掉了既有 regression-protected hot-path anchors，包括 methodology/persistence separation、mid-turn checkpoint 和 plausible-defect triage 的精确语义；
2. owner registry validator 又把 open-world synthetic BUSINESS admission 无关地收紧成必须 `agent_manifest_ref + READY_V37 prefix`，超出了本轮“禁止 mutable assurance status”的修复目标。

因此 controller 已真实 reopen 到 M7 revision 14。当前修正原则：恢复被保护的语义但继续保留至少 512-byte headroom；owner `adapter_status` 只机械禁止 mutable assurance tokens，不额外改变旧的 owner-admission contract。修正后重新进入 M8 全量验证。

## 本轮仍确认成立的主链

- lease_id + resume_epoch + stale-writer fail-closed；
- active lease + observed-HEAD CAS + CI + authoritative reread；
- bare inherit quorum 动态派生，partial discovery 不得伪装完整；
- executor/assurance label 是内部 dispatch，不得改 owner SOP；
- metadata → short handoff → exact refs → selective history → old chat last resort；Memory/chat 不是执行权威；
- artifact/context authority 分层仍成立；
- 当前没有 open PR。

## live / stale / obsolete 边界

- live automation reread没有启用中的 Continuity 核心 monitor；用户此前主动删除仍是当前事实，不自动重建。
- `HARNESS_STATUS.json` 的旧 monitor 字段仍是 lower-authority historical cache，不能覆盖 live reread。
- Novel #3、Video #4 仍是 active drift signals；Financial #7、A-share #2 是 resolved historical evidence。

### 本轮操作失误产生的 branch clutter

M7 工具选择时误创建了五个非权威分支：`__noop`、`__noop2`、`__noop3`、`__noop4`、`__noop5`。它们没有 PR，也没有进入 main/authority。当前 connector 没有 delete-ref primitive，因此不能假装已经删除，也不允许用 force-reset 冒充删除；cleanup 状态为 `OPEN_TOOL_LIMITED`。

## 保留边界

- 不取得 BUSINESS task lease，不改文章、市场日、小说 Canon/project、视频项目业务真值。
- private owner CI runner 未实际执行的地方不能说 PASS。
- Financial fresh-chat DUAL 3-output business retest 仍由 Financial owner 完成。
- independent semantic/live-outcome assurance 与 formal controller-meta promotion 仍 OPEN。
- 本轮不能证明所有未来未知缺陷都已预知，只能对实际检查范围声明 bounded assurance。

## v65 direct-main / PR-first 回归锚点

当前模型不是 PR-first。

Universal material compliant writes 继续使用 active lease + observed-HEAD CAS + CI + authoritative reread；`main protected=false` 本身不是当前 `SINGLE_ACTIVE_CHAT` 威胁模型下的 HIGH defect。

实验分支 `continuity/pr-first-mutation-gate-v65` 没有 merge，也不是 authoritative implementation；它仍无 PR，除非未来 writer topology / permission threat model 出现新的真实证据，否则不得自动 promotion。
