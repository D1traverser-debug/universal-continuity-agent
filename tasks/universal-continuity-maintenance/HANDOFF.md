# 跨对话继承系统建设与维护｜Handoff

- task_id: `continuity:universal-continuity-maintenance`
- task_class: `SYSTEM_INFRA`
- owner: `UNIVERSAL_CONTINUITY_HARNESS`
- status: `ACTIVE`
- contract: `CONTINUITY_V3_7`
- current_stage: `SYSTEM_MAINTENANCE_ACTIVE`
- current writer lease: `lease-8ecdf71e-46b3-4e7d-b2ea-61ee05c6d654`
- resume_epoch: `8`
- manifest_version: `77`
- current controller run: `universal-global-control-plane-audit-v67-2026-10-13`
- controller status: `ACTIVE` revision `12` at `M7_IMPLEMENTATION_AND_SUPERSESSION`
- prepatch audit: `audits/UNIVERSAL_GLOBAL_CONTROL_PLANE_AUDIT_V67_PREPATCH_2026-10-13.json`

## v67 全局总控审计

用户明确要求对 Universal 本身做全局隐患审计，覆盖入口、执行、工作流、竞争/并发、冲突、遗忘、废旧、覆盖/绕过、调用、继承、状态权威、CI/测试、跨 Agent 边界与恢复。

本轮不是拿历史 PASS 当当前结论。已重读当前 `main`、SYSTEM_INFRA lease、入口/启动合同、owner membership/observation、writer lease/CAS、控制信号、自动化 live surface、分支/PR、当前 BUSINESS owner heads 和关键测试。

当前确认 3 个需要修复的 control-plane defect：

1. `INGRESS_PREFLIGHT_SCOPE_CONTRACT_DRIFT`：`ENTRYPOINT.md` / `STARTUP_HOOK.md` 已要求所有 material 输入先做轻量 defect preflight，但 `NEW_CHAT_BOOTSTRAP.json` / `CONTINUITY_CONTRACT.json` 的 performance metadata 仍把 startup hook 描述成 continuation-intent-only，存在机器可读语义冲突。
2. `MEMBERSHIP_AUTHORITY_CONTAINS_MUTABLE_ASSURANCE_STATUS`：`OWNER_REGISTRY.json` 已是唯一 membership authority，却仍在 BUSINESS `adapter_status` 里塞入 CI PASS/PENDING/LIVE/current-assurance 等易过期状态；这绕开了此前把远端 observation 拆到 `OWNER_ARCHITECTURE_OBSERVATIONS.json` 的架构意图。本项属于 prior separation fix 后的 recurrence，必须提升到 validator + stable admission vocabulary，而不是只改字符串。
3. `CONTROL_SIGNAL_LIFECYCLE_STALENESS`：A-share #2 仍 open，但当前 Skill 已是 6,733 bytes，小于 8,192 target；Financial observation 仍用 `control_signal_ref` 指向已经关闭的 #7。active 与 resolved signal 没有在 observation cache 中区分。

另有一个 preventive reliability finding：Universal `ENTRYPOINT.md` 当前 8,118 bytes，只比 8,192 hard regression budget 少 74 bytes；v65 已经真实发生过 8,447-byte CI failure。本轮会压缩热路径并加入 reserve/headroom regression，**不放宽预算**。

## 已核查且暂未发现新缺陷的关键边界

- single-writer：lease_id + resume_epoch 验证、stale writer fail-closed 仍成立。
- Universal `main` mutation：仍是 active lease + observed-HEAD CAS + CI + authoritative reread。
- bare inherit：owner quorum 从 `OWNER_REGISTRY.json` 动态派生；缺任一 source 即 `INCOMPLETE_DISCOVERY`；partial 不得当完整列表/不得 auto-resume。
- execution/readiness：v66 后 executor label 为内部 dispatch/evidence，不是用户路线；hard capability 缺失只阻塞精确 gate，不改业务 SOP。
- artifact/context：GitHub authority、durable task state、business evidence、cache、scratch、external refs、Memory/chat 已分层；lower authority 不能静默覆盖更高 authority。
- protocol reconciliation：必须持当前 lease，且不能借协议迁移改业务 stage/status/next_action/lease。
- 当前没有 open PR。

## 当前 live / stale / obsolete 边界

- live automation reread：没有启用中的 Continuity 核心 monitor；只看到 3 个无关 task，且全部 disabled。用户此前主动删除核心 monitors 的事实继续有效，不得自动重建。
- `HARNESS_STATUS.json` 仍是 lower-authority historical cache，里面部分 present-looking monitor booleans 已过期；它不能覆盖这次 live reread。安全全量 cache rebuild 仍是 cleanup，不为“看起来干净”冒险重写 30KB 状态镜像。
- stale branches：`continuity/pr-first-mutation-gate-v65` 与 3 个旧 maintenance branch 都不是 authority；没有 open PR。当前 connector 没有 delete-ref，禁止用 force-reset 冒充删除。
- `PROTOCOL.md` 仍只做人类 reference，不是 bootstrap/执行 authority；目前未发现 hot path 依赖它。

## M7 计划

- 对齐 startup/preflight machine-readable scope；
- 收敛 OWNER_REGISTRY `adapter_status` 为稳定 admission metadata，并在 `runtime/owner_topology.py` 加机械禁止 mutable assurance tokens；
- observation cache 区分 `active_control_signal_ref` 与 `resolved_control_signal_ref`，live reobserve 后关闭 stale A-share #2；
- 压缩 ENTRYPOINT 并建立 reserved headroom regression；
- 补 focused tests；
- M8 必须跑 Universal risk-tiered/full-control-plane audit、Agent architecture harness、full pytest；失败就 reopen/继续修，不能硬关。

## 保留边界

- 不取得任何 BUSINESS task lease，不改文章、市场日、小说 Canon/project、视频项目业务真值。
- private owner CI runner 未执行的地方仍不能说 PASS。
- Financial fresh-chat DUAL 3-output business retest 仍由 Financial owner 完成。
- independent semantic/live-outcome assurance 仍 OPEN。
- formal controller-meta promotion 仍 OPEN，不伪造 chronology。

## v65 direct-main / PR-first 回归锚点

当前模型不是 PR-first。

Universal material compliant writes 继续使用 active lease + observed-HEAD CAS + CI + authoritative reread；`main protected=false` 本身不是当前 `SINGLE_ACTIVE_CHAT` 威胁模型下的 HIGH defect。

实验分支 `continuity/pr-first-mutation-gate-v65` 没有 merge，也不是 authoritative implementation；它仍无 PR，除非未来 writer topology / permission threat model 出现新的真实证据，否则不得自动 promotion。
