# 跨对话继承系统建设与维护｜Handoff

- task_id: `continuity:universal-continuity-maintenance`
- task_class: `SYSTEM_INFRA`
- owner: `UNIVERSAL_CONTINUITY_HARNESS`
- status: `ACTIVE`
- contract: `CONTINUITY_V3_7`
- current writer: `lease-d5136fdf-0661-4cd9-aeba-74db63c4dc3f`
- resume_epoch: `7`
- manifest_version: `59`
- meta-maintenance: `1.2`
- latest meta-run: `audits/META_MAINTENANCE_UNIFIED_SELF_EVOLUTION_V59_2026-10-11.json`

## 当前阶段

`V3_7_AGENT_CONTROL_PLANE_V1_1_REGRESSION_VERIFIED__GLOBAL_LIVE_OWNER_REOBSERVATION_V51_PASS__VIDEO_SHARED_ARCHITECTURE_VERSION_DRIFT_REPAIRED__OWNER_REGISTRY_MEMBERSHIP_OBSERVATION_SEPARATION_REGRESSION_VERIFIED__ARCHITECTURE_WATCH_HOURLY__TOP10_SELECTED_PRIMITIVES_REGRESSION_VERIFIED__OWNER_DRIFT_SIGNALS_OPEN__OPERATOR_DEPENDENCE_LIVE_EVIDENCE_OPEN__PRIOR_LIVE_EVIDENCE_GATES_OPEN__CONTEXT_CAPACITY_PREFLIGHT_REGRESSION_VERIFIED__UNIFIED_SELF_MAINTENANCE_EVOLUTION_LOOP_REGRESSION_VERIFIED`

## V59 本轮闭环

1. 用户指出“挑刺/反思”“进化”“传播/防污染”不应作为三个并列父系统；真正目标是让总控与子系统在发现重要问题后自主完成系统级诊断、学习、方案竞争、修复、验证、二次全局审视、传播清理与经验沉淀。
2. 复核当前 authority 后确认：`SYSTEM_MAINTENANCE_POLICY.json` 原本已经有从 DETECT 到 impact/root cause、learning scout、alternatives/falsification、minimum patch、validation、propagation、second-order challenge、durable learning 的单一路径；`CONTINUOUS_LEARNING_POLICY.md` 也已把 learning 定义为 maintenance 的输入。真实缺口主要是 `OWNER_ADAPTER_CONTRACT.json` 没有把 `operational_hygiene` 与 `evolution` 的关系明确收束成“一个父循环里的职责/证据切片”。
3. 外部 scout 复核了 OpenAI Agent Improvement Loop / agent evals、Anthropic agent eval 与 long-running harness 方法，以及 Reddit / YouTube 等 practitioner 反例。共同结论是：把真实失败/trace 连到 eval、harness change、再验证是合理的；但额外堆 supervisor/watcher/agent 会增加误报、自证和架构臃肿风险。
4. 采用方案：**one parent self-maintenance-evolution loop + narrow profile slices**。不新增 Reflection Agent，不新增 root policy，不合并破坏现有 profile 接口，不 bump Continuity/profile version。
5. `OWNER_ADAPTER_CONTRACT.json` 现在明确：reflection/critique、learning/evolution、repair、propagation/cleanup 是一个 evidence-backed loop；同一 material signal 共享 problem statement / impact model / evidence chain / closure boundary。
6. 统一循环新增明确约束：
   - user correction、assistant-detected defect/inefficiency、CI/eval/trace regression、drift/stale authority、routing/tool nonuse、context/state loss、duplicate/superseded mechanism、performance/complexity regression、product/ecosystem change 都可触发；
   - patch 前必须先脱离局部症状做 parent-system reframe；
   - 对非平凡/系统级不确定问题主动 scout 当前 first-party/original + 多样 practitioner lanes；
   - 方案必须比较/反例攻击，优先 reuse / deletion / consolidation；
   - first-pass regression 后必须再次脱离做 second-order system reframe；
   - 闭环必须沉淀 reusable failure class / eval / guard / workflow-method update 或明确 rejection rationale；
   - 传播共享 method/invariant，不传播 owner-local business truth / threshold / task state / evidence；
   - 健康普通业务回合不执行 broad scout / full control-plane audit，避免把“进化”变成热路径负担。
