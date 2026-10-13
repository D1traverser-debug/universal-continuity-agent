# 跨对话继承系统建设与维护｜Handoff

- task_id: `continuity:universal-continuity-maintenance`
- task_class: `SYSTEM_INFRA`
- owner: `UNIVERSAL_CONTINUITY_HARNESS`
- status: `ACTIVE`
- contract: `CONTINUITY_V3_7`
- current_stage: `SYSTEM_MAINTENANCE_ACTIVE`
- current writer lease: `lease-8ecdf71e-46b3-4e7d-b2ea-61ee05c6d654`
- resume_epoch: `8`
- manifest_version: `78`
- current controller run: `universal-global-control-plane-audit-v67-2026-10-13`
- controller status: `ACTIVE` revision `13` at `M8_MULTI_LAYER_VALIDATION`
- prepatch audit: `audits/UNIVERSAL_GLOBAL_CONTROL_PLANE_AUDIT_V67_PREPATCH_2026-10-13.json`

## v67 全局总控审计

本轮按用户明确要求，对 Universal 本身做全局隐患审计，覆盖入口、执行、工作流、竞争/并发、冲突、遗忘、废旧、覆盖/绕过、调用、继承、状态权威、CI/测试、跨 Agent 边界和恢复。

不是拿历史 PASS 代替当前检查。已重新观察当前 `main`、SYSTEM_INFRA lease、启动/入口合同、owner membership/observation、writer lease/CAS、控制信号、live automations、分支/PR、BUSINESS owner heads 和关键回归。

## M7 已实施的修复

1. **入口范围冲突**：继续/恢复的 Continuity bootstrap 仍只由显式 continuation intent 触发；但所有 material input 先走便宜的 `NO_DEFECT / INVESTIGATE / CONFIRMED_DEFECT` preflight。`NO_DEFECT` 不加载完整 maintenance，不做 global discovery。`ENTRYPOINT.md`、`NEW_CHAT_BOOTSTRAP.json`、`CONTINUITY_CONTRACT.json` 已对齐。

2. **membership authority 混入易过期 assurance**：四个 BUSINESS owner 的 `adapter_status` 收敛为稳定的 `READY_V37_PROTOCOL_ADAPTER_DECLARED`。CI PASS/FAIL、PENDING、LIVE quality、当前 blocker 等动态事实只能放在 observation/evidence surfaces。`runtime/owner_topology.py` 现在会机械拒绝这些 token 重新混回 `OWNER_REGISTRY.json`。

3. **control signal 生命周期含混**：`CONTROL_SIGNAL_CONTRACT.json` 明确 `active_control_signal_ref` 与 `resolved_control_signal_ref`。A-share #2 已 live reobserve：当前 Skill 6,733 bytes，小于 8,192 target，因此 issue 已关闭并转成 resolved historical evidence；Financial #7 本来已关闭，也改为 resolved；Novel #3、Video #4 仍是 active。

4. **ENTRYPOINT headroom**：没有放宽 8,192-byte hard cap，而是压缩热路径；新回归要求至少保留 512 bytes reserve，降低再次出现 v65 8,447-byte overflow 的概率。

5. **M7 额外发现并修复**：task manifest 的 `control_signal_contract_version` 仍写 `1.0`，而实际 `CONTROL_SIGNAL_CONTRACT.json` 已是 `1.1`；已对齐为 `1.1` 并纳入回归。

## 本轮确认未出现新缺陷的主链

- writer competition：lease_id + resume_epoch 校验、stale-writer fail-closed 仍成立。
- direct-main：active lease + observed-HEAD CAS + CI + authoritative reread 仍是当前单 writer 标准。
- bare inherit：required source quorum 从 `OWNER_REGISTRY` 动态派生；任一 source 缺失即 `INCOMPLETE_DISCOVERY`，partial 不得伪装完整或 auto-resume。
- execution/readiness：executor/assurance label 是系统内部 dispatch；hard capability 缺失只阻塞精确 gate，不改 owner SOP。
- recovery/遗忘：metadata → short handoff → exact refs → selective history → old chat last resort；Memory/chat 不是执行权威。
- artifact/conflict：engineering/task/evidence/cache/scratch/external/personalization 分层，lower authority 不得覆盖 fresher higher-authority truth。
- protocol reconciliation：不得借迁移改业务 stage/status/next_action/lease。
- 当前没有 open PR。

## live / stale / obsolete 边界

- live automation reread：没有启用中的 Continuity 核心 monitor；用户此前主动删除仍是当前事实，不自动重建。
- `HARNESS_STATUS.json` 仍有 lower-authority historical monitor cache；不能覆盖 live product reread。全量 cache rebuild 仍是安全 cleanup，不为了表面整洁冒险重写大状态镜像。
- `PROTOCOL.md` 仍是 human reference，不是 bootstrap/执行 authority；当前未发现 hot path 依赖。
- 旧 maintenance branches 与 v65 PR-first 实验均不是 authority、没有 open PR。

### 本轮操作失误产生的 branch clutter

M7 工具选择时误创建了五个指向当时 main 的非权威分支：`__noop`、`__noop2`、`__noop3`、`__noop4`、`__noop5`。它们没有 PR，也没有进入 main/authority。当前 GitHub connector 没有 delete-ref primitive，因此不能假装已经删除；也不允许用 force-reset 冒充删除。该 cleanup 明确保留为 `OPEN_TOOL_LIMITED`。

## M8 下一步

运行 Universal risk-tiered/full control-plane audit、Agent architecture harness、full pytest。任何失败都必须按 controller 回到需要的阶段修复；不能把结构看起来合理当作 PASS。绿灯后再做 M9 owner/head/signal reobservation、M10 二阶复核、M11 durable closure，并在 closure commit 后再次观察 CI + authoritative reread。

## 保留边界

- 不取得 BUSINESS task lease，不改文章、市场日、小说 Canon/project、视频项目业务真值。
- private owner CI runner 未实际执行的地方不能说 PASS。
- Financial fresh-chat DUAL 3-output business retest 仍由 Financial owner 完成。
- independent semantic/live-outcome assurance 仍 OPEN。
- formal controller-meta promotion 仍 OPEN，不伪造 chronology。
- 这次全局审计不能证明“所有未来未知缺陷都已预知”；只能证明本轮列明的结构/live surface 已检查到声明的 assurance ceiling。

## v65 direct-main / PR-first 回归锚点

当前模型不是 PR-first。

Universal material compliant writes 继续使用 active lease + observed-HEAD CAS + CI + authoritative reread；`main protected=false` 本身不是当前 `SINGLE_ACTIVE_CHAT` 威胁模型下的 HIGH defect。

实验分支 `continuity/pr-first-mutation-gate-v65` 没有 merge，也不是 authoritative implementation；它仍无 PR，除非未来 writer topology / permission threat model 出现新的真实证据，否则不得自动 promotion。
