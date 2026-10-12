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

`V3_7_AGENT_CONTROL_PLANE_V1_1_REGRESSION_VERIFIED__GLOBAL_LIVE_OWNER_REOBSERVATION_V51_PASS__VIDEO_SHARED_ARCHITECTURE_VERSION_DRIFT_REPAIRED__OWNER_REGISTRY_MEMBERSHIP_OBSERVATION_SEPARATION_REGRESSION_VERIFIED__ARCHITECTURE_WATCH_HOURLY__TOP10_SELECTED_PRIMITIVES_REGRESSION_VERIFIED__OWNER_DRIFT_SIGNALS_OPEN__OPERATOR_DEPENDENCE_LIVE_EVIDENCE_OPEN__PRIOR_LIVE_EVIDENCE_GATES_OPEN__CONTEXT_CAPACITY_PREFLIGHT_REGRESSION_VERIFIED__UNIFIED_SELF_MAINTENANCE_EVOLUTION_LOOP_REGRESSION_VERIFIED__FINANCIAL_GITHUB_CHAT_GUARD_SCOPED_EXECUTION_AND_ARCHITECTURE_PASS__FINANCIAL_FULL_OWNER_CI_AND_LIVE_TRAJECTORY_OPEN`

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
7. **产品传播边界**：repository 已更新 canonical `ACCOUNT_ROUTER_V2` 文本；用户于本轮明确确认已更新 ChatGPT Custom Instructions。该用户确认可作为安装状态输入，但 repository 仍无法独立 product-readback 账户文本，不能把用户确认升级为独立产品侧 attestation。
8. complexity/efficiency：没有新增 root authority、Agent、profile 或业务 owner 改动；`ENTRYPOINT.md` 仍满足既有 hot-path 大小预算，健康业务回合不增加 broad scout/full audit。

## Post-V59：完整自维护轨迹参考推演

1. 用户追问：此前声称 repo 已具备完整机制时，是否真正做过“系统运行推演”。复核后确认：此前证据主要是 contract、静态/结构回归、CI、architecture harness，以及 maintenance-decision escalation eval；**没有执行一条完整的 deterministic self-maintenance/evolution reference trajectory**。因此此前“已经具备”的表述若被理解为“完整运行链已推演验证”，属于 assurance overreach。
2. 根因：`evals/maintenance_decision_cases.json` + `runtime/maintenance_decision_eval.py` 主要验证是否应 ESCALATE / DO_NOT_ESCALATE，以及真实 product trajectory grading seam；它们没有覆盖 `defect triage → parent reframe → learning decision → candidate falsification → minimum patch → validation → second-order review → propagation/cleanup → durable learning → authority reread` 的完整参考状态转移。
3. 最小修复：新增窄 harness `runtime/self_maintenance_trajectory.py`，不作为业务 authority、不作为 child owner executor，只做 deterministic reference simulation。它的 assurance ceiling 固定为 `DETERMINISTIC_REFERENCE_SIMULATION_ONLY`，明确禁止外推成 live ChatGPT / remote child-owner execution proof。
4. 新增/扩展 `tests/test_self_maintenance_evolution.py` 的代表性轨迹：
   - `CONFIRMED_DEFECT + material + systemic + uncertain + shared change + validation PASS` 必须按序经过 parent reframe、learning scout、candidate challenge、minimum patch、validation、second-order review、shared-method-only propagation、cleanup、durable learning、authority reread；
   - `NO_DEFECT` 只能解释并停止，不能进入 patch；
   - `INVESTIGATE` 必须停在继续取证，不能进入 patch；
   - local/non-material defect 只能 local repair，不跑 full loop；
   - validation FAIL 必须 keep active with blocker，不能假装 propagation / durable closure；
   - shared propagation 永远不把 owner business truth 标记为传播对象。
5. commit `934fc51d874e23bd7455250e70ff60e32fd8968f` 引入可执行轨迹测试；CI `38153628452` / job `114511998218`：risk-tiered control-plane audit PASS、Agent architecture harness PASS、pytest PASS。
6. 第二序审查结论：该 simulator 只用于“在做 repo/mechanism completeness 声明前先做代表性 dry-run”；不得取代现有 `maintenance_decision_eval` 的真实 product-trace / independent-grader gate，也不得作为“四个子系统已经真实自主进化”的证据。

## Post-V59：Financial 子系统真实事故的父级进化复核与执行控制加固

