# 跨对话继承系统建设与维护｜Handoff

- task_id: `continuity:universal-continuity-maintenance`
- task_class: `SYSTEM_INFRA`
- owner: `UNIVERSAL_CONTINUITY_HARNESS`
- status: `ACTIVE`
- contract: `CONTINUITY_V3_7`
- current writer: `lease-2c5946fb-3d78-4a23-9440-2df7d41817ec`
- resume_epoch: `5`
- manifest_version: `51`
- system maintenance policy: `1.7`
- meta-maintenance harness: `1.2`
- Agent architecture contract: `1.1`

## 当前阶段

`V3_7_AGENT_CONTROL_PLANE_V1_1_REGRESSION_VERIFIED__GLOBAL_LIVE_OWNER_REOBSERVATION_V51_PASS__VIDEO_SHARED_ARCHITECTURE_VERSION_DRIFT_REPAIRED__OWNER_REGISTRY_MEMBERSHIP_OBSERVATION_SEPARATION_REGRESSION_VERIFIED__ARCHITECTURE_WATCH_HOURLY__TOP10_SELECTED_PRIMITIVES_REGRESSION_VERIFIED__OWNER_DRIFT_SIGNALS_OPEN__OPERATOR_DEPENDENCE_LIVE_EVIDENCE_OPEN__PRIOR_LIVE_EVIDENCE_GATES_OPEN`

同聊天继续维护；保持 epoch `5` 与当前 lease，不伪造 takeover。

## v51 为什么触发

用户追问“系统到底运用上没有、有没有全局自检、需不需要改 GPT 个性化”，按 `SYSTEM_MAINTENANCE_POLICY` 属于对维护完整性与 instruction surface 的实质挑战，因此不能只引用 v50 CI。执行了真实的跨仓远端 re-observation，并把“用户再次提醒”继续记为 operator-dependence 负证据。

## v51 全局实时检查打出的真实问题

1. **远端 observation cache 陈旧**：Financial 仍在既有 HEAD；A-share、Novel、Video 的 `main` 都已前进，但 `OWNER_ARCHITECTURE_OBSERVATIONS.json` 仍绑定旧 HEAD。Universal 本地 CI 本来就声明无法自行发现 sibling private repo 的更新，因此旧绿灯不能冒充实时全局 freshness。
2. **Video 共享架构版本漂移**：Video 当前 owner-local CI 为绿，但 `continuity/AGENT_MANIFEST.json` 宣告 `architecture_contract_version=1.2`；Universal 当前共享合同只支持 `1.0/1.1` 并要求未知未来版本 fail closed。这证明 owner CI ≠ Universal shared-contract conformance。
3. **membership authority 混入 rebuildable cache**：`OWNER_REGISTRY.json` 的 Novel 行曾嵌入 `observed_skill_version / observed_runtime_version / observed_owner_head`，而这些字段已经变旧；这违反“OWNER_REGISTRY 只拥有 membership，远端 observation 属于 rebuildable cache”的 authority 边界。
4. **主动监测太慢**：已有 `Agent Architecture Watch` 是 daily condition watch，在 owner 活跃开发期会留下数小时盲区。

## 已执行修复

- Video：只把共享 `architecture_contract_version` 从不受支持的 `1.2` 调回中央支持的 `1.1`；保留 owner-local `schema_version=1.2`、runtime 0.5.2、项目/任务/lease/业务证据不动。
  - commit `977ad5329b1ffb1f971db922fac3e17bf91a412a`
  - owner CI `38129311234` = SUCCESS。
- Universal：`runtime/owner_topology.py` 新增 fail-closed guard，禁止 `observed_*` / `architecture_validation_*` rebuildable 远端 observation 重新进入 `OWNER_REGISTRY`。
- `OWNER_REGISTRY.json` 删除 Novel stale observed fields，并显式声明 `rebuildable_remote_observations_allowed=false`、专用 cache=`OWNER_ARCHITECTURE_OBSERVATIONS.json`。
- 新增 `tests/test_owner_registry_authority.py`，覆盖当前态与 adversarial reintroduction。
- 刷新 `OWNER_ARCHITECTURE_OBSERVATIONS.json` 到四个 owner 的当前真实 HEAD/CI；A-share、Novel、Video 的 acknowledged drift 继续保留，不假装 PASS。
- 更新 #2/#3/#4 control signals 到当前 owner HEAD；signal 仍是 non-authoritative，不是 task authority/lease。
- `Agent Architecture Watch` 从 daily 提升为 **hourly condition watch**；仍禁止业务状态 mutation/lease takeover。平台用户通知 delivery 目前 disabled 或未证明，所以不声称能主动弹通知，但 durable GitHub signal emission 已有证据。

## 当前 live owner observation

