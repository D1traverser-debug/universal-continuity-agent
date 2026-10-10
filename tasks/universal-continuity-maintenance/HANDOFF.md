# 跨对话继承系统建设与维护｜Handoff

- task_id: `continuity:universal-continuity-maintenance`
- task_class: `SYSTEM_INFRA`
- owner: `UNIVERSAL_CONTINUITY_HARNESS`
- status: `ACTIVE`
- contract: `CONTINUITY_V3_7`
- current writer: `lease-4b4bc507-0949-4b2e-aed4-c0186dd07566`
- resume_epoch: `2`
- manifest_version: `38`

## 当前阶段

`V3_7_META_GOVERNANCE_HARNESS_REGRESSION_VERIFIED__SYSTEMIC_MAINTENANCE_OUTLINE_ACTIVE__PRIOR_LIVE_EVIDENCE_GATES_OPEN`

这不是“整个系统无误”的状态。它只表示：本轮暴露出的 **repair-first / self-review / user-correction assimilation / instruction-impact / propagation / complexity-efficiency / premature-closure** 治理缺口已经形成新的规范层 + 确定性过程验证层，并达到 `REGRESSION_VERIFIED`。独立语义/产品效果证据仍按各自 gate 保持 OPEN。

## 这轮为什么重新打开维护

用户连续指出：过去即使总控能挑刺、学习、跑 CI，维护仍容易按“收到问题 → 自己闷头修 → 绿灯 → 说好了”的旧路径推进，缺少默认且显式的：

- 用户修正/需求变化的分类与吸收；
- 全系统 impact map；
- 是否需要外部学习/逆向/蒸馏工具的决策；
- 是否应该修改 GPT/account/startup instruction 的专门判断；
- 子系统是否真正继承、是否存在 stale override/shadow copy；
- 复杂度、上下文、工具调用、延迟、迁移成本和臃肿审查；
- 修复后对“全局没问题/未来问题都考虑过”的 claim calibration。

这不是用户方案自动成为架构命令。它被分类为：`GOAL_OR_CONSTRAINT + COUNTEREXAMPLE_OR_FAILURE_REPORT + PROPOSED_MECHANISM`，然后重新比较架构候选。

## 外部学习 / 逆向结果

Durable machine-readable record：`audits/META_MAINTENANCE_GOVERNANCE_RUN_2026-10-11.json`。

实际检查并蒸馏的模式包括：

- OpenAI tracing / agent eval：执行 trace 与 grader/eval 分离；不要从声明推断“真的执行过”。
- Anthropic agent evals / long-running harness：用 eval 和 durable progress artifact 代替生产后被动补洞；跨 context 由 harness 管持久进度。
- Anthropic Agent Skills：progressive disclosure，复杂方法按事件加载，避免把完整方法塞进常驻 prompt。
- mini-SWE-agent：真实实现保持 agent/harness 极简，同时保留 trajectory、step/cost/time limit 与可回放 observation；“层更多”不是成熟度指标。
- GEPA / DSPy 类 optimizer：只有在可靠 evaluator + train/heldout 数据存在时才适合自动优化 prompt/code/agent architecture；当前不把它们升级成总控架构权威，避免 Goodhart/过拟合。
- OpenAI Prompt Optimizer：吸收“优化前后必须 eval/人工复核”的纪律，但不把 prompt optimizer 作为当前核心依赖，也不允许用 prompt 增长掩盖 runtime/eval 缺陷。

外部方法没有整套照搬；每一项都记录 ADOPT / NARROW 及本系统失败模式映射。

## 架构候选与结论

比较了三种：

1. **只继续扩 `SYSTEM_MAINTENANCE_POLICY`** → REJECTED as complete solution。规范必要，但维护者仍可自己跳步骤、自己解释完成。
2. **再建一个上层 LLM Meta Agent** → REJECTED FOR NOW。当前没有 distinct executor / trace / held-out measured lift；新增角色名会重演 self-attestation inflation，并增加协调/context 成本。
3. **规范层 + deterministic Meta-Governance Harness + 现有独立 grader/live gate** → ACCEPTED。

职责分离：

- `SYSTEM_MAINTENANCE_POLICY.json`：规范 authority；
- `runtime/meta_maintenance.py`：窄职责、确定性过程完整性 verifier；
- 独立 trajectory grader / distinct evidence verifier / real outcome：真正语义与效果保证。

