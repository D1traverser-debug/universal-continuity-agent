# 跨对话继承系统建设与维护｜Handoff

- task_id: `continuity:universal-continuity-maintenance`
- task_class: `SYSTEM_INFRA`
- owner: `UNIVERSAL_CONTINUITY_HARNESS`
- status: `ACTIVE`
- contract: `CONTINUITY_V3_7`
- current writer: `lease-ada3389a-6b09-4713-bc2a-ae7391582224`
- resume_epoch: `4`
- manifest_version: `44`
- system maintenance policy: `1.6`
- meta-maintenance harness: `1.1`
- Agent architecture contract: `1.0`
- control signal contract: `1.0`

## 当前阶段

`V3_7_AGENT_CONTROL_PLANE_ARCHITECTURE_CONTRACT_ACTIVE__THIN_BOOTSTRAP_ENFORCED__SIGNAL_PLANE_ACTIVE__REMOTE_ARCHITECTURE_WATCH_ENABLED__OWNER_SKILL_DRIFT_TRACKED__PRIOR_LIVE_EVIDENCE_GATES_OPEN`

这轮不是继续给旧总控加 checklist。用户指出 GitHub 迁移与 Agent 模式的真正目标没有被机械验收：**Skill / Agent Runtime / Workflow / Harness / References / Continuity 的职责仍可能混在一起；Universal 自己虽然 Skill 很薄，但强制启动 ENTRYPOINT 仍然很胖；发现 drift 仍可能依赖用户提醒。**

本轮将这个问题升级为 Agent Control Plane 架构，而不是新的永久 LLM 角色。

Durable machine-readable record：`audits/META_MAINTENANCE_AGENT_CONTROL_PLANE_2026-10-11.json`。

## 本轮接管

用户明确要求当前聊天接管 SYSTEM_INFRA。按 `CONTINUITY_CONTRACT.json` 的显式 SYSTEM_INFRA takeover 规则：

- previous lease: `lease-0f3dc1cd-1656-4493-af73-97f3b334c858`
- current lease: `lease-ada3389a-6b09-4713-bc2a-ae7391582224`
- resume_epoch: `3 -> 4`

接管后已回读 authority。此后同聊天维护保持 epoch 4 / 当前 lease，不再伪造 takeover。

## 根因

1. **Agent 产品化验收标准隐式**：过去验证 GitHub authority、CI、continuity、receipt，却没有共享 contract 机械检查“Skill 是路由、Runtime 真执行、Workflow 真管状态、Harness 真验 Agent”。
2. **thin Skill / fat bootstrap**：Universal `skills/universal-continuity/SKILL.md` 已是 thin capability map，但旧 `ENTRYPOINT.md` 约 17KB 且每次必读；因此“Skill 薄”没有等于“启动路径薄”。
3. **owner architecture drift 不可见**：Financial/Novel/Video 的 Skill 已明显超出适合作为 router 的体积，但系统此前不会把这当架构 drift。
4. **State Plane / Signal Plane 混合**：stale writer 必须停止 authority mutation 是正确的，但此前没有一条 first-class 非权威 signal 通道把新发现交给 active writer，因此发现仍可能依赖用户转述。
5. **remote freshness 缺口**：Universal 本地 CI 可以检查缓存一致性，但没有私有 owner 远端观察能力时，不能知道 owner HEAD 已前进。

## Agent Product Architecture

新增 `AGENT_ARCHITECTURE_CONTRACT.json`，统一职责模型：

`Skill/router -> Runtime/executor -> Workflow/state -> Harness/eval -> References -> Continuity`

它不强制所有 owner 使用 OpenAI Agents SDK：

- runtime 可为 `AGENTS_SDK / DETERMINISTIC_WORKFLOW / HYBRID / EXTERNAL_RUNTIME`；
- formal tool surface 可选，避免 Novel 这类 repo-native runtime 为通过 contract 伪造 MCP/API；
- missing runtime/workflow/harness = structural FAIL；
- Skill 超过 8192-byte target = `PASS_WITH_DRIFT`，不是把“上下文架构问题”误判为 runtime 不存在。

Universal 自己也有 root `AGENT_MANIFEST.json`，不会只要求别人 Agent 化。

## 四个 BUSINESS owner 已接入

每个当前 BUSINESS owner 都已有 `continuity/AGENT_MANIFEST.json`，且 `OWNER_REGISTRY.json` schema 升到 `3.2`，BUSINESS admission 必须声明 `agent_manifest_ref`。

Rollout observation：`OWNER_ARCHITECTURE_OBSERVATIONS.json`。

