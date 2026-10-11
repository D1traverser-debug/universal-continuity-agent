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

## Post-V59：缺陷假设入口加固

1. 用户进一步指出：如果用户只是问“这个入口是不是有问题？”而不是直接断言“这是 bug”，系统不能把它当普通探讨；必须先判断它究竟是问题、证据不足，还是并无缺陷。若已经确认存在缺陷，就不能只描述成“未来风险”后结束。
2. 本次 signal 分类为 `GOAL_OR_CONSTRAINT + COUNTEREXAMPLE_OR_FAILURE_REPORT`。根因不是 unified self-maintenance-evolution loop 内部缺步骤，而是 **pre-repository activation / routing ambiguity**：旧规则对“用户实质纠正”有入口，但对“可信的系统缺陷假设”没有足够明确的前置 triage 语义。
3. 采用最小修复，不新增 root policy / Agent / profile：
   - `STARTUP_HOOK.md` 的 canonical account hook 增加 defect-hypothesis triage：`确认无问题 → 解释并停止`；`证据不足 → 继续核查`；`确认有问题 → 同一轮进入维护/进化闭环`；禁止把已确认缺陷降级成无主的“未来风险”。
   - `ENTRYPOINT.md` 增加 `Plausible system-defect hypothesis` event-driven route，结果空间固定为 `NO_DEFECT / INVESTIGATE / CONFIRMED_DEFECT`。
   - `tests/test_self_maintenance_evolution.py` 增加回归，保证缺陷假设先进入 triage，而不是普通讨论。
4. 学习/证据：OpenAI Agent Improvement Loop 与 agent-eval/trace-grading方法继续支持“反馈必须转成可重跑的 eval/行为改变”，而不是停在评论层；本次未引入额外 supervisor/watch Agent。
5. 二次审查真实发现并修复了两个 collateral regression：
   - 初版把 `ENTRYPOINT.md` 推过 hot-path/context-footprint budget，CI `38149091236` 失败；随后压缩入口，保持最小 bootstrap。
   - 压缩时误伤既有 assurance anchor，CI `38149238114` 因 `declaration conformance, owner regression or CI must not substitute` 回归失败；随后恢复该不变量并从其他冗余文字中腾预算。
6. 最终代码 HEAD `bce5f7e6401bf9b611982334c481232f0c553062`；CI `38149331926` / job `114499269701`：risk-tiered control-plane audit PASS、Agent architecture harness PASS、pytest PASS。
7. **产品传播边界**：repository 已更新 canonical `ACCOUNT_ROUTER_V2` 文本，但 GitHub 写入不能修改 ChatGPT 账户里的 Custom Instructions，也不能证明实际账户文本已同步。因此本次 repo 修复对“下一次 bootstrap 后的行为”已回归验证；对“所有已打开聊天是否已获得更强 defect-hypothesis trigger”的产品级声明仍需要 account-level hook 实际安装/更新证据。
8. complexity/efficiency：没有新增 authority surface、Agent、profile 或业务 owner 改动；`ENTRYPOINT.md` 仍满足既有 hot-path 大小预算，健康业务回合不增加 broad scout/full audit。

## 子系统继承边界

- 当前 BUSINESS owner 集合：`A_SHARE_MARKET_AGENT`、`FINANCIAL_WRITING_AGENT_RUNTIME`、`NOVEL_WRITING_AGENT`、`VIDEO_GROWTH_AGENT`。
- Shared loop 通过现有 `OWNER_ADAPTER_CONTRACT` + owner `operational_hygiene/evolution` hooks 传播，不复制大段父系统 prose，也不修改子系统业务 state/lease。
- Financial / A-share / Novel 已有两类 profile 的明确 owner-local hooks；Video 已有 challenge→pollution/bypass→minimum patch→supersession→adversarial regression→CI→reread 的维护方法，但其已知 architecture/assurance drift 仍是 OPEN evidence gate。
- 因此 V59 能声明 contract-level / regression-level shared-method propagation，不能声称四个子系统都已经在真实业务事故中独立执行过完整自动进化闭环。

## 当前 Next action

保持 turn-entry capacity preflight 和 unified self-maintenance-evolution loop。任何可信的系统缺陷假设先完成 `NO_DEFECT / INVESTIGATE / CONFIRMED_DEFECT` triage；确认缺陷后同一轮进入维护/进化闭环，不停在“风险”表述。以后出现 material signal 时，先做系统级 preframe，再按证据决定 scout 深度、方案竞争和最小修复；第一轮验证后执行 second-order reframe；只传播共享方法与 invariant，清理 superseded/shadow mechanism，沉淀可复用 failure pattern。没有 material signal 时保持 hot path 精简，不制造学习/审计仪式。

## 仍然 OPEN

1. account-level `ACCOUNT_ROUTER_V2` 当前实际安装文本/产品级 readback：repo 不能自证账户 Custom Instructions 已包含本次 defect-hypothesis delta；
2. real child-owner self-triggered incident/action evidence：需要未来真实子系统事故证明它们会在无需用户逐项提醒时启动并完成该闭环；
3. operator-dependence independent heldout/live trajectory grader；
4. A-share / Novel / Video 等已确认的 owner-specific architecture / assurance drift；
5. owner-local action-level independent methodology verification 与 live quality/outcome；
6. recurring scout / architecture watch 的长期质量与 future remote-owner freshness；
7. 不得把 contract wiring + CI 外推成“以后不会再犯错”或“所有子系统已经完成 live 自进化证明”。

## Recovery refs

- `tasks/universal-continuity-maintenance/TASK_MANIFEST.json`
- `tasks/universal-continuity-maintenance/HANDOFF.md`
- `ENTRYPOINT.md`
- `STARTUP_HOOK.md`
- `OWNER_ADAPTER_CONTRACT.json`
- `SYSTEM_MAINTENANCE_POLICY.json`
- `CONTINUOUS_LEARNING_POLICY.md`
- `tests/test_self_maintenance_evolution.py`
- `audits/META_MAINTENANCE_UNIFIED_SELF_EVOLUTION_V59_2026-10-11.json`
- `HARNESS_STATUS.json`
- `GENERIC_TASK_REGISTRY.json`
- `CONTEXT_RECOVERY_POLICY.json`
- `PROGRESS_OBSERVABILITY_POLICY.json`