Meta Harness PASS 的保证上限固定为：`STRUCTURED_PROCESS_CONFORMANCE_ONLY`。它不能证明同一模型没有事后补写 run，也不能证明研究/诊断/架构判断语义正确。

## SYSTEM_MAINTENANCE_POLICY 1.6

默认 systemic/non-trivial maintenance 现在显式经过：

`signal classification → failure/impact model → learning scout → alternatives/falsification → instruction-surface decision → complexity/efficiency budget → minimum implementation → multi-layer validation → cross-subsystem propagation → second-order challenge → durable learning/checkpoint`

关键新增边界：

- 一次 material user correction 即可触发 system-impact review；不需要等用户重复三次。
- user goal/constraint 是高权威输入；user proposed mechanism 不是默认架构权威。
- systemic/architecture change 默认要求 learning scout；local deterministic bug 可 `NOT_REQUIRED_WITH_REASON`。
- prompt/account instruction 不是默认修法；先判断根因层。
- shared control-plane change 必须从当前 owner registry 推导 impacted owners 并扫 stale override/shadow logic。
- nontrivial control-plane change 必须评估 authority surface、startup context、tool/remote reads、steady-state latency、duplicate rule、cross-owner touch、migration/test burden。
- 禁止声称 global system error-free、所有未来 failure class 已提前考虑、或所有机制都已被证明合适。

## Instruction / GPT 指令结论

**没有扩写外部 ChatGPT Custom Instructions。**

原因不是“嫌麻烦”，而是根因不在 account routing：现有 `STARTUP_HOOK.md` 已能把 system maintenance 路由到当前 repo authority，本次聊天本身也进入了正确 maintenance task。把完整 meta 方法复制进 Custom Instructions 会：

- 重复 repo authority；
- 增加常驻 prompt；
- 产生 future drift；
- 掩盖真正的 internal governance/eval defect。

内部 `ENTRYPOINT.md` 已做最小修改：
- material user correction / challenge to maintenance completeness 明确进入 current meta-maintenance path；
- stale methodology receipt wording `1.2` 已统一为 `1.3`；
- 明确 systemic meta work 是 cold path，不进入普通业务热路径。

如果未来真实 product evidence 表明当前 account hook 对这种 maintenance signal 路由失败，再持久化最小外部 instruction delta 并只要求用户执行一次 UI 修改；repo write 本身不冒充 account propagation。

## 子系统继承 / propagation review

当前 `OWNER_REGISTRY` 的 4 个 BUSINESS owner 均重新读取：

- `FINANCIAL_WRITING_AGENT_RUNTIME`
- `A_SHARE_MARKET_AGENT`
- `NOVEL_WRITING_AGENT`
- `VIDEO_GROWTH_AGENT`

四个都继续 exact-version 绑定 `artifact_io@1.0 + operational_hygiene@1.0 + evolution@1.0`。当前 owner override 属于 evaluator/artifact/domain specialization，没有发现覆盖 shared maintenance evidence/reliability/authority invariant 的 shadow override。

因此这次是兼容 semantics-owner hardening：不 bump Continuity protocol，不 bump methodology profile version，也不复制同一套 prose 到四仓。

Propagation sweep 还实际发现：Novel owner 在上一轮 sweep 后已独立升级到 `Novel Writing Agent 2.2.0-github / github-owner-2.3`，而中央 derived registry 仍是 `2.1.1 / 2.2.1`。中央 `OWNER_REGISTRY / OWNER_PROTOCOL_ADAPTATION_REGISTRY / HARNESS_STATUS` 已只刷新 metadata；没有改小说正文、Canon、业务 task stage、next_action 或 lease。当前 Novel 业务状态以 owner 自身权威为准，Universal 不覆盖。

## Complexity / efficiency

本轮结论：`ACCEPTABLE`，但原因写死：

- 新 root policy/registry/permanent Agent：`0`；
- `runtime/meta_maintenance.py` 是 verifier implementation，不是第二 authority；
- mandatory startup context delta：`0`；
- ordinary business hot-path preload：`0`；
- 外部学习/全 owner impact review 只在 systemic/non-trivial maintenance 触发；
- local deterministic fix 可以带理由走 lightweight path；
- 不复制 meta doctrine 到 owner prompts/Custom Instructions；
- 不创建上层 LLM Agent，除非未来有 distinct executor/trace + held-out measured lift。