- **A_SHARE_MARKET_AGENT** — `PASS`; Skill 7384 bytes; owner CI `38087222816` SUCCESS。
- **FINANCIAL_WRITING_AGENT_RUNTIME** — `PASS_WITH_DRIFT`; hybrid runtime + MCP/state machine/harness 已分层，但 Skill 约 20KB，仍需 owner-specific slimming; owner CI `38087159770` SUCCESS。
- **NOVEL_WRITING_AGENT** — `PASS_WITH_DRIFT`; current observed owner head 已刷新到 `4cafb0ec1240f19f44e442d3b74f173173865555`，Skill 19540 bytes，judgment 仍 CHAT_BRIDGED; owner CI `38087533724` SUCCESS。
- **VIDEO_GROWTH_AGENT** — `PASS_WITH_DRIFT`; AgenticStudio/work-order runtime 存在，但 Skill 约 10KB，strict isolated reviewer 仍是独立 assurance blocker; owner CI `38087238851` SUCCESS。

这轮没有改任何 owner business task stage / lease / Canon / article / market state。

## 二阶挑刺推翻了三版错误设计

### 1. AGENT_MANIFEST 自己记录 current HEAD — REJECTED

第一版想让 manifest 同时记录 `observed_owner_head` 与验证 HEAD。问题是：**写 manifest 自己会改变 HEAD，因此 receipt 立即自我过期。**

最终：
- `AGENT_MANIFEST` 只描述静态 architecture；
- `OWNER_ARCHITECTURE_OBSERVATIONS.json` 记录外部 observed/validated HEAD；
- remote observer 比较 freshness。

### 2. 所有 Agent 都必须有 tool surface — REJECTED

Novel 是 repo-native workflow/guards，没有正式 MCP/API。强制 `tool_surface_refs` 会鼓励编造 capability。

最终：runtime entrypoint 必须存在，tool surface 按真实实现可选。

### 3. 每个 owner 复制一份 architecture checker — REJECTED

这会让共享控制语义在四个仓分别漂移。

最终：
- owner local Harness 负责 domain contract / trajectory / quality；
- Universal `runtime/agent_architecture_audit.py` 负责 shared architecture contract。

## Harness 真正执行

新增：
- `runtime/agent_architecture.py`
- `runtime/agent_architecture_audit.py`
- `tests/test_agent_architecture.py`

Universal CI 现在固定跑三层：

1. risk-tiered control-plane audit；
2. Agent architecture harness；
3. full pytest。

不是“contract 文件存在”就算 Agent architecture PASS。

## Thin bootstrap 已真正执行

旧 `ENTRYPOINT.md` 约 17KB；旧 `STARTUP_HOOK.md` 也承担过多细节。

现在两者都受 `tests/test_hot_path_loading.py` 的 **8192-byte hard budget** 约束：

- bootstrap 只保留 intent、lease、authority、execution boundary、Agent architecture、maintenance trigger、progress receipt 等 kernel；
- methodology receipt 版本/字段算法不再复制进 hot path；
- 入口委托给 `OWNER_ADAPTER_CONTRACT.json`、`runtime/methodology_conformance.py` 等事件 authority；
- 仍保留 existing-chat reconciliation、OPEN/BLOCKED 可持久化、COMMITTED 只表示 persistence 等历史核心不变量。

在这个过程中，旧 `system_audit` 一度因为要求 ENTRYPOINT 复制 receipt 版本语义而正确红灯。该检查已重构为“必须正确委托、禁止 bootstrap 硬编码 receipt version”。

## Signal Plane

新增：
- `CONTROL_SIGNAL_CONTRACT.json`
- `runtime/control_signal.py`
- `SIGNAL_PLANE.md`
- `tests/test_control_signal.py`
- `tests/test_signal_plane_contract.py`

边界：

- State Plane = task/lease/business truth，只有合法 writer 可写；
- Signal Plane = observation/event，可由 stale chat / CI / remote monitor / active writer 发出；
- signal 不是 lease、不是 checkpoint、不是业务 authority；
- active maintenance writer必须重新观察证据后再决定是否修改权威状态。

第一条真实 transport 已建立：GitHub Issue `#1 [CONTROL_SIGNAL] Agent productization drift`。

## Remote Architecture Watch

已启用条件监控任务：

- title: `Agent Architecture Watch`
- id: `6acab16812248191b9f8c8ab52803491`
- cadence: daily condition watch
- behavior: 动态读取当前 BUSINESS owner topology，检查 owner HEAD / `AGENT_MANIFEST` / Skill/router / latest CI / recorded architecture receipt；只在 meaningful drift 时通知，并在可用时创建/更新 `[CONTROL_SIGNAL]`；绝不改业务 state / 抢业务 lease。