7. 新增 `tests/test_self_maintenance_evolution.py`，防止未来回退成多个并列父循环、把 profiles 当独立系统、漏掉主动触发/二次 reframe，或通过新增 Reflection/Supervisor root surface 解决问题。
8. preclosure commit `bbb36f4b87cc7c95dcb84db0172b186816dc2833`；CI `38144838013` / job `114485910330` 为 SUCCESS，risk-tiered control-plane audit、Agent architecture harness、pytest 均成功。
9. V59 closure 同步 authoritative TASK_MANIFEST、meta-run、HARNESS_STATUS、GENERIC_TASK_REGISTRY 与本 Handoff；最终 acceptance 仍要求 V59 closure commit 自身 CI 绿色。若 closure CI 失败，只修真实失败范围，不弱化 invariant。

## 子系统继承边界

- 当前 BUSINESS owner 集合：`A_SHARE_MARKET_AGENT`、`FINANCIAL_WRITING_AGENT_RUNTIME`、`NOVEL_WRITING_AGENT`、`VIDEO_GROWTH_AGENT`。
- Shared loop 通过现有 `OWNER_ADAPTER_CONTRACT` + owner `operational_hygiene/evolution` hooks 传播，不复制大段父系统 prose，也不修改子系统业务 state/lease。
- Financial / A-share / Novel 已有两类 profile 的明确 owner-local hooks；Video 已有 challenge→pollution/bypass→minimum patch→supersession→adversarial regression→CI→reread 的维护方法，但其已知 architecture/assurance drift 仍是 OPEN evidence gate。
- 因此 V59 能声明 contract-level / regression-level shared-method propagation，不能声称四个子系统都已经在真实业务事故中独立执行过完整自动进化闭环。

## 当前 Next action

保持 turn-entry capacity preflight 和 unified self-maintenance-evolution loop。以后出现 material signal 时，不先做局部缝补：先做系统级 preframe，再按证据决定 scout 深度、方案竞争和最小修复；第一轮验证后执行 second-order reframe；只传播共享方法与 invariant，清理 superseded/shadow mechanism，沉淀可复用 failure pattern。没有 material signal 时保持 hot path 精简，不制造学习/审计仪式。

## 仍然 OPEN

1. real child-owner self-triggered incident/action evidence：需要未来真实子系统事故证明它们会在无需用户逐项提醒时启动并完成该闭环；
2. operator-dependence independent heldout/live trajectory grader；
3. A-share / Novel / Video 等已确认的 owner-specific architecture / assurance drift；
4. owner-local action-level independent methodology verification 与 live quality/outcome；
5. recurring scout / architecture watch 的长期质量与 future remote-owner freshness；
6. 不得把 V59 contract wiring + CI 外推成“以后不会再犯错”或“所有子系统已经完成 live 自进化证明”。

## Recovery refs

- `tasks/universal-continuity-maintenance/TASK_MANIFEST.json`
- `tasks/universal-continuity-maintenance/HANDOFF.md`
- `OWNER_ADAPTER_CONTRACT.json`
- `SYSTEM_MAINTENANCE_POLICY.json`
- `CONTINUOUS_LEARNING_POLICY.md`
- `tests/test_self_maintenance_evolution.py`
- `audits/META_MAINTENANCE_UNIFIED_SELF_EVOLUTION_V59_2026-10-11.json`
- `HARNESS_STATUS.json`
- `GENERIC_TASK_REGISTRY.json`
- `CONTEXT_RECOVERY_POLICY.json`
- `PROGRESS_OBSERVABILITY_POLICY.json`
