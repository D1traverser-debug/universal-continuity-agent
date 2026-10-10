# 跨对话继承系统建设与维护｜Handoff

- task_id: `continuity:universal-continuity-maintenance`
- task_class: `SYSTEM_INFRA`
- owner: `UNIVERSAL_CONTINUITY_HARNESS`
- status: `ACTIVE`
- contract: `CONTINUITY_V3_7`
- methodology profile contract: `1.0`
- system-maintenance policy: `1.5`
- artifact/context governance: `1.1`
- execution-readiness contract: `1.0`

## Current truth
- 工程真源：`D1traverser-debug/universal-continuity-agent@main`。同聊天 lease 仍是 `lease-f266a907-aaf1-4b6a-a283-0e64b979d652`，`resume_epoch=1`；本轮没有 takeover。
- 产品传播链已完成双路径真实 E2E：existing-chat refresh PASS；fresh-chat bare-inherit discovery PASS。
- Universal composable methodology self-pilot 已完成；Video 已合法绑定 `artifact_io@1.0 + operational_hygiene@1.0` 且 owner regression PASS，但 central executable methodology conformance 仍待补。
- canonical bootstrap 仍为 `ENTRYPOINT.md -> CURRENT_PROTOCOL.json -> event-specific authority -> exact owner state`；`PROTOCOL.md` 是人类可读参考，不是固定热路径输入。
- 新的全局审计基线已进入 `SYSTEM_MAINTENANCE_POLICY.json` v1.5，并由 `runtime/system_audit.py` + CI preflight 机械执行；没有创建平行 `GLOBAL_AUDIT_POLICY`。

## Product E2E — PASS

### Existing chat
- 被测 owner/task：`VIDEO_GROWTH_AGENT` / `video-growth:main`，使用升级前已存在旧对话。
- 旧对话从当前 GitHub authority 重新读取 manifest/checkpoint、Skill 与 execution capabilities；不是根据聊天记忆猜测。
- task 从 legacy marker `3.5` 原地 reconcile 到 canonical `continuity_protocol_version=3.7`。
- `resume_epoch` 刷新前后均为 `2`；active lease 均为 `8e1bc149-5371-4476-ad94-66c8bee07d94`；没有制造 new-chat takeover。
- `current_stage=VISUAL_PREVIEW_PROCESS_REENTRY` 和业务 `next_action` 均未推进。
- Video owner CI：run `38037773281` / job `114171705917` / head `a6c1894667088f533771f3b0972aa1ae00ac0a1b`，84 tests + installed CLI smoke PASS。

### Fresh chat
- 真正全新的普通聊天首轮只发送裸 `继承`。
- `BARE_INHERIT_DISCOVERY.json` 规定的 5/5 required sources 均读取成功，完整 DEFAULT USER resumable 候选总数为 4。
- `SYSTEM_INFRA + EXPLICIT_ONLY` 与 `PAUSED + EXPLICIT_ONLY` 被正确排除。
- 首轮只列候选，没有选择业务 task、没有 takeover，回执 `NO_MATERIAL_CHANGE`。
- 公开 harness 只持久化数量/验收结果，不持久化 live candidate names/task ids。

## Global system audit — risk-tiered model ACTIVE

本轮明确拒绝“每次全跑所有项目/业务流水线”作为默认总控检查方案。原因：它会把 Continuity 变成巨型业务编排器，引入实时数据/模型/provider 假失败、增加 owner/lease 干扰和上下文成本，而且并不能更好覆盖 unknown-unknown。

采用五层模型：

1. `CORE_ALWAYS`：每次 CI/物质维护闭环必跑核心跨表面一致性。
2. `IMPACT_SCOPED`：按本次改动面检查直接依赖、runtime/tests、owner 指针。
3. `OWNER_SENTINEL_ROTATION`：需要额外置信度时轮换读 owner 元数据，不执行业务、不抢 lease。
4. `FULL_CONTROL_PLANE`：协议、authority、startup/discovery、storage/artifact、methodology/execution contract、跨 owner 迁移、系统事故、重大 release 或显式深审计时触发。
5. `SYNTHETIC_FAULT_INJECTION`：高风险边界用 deterministic/non-production 负向 fixture；默认不在生产业务状态上注入破坏。

语义权威：`SYSTEM_MAINTENANCE_POLICY.json` v1.5。执行器：`runtime/system_audit.py`。详细审计证据：`audits/GLOBAL_SYSTEM_AUDIT_2026-10-10.md`。

## Concrete defects found and repaired