1. 用户先让 Financial 子系统用一个可信缺陷假设自查；子系统确认了“material 写作反馈可能只局部修文、没有 durable system-impact obligation”的 declaration-to-operation gap，并在 owner-native 路径加入 v0.8.1 system-impact wiring。该实验提供了真实 child-owner defect-hypothesis→triage→maintenance 行为证据，但仍不是“完全无人提示的自主发现”。
2. 随后的真实写作实验又暴露更严重事故：GPT 聊天可以绕过 Financial owner workflow，直接从用户 prompt 产出伪成稿。第一次父维修把当前用户运行形态 `GitHub-mounted authority + GPT chat execution` 提升为 `GITHUB_CHAT` mode，并在 `d50adb726fd1a8671a2bd23bf04105797d6faeab` 合入 state/checkpoint/CAS 机制。
3. 用户随后质疑：该维修是否真正按进化系统先做 parent-system reframe、方案竞争、验证和二次攻击。复核确认该质疑是 **CONFIRMED_DEFECT**：第一次维修并非完全没有系统思路，但过早把“Python runtime 与 GPT chat 缺桥”提升为主根因，并在 full owner CI 没有执行、architecture validation 仍 stale 时用“已经修了”描述，属于 assurance/closure 过度。
4. C 的 architecture-watch control signal `#5` 正确报告：Financial `d50adb...` 与旧 `architecture_validation_head=a76c83...` 不一致。该 signal 被重新分类为可执行证据，而不是 freshness noise。
5. 重新按 `SYSTEM_MAINTENANCE_POLICY` M0→M11 做全系统 reframe 后，根因被拆成：
   - `OWNER_BINDING / EXECUTION_READINESS`：真实 GPT+GitHub 路径能绕开 owner workflow；
   - `EXECUTION_CONTROL_GAP`：第一版 GITHUB_CHAT 有 GitHub state/CAS，但 stage order 仍依赖聊天遵守声明，没有 deterministic fail-closed transition guard 与 exact action-bound execution receipt；
   - `ARCHITECTURE_DESCRIPTION_DRIFT`：Financial `AGENT_MANIFEST` 当时只描述 Python state/guards，没有把 chat state/guard 建模进去；
   - `ASSURANCE_CLOSURE_GAP`：新 HEAD 未经当前 architecture harness fresh validation；
   - `HARNESS_DRIFT`：若干 profile-10 tests 仍锁定旧 executor/status 文案，runner 真恢复时会暴露。
   因而“执行顺序没跑”是下游症状，不是父级根因。
6. reuse-before-build / candidate competition：
   - 否决继续加 Skill 提醒；原事故已证明 declaration-only 不够；
   - 否决现在强制 Site/MCP；用户当前明确采用 GitHub+GPT 模式；
   - 否决把 same-chat review 升级成 owner-native PASS；会破坏 assurance；
   - 否决新增 Financial supervisor/reviewer Agent；没有独立执行身份，只会增加 review theatre；
   - 选中：复用 Financial 既有 stage semantics + Universal execution-receipt invariant + GitHub CAS + Novel CHAT_BRIDGED deterministic guard pattern，加入 owner-local deterministic GitHub-chat transition guard。
7. Financial PR `#13` 已 squash 合入 main，最终 HEAD：`cf5236a8218678a85bd95bd6782442086d2d891c`。核心修复：
   - 新增 `financial_writing_agent/github_chat_guard.py`；
   - GITHUB_CHAT state schema 1.1；
   - 每次 material transition 必须绑定 fetched prior `STATE.json` blob SHA、task/stage/capability/action、executor identity、subject/input bindings、output refs，并追加 `SELF_ATTESTED_CHAT_EXECUTION_RECEIPT`；
   - GitHub update 必须使用同一 prior blob SHA，stale writer 由 provider CAS 拒绝；
   - 缺 current-stage artifact、错 route、foreign-task artifact、future-stage artifact/review 预塞、owner-native `COMPLETE` spoof、chat assurance inflation 均 fail closed；
   - `REVISE` 会失效目标阶段及全部下游 active artifact/review refs，必须产生新 artifact 才能重新推进；
   - material negative/corrective feedback + OPEN system-impact 由 guard 绑定同一 state mutation；
   - `AGENT_MANIFEST` 现在真正把 GITHUB_CHAT state authority 和 guard 纳入 runtime/workflow；
   - profile 10 execution capabilities 只有在当前 session 具备 model + GitHub read/write + deterministic guard（及 exact-stage web/document 工具）时才可标 session-executable；否则阻塞，禁止 free-form publishable fallback。
