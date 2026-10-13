# 跨对话继承系统建设与维护｜Handoff

- task_id: `continuity:universal-continuity-maintenance`
- task_class: `SYSTEM_INFRA`
- owner: `UNIVERSAL_CONTINUITY_HARNESS`
- status: `ACTIVE`
- contract: `CONTINUITY_V3_7`
- current_stage: `SYSTEM_MAINTENANCE_ACTIVE`
- current writer lease: `lease-8ecdf71e-46b3-4e7d-b2ea-61ee05c6d654`
- resume_epoch: `8`
- manifest_version: `81`
- current controller run: `universal-global-control-plane-audit-v67-2026-10-13`
- controller status: `ACTIVE` revision `17` at `M10_SECOND_ORDER_REVIEW_AND_GLOBAL_CLAIM_CALIBRATION`
- corrective validation: GitHub Actions `38358219416` / job `115165991116` — risk-tiered/full control-plane audit PASS, Agent architecture PASS, full pytest PASS

## v67 已验证修复

本轮全局审计覆盖入口、执行、工作流、竞争/并发、冲突、遗忘/恢复、废旧/影子机制、覆盖/绕过、调用、继承、状态权威、CI/测试和跨 Agent 边界。

当前已修并通过 M8：
- continuation bootstrap 与 all-material-input cheap defect preflight 的 machine-readable scope 对齐；`NO_DEFECT` 不加载完整 maintenance/global discovery。
- BUSINESS owner membership authority 不再承载动态 CI/PASS/PENDING/LIVE assurance；`runtime/owner_topology.py` 对 mutable operational assurance token fail closed。
- control signals 区分 active/resolved；A-share #2 在当前 Skill 6,733 bytes 的 live reobserve 后关闭，Financial #7 保持 resolved；Novel #3、Video #4 保持 active。
- `control_signal_contract_version` 指针已从 1.0 对齐到 1.1。
- ENTRYPOINT 在恢复所有既有 methodology/progress/defect-triage regression anchors 后，仍满足 8,192-byte hard cap，并保留至少 512 bytes reserve。
- 第一次 M8 曾真实失败 `303 passed / 7 failed`，controller reopen 到 M7；没有掩盖。修复 stale synthetic owner fixtures 后，第二次 M8 `38358219416 / 115165991116` 全绿。

## M9 fresh reobservation

四个 BUSINESS owner 当前 head 均与已验证 observation set 一致：
- Financial `6494cd58a93d82f7fc6849803b6b7493cf66443f`
- A-share `651d97533cd62d34dc230f0b5047715074ab1803`
- Novel `46606fee061a5cf5421a5d0ef145a5955fd66760`
- Video `8f7d0cfb8121fc1a06e1e3a24c1167649d4def94`

因此本轮无需取得任何 BUSINESS lease，也没有修改文章、市场日、小说 Canon/project 或视频项目业务真值。`OWNER_ARCHITECTURE_OBSERVATIONS.json` 只刷新 rebuildable observation 时间和 signal lifecycle。

## 已确认仍成立的主链

- **入口**：最小 bootstrap 只从 `ENTRYPOINT.md + CURRENT_PROTOCOL.json` 起；正常 BUSINESS 产品仍是一个 ChatGPT owner/Skill 入口，executor/readiness 是内部选择。
- **执行/调用**：repository capability 声明只是 ceiling，不是当前执行证明；material owner action 必须按 exact capability/readiness/methodology evidence 放行。
- **工作流**：systemic maintenance 由 controller 约束 M0→M11；业务 owner 的 workflow/state 仍归业务 owner，不复制进 Universal。
- **竞争/并发**：当前 `SINGLE_ACTIVE_CHAT`，lease_id + resume_epoch + stale-writer fail-closed；Universal material main write 使用 observed-HEAD CAS。
- **冲突/覆盖**：engineering authority、task state、business evidence、cache、scratch、external refs、Memory/chat 分层；lower authority 不能静默覆盖 fresher higher authority。
- **遗忘/恢复**：metadata → short handoff → exact refs → selective history → old chat last resort；Memory/chat 不作为 task execution authority。
- **继承**：bare inherit quorum 从 `OWNER_REGISTRY` 动态派生；任一 required source 缺失即 `INCOMPLETE_DISCOVERY`，partial 不得声称完整或自动恢复。
- **废旧/影子机制**：`PROTOCOL.md` 仍只作 human reference，不进入 hot-path authority；旧 branches 无 PR 且非 authority。

## M10 需要明确校准的剩余边界

- `HARNESS_STATUS.json` 仍含 lower-authority historical monitor cache；当前 live product reread没有启用的 Continuity 核心 monitor，用户主动删除的事实优先。安全 cache rebuild 仍是 cleanup，不以风险重写换表面整洁。
- Novel #3、Video #4 是仍然 open 的 owner-local hot-path drift；不是本轮 Universal 可越权修改的 BUSINESS truth。
- 历史 monitor #12 只保留原 silent disable provenance 未解；当前 monitor absence 是用户意图，不是 recurrence 证据。
- private owner CI runner 未执行的地方仍不能称 PASS；Financial fresh-chat DUAL 3-output retest 仍是 Financial-owner scoped OPEN。
- independent semantic/live-outcome assurance 与 formal controller-meta promotion 仍 OPEN。
- 本次全局审计证明的是声明范围内的结构/live-control-surface检查，不声称所有未来未知失败均被预知。

### 本轮工具操作失误产生的非权威 branch clutter

误创建的 `__noop`、`__noop2`、`__noop3`、`__noop4`、`__noop5` 没有 PR、没有进入 main/authority。当前 connector 没有 delete-ref primitive，cleanup=`OPEN_TOOL_LIMITED`；不得用 force-reset 冒充删除。

## v65 direct-main / PR-first 回归锚点

当前模型不是 PR-first。

Universal material compliant writes 继续使用 active lease + observed-HEAD CAS + CI + authoritative reread；`main protected=false` 本身不是当前 `SINGLE_ACTIVE_CHAT` 威胁模型下的 HIGH defect。

实验分支 `continuity/pr-first-mutation-gate-v65` 没有 merge，也不是 authoritative implementation。
