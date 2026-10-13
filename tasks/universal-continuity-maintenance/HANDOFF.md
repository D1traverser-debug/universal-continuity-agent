# 跨对话继承系统建设与维护｜Handoff

- task_id: `continuity:universal-continuity-maintenance`
- task_class: `SYSTEM_INFRA`
- owner: `UNIVERSAL_CONTINUITY_HARNESS`
- status: `ACTIVE`
- current_stage: `SYSTEM_MAINTENANCE_ACTIVE`
- current writer lease: `lease-8ecdf71e-46b3-4e7d-b2ea-61ee05c6d654`
- resume_epoch: `8`
- manifest_version: `86`
- completed controller run: `universal-global-control-plane-audit-v67-2026-10-13`
- controller status: `COMPLETE` revision `27`
- final audit: `audits/UNIVERSAL_GLOBAL_CONTROL_PLANE_AUDIT_V67_FINAL_2026-10-13.json`
- final M8 validation: GitHub Actions `38360434605` / job `115173076661` — control-plane audit PASS, Agent architecture PASS, full pytest PASS

## v67 全局审计结论

本轮按用户要求检查了 Universal 自身的入口、执行、工作流、竞争/并发、冲突、遗忘/恢复、废旧/影子机制、覆盖/绕过、调用、继承、状态权威、CI/测试、跨 owner 边界和外部产品状态。

不是“扫一遍然后说没问题”。本轮真实发现并修复：

1. **入口/启动范围漂移**：显式 continuation bootstrap 仍只由继续/继承意图触发；所有 material input 只先做便宜的三态 defect preflight。`NO_DEFECT` 不加载 full maintenance，也不做 global discovery。机器合同和 hot-path prose 已对齐。
2. **membership authority 混入动态 assurance**：BUSINESS `adapter_status` 现在只表示稳定 admission/protocol metadata。CI PASS/FAIL、PENDING、LIVE/current quality 等动态状态不得写回 `OWNER_REGISTRY.json`，validator 会 fail closed。
3. **control signal 生命周期过粗**：当前使用 `ACTIVE / HISTORICAL_OPEN / RESOLVED`。A-share #2、Financial #7 是 RESOLVED；Novel #3、Video #4 是 ACTIVE；monitor #12 是 HISTORICAL_OPEN，只保留历史 silent-disable provenance 未解，不是当前 drift。
4. **历史 issue 驱动当前操作的风险**：`runtime/control_signal.py` 只允许 `ACTIVE + fresh reobservation + current authorization` 驱动 present-tense remediation；HISTORICAL_OPEN/RESOLVED 不能单独触发重建、重启或当前状态修改。
5. **ENTRYPOINT 热路径余量过窄**：没有放宽 8,192-byte hard cap，而是压缩并加 >=512-byte reserve regression，同时保留 methodology、defect triage、mid-turn checkpoint、persistence assurance 等既有语义锚点。
6. **版本指针滞后**：maintenance manifest 的 control-signal contract pointer 已跟随 1.2。

## 验证过程不是形式 PASS

本轮有四次真实 reopen：
- 第一版 M8：`303 passed / 7 failed`；
- historical-open 第一版：`310 passed / 2 failed`；
- 再修后：`311 passed / 1 failed`；
- 最终 M8：control-plane audit、Agent architecture harness、full pytest 全部 PASS。

因此这些 regression 没有被“解释过去”；controller 实际回退到 M7 修复后才重新验证。

## 当前确认成立的主链

- **入口**：Continuity bootstrap 从 `ENTRYPOINT.md + CURRENT_PROTOCOL.json` 最小启动；BUSINESS 产品维持一个 ChatGPT owner/Skill 入口，executor/readiness 是系统内部选择，不是第二套业务 SOP。
- **执行/调用**：声明能力只是 ceiling，不是当前执行证明；material owner action 仍需 exact capability/readiness/methodology evidence。
- **工作流**：systemic maintenance 由 M0→M11 controller fail closed；业务 workflow/state 仍归业务 owner。
- **竞争/并发**：`SINGLE_ACTIVE_CHAT` 下 lease_id + resume_epoch + stale-writer fail-closed；Universal material main mutation 使用 active lease + observed-HEAD CAS + CI + authoritative reread。
- **冲突/覆盖**：engineering authority、durable task state、business evidence、cache、scratch、external ref、Memory/chat 分层；低权威不能覆盖更新的高权威。
- **遗忘/恢复**：metadata → short handoff → exact refs → selective history → old chat last resort；Memory/chat 不是执行权威。
- **继承**：bare inherit quorum 从 `OWNER_REGISTRY.json` 动态派生；缺任一 required source 即 `INCOMPLETE_DISCOVERY`，partial 不得声称完整，也不得 auto-resume。
- **协议迁移**：不能借 reconciliation 修改业务 stage/status/next_action/lease。

## 当前仍 OPEN，但不是隐藏 PASS

- `HARNESS_STATUS.json` 的 monitor 字段仍是 lower-authority historical cache；当前 product live reread优先。安全全量 cache rebuild 仍是 cleanup。
- Novel #3、Video #4 仍是 owner-local hot-path drift；Universal 不越权取得 BUSINESS lease 去修。
- issue #12 的历史 silent-disable provenance 仍不可观测；当前 monitor 缺席是用户明确删除，不是 recurrence。
- Financial fresh-chat DUAL 3-output business retest 仍由 Financial owner 完成。
- private owner CI runner 没有真实执行的地方仍是 UNVERIFIED，不称 PASS。
- independent semantic/live-outcome assurance 仍 `OPEN_OPERATOR_DEPENDENCE_LIVE_HELDOUT_GRADER_REQUIRED`。
- formal controller-meta promotion 仍 OPEN。

## 废旧 / branch 边界

当前模型不是 PR-first。

Universal material compliant writes 继续使用 active lease + observed-HEAD CAS + CI + authoritative reread。PR-first 和 branch protection 不是当前 `SINGLE_ACTIVE_CHAT` 的默认要求；unprotected `main` 本身不是 HIGH defect。

实验分支 `continuity/pr-first-mutation-gate-v65` 没有 merge，也不是 authoritative implementation；没有 PR，也从未成为 `main` 权威实现。

本轮工具探测时误创建的 `__noop`、`__noop2`、`__noop3`、`__noop4`、`__noop5` 也是非权威 branch clutter，无 PR、未进入 main。当前 connector 没有 delete-ref primitive，因此 cleanup 明确为 `OPEN_TOOL_LIMITED`，不得假称已删除。

## Assurance ceiling

这次 COMPLETE 表示：声明范围内的结构、当前 owner heads、signal 生命周期和 live automation surface 已完成有边界的审计、修复和回归验证。它不表示“系统永远不会再有未知缺陷”，也不表示 BUSINESS 的实时质量/结果已被独立证明。