8. 二次攻击没有停在第一版 guard：实际又发现并修复三类绕过：
   - REVISE 后旧 target/downstream artifact 仍可能被复用；
   - future-stage artifact/review 可被预塞进 state；
   - chat state 可手工注入不属于 GITHUB_CHAT 的 `COMPLETE` status。
   最终 guard 已做 downstream invalidation、future-state pollution rejection 与 status allow-list。
9. **scoped code-level regression**：直接从 GitHub 取回最终 guard blob `ffa2e5f7f10ff8940a257fa560683bb400195201` 的实际源码并 compile/import/执行，验证 COMPLETE spoof rejection、future-artifact rejection、missing-artifact rejection、revision invalidation + fresh-artifact requirement、feedback/system-impact pairing，以及完整 happy path；最终只能到 `DELIVERED_CHAT_REVIEWED__CERTIFICATION_OPEN`，不会冒充 owner-native COMPLETE。
10. **真实 provider-boundary tracer**：隔离 branch `test/github-chat-guard-tracer-20261012` 真创建 STATE、Research artifact、action receipts；Research receipt 真绑定 artifact blob SHA；故意用 stale STATE SHA 更新得到 HTTP 409；随后 `RESEARCH_AUDIT → REVISE → RESEARCH`，回读确认 `stage_artifacts={}`、`review_decisions={}`。synthetic workspace 随后删除，只保留 commit/audit history。该 tracer 证明 state/CAS/receipt/invalidation 能组合，不证明真实文章质量或 live autonomous routing。
11. **最终架构 freshness 已关闭 #5 对应问题**：对最终 Financial main `cf5236...` 使用当前 Universal `runtime/agent_architecture.py` / `AGENT_ARCHITECTURE_CONTRACT.json` 实际 validator，结果 `PASS / errors=0 / warnings=0`；Skill 7549 B < 8192 B。新 receipt：`audits/FINANCIAL_ARCHITECTURE_REVALIDATION_CF5236_2026-10-12.json`。`OWNER_ARCHITECTURE_OBSERVATIONS.json` 已更新到 `observed_owner_head == architecture_validation_head == cf5236...`，control signal Issue `#5` 已按 completed 关闭。
12. **严格证据边界仍保留**：GitHub Hosted Runner 仍未真正执行 Financial full CI。最新 PR run `38192604882` / job `114628380998` 为 `steps=null`，因此 SDK smoke、MCP smoke、全量 pytest、static audit、wheel、DOCX render 均不能宣称 PASS；本轮只建立 scoped guard code regression + provider tracer + final-head architecture PASS。真实 post-fix Financial article trajectory、live prose quality、independent/provider review 仍 OPEN。
13. **owner boundary**：Financial 的 BUSINESS task manifest 仍处于 profile 9，由另一个有效 Financial writer 持有；本 SYSTEM_INFRA writer没有越权改 lease/task state。下一次真实 Financial owner turn 必须先 reconcile 到 profile 10，再正常接受文章任务。另有 owner-native `list_recent_writing_tasks` 与 MCP wrapper 对 COMPLETE+未清维护债务的 shadow filtering 缺陷仍 OPEN，本轮未用大范围 runtime rewrite 冒险顺手修。
14. 本次经验固化：
   - “知道 SOP”不等于“执行 SOP”；formal execution mode 必须有 durable state + fail-closed transition guard + action-bound receipt，而不是只靠 Skill prose；
   - architecture change 未完成 freshness validation 时不得用旧 PASS 给新 HEAD 背书；
   - CI runner 没执行不是 regression PASS；必须降级 claim，并用 scoped exact-code regression / provider tracer补最相关证据，但不能冒充 full suite；
   - 第一次修法也必须被 M9 second-order challenge 攻击，尤其检查 stale evidence reuse、future-state pollution、status/assurance spoof 和 shadow authority。

## 子系统继承边界

- 当前 BUSINESS owner 集合：`A_SHARE_MARKET_AGENT`、`FINANCIAL_WRITING_AGENT_RUNTIME`、`NOVEL_WRITING_AGENT`、`VIDEO_GROWTH_AGENT`。
- Shared loop 通过现有 `OWNER_ADAPTER_CONTRACT` + owner `operational_hygiene/evolution` hooks 传播，不复制大段父系统 prose，也不修改子系统业务 state/lease。
- Financial 当前共享方法已经真实落到其 GitHub+GPT 执行控制：durable state + deterministic transition guard + exact self-attested action receipt + second-order invalidation/pollution guards；这仍不等于 owner-native independent review 或 live quality PASS。
- A-share / Novel / Video 继续按各自 authority 与现有 control signals 处理；本轮 Financial 修复不传播 Financial 业务写作规则到其他 owner。
- 因此现在可以声明：共享机制有 contract/regression + deterministic reference trajectory；Financial 额外已有 scoped guard exact-code regression + provider-boundary tracer + fresh architecture PASS。仍不能声称四个子系统都已经在真实业务事故中独立执行过完整自动进化闭环。

