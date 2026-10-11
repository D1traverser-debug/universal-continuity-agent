# 跨对话继承系统建设与维护｜Handoff

- task_id: `continuity:universal-continuity-maintenance`
- task_class: `SYSTEM_INFRA`
- owner: `UNIVERSAL_CONTINUITY_HARNESS`
- status: `ACTIVE`
- contract: `CONTINUITY_V3_7`
- current writer: `lease-4812a7a8-83cf-414d-87e9-198a60a9cfeb`
- resume_epoch: `6`
- manifest_version: `53`
- system maintenance policy: `1.7`
- meta-maintenance harness: `1.2`
- Agent architecture contract: `1.1`

## 当前阶段

`V3_7_AGENT_CONTROL_PLANE_V1_1_REGRESSION_VERIFIED__GLOBAL_LIVE_OWNER_REOBSERVATION_V51_PASS__VIDEO_SHARED_ARCHITECTURE_VERSION_DRIFT_REPAIRED__OWNER_REGISTRY_MEMBERSHIP_OBSERVATION_SEPARATION_REGRESSION_VERIFIED__ARCHITECTURE_WATCH_HOURLY__TOP10_SELECTED_PRIMITIVES_REGRESSION_VERIFIED__OWNER_DRIFT_SIGNALS_OPEN__OPERATOR_DEPENDENCE_LIVE_EVIDENCE_OPEN__PRIOR_LIVE_EVIDENCE_GATES_OPEN`

本聊天已完成真实新聊天 takeover（`resume_epoch 5 -> 6`）；当前 lease 仍是本聊天。主 `current_stage` 与权威 `TASK_MANIFEST.json` 保持一致。本轮 `PROACTIVE_EVOLUTION_OPERATIONALIZATION_REGRESSION_VERIFIED` 是该 ACTIVE 主阶段内已经闭环的 maintenance substage，不单独制造 manifest 版本或第二套阶段权威。

## 本轮主动进化 / Custom Instructions 修复

用户指出：总控多次升级后仍需要用户反复提醒其主动学习、全局检查和外部工具蒸馏；前一回复还把“GPT 个性化”错误理解成 Personality，而用户实际指的是 account-level Custom Instructions / startup hook。这被分类为系统性路由理解漂移 + declaration-to-operation gap，而不是单纯措辞问题。

本轮完成并验证：

