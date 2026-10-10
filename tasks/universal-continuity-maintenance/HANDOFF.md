# 跨对话继承系统建设与维护｜Handoff

- task_id: `continuity:universal-continuity-maintenance`
- task_class: `SYSTEM_INFRA`
- owner: `UNIVERSAL_CONTINUITY_HARNESS`
- status: `ACTIVE`
- contract: `CONTINUITY_V3_7`
- current writer: `lease-4b4bc507-0949-4b2e-aed4-c0186dd07566`
- resume_epoch: `2`

## 当前总状态

- **Known-topology** existing-chat / fresh-chat Continuity product E2E：历史真实证据仍 PASS。
- **Real new-owner cold-start product E2E：OPEN。** 过去的 fresh-chat PASS 不能泛化成“未来新增任意 Agent 后，真正失忆的新聊天一定能自动接入”。
- Dynamic owner membership/admission mechanics：`REGRESSION_VERIFIED`。`OWNER_REGISTRY.json` 已成为唯一 owner-membership authority；bare discovery 与 system-audit scope 动态推导。
- Universal operator-dependence incident：仍 OPEN。本轮用户再次需要提醒“从遗忘的新对话 / 新 Agent 视角重审”，这是该 incident 的新增真实证据，不视为用户应继续提供测试用例。
- Second-order challenge / closure calibration 已在 `evolution@1.0`；本轮正是它发现了 closed-world E2E 被错误扩大成 open-world extensibility claim。
- Operational methodology receipt contract = 1.2，evidence ref verification 与 hook-claim semantic verification 分离。
- Novel：release-evidence binding 已加固；真实 CH9 production proof / true independent execution attestation 仍 OPEN。
- Financial：三 profile 已绑定并 regression PASS；真实 article action-level methodology conformance / prose-quality promotion 仍 OPEN。

## 本轮根因：总控“认识谁”存在多份名单

从零知识 / 新 Agent 接入视角重新检查后发现：

1. `OWNER_REGISTRY.json` 看起来像 owner registry；
2. 但旧 `BARE_INHERIT_DISCOVERY.json` 又硬编码 `GENERIC + Financial + A-share + Novel + Video` 五个 source；
3. 旧 `runtime/system_audit.py` 又硬编码四个 `BUSINESS_OWNERS`；
4. 回归测试还把具体 owner 名称和 `required_owner_quorum == 5` 当成永久不变量。

因此“接一个新 Agent”实际上要求维护者记得同步多个 owner-name surface。即使所有旧表彼此一致，也只能证明**已知名单内部一致**，不能证明未来未知 owner 会自动进入 discovery/audit。

这解释了为什么此前我会说“fresh-chat E2E PASS”但仍没真正覆盖用户指出的视角：那次真实 E2E 是 closed-world evidence，只测试了当时已经存在的 topology。

## 架构决策

比较三种方案：

- 再维护一份 central/static owner list：拒绝，继续制造第二 membership authority；
- 新建 onboarding/challenge Agent：拒绝，角色本身不能消除拓扑漂移，也不能创造独立产品证据；
- **`OWNER_REGISTRY` = sole owner-membership authority**：采用。

现在：

- `owner_kind == BUSINESS` 决定 durable business membership；
- `bare_inherit_participant == true` + `bare_inherit_source` 决定 bare discovery quorum；
- `runtime/owner_topology.py` 动态推导 business owners / bare sources，并校验 admission metadata；
- `BARE_INHERIT_DISCOVERY.json` 已删除具体 `required_sources` owner 名单；
- `runtime/system_audit.py` 已删除 `BUSINESS_OWNERS` 常量；
- `OWNER_PROTOCOL_ADAPTATION_REGISTRY` / `OWNER_EXECUTION_REGISTRY` 是 rebuildable conformance/status caches，不是 membership authority；它们必须收敛到 derived BUSINESS set，否则 audit fail closed。

## Synthetic unknown-owner regression

测试中临时加入一个生产代码从未认识过的 `SYNTHETIC_NEW_AGENT`：

1. 只加入 `OWNER_REGISTRY` 后，它自动进入 bare discovery 和 global audit scope；
2. 因 adaptation/execution caches 尚未有它，control-plane audit 必须 FAIL；
3. 测试再补齐两份派生 cache；
4. audit PASS，并且 synthetic owner 同时出现在 checked business/bare sets。

没有修改任何 Python owner-name allowlist 来“教会”系统这个 synthetic name。

Intermediate head `4535ce6fcada3d04fc8bde60d87211432edd00f7`：system_audit PASS，pytest 139 PASS / 1 FAIL；唯一失败是旧 test 精确要求 `OWNER_REGISTRY schema_version == 3.0`。

该旧 topology assertion 被更新，而不是回滚新模型。

Validated behavioral head `e878f8b217356d67ad986033ca04705179197164`：Actions run `38067271852` / job `114257353885`，system_audit PASS + full pytest PASS。

随后 `STARTUP_HOOK.md`、`NEW_CHAT_BOOTSTRAP.json`、`ENTRYPOINT.md` 也改为：每次裸继承从**当前** `OWNER_REGISTRY` 推导 quorum，禁止历史 owner count / copied list；并明确 known-topology E2E 不是 future-owner proof。

