# 跨对话继承系统建设与维护｜Handoff

- task_id: `continuity:universal-continuity-maintenance`
- task_class: `SYSTEM_INFRA`
- owner: `UNIVERSAL_CONTINUITY_HARNESS`
- status: `ACTIVE`
- contract: `CONTINUITY_V3_7`
- current_stage: `SYSTEM_MAINTENANCE_ACTIVE`
- current writer lease: `lease-8ecdf71e-46b3-4e7d-b2ea-61ee05c6d654`
- resume_epoch: `8`
- manifest_version: `82`
- current controller run: `universal-global-control-plane-audit-v67-2026-10-13`
- controller status: `ACTIVE` revision `18`, M10 second-order review reopened to `M7_IMPLEMENTATION_AND_SUPERSESSION`

## M10 新发现：open 不等于 current drift

第二次 M8 已全绿，M9 也完成 fresh owner-head/signal reobservation。但 M10 继续查 control-signal 生命周期时发现：历史 issue #12 **仍然 OPEN**，只因为早期 silent enabled→disabled 的 provenance 仍无法解释；当前核心 monitor 的缺席则是用户后来明确主动删除。

issue #12 的 comments 已明确“不得自动重建/重启”，但 issue 原始 title/body 仍是过去的 present-tense incident 描述。只靠 `active / resolved` 二分，会让未来只读 issue 主体的 consumer 把这个 historical unresolved incident 误判成当前 drift，进而错误建议恢复 monitor。

因此本轮再次真实 reopen：新增 `HISTORICAL_OPEN` 语义。预期状态为：
- #3 / #4：`ACTIVE`，当前 owner-local drift；
- #2 / #7：`RESOLVED`，历史证据；
- #12：`HISTORICAL_OPEN`，历史 provenance 未解，但**不得作为当前 remediation trigger**，除非重新观察到与当前用户意图冲突的新 product-state drift。

M7 将更新 `CONTROL_SIGNAL_CONTRACT.json`、task manifest signal sets、issue #12 的标题/主体 current-state banner，并加入 regression。随后必须重新跑 M8/M9/M10，不能沿用 reopen 前的 validation/propagation receipts。

## 此前已验证的修复仍保留

- continuation bootstrap 与 cheap defect preflight scope 对齐；
- OWNER_REGISTRY 不承载 mutable CI/PASS/PENDING/LIVE assurance；
- A-share #2 已 live reobserve 后关闭；
- control-signal contract pointer 已对齐；
- ENTRYPOINT 在恢复全部既有语义 anchors 后仍保留 >=512-byte headroom；
- synthetic new-owner fixtures 已跟随当前 `AGENT_ARCHITECTURE_CONTRACT` 的 `agent_manifest_ref` admission requirement，而不是削弱 validator。

## 其余边界

- lease/resume_epoch/CAS/stale-writer fail-closed 未发现新缺陷。
- bare inherit quorum、incomplete discovery、artifact authority layering、Memory/chat 非执行权威、内部 executor routing 仍成立。
- private owner CI 未执行的地方不能称 PASS；Financial fresh-chat DUAL 3-output retest 仍 owner-scoped OPEN。
- HARNESS_STATUS 历史 monitor cache 仍 lower-authority；live product reread优先。
- `__noop*` 非权威 branch clutter 仍 `OPEN_TOOL_LIMITED`，无 PR，当前 connector 无 delete-ref。

## v65 direct-main / PR-first 回归锚点

当前模型不是 PR-first。

Universal material compliant writes 继续使用 active lease + observed-HEAD CAS + CI + authoritative reread；`main protected=false` 本身不是当前 `SINGLE_ACTIVE_CHAT` 威胁模型下的 HIGH defect。

实验分支 `continuity/pr-first-mutation-gate-v65` 没有 merge，也不是 authoritative implementation。