1. **产品层假阳性被发现**：实际读取 automation state 后，`Agent Architecture Watch` 与 `Continuity Self Audit` 当时均为 disabled；这与仓库声明不一致，证明仓库状态不能替代产品执行事实。
2. **真实主动监控已恢复**：`Agent Architecture Watch` 已重新启用为 hourly condition watch，并改为先读当前 `CURRENT_PROTOCOL.json`、动态推导 BUSINESS owners，不硬编码 owner count/version。
3. **Self Audit 已恢复并去旧版本绑定**：`Continuity Self Audit` 已重新启用；旧 prompt 的 v3.6 硬编码已删除，现要求先读 current protocol，并检查 thin bootstrap、safe checkpoint、child inheritance、monitor enablement、policy-only mechanism、stale hard-coded versions、contradictory status 与 user-prompt-only learning。
4. **Learning Scout 已上线**：新增并启用 `Continuity Learning Scout`，周期扫描 OpenAI Skills/Agents 文档、`skills.sh` All Time/Trending/Hot、GitHub Agent Skills、MCP/tool catalogs、ChatGPT Plugin Directory 与小众 novelty lane。无 material change 不通知；候选不自动晋升 production authority。
5. **Custom Instructions 已去臃肿**：`STARTUP_HOOK.md` 已改为 `ACCOUNT_ROUTER_V2`，并由测试限制为 `<=4096B`。账户级文本只保留 pre-repository trigger、最小 bootstrap、旧对话覆盖、继承前进度/进度提交用户可见边界、fail-closed 与主动维护触发；owner/capability/methodology/learning/migration 的细节留在 current repository authority。
6. **持续学习从 policy-only 变成 operational contract**：`CONTINUOUS_LEARNING_POLICY.md` 新增 `Operational scout loop`，将 disabled scout、stale hard-coded version、仅用户提供候选后才学习定义为维护缺陷；规定来源覆盖、候选状态、deep-dive evidence floor、最多五个 unresolved deep dives、quiet-no-change 与 `evolution@1.0` child propagation。
7. **新增回归**：`tests/test_hot_path_loading.py` 防止账户 hook 再次膨胀/复制详细 capability routing；`tests/test_continuous_learning_policy.py` 验证 operational scout、deep-dive 标准、bounded queue 与 child inheritance。
8. **第一轮 proactive scout 已落证据**：`research/proactive-learning/2026-10-11-initial-scout.md`。Anthropic `skill-creator` 被分类为 `UNIVERSAL_CANDIDATE`，已追到 pinned Skill + runtime scripts，并抽取 Skill-vs-baseline、trigger precision/recall、repeated runs、train/test holdout、防过拟合与 cost/quality separation。`self-improving-agent` 直接架构采用被拒绝（OpenClaw-specific + markdown-memory authority 弱于现有模型）；`last30days` 与 `Understand Anything` 暂列 owner-local/monitor cold-path 候选。
9. **回读再发现 rebuildable cache 漂移并修复**：`HARNESS_STATUS.json` 原本仍写 `startup_hook_budget_bytes=8192`，且把最新 account hook 当作已确认；现已对齐为 `4096`，保留旧 hook 的历史产品证据，同时明确 `ACCOUNT_ROUTER_V2` 当前账户安装/实时文本未证明。三个产品自动机制的 `enabled` 与 `post-update first-run` 证据也已拆开，避免 enabled=执行过 的假阳性。

## 本轮验证闭环

- 薄化 `STARTUP_HOOK.md` 后 CI `38134906549`：control-plane audit PASS、Agent architecture harness PASS、pytest `2 failed, 243 passed`。失败指出旧对话覆盖与“继承前进度”仍属账户级最小用户可见契约。
- 第一次最小补回后 CI `38134970836`：同样只有 pytest 两个失败，进一步指出“进度提交”、`OWNER_REGISTRY.json`/historical-owner-count 动态边界仍需在薄 hook 保留最小表述。
- 没有删测试或放宽 hook 预算；只补回必要最小语义，详细算法仍不复制到账户 prompt。
- `ACCOUNT_ROUTER_V2` 最终修复 CI `38135016993`：risk-tiered control-plane audit PASS、Agent architecture harness PASS、完整 pytest PASS。
- closure Handoff commit CI `38135084642`：control-plane audit PASS、Agent architecture harness PASS、完整 pytest PASS。
- `HARNESS_STATUS` cache 对齐 commit `04fb412df24b1a0d36abc51a773b26da59b12e84` 的 CI `38135374647`：control-plane audit PASS、Agent architecture harness PASS、完整 pytest PASS。
- 产品 automation closure 回读：`Agent Architecture Watch`、`Continuity Self Audit`、`Continuity Learning Scout` 三者当前均 `is_enabled=true`。
- Assurance boundary：enabled/CI-green 证明 wiring 与当前结构回归，不证明新版 automation 已完成首次自然运行或长期质量收益。Learning Scout 尚无首次 run；更新后的 Self Audit/Architecture prompt 也需后续自然运行形成 execution evidence。

## 当前系统大纲能力边界

Universal 当前共享控制面覆盖：

1. thin bootstrap / intent routing；
2. durable task discovery / resume / single-writer lease / takeover；
3. intra-turn safe checkpoint / cross-chat recovery；
4. owner execution readiness / exact-action evidence binding；
5. composable methodology profiles (`artifact_io`, `operational_hygiene`, `evolution`)；
6. artifact/context authority / invalidation / destructive-mutation guards；
7. maintenance self-audit / risk-tiered CI / fault injection / second-order review；
8. state-vs-signal separation / owner architecture drift monitoring；
9. proactive learning / external Skill-tool discovery / distillation / promotion gates；
10. child-owner inheritance through shared contracts/profiles while BUSINESS truth remains owner-local。