- Financial: `a76c83c917ae6c81ec398ef99749125131e6be2c`，Skill 5540B，architecture PASS，CI `38108186593` SUCCESS。
- A-share: `f8ad4decde3adb0f3f87ed7019ce6e9f5981e07c`，Skill 8272B，仍高于 8192B 目标 80B，CI `38108652297` SUCCESS，状态 `PASS_WITH_DRIFT`。
- Novel: `7988b96c8be661a2f92bad96daac6322bcf664ef`，Skill 19540B，CHAT_BRIDGED assurance 未升级，CI `38110065043` SUCCESS，状态 `PASS_WITH_DRIFT`。
- Video: `977ad5329b1ffb1f971db922fac3e17bf91a412a`，Skill 9310B，共享 architecture contract 已重新对齐 1.1，strict isolated-review assurance 仍 OPEN，CI `38129311234` SUCCESS，状态 `PASS_WITH_DRIFT`。

## Universal 验证

v51 预 checkpoint HIGH-risk integrated run：

- Universal HEAD: `940b7a5e76a0f178ac40dfbc90438e1050706a18`
- Actions run: `38129508719`
- job: `114440713163`
- modes: `FULL_CONTROL_PLANE + SYNTHETIC_FAULT_INJECTION`
- local system audit: PASS
- synthetic fault injection: PASS, zero failed
- Agent Architecture harness: PASS with only acknowledged A-share / Novel / Video drift warnings
- all current BUSINESS owners in metadata scope
- pytest: `240 passed in 0.69s`

注意：这个 CI 自己仍明确写着 remote freshness boundary；实时远端 HEAD 是由本轮 maintenance runner 额外 re-observe 后写入 audit/cache 的，不能反过来说“CI 自动扫描所有 private sibling repos”。

本轮完整 meta-run：`audits/META_MAINTENANCE_GLOBAL_SELF_AUDIT_V51_2026-10-11.json`。实时结构审计：`audits/AGENT_ARCHITECTURE_GLOBAL_SELF_AUDIT_V51_2026-10-11.json`。

## GPT Personality / Custom Instructions 边界

- **Personality 不是 control plane。** 本轮根据用户对回复方式的反馈，ChatGPT Personality 已切换为官方预设 `高效务实`；它只影响表达风格，不承担 CONTINUE routing、Agent execution 或 evidence authority。
- **真正影响新聊天裸“继承/继续”的是 account-level Custom Instructions / 等价 product routing surface。** `STARTUP_HOOK.md` 仍是 canonical compact rule，本轮没有理由继续膨胀它。
- 历史状态记录表明该 account hook 曾由用户确认过；但当前可用设置接口不能实时读取/改写 Custom Instructions 文本，所以 v51 不重新声称“当前账户里的文字已经核验”。若产品侧文本被用户/平台改过，需要重新对照 `STARTUP_HOOK.md`；仓库本身不能证明传播。

## 当前 assurance ceiling

本轮达到：**LIVE REMOTE STRUCTURAL RE-OBSERVATION + OWNER CI + UNIVERSAL REGRESSION VERIFIED**。

仍不等于：

- `ACTION_LEVEL_INDEPENDENTLY_VERIFIED`；
- `LIVE_OUTCOME_VERIFIED`；
- account-level Custom Instructions 当前文本已实时读取；
- operator-dependence 已解决；
- 全系统无缺陷。

## 仍 OPEN

1. real new-owner fresh-chat product E2E；
2. operator-dependence independent heldout/live trajectory grader；
3. A-share 80B thin-router drift；
4. Novel thin-router drift + CHAT_BRIDGED ceiling；
5. Video thin-router drift + strict isolated reviewer / live provider / generation-gateway assurance gaps；
6. owner-local action-level methodology/evidence 与各业务 live quality/outcome gates；
7. 通用 ChatGPT→GitHub pre-write `WRITE_PATH_ENFORCED` 仍未成立。

## Next action

保持小时级 architecture watch 与 membership/cache separation；未来 owner HEAD 漂移时自动 re-observe 并更新 non-authoritative signal。只有唯一 authority 和兼容结论明确时才做 metadata-only repair；绝不借 Universal maintenance 偷 business lease。真实新 owner、真实 owner action、operator-dependence heldout/live trajectory 出现时再升级对应 evidence。没有新证据/缺陷时遵守 stop rule，不制造额外层。

## Recovery refs

- `tasks/universal-continuity-maintenance/TASK_MANIFEST.json`
- `audits/META_MAINTENANCE_GLOBAL_SELF_AUDIT_V51_2026-10-11.json`
- `audits/AGENT_ARCHITECTURE_GLOBAL_SELF_AUDIT_V51_2026-10-11.json`
- `OWNER_REGISTRY.json`
- `OWNER_ARCHITECTURE_OBSERVATIONS.json`
- `runtime/owner_topology.py`
- `tests/test_owner_registry_authority.py`
- `AGENT_ARCHITECTURE_CONTRACT.json`
- `STARTUP_HOOK.md`
- `HARNESS_STATUS.json`

不要把 `COMMITTED`、Personality、owner CI、Universal CI、结构化 Harness 或实时 structural re-observation 外推成 live business quality、independent semantic correctness 或 global flawlessness。
