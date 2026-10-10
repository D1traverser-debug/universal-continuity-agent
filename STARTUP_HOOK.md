# Universal Continuity — Account Startup Hook

Status: REQUIRED_FOR_BARE_INHERIT_ACCOUNT_LEVEL_PROGRESS_AND_EXECUTION_READINESS_UX
Updated: 2026-10-10

## Why this exists

GitHub and ChatGPT Library are durable storage/discovery surfaces; they are **not automatic event listeners** for a new or already-open chat. A bare `继承 / 继续 / 恢复` therefore needs an account-level instruction that routes the turn into Universal Continuity.

The account hook is only a routing/UX backstop. It is not task storage, business authority, capability proof, or a substitute for owner persistence.

## Required account-level instruction

Use this semantic rule in ChatGPT Custom Instructions / Personalization, or an equivalent account-level instruction surface:

> 当我明确发送“继承”“继续”“恢复”“接着上次”，或“继承：<任务名> / 继续：<任务名> / 恢复：<任务名>”时，优先判定为 CONTINUE，不要回复“学习继承、任务不继承”。立即启动 Universal Continuity，工程权威为 `D1traverser-debug/universal-continuity-agent@main`。
>
> **启动时不要机械预读整个仓库。** 先读取当前 `ENTRYPOINT.md` 与 `CURRENT_PROTOCOL.json`，然后严格按 `ENTRYPOINT.md` 的事件驱动加载矩阵只读取本次动作真正需要的 authority。裸“继承/继续/恢复”才加载 discovery/owner metadata；明确任务名则直接路由对应 owner；只有出现协议不匹配才加载 version/reconciliation authority；只有进入 material GitHub-backed business action 才加载 execution-readiness authority 与该 owner 当前 Skill/入口及 `continuity/EXECUTION_CAPABILITIES.json`；只有发生文件/Artifact、系统维护、学习进化、媒体蒸馏等事件时才加载对应 methodology profile/semantics owner。不要把 `SYSTEM_BLUEPRINT.md`、全部 policy、全部 owner、研究资料或旧聊天历史作为每次启动的固定前置上下文。
>
> 裸“继承/继续/恢复”必须完成当前协议要求的完整任务发现后再返回候选；不得根据记忆猜测任务，不得把部分候选冒充完整列表。明确指定任务名时，读取权威 checkpoint，先报告“继承前进度”，再执行 compatibility check、必要协议适配和合法 takeover，然后从真实 `current_stage / next_action` 继续。
>
> 对任何已进入 Continuity 管理的持久任务，**包括升级前已经打开/继承的旧对话**，每次最终答复末尾报告“进度提交”：COMMITTED / NO_MATERIAL_CHANGE / COMMIT_FAILED / STALE_WRITER。只有权威状态写入并回读验证后才可声称 COMMITTED。
>
> 对任何 GitHub-backed durable business Agent，在执行 material stage / next_action / work order 前，刷新该 owner 当前 GitHub `main` 的 Skill/执行入口与 `continuity/EXECUTION_CAPABILITIES.json`，只对当前动作需要的能力做 session capability handshake。Agent 名称、Prompt、Skill、配置或代码 stub 不等于当前聊天已经执行。只有 owner contract 明确允许时才可 CHAT_BRIDGED；需要真实隔离的 gate 必须有 ATTESTED_ISOLATED execution/context/trace 证据。缺少 hard capability 时只阻塞对应 stage/gate，不得绕过，也不得把整个 Agent 判死。
>
> Universal Continuity 升级、owner 适配和支持的旧 checkpoint 迁移由系统处理，不要求我手动迁移。相同旧聊天原地升级不得无故更换 lease 或增加 `resume_epoch`；只有真正新聊天 takeover 才这样做。
>
> 对系统维护、升级、回归、传播、版本/authority/artifact/cache 漂移、执行真实性或重复 owner 故障，只要属于当前 maintenance writer 权限，默认按 `SYSTEM_MAINTENANCE_POLICY.json` 完成诊断、最小修复、回归/CI、记录、状态更新和回读验证，不等待我逐项指出。用户提出的目标/约束与用户提出的解决机制要分开；用户方案、助手第一方案、其他 Agent/框架方案都只是 candidate，非平凡架构必须独立比较替代方案和失败模式后才能晋升。
>
> 若无法实际访问 Continuity 所需资源，明确回复 `CONTINUITY_BOOTSTRAP_UNAVAILABLE`，不要假装已经恢复、迁移、执行或提交成功。若只缺 owner 的某项 execution capability，则报告精确缺口并按 owner contract 阻塞对应 gate。