这解决“没有对话时主控完全不会观察”的一部分问题。它仍不是全知监控：首个真实 drift alert trajectory 尚未发生，未来 unknown failure class 也不能被预先宣称覆盖。

## Blueprint

`SYSTEM_BLUEPRINT.md` 已同步 Agent Control Plane 形状，包括：

- thin bootstrap；
- Agent 六层产品架构；
- centralized architecture harness；
- State Plane vs Signal Plane；
- remote owner monitoring boundary；
- Meta-Governance 仍只是 structured process verifier，不是独立语义 reviewer。

## CI 不是一路绿

本轮保留失败证据：

1. 新 architecture surface 首轮 CI 在旧 `system_audit` 因 ENTRYPOINT receipt-version复制假设红灯；没有把版本算法塞回入口，而是重构 audit 为 delegation invariant。
2. 之后 full pytest 暴露 6 个旧假设/状态漂移：其中 manifest/cache 确实需要切到 `SELF_AUDIT_IN_PROGRESS`；receipt version/registry schema 等旧测试升级为新 contract；existing-chat / COMMITTED 等仍有效 kernel 语义被恢复。
3. 再跑只剩两条 OPEN-blocker / manual-migration kernel 措辞与 19-byte budget 超标；没有放宽 8192 阈值，而是继续删冗余并恢复核心语义。
4. behavioral head `e82a0f4e86f47ddebfa4d516ff710d4bc7b22ce2`：GitHub Actions run `38088847214` 最终 **SUCCESS**，control-plane audit PASS + Agent architecture harness PASS + full pytest PASS。

最终 metadata/Handoff 写入后仍需验证最终 `main` CI，不能拿 behavioral head 替代最终 HEAD。

## 当前 assurance ceiling

本轮证明：

- `REGRESSION_VERIFIED` Agent architecture contract/harness；
- thin bootstrap budget 已机械执行；
- owner architecture pointers/observations 已建立；
- Signal Plane transport 与 daily remote watch 已启用；
- shared architecture checker 不再靠 user memory 或 owner 自述。

本轮**没有**证明：

1. Financial/Novel/Video 的胖 Skill 已经完成 slimming；它们仍是明确 drift。
2. Remote Watch 已成功抓到过一次真实未来 drift；首次 live alert trajectory 仍待自然事件。
3. Universal operator-dependence 已完全消失；独立 held-out/live maintenance trajectory grader + distinct verifier 仍 OPEN。
4. real newly admitted BUSINESS owner + genuinely fresh ChatGPT product chat cold-start E2E 已证明。
5. owner methodology 1.3 的真实 action independent semantic verification 已普遍完成。
6. Financial live prose quality / Personalized Writing DNA、Video strict isolated reviewer 等 owner live quality/isolation gate 已通过。
7. arbitrary ChatGPT -> GitHub mutation 已获得 universal pre-write `WRITE_PATH_ENFORCED`。
8. 整个动态系统“全局无误”或“未来所有 failure class 已提前覆盖”。

## Next action

没有新 signal 时不制造维护工作。

- remote watch 自动检查 architecture drift；
- meaningful drift -> non-authoritative signal -> 当前 maintenance writer 复核/处理；
- Financial/Novel/Video Skill slimming 在对应 owner 工程上下文安全进行并重新验证，不由 Universal 直接改业务状态；
- prior independent/live evidence gates 按真实事件继续。

## Recovery refs

- `tasks/universal-continuity-maintenance/TASK_MANIFEST.json`
- `audits/META_MAINTENANCE_AGENT_CONTROL_PLANE_2026-10-11.json`
- `AGENT_ARCHITECTURE_CONTRACT.json`
- `AGENT_MANIFEST.json`
- `OWNER_REGISTRY.json`
- `OWNER_ARCHITECTURE_OBSERVATIONS.json`
- `CONTROL_SIGNAL_CONTRACT.json`
- `SIGNAL_PLANE.md`
- `ENTRYPOINT.md`
- `STARTUP_HOOK.md`
- `SYSTEM_BLUEPRINT.md`
- `runtime/agent_architecture.py`
- `runtime/agent_architecture_audit.py`
- `runtime/system_audit.py`
- `runtime/control_signal.py`

恢复时先读 manifest + 本 Handoff。不要把 Agent manifest、architecture harness、CI、control signal、monitor task 或 COMMITTED 外推成 independent semantic correctness / live business quality / global flawlessness。
