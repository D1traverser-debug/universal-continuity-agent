# 跨对话继承系统建设与维护｜Handoff

- task_id: `continuity:universal-continuity-maintenance`
- task_class: `SYSTEM_INFRA`
- owner: `UNIVERSAL_CONTINUITY_HARNESS`
- status: `ACTIVE`
- current_stage: `SYSTEM_MAINTENANCE_ACTIVE`
- current writer lease: `lease-8ecdf71e-46b3-4e7d-b2ea-61ee05c6d654`
- resume_epoch: `8`
- manifest_version: `84`
- current controller run: `universal-global-control-plane-audit-v67-2026-10-13`
- controller status: `ACTIVE` revision `21` at `M8_MULTI_LAYER_VALIDATION`

## v67 当前状态

第二次 M10 reopen 已完成 M7 修复：control signal 现在明确区分 `ACTIVE / HISTORICAL_OPEN / RESOLVED`。issue #12 已标记为 `HISTORICAL_OPEN`，只保留早期 silent-disable provenance 未解这一历史问题；当前 core monitor 缺席是用户明确删除，不允许从历史 issue 推导重建/重启。

`runtime/control_signal.py` 的 present-tense remediation guard 只有在 `ACTIVE + fresh reobservation + current authorization` 三者都满足时才允许当前状态修复；HISTORICAL_OPEN / RESOLVED 不能单独触发 remediation。

第一次重跑 M8（CI `38360013380` / job `115171721582`）出现 2 个真实回归：
1. lifecycle enum 转换实现错误，导致 ACTIVE 也被误判为不可 remediation；
2. handoff 压缩时误删 v65 回归锚点 `当前模型不是 PR-first`。

这两个问题均已在 M7 修正：enum 直接接受 `SignalLifecycleState` 实例；handoff 恢复 direct-main threat-model 锚点。现在重新进入 M8，必须重新跑 control-plane audit、Agent architecture harness、full pytest；任何失败继续 reopen。

## 其余已修项

- continuation bootstrap 与 all-material cheap defect preflight scope 已对齐；
- `NO_DEFECT` 不加载 full maintenance/global discovery；
- BUSINESS `adapter_status` 只保留 stable admission/protocol metadata，动态 CI/PASS/PENDING/LIVE assurance 被 validator 拒绝；
- A-share #2 已 live reobserve 后关闭；Financial #7 为 resolved；Novel #3 / Video #4 仍 active；
- ENTRYPOINT 保留 8,192-byte hard cap 且至少 512-byte reserve；
- current architecture synthetic admission fixtures 已跟随 `agent_manifest_ref` requirement。

## 主链边界

- single writer：lease_id + resume_epoch + stale-writer fail-closed；
- Universal material main writes：active lease + observed-HEAD CAS + CI + authoritative reread；
- bare inherit quorum 动态派生，partial discovery 不得伪装完整或 auto-resume；
- recovery：metadata → short handoff → exact refs → selective history → old chat last resort；Memory/chat 不是执行权威；
- lower-authority cache/evidence 不能覆盖 fresher authority；
- BUSINESS truth/lease 本轮不触碰。

## v65 direct-main / PR-first 回归锚点

当前模型不是 PR-first。

Universal material compliant writes 继续使用 active lease + observed-HEAD compare-and-swap + CI + authoritative reread。PR-first 和 branch protection 不是当前 `SINGLE_ACTIVE_CHAT` 的默认要求；unprotected `main` 本身不是 HIGH defect。

实验分支 `continuity/pr-first-mutation-gate-v65` 未 merge、无 PR、非 authoritative implementation。

## 仍 OPEN 的边界

- live automation 当前没有启用的 Continuity core monitors；不自动重建；
- `HARNESS_STATUS.json` 的旧 monitor 字段仍是 lower-authority historical cache；
- private owner CI runner 未实际执行的地方不能称 PASS；
- Financial fresh-chat DUAL 3-output retest 仍 owner-scoped OPEN；
- independent semantic/live-outcome assurance 与 formal controller-meta promotion 仍 OPEN；
- `__noop*` 非权威 branch clutter 仍 `OPEN_TOOL_LIMITED`，无 PR，当前 connector 无 delete-ref。