## Meta Harness 1.0

`runtime/meta_maintenance.py` 会 fail closed 检查 systemic maintenance run 是否具备：

- user signal classification + goal/constraint；
- authority refs + root-cause layers + system impact map；
- systemic learning scout 及 source observation/disposition/rationale；
- 至少两个 credible alternatives 且只有一个 accepted；
- instruction-surface decision + reason；
- registry-derived propagation scope + stale override scan；
- complexity/efficiency budget；
- implementation / supersession record；
- regression/eval refs + second-order challenge + systemic cross-surface/fault audit；
- assurance ceiling + open gates + unknown/open-world boundary；
- `global_flawlessness_claimed=false`。

`tests/test_meta_maintenance.py` 还把最终 maintenance closure 与机器可读 run 绑定：manifest 离开本轮 IN_PROGRESS stage 后，必须 `meta_maintenance_harness_version=1.0`、指向本轮 run，且 run 的 `target_manifest_version` 必须匹配最终 manifest version。

`tests/test_meta_governance_status_alignment.py` 额外要求 Policy / Manifest / Harness policy version 一致，并检查 Blueprint 不能把 Meta Harness 描述成独立语义 reviewer。

## 当前已验证证据

- candidate policy/harness 初次集成曾因 manifest 仍写 policy 1.5 被 system audit 正确打红；不是关闭检查器。
- 修复状态版本同步后，旧 `tests/test_system_audit.py` 又因精确断言 1.5 红；更新 stale expectation，不回滚 1.6。
- head `7e902847427a624bbc60fcbfb25f732b70781f78`：run `38077001860` SUCCESS。
- head `7ccc80e47eb42058d1085b40243dd969e282c787`：run `38077281754` SUCCESS，包含 machine-readable meta-run + closure-binding + current receipt-semantic tests。
- head `3d98d5d78518ecaeda8171c440b7799bbd94510b`：run `38077334862` SUCCESS，包含 Blueprint 架构同步。
- 最终 registry/HARNESS/manifest/Handoff/cache 同步仍必须以最新 `main` 再跑 CI 后才可用户侧报告 `COMMITTED`。

## 仍然 OPEN，不能被 Meta Harness 冒充解决

1. Universal operator-dependence incident：真正独立 held-out/live trajectory grader + evidence verifier。
2. real new BUSINESS owner + genuinely fresh ChatGPT chat 的 cold-start E2E。
3. owner real action 的 methodology 1.3 independent semantic verification。
4. Financial live prose-quality independent blind pairwise promotion；Personalized Writing DNA 的真实 user/outcome evidence。
5. Video strict isolated reviewer / unique quality-critical generation gateway。
6. arbitrary ChatGPT→GitHub mutation 仍是 repository CI post-write enforcement，不是 universal pre-write `WRITE_PATH_ENFORCED`。
7. Meta Harness 不能证明未来 unknown failure classes 都被预见，也不能证明自己结构记录的语义真伪。

## Next action

没有新的真实 maintenance signal / capability / external evidence 时，不发明内部工作。

下次出现 systemic/non-trivial signal，默认走 policy 1.6 + Meta Harness；不能再退回“收到例子 → 直接补丁 → CI 绿 → 泛化说好了”的旧路径。

## Recovery refs

- `tasks/universal-continuity-maintenance/TASK_MANIFEST.json`
- `audits/META_MAINTENANCE_GOVERNANCE_RUN_2026-10-11.json`
- `SYSTEM_MAINTENANCE_POLICY.json`
- `SYSTEM_BLUEPRINT.md`
- `ENTRYPOINT.md`
- `runtime/meta_maintenance.py`
- `tests/test_meta_maintenance.py`
- `tests/test_meta_governance_status_alignment.py`
- `HARNESS_STATUS.json`
- `OWNER_REGISTRY.json`
- `OWNER_PROTOCOL_ADAPTATION_REGISTRY.json`
- `CONTINUOUS_LEARNING_POLICY.md`
- `audits/UNIVERSAL_OPERATOR_DEPENDENCE_RELIABILITY_INCIDENT_2026-10-10.md`

恢复时先读 manifest + 本 Handoff。不要把 Meta Harness PASS、CI、COMMITTED、同会话 self-review 或外部方法引用外推成 independent semantic correctness / global flawlessness。