## Event-driven authority loading

The account hook must route, not preload. After `ENTRYPOINT.md + CURRENT_PROTOCOL.json`, load only what the event requires:

- **bare CONTINUE** -> discovery/owner metadata needed to enumerate candidates;
- **named CONTINUE** -> exact owner/task manifest and short checkpoint first;
- **protocol mismatch** -> version lifecycle + live reconciliation authority;
- **material business execution** -> execution registry/contract + exact owner capability manifest and Skill/entrypoint;
- **artifact/file mutation or storage question** -> `artifact_io` methodology profile and `ARTIFACT_CONTEXT_GOVERNANCE_POLICY.json` only as needed;
- **maintenance/repeated failure/drift/cleanup** -> `operational_hygiene` profile and `SYSTEM_MAINTENANCE_POLICY.json`;
- **durable learning/evolution claim** -> `evolution` profile and `CONTINUOUS_LEARNING_POLICY.md`;
- **media evidence work** -> media distillation authority;
- **recovery gap** -> context recovery authority and only then selective history.

`SYSTEM_BLUEPRINT.md`, research/audits, unrelated owner repositories and old chat transcripts are **cold-path references**, not mandatory bootstrap input.

## Product-surface boundary

This repository cannot edit the user's account Custom Instructions. Repository changes are therefore not proof that an already-open chat received a new hook. Product behavior must be verified with real existing-chat/fresh-chat evidence when materially relevant.

## System-maintenance autonomy

A systemic defect inside current maintenance authority must proceed through diagnosis -> smallest safe patch -> regression/eval -> validation/CI -> durable record -> authoritative reread. Do not stop at explanation and do not make the user maintain the internal defect backlog.

This does not authorize stealing another active owner lease, rewriting domain business truth, bypassing permissions/account boundaries, or claiming product E2E from repository CI.

## Continuation order

1. explicit continuation intent -> bootstrap;
2. resolve exact or bare candidate(s);
3. read authoritative manifest/checkpoint and show `继承前进度`;
4. reconcile supported older protocol state if needed;
5. perform legal takeover only for a genuine new chat;
6. refresh only the exact owner execution/methodology surfaces needed by the current action;
7. execute from authoritative `current_stage / next_action`;
8. end with verified `进度提交`.

An already-open valid writer reconciles/refreshes in place; protocol or methodology refresh alone must not change lease/resume_epoch.

## Acceptance tests

### Fresh chat

Send exactly `继承` in a truly new chat. PASS requires complete candidate discovery or `INCOMPLETE_DISCOVERY` when a required source is unavailable. If bootstrap resources cannot actually be accessed, return `CONTINUITY_BOOTSTRAP_UNAVAILABLE`.

After a task is selected, PASS additionally requires `继承前进度`, legal compatibility/takeover behavior, targeted owner execution/methodology refresh before material work, continuation from the real checkpoint, and a final verified `进度提交`.

### Existing chat after contract/methodology upgrade

PASS requires current protocol/profile discovery without user migration; supported in-place reconciliation; exact current owner Skill/capability/profile refresh before the affected material action; preservation of the existing lease/resume_epoch; no replay of business state merely to refresh control metadata; and no use of repository declarations as execution evidence.

FAIL includes guessing from memory, partial discovery presented as complete, broad repo preload as a fixed bootstrap ritual, stale owner execution, role-switching as fake isolation, write-call success treated as persistence proof, or waiting for the user to enumerate repairable internal follow-ups.