## 当前 Next action

保持 turn-entry capacity preflight 和 unified self-maintenance-evolution loop。任何可信的系统缺陷假设先完成 `NO_DEFECT / INVESTIGATE / CONFIRMED_DEFECT` triage；确认缺陷后同一轮进入维护/进化闭环，不停在“风险”表述。涉及“系统已经具备完整运行链”的声明时，先用 `runtime/self_maintenance_trajectory.py` 做代表性 reference simulation，并把 contract/regression、reference simulation、scoped code execution、provider-boundary tracer、action-level proof、independent verification 与 live product outcome 分开。

Financial 下一条最高价值证据不是继续人工喂“启动进化系统”，而是在原 Financial 聊天正常提出真实文章任务：当前 Financial writer 应先 reconcile business task metadata profile 9→10；若 owner-native runtime 不可用且 session 有 GitHub+deterministic guard 能力，应自主进入 guard-enforced GITHUB_CHAT，在 Research 前建立 STATE，并为每个 material stage 留 durable artifact + action receipt；若仍直接自由写正文，则证明 live owner-binding 仍未闭环。Hosted Runner 恢复后再跑未弱化的完整 owner CI。

## 仍然 OPEN

1. account-level `ACCOUNT_ROUTER_V2`：用户已明确确认完成 Custom Instructions 更新；独立产品侧 readback/attestation 仍不可用；
2. real child-owner self-triggered incident/action evidence：Financial 已有“用户给可信 defect hypothesis 后自主 triage+maintenance”的真实证据，但完全无人提示的 assistant-detected live incident/self-trigger 仍未证明；其他 owner 也仍需真实 trajectory；
3. Financial full owner CI：Hosted Runner 当前 `steps=null`，不能宣称全套 regression verified；
4. Financial real post-fix GITHUB_CHAT article trajectory + live writing-quality outcome；
5. Financial BUSINESS task metadata profile 9→10 reconciliation，只能由当前 Financial writer 执行；
6. Financial owner-native recent-task maintenance-debt filtering shadow logic；
7. operator-dependence independent heldout/live trajectory grader；
8. A-share / Novel / Video 等 owner-specific architecture / assurance drift 与其已有 control signals；
9. owner-local action-level independent methodology verification 与 live quality/outcome；
10. recurring scout / architecture watch 的长期质量与 future remote-owner freshness；
11. 不得把 contract wiring + architecture PASS + scoped guard regression + provider tracer 外推成“以后不会再犯错”“文章质量已经提升”或“所有子系统已经完成 live 自进化证明”。

## Recovery refs

- `tasks/universal-continuity-maintenance/TASK_MANIFEST.json`
- `tasks/universal-continuity-maintenance/HANDOFF.md`
- `ENTRYPOINT.md`
- `STARTUP_HOOK.md`
- `OWNER_ADAPTER_CONTRACT.json`
- `SYSTEM_MAINTENANCE_POLICY.json`
- `EXECUTION_READINESS_CONTRACT.json`
- `AGENT_ARCHITECTURE_CONTRACT.json`
- `OWNER_ARCHITECTURE_OBSERVATIONS.json`
- `CONTINUOUS_LEARNING_POLICY.md`
- `runtime/self_maintenance_trajectory.py`
- `runtime/maintenance_decision_eval.py`
- `runtime/agent_architecture.py`
- `tests/test_self_maintenance_evolution.py`
- `tests/test_maintenance_decision_eval.py`
- `audits/META_MAINTENANCE_UNIFIED_SELF_EVOLUTION_V59_2026-10-11.json`
- `audits/FINANCIAL_ARCHITECTURE_REVALIDATION_CF5236_2026-10-12.json`
- `D1traverser-debug/financial-writing-agent@main:evals/FINANCIAL_GITHUB_CHAT_GUARD_EVOLUTION_AUDIT_2026-10-12.md`
- `D1traverser-debug/financial-writing-agent@main:financial_writing_agent/github_chat_guard.py`
- `HARNESS_STATUS.json`
- `GENERIC_TASK_REGISTRY.json`
- `CONTEXT_RECOVERY_POLICY.json`
- `PROGRESS_OBSERVABILITY_POLICY.json`
