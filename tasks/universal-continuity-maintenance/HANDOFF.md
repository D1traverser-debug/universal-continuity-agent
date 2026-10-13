# 跨对话继承系统建设与维护｜Handoff

- task_id: `continuity:universal-continuity-maintenance`
- task_class: `SYSTEM_INFRA`
- owner: `UNIVERSAL_CONTINUITY_HARNESS`
- status: `ACTIVE`
- current_stage: `SYSTEM_MAINTENANCE_ACTIVE`
- current writer lease: `lease-8ecdf71e-46b3-4e7d-b2ea-61ee05c6d654`
- resume_epoch: `8`
- manifest_version: `83`
- current controller run: `universal-global-control-plane-audit-v67-2026-10-13`
- controller status: `ACTIVE` revision `19` at `M8_MULTI_LAYER_VALIDATION`

## 当前状态

v67 的第二次 reopen 已完成 M7 修复。此前 M10 发现 control signal 只有 active/resolved 二分不够：issue #12 仍 open 只是因为历史 silent-disable provenance 未解，而当前 core monitor 缺席是用户明确主动删除。若未来 consumer 只看 open issue，可能把历史 unresolved incident 误当当前 drift。

现已加入 `ACTIVE / HISTORICAL_OPEN / RESOLVED` 三态语义：
- #3 / #4 = ACTIVE owner-local drift；
- #12 = HISTORICAL_OPEN，仅保留历史 provenance 问题，不允许单独触发当前 remediation；
- #2 / #7 = RESOLVED historical evidence。

`runtime/control_signal.py` 新增机械 guard：只有 `ACTIVE + fresh reobservation + current authorization` 才允许当前 state remediation；HISTORICAL_OPEN / RESOLVED 均不能因为 issue 仍存在就触发重建、重启或其他 present-tense 修复。issue #12 的 title/body 已同步改成 `[HISTORICAL_OPEN]` 并显式写明当前用户删除意图优先。

同时保留本轮此前修复：startup/preflight scope 对齐、OWNER_REGISTRY dynamic assurance 清理与 validator、A-share #2 关闭、ENTRYPOINT >=512-byte reserve、current architecture admission fixture 对齐。

## 下一步

M8：重新跑 risk-tiered/full control-plane audit、Agent architecture harness、full pytest。任何失败都 reopen。

M8 绿后必须重新做 M9 owner-head/signal live reobservation，再做 M10 second-order review；reopen 前的 M8/M9 receipts 不可复用。最后 M11 closure 后还要观察 closure commit 的 CI 并 reread `main + TASK_MANIFEST + controller state` 才能报 `COMMITTED`。

## 保留边界

- 不取得 BUSINESS lease，不改文章、市场日、小说 Canon/project、视频项目业务真值。
- live automations 当前没有启用的 Continuity core monitors；不自动重建。
- `HARNESS_STATUS.json` 仍是 lower-authority historical cache，不能覆盖 live product reread。
- private owner CI runner 未实际执行的地方不能称 PASS。
- Financial fresh-chat DUAL 3-output retest 仍 owner-scoped OPEN。
- independent semantic/live-outcome assurance 与 formal controller-meta promotion 仍 OPEN。
- `__noop*` 非权威 branch clutter 仍 `OPEN_TOOL_LIMITED`，无 PR，当前 connector 无 delete-ref。