## 证据边界

当前可以说：

- `KNOWN_TOPOLOGY_FRESH_CHAT_E2E = PASS`
- `DYNAMIC_OWNER_MEMBERSHIP_MECHANICS = REGRESSION_VERIFIED`

当前**不能**说：

- `REAL_NEW_OWNER_FRESH_CHAT_PRODUCT_E2E = PASS`

因为这个聊天无法制造一个真正独立的新 ChatGPT product session，也不能用 synthetic Python fixture 冒充该产品轨迹。

真实新-owner cold-start PASS 至少需要：

1. 一个真实新 BUSINESS owner 按 canonical registry admission 接入；
2. derived adaptation/execution metadata 收敛；
3. 一个真正新聊天从 `ENTRYPOINT + CURRENT_PROTOCOL` 启动；
4. 它从当前 registry 自动发现/路由该新 owner；
5. 若进入 material work，再通过该 owner 当前 capability/methodology handshake。

在此之前保持 OPEN，不再使用无范围限定的“fresh-chat E2E 已证明一切”。

## 本轮新增 authority / evidence

- `runtime/owner_topology.py`
- `OWNER_REGISTRY.json` schema 3.1 membership authority
- `BARE_INHERIT_DISCOVERY.json` schema 1.1 dynamic quorum
- `runtime/system_audit.py` dynamic owner scope
- `STARTUP_HOOK.md` dynamic topology + cold-start evidence boundary
- `NEW_CHAT_BOOTSTRAP.json` dynamic quorum / new-owner verification boundary
- `ENTRYPOINT.md` owner admission + closed-world/open-world claim boundary
- `tests/test_bare_inherit_discovery.py`
- `tests/test_system_audit.py`
- `tests/test_universal_continuity.py`
- `tests/test_startup_hook.py`
- `audits/COLD_START_NEW_OWNER_TOPOLOGY_INCIDENT_2026-10-11.md`

## 仍未闭环

1. **Universal real new-owner fresh-chat product E2E**：OPEN。
2. **Universal operator-dependence incident**：OPEN；仍需 independently graded held-out product trajectories，且本轮新增用户提醒作为真实负向证据。
3. **Novel first hardened CH9 real production trajectory**：OPEN。
4. **Novel true independent execution attestation**：OPEN。
5. **Financial action-level operational methodology proof**：OPEN。
6. **Financial prose-quality blind pairwise promotion**：OPEN。
7. **Personalized Writing DNA**：仍需自然产生的 acceptance/edit/performance evidence。

## Current stage

`V3_7_KNOWN_TOPOLOGY_PRODUCT_E2E_PASS__NEW_OWNER_COLD_START_PRODUCT_E2E_PENDING__DYNAMIC_OWNER_MEMBERSHIP_REGRESSION_PASS__OPERATOR_DEPENDENCE_INCIDENT_ACTIVE__OWNER_PROFILE_APPLICABILITY_GUARD_PASS__SECOND_ORDER_EVOLUTION_METHOD_DISTILLED__NOVEL_RELEASE_EVIDENCE_BINDING_HARDENED__FINANCIAL_THREE_PROFILES_BOUND_AND_REGRESSION_PASS__ACTION_LEVEL_CONFORMANCE_PENDING__LIVE_QUALITY_EVIDENCE_PENDING`

## Next action

- 任何新的 owner admission：只在 `OWNER_REGISTRY` 声明 membership；不新增第二 owner-name allowlist；派生 caches 未收敛则 fail closed。
- 出现真实新 BUSINESS owner 后，用真正 fresh chat 跑 new-owner cold-start product E2E；没有真实产品轨迹前保持 OPEN。
- 任何 non-trivial evolution 继续执行二阶挑刺，特别检查 known-case evidence 是否被误说成 open-world/generalized proof。
- Universal operator-dependence incident 在真实 independently graded held-out trajectories 前不关闭，也不再要求用户继续举例。
- Novel / Financial 保持各自现有 live-evidence gates，不偷 business lease，不伪造 independent evidence。

## Recovery refs

- `tasks/universal-continuity-maintenance/TASK_MANIFEST.json`
- `ENTRYPOINT.md`
- `STARTUP_HOOK.md`
- `NEW_CHAT_BOOTSTRAP.json`
- `OWNER_REGISTRY.json`
- `BARE_INHERIT_DISCOVERY.json`
- `runtime/owner_topology.py`
- `runtime/system_audit.py`
- `audits/COLD_START_NEW_OWNER_TOPOLOGY_INCIDENT_2026-10-11.md`
- `CONTINUOUS_LEARNING_POLICY.md`
- `audits/UNIVERSAL_OPERATOR_DEPENDENCE_RELIABILITY_INCIDENT_2026-10-10.md`

恢复时先读 manifest + 本 Handoff，再按 `ENTRYPOINT.md` 事件矩阵加载当前动作所需 authority。不要从旧聊天、历史 owner 数量或旧 topology 重建当前执行真相。