这些是“常见失败类别的控制机制覆盖”，不是“已证明避免 90% 所有未来问题”。目前没有足够 held-out incident corpus 支持一个诚实的 90% 数字；若未来要声称 90%，必须用真实/held-out failure corpus 测得 coverage，而不是凭架构感觉。

## 当前 owner / assurance 状态

最近一次实际 re-observation 的 BUSINESS owner HEAD：

- Financial: `a76c83c917ae6c81ec398ef99749125131e6be2c`
- A-share: `f8ad4decde3adb0f3f87ed7019ce6e9f5981e07c`
- Novel: `7988b96c8be661a2f92bad96daac6322bcf664ef`
- Video: `977ad5329b1ffb1f971db922fac3e17bf91a412a`

这些与 v51 recorded observations 一致。共享 `evolution@1.0` 已提供 child inheritance 路径，但不能把“合同可继承”外推成“所有 owner live action 已证明采用/有效”。A-share / Novel / Video 的既有 thin-router / assurance drift 仍保持 OPEN。

## 当前已知 OPEN gates

1. 三个新版 recurring mechanisms 的 **post-update first-run / repeated-run execution evidence**；
2. account-level Custom Instructions **实际安装文本** 的 live readback/propagation：仓库维护 canonical `ACCOUNT_ROUTER_V2`，但当前可用工具不能把 repo 更新证明成账户设置已同步；
3. real new-owner fresh-chat product E2E；
4. operator-dependence independent heldout/live trajectory grader；
5. A-share / Novel / Video acknowledged router/assurance drift；
6. owner-local action-level methodology/evidence 与业务 live quality/outcome gates；
7. 通用 ChatGPT -> GitHub pre-write `WRITE_PATH_ENFORCED` 未建立；
8. “避免 >=90% 问题”的量化 coverage 尚无 held-out incident benchmark，不得声称已证明。

## Next action

保持 stop rule，不继续为“主动”制造新层。后续由已启用的 architecture/self-audit/learning scouts 产生的新 signal 驱动维护；首次新版 automation run 到来时，把真实 execution evidence 与当前声明对齐。

`skill-creator` 的 trigger/baseline/holdout primitive 仅保留为 production candidate；只有与现有 harness 对比证明缺口与增益后才实现，避免“看到优秀工具就复制”。跨-owner 通过证据门的机制走既有 `evolution@1.0` inheritance；owner-local candidate 不全局化。

## Recovery refs

- `tasks/universal-continuity-maintenance/TASK_MANIFEST.json`
- `tasks/universal-continuity-maintenance/HANDOFF.md`
- `ENTRYPOINT.md`
- `STARTUP_HOOK.md`
- `SYSTEM_BLUEPRINT.md`
- `SYSTEM_MAINTENANCE_POLICY.json`
- `CONTINUOUS_LEARNING_POLICY.md`
- `PROGRESS_OBSERVABILITY_POLICY.json`
- `OWNER_ADAPTER_CONTRACT.json`
- `OWNER_REGISTRY.json`
- `OWNER_ARCHITECTURE_OBSERVATIONS.json`
- `AGENT_ARCHITECTURE_CONTRACT.json`
- `research/proactive-learning/2026-10-11-initial-scout.md`
- `research/skill-library/2026-global-ai-skills-top10/README.md`
- `audits/META_MAINTENANCE_TAKEOVER_V53_2026-10-11.json`
- `audits/META_MAINTENANCE_GLOBAL_SELF_AUDIT_V51_2026-10-11.json`
- `audits/AGENT_ARCHITECTURE_GLOBAL_SELF_AUDIT_V51_2026-10-11.json`
- `HARNESS_STATUS.json`
