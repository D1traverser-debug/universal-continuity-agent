# 跨对话继承系统建设与维护｜Handoff

- task_id: `continuity:universal-continuity-maintenance`
- task_class: `SYSTEM_INFRA`
- owner: `UNIVERSAL_CONTINUITY_HARNESS`
- status: `ACTIVE`
- contract: `CONTINUITY_V3_7`
- current writer: `lease-4b4bc507-0949-4b2e-aed4-c0186dd07566`
- resume_epoch: `2`

## 当前结论

Universal v3.7 existing-chat / fresh-chat Continuity 产品传播 E2E 已 PASS。四个业务 owner 的 methodology declaration 现在不仅有 exact-version profile binding，还必须覆盖**所有当前 contract profiles 的 applicability**；但 declaration/applicability/owner CI 仍不是 action-level operational proof。

本轮由用户再次质疑触发 reliability/evolution maintenance。上一轮 Financial Writing 漏绑 `artifact_io@1.0` 的根因不是单一粗心，而是两层同时失效：

1. **判断错误**：维护者先入为主地把 Financial 归类成只需要 `operational_hygiene + evolution`；
2. **验收结构缺口**：旧 `evaluate_methodology_conformance()` 只验证 `profile_refs` 中已经声明的 profile，不检查“未声明 profile 是否其实适用”，因此错误的 omission assumption 可以穿过 CI。

这类缺口命名为 **methodology negative-space blind spot / silent applicable-profile omission**。

## 进化方案与取舍

比较过三种方案：

- 所有 owner 强制绑定全部 profile：拒绝，会破坏 composability / event-driven loading，并给真实不适用 owner 增加虚假义务；
- 依赖维护者每次人工阅读 Skill/代码决定：拒绝，仍然依赖同一判断者，无法机械防复发；
- **显式 profile applicability contract**：采用。每个 current-contract profile 都必须是 `APPLIES` 或 `NOT_APPLICABLE`，并带 owner-local `reason + evidence_refs`；`APPLIES` 必须 exact-version 绑定，`NOT_APPLICABLE` 不能同时声明 profile，省略不再代表“不适用”。

## 已落地的中央修复

- `runtime/methodology_conformance.py`：加入 negative-space declaration validation；`APPLIES` 但漏绑直接 `applicable_profile_not_declared:<profile>`。
- `OWNER_ADAPTER_CONTRACT.json`：profile contract 仍为 `1.0`；新增 `owner_declaration_contract_version=1.1`，因为 hook/invariant contract 未变化，但 declaration shape 被强化。
- `ENTRYPOINT.md`：material owner action 在执行前先验证完整 profile applicability，再进入 event-activated operational conformance。
- `tests/test_methodology_conformance.py`：覆盖 missing applicability、APPLIES-but-omitted、NOT_APPLICABLE 缺 reason/evidence、声明/不适用矛盾。
- `runtime/system_audit.py`：加入真实失败类负例 `methodology_applicable_profile_is_silently_omitted`；synthetic owner 明确模拟“会持久化/render artifact，但漏绑 artifact_io”，必须 FAIL。
- `tests/test_system_audit.py`：固定该 fault scenario，防后续静默删除。

关键 commits：
- validator `a7c94124a57b24e9d646bf5755ccd409c620c792`
- methodology tests `547ed96aba63cf0ca74762f1ebbeee4d0f680b0d`
- owner declaration contract `ba4fe98b6afda19cf6eadae5095ffce356a0287d`
- ENTRYPOINT `2517ffd86436abf2130a5999b04ba84a0300e210`
- system-audit regression `c42cc58dadf53625bb48255ecaa59dc44208ef54`
- fault-scenario test `31bf410cba1303ab0f36b7de8d723ea8f381a4f3`

第一次 Universal CI run `38063164287` **FAIL**，原因是 `system_audit` 旧 synthetic declaration fixture 没有新 `profile_applicability`；没有绕过失败。升级 fixture 并加入 omission negative case 后，run `38063287004` **PASS**，其中 `runtime.system_audit` 与完整 pytest 均 PASS。

## 四个 owner applicability evidence

未接管任何业务 task lease/state，只更新 owner 工程 adapter：

- Financial: `8f7710b64c330e0770154e65a40b4abc9a4e932d` / CI `38063063135` PASS。
- A-share: `d001a857d94eaa2a103798d7186589a4931b2af1` / CI `38063084164` PASS。
- Novel: `94d3626fa6695fdcb41b9139f42cd28853d3106a` / CI `38063108153` PASS；Canon/正文/发布事实/stage/lease 未改。
- Video: `e3b60458ef858e963acd3417d4f188a2d0518f6b` / CI `38063131876` PASS。

四者当前三个 profile 都是 APPLIES，但新 contract 不要求未来 owner 必须“三件套”；真实不适用 profile 可声明 NOT_APPLICABLE，只是必须可审计，不能静默省略。

## Financial 当前边界

Financial 已绑定：
- `artifact_io@1.0`
- `operational_hygiene@1.0`
- `evolution@1.0`

且 artifact_io binding 与 applicability evidence 已 owner CI 验证。Financial 业务 durable task `financial-writing:main` 的 active lease、manifest/Handoff、文章 stage/内容未被本 maintenance writer 修改。

仍不能声称：
- 一篇新的真实 Financial article 已通过 action-level methodology receipt；
- prose quality 已客观提升；
- Personalized Writing DNA 已成熟。

## 仍未闭环

1. **Financial action-level operational proof**：下一次真实 material article action 必须留下 event-activated `profile_runs`、observed hooks、stable evidence refs，并由 independent verifier 验证后跑 operational methodology conformance。
2. **Financial prose-quality promotion**：仍需 independently verifiable blind pairwise evidence；offshore-wind rejection 必须改善，rutile held-out 不退化。
3. **Personalized Writing DNA**：仍需自然产生的真实 user acceptance/edit 或 post-publication performance evidence。
4. **Universal operator-dependence incident**：本轮证明系统能从用户纠正中形成 durable guard，但事故总体仍需真实 held-out maintenance-decision trajectories + independent grading 才能关闭。

## Current stage

`V3_7_PRODUCT_E2E_PASS__OPERATOR_DEPENDENCE_INCIDENT_ACTIVE__OWNER_PROFILE_APPLICABILITY_GUARD_PASS__FINANCIAL_THREE_PROFILES_BOUND_AND_REGRESSION_PASS__ACTION_LEVEL_CONFORMANCE_PENDING__LIVE_QUALITY_EVIDENCE_PENDING`

## Next action

- 下一次真实 Financial material action：先 declaration/applicability conformance，再仅激活本动作需要的 profiles，最后用真实 receipt + independent verifier 做 operational conformance。
- 有独立 Financial blind pairwise judge/verifier 时跑 quality promotion。
- 有独立 Universal product-run/grader path 时跑 maintenance-decision held-out suite。
- 不以 CI 替代 live evidence，不要求用户制造内部验收样本，不偷 owner business lease。

## Recovery refs

- `tasks/universal-continuity-maintenance/TASK_MANIFEST.json`
- `OWNER_ADAPTER_CONTRACT.json`
- `OWNER_REGISTRY.json`
- `OWNER_PROTOCOL_ADAPTATION_REGISTRY.json`
- `ENTRYPOINT.md`
- `runtime/methodology_conformance.py`
- `runtime/system_audit.py`
- `tests/test_methodology_conformance.py`
- `tests/test_system_audit.py`

恢复时先读 manifest + 本 Handoff，再按 ENTRYPOINT 事件矩阵加载当前动作所需 authority；不要从旧聊天重建执行真相。