1. `OWNER_PROTOCOL_ADAPTATION_REGISTRY.json` 漂移：Financial/Video 已实际 v3.7，registry 仍写历史协议 pending；已拆分 historical protocol 与 current observed protocol 并同步为 compatible。
2. Financial 悬空引用：registry 指向不存在的 `continuity/HANDOFF_COMPACTION_PLAN.json`；已换成实际当前 `continuity/tasks/financial-writing-main/HANDOFF.md`。
3. `OWNER_REGISTRY.json` reconciliation status 漂移；已同步。一次无结构变化的 3.1 schema bump 被回归测试拒绝，最终保持 schema 3.0。
4. README 漂移：旧文档仍写 `ENTRYPOINT -> PROTOCOL` 和 Library bootstrap pointer；已改成 `ENTRYPOINT + CURRENT_PROTOCOL` minimal bootstrap，并明确外部 store 非隐式 control-plane authority。
5. system-maintenance policy 升到 1.5 后 task manifest 仍写 1.4；新的 CI preflight 主动打红并阻断 pytest，状态已同步。
6. 初版 local audit 存在“两个 stale cache 互相证明”的循环验证缺口；负向 fixture 打红后，现改为利用已验证 existing-chat product E2E 作为独立 witness，不能再仅靠两个派生缓存相互认证。

## Regression / audit evidence

- run `38039484874` / job `114176702308` / head `00781136f9d729efbd07b0171d09ae90ddb7be10`：system-audit preflight FAIL，准确抓到 task manifest 的 `system_maintenance_policy_version` 仍为 1.4。检查未被弱化。
- run `38039596056` / job `114177014133` / head `cb503dc17133ee6a8c01fd7c7ca03034ce2b934c`：preflight PASS，但 pytest 2 failures，分别暴露无必要 schema bump 与 circular cache validation。测试未被删改来“求绿”。
- run `38039769573` / job `114177507423` / head `fc6de3b4d43b81b68a3df43974fd7c3ba4019204`：system-audit preflight PASS，`110 passed in 0.18s`。
- 本 Handoff、HARNESS_STATUS、审计记录和最终 stage 更新属于 closure metadata；当前 turn 结束前仍必须在最终 current-main 再跑一次 CI，才能报告 `COMMITTED`。

## Full owner metadata sweep

本次显式深审计已读 4 个 durable business owner 的当前 metadata/authority pointers，没有执行其业务流水线，也没有抢 lease：

- Financial Writing：active v3.7 manifest、compact Handoff、Universal adapter、execution capabilities 均可达；旧悬空 compaction ref 已清理。
- A-share：recommendation manifest v3.7、task index、adapter、execution capabilities 可达；未跑 market-day/live-data 业务动作。
- Novel：active project manifest v3.7、task index、adapter、artifact governance、execution capabilities 可达；未修改小说业务状态。
- Video Growth：active task canonical 3.7、owner adapter、execution capabilities、checkpoint compaction plan 可达；profile refs=`artifact_io@1.0 + operational_hygiene@1.0`，`overrides={}`；checkpoint compaction 仍 defer 到合法 owner scope。

## Synthetic negative coverage boundary

已有 executable negative evidence：same-chat lease preservation、stale-writer rejection、unsupported protocol fail-closed、floating/missing/forbidden methodology profile rejection、COMMITTED-without-reread rejection、declared-only/session-unobserved executor blocking、isolated review cannot be same-chat roleplay、stale registry/circular-cache fixture。

仍属于 owner/provider boundary 的检查：具体 destructive file mutation transaction、具体 external artifact provider authority/identity、owner-local business artifact invalidation。Universal 只拥有 shared invariant/profile conformance，不能为了“全局测试”接管各 owner 的实际文件/业务操作；这些必须随 owner profile rollout 用 owner-specific regression/eval 验证。

## Remaining owner rollout
- Video Growth：`artifact_io@1.0 + operational_hygiene@1.0` 已绑定且 owner regression PASS；central `runtime/methodology_conformance.py` executable conformance 待补。
- Financial Writing：durable feedback capture 已 wired；methodology profile binding 待合法 owner turn。
- A股、Novel：profile/operational-hygiene conformance 待各自合法 maintenance/writer turn。
- legacy `owner_must_expose` compatibility mirrors 暂保留，直到所有支持 owner 迁移且 regression 证明无旧 reader。

## Current stage
`V3_7_PRODUCT_E2E_PASS__RISK_TIERED_GLOBAL_AUDIT_ACTIVE_CI_PASS__OWNER_PROFILE_MIGRATION_IN_PROGRESS`

## Next action
1. 先保持 `runtime/system_audit.py` CI preflight 为常驻核心门；普通变更不机械全跑 owner business pipelines。
2. 补 Video central methodology conformance，并保持 Video owner regression PASS。
3. 在 Financial Writing / A股 / Novel 合法 owner turn 做 thin exact-version profile binding + owner-specific regression/eval。
4. owner rollout 时补 artifact-operation 的 owner-local executable evidence；如果 profile 只增加配置/重复而未降低漂移与上下文负担，则拒绝推广或回退。
5. 无 scheduler/event-watch infrastructure 时，不声称聊天关闭后的离线持续自维护。

## Recovery rule
恢复本系统任务时先读 `TASK_MANIFEST.json` + 本 Handoff，再按 `ENTRYPOINT.md` 的事件驱动矩阵加载所需 authority；不要机械预读全部 policy/audit，也不要从聊天记忆重建执行真相。
