# Universal Continuity — Account Startup Hook

Status: REQUIRED_FOR_BARE_INHERIT_ACCOUNT_LEVEL_ROUTING  
Updated: 2026-10-11

## Purpose

GitHub and ChatGPT Library are durable storage/discovery surfaces, **not automatic event listeners**. This hook only routes explicit continuation intent into Universal Continuity; it is not business authority, task storage, execution proof, or a copy of the full control plane.

## Account-level semantic rule

Use the following meaning in ChatGPT Custom Instructions / Personalization, or an equivalent account-level instruction surface:

> 当我明确发送“继承”“继续”“恢复”“接着上次”，或明确指定“继承/继续/恢复：<任务名>”时，优先判定为 CONTINUE，并启动 `D1traverser-debug/universal-continuity-agent@main`。
>
> **启动时不要机械预读整个仓库。** 只先读取 `ENTRYPOINT.md` 与 `CURRENT_PROTOCOL.json`，随后按 `ENTRYPOINT.md` 的 Event-driven authority loading 只加载当前动作真正需要的 authority。`SYSTEM_BLUEPRINT.md`、审计、研究资料、无关 owner 和旧聊天历史都是 cold-path。
>
> 裸 CONTINUE 必须从当前 `OWNER_REGISTRY.json` 动态推导完整 discovery quorum，不能使用记忆、复制名单或 historical owner count。明确任务名则直接读取该任务权威 manifest/checkpoint，先报告“继承前进度”，再做必要 compatibility / takeover，并从真实 `current_stage / next_action` 继续。
>
> 对 material GitHub-backed owner action，刷新该 owner 当前 Skill/入口与 `continuity/EXECUTION_CAPABILITIES.json`，只握手当前动作需要的 capability。Prompt、Skill、配置、角色名或代码 stub 都不等于执行证据；缺 hard capability 时只阻塞对应 gate。
>
> 对系统维护、重复故障、架构/authority 漂移或用户对维护完整性的实质纠正，进入当前 maintenance/evolution authority，不等待我继续列举内部问题。用户提出的目标和建议机制要分开，非平凡修复必须比较替代方案并攻击自己的修复。
>
> 每次最终答复末尾必须报告“进度提交”：COMMITTED / NO_MATERIAL_CHANGE / COMMIT_FAILED / STALE_WRITER。COMMITTED 只表示权威状态已写入并回读，不表示质量、审核或执行保证已通过。
>
> 若无法访问 Continuity 必需资源，回复 `CONTINUITY_BOOTSTRAP_UNAVAILABLE`，不得从 Memory/旧聊天猜恢复状态。

该路由/兼容规则也覆盖**包括升级前已经打开/继承的旧对话**；已有合法 writer 先做 in-place reconciliation，不因为协议升级伪造 takeover，**不要求我手动迁移旧对话**。只有真正的新聊天 takeover 才替换 writer lease / `resume_epoch`。

This repository cannot prove that account-level Custom Instructions were changed merely because this file changed. Product-surface propagation needs real product evidence when relevant.

## Event-driven authority loading

After `ENTRYPOINT.md + CURRENT_PROTOCOL.json`:

- bare CONTINUE → current `OWNER_REGISTRY.json` + `BARE_INHERIT_DISCOVERY.json`;
- named CONTINUE → exact owner/task manifest + short checkpoint;
- protocol mismatch → version/reconciliation authority;
- material owner execution → exact owner Skill/capability + execution-readiness authority;
- owner admission / architecture drift → `OWNER_REGISTRY.json` + `AGENT_ARCHITECTURE_CONTRACT.json` + architecture observations;
- artifact/file work → `artifact_io@1.0` only when activated;
- maintenance/drift/repeated failure → `operational_hygiene@1.0` + `SYSTEM_MAINTENANCE_POLICY.json`;
- durable learning/evolution → `evolution@1.0` + `CONTINUOUS_LEARNING_POLICY.md`;
- media evidence → media distillation authority;
- recovery gap → recovery authority, then selective history only if still needed.

只有发生文件/Artifact、系统维护、学习进化、媒体蒸馏等事件时，才加载对应 profile/semantics owner；不要把它们复制成固定启动 prompt。

## Cold-start evidence boundary

Historical fresh-chat evidence proves only the owner topology actually observed at that time. It is not open-world proof for a future owner.

A real **new-owner cold-start** claim requires, after admission, a genuinely fresh product chat that routes/discovers that owner from current authority. Synthetic regression can prove registry/discovery mechanics but cannot impersonate that product trajectory.

## Single-writer boundary

An active writer refreshes compatible control metadata in place. A legal takeover supersedes the old lease according to the task contract; stale writers stop authoritative mutation. Maintenance authority does not permit stealing another business task lease or rewriting owner business truth.
