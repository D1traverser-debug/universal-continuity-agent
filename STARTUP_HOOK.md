# Universal Continuity — Account Startup Hook

Status: REQUIRED_FOR_BARE_INHERIT_ACCOUNT_LEVEL_PROGRESS_AND_EXECUTION_READINESS_UX
Updated: 2026-10-10

## Why this exists

GitHub and ChatGPT Library are durable storage/discovery surfaces. They are **not automatic event listeners** for a new chat or an already-open chat.

A bare user message such as `继承` will only reach Universal Continuity reliably if the chat has an account-level instruction that tells ChatGPT to invoke the continuity bootstrap. Without that hook, ChatGPT may answer from generic Memory/past-chat context instead and never query GitHub/Library.

The same account-level instruction is also the UX backstop for the per-turn `进度提交` receipt and for execution-readiness refresh in already-existing GitHub-backed durable-task chats. It does not replace owner persistence, owner Skills, capability manifests or authoritative verification.

## Required account-level instruction

Use this exact semantic rule in ChatGPT Custom Instructions / Personalization (or an equivalent account-level instruction surface):

> 当我在任何对话中明确发送“继承”“继续”“恢复”“接着上次”，或“继承：<任务名> / 继续：<任务名> / 恢复：<任务名>”时，优先判定为 CONTINUE，不要回复“学习继承、任务不继承”。立即启动我的 Universal Continuity，工程权威为 `D1traverser-debug/universal-continuity-agent@main`。先读取并严格遵循该仓库当前 `ENTRYPOINT.md`、`SYSTEM_BLUEPRINT.md`、`CURRENT_PROTOCOL.json`、`STARTUP_HOOK.md`，再按其要求读取 Continuity contract、bootstrap、owner registry、discovery policy、`SYSTEM_MAINTENANCE_POLICY.json` 和对应业务 owner。裸“继承/继续/恢复”必须完成当前协议要求的完整任务发现后再返回候选；不得根据记忆猜测任务，不得把部分候选冒充完整列表。明确指定任务名时，直接路由对应 owner，读取权威 checkpoint，先报告“继承前进度”，再执行 compatibility check、必要的协议自动适配和 takeover，然后从真实 current_stage / next_action 继续。对于任何已经进入 Universal Continuity 管理的持久任务，包括升级前已经打开/继承的旧对话，每次最终答复末尾必须报告“进度提交”：COMMITTED / NO_MATERIAL_CHANGE / COMMIT_FAILED / STALE_WRITER，并说明当前权威持久化的 stage / next_action；只有权威状态写入成功并回读验证后才能声称 COMMITTED。对于任何 GitHub-backed durable business Agent，在执行 material stage / next_action / work order 之前，必须重新读取该 owner 当前 GitHub `main` 的 Skill/执行入口与 `continuity/EXECUTION_CAPABILITIES.json`，只对当前步骤需要的能力做 session capability handshake；GitHub 中存在 Agent 名称、Prompt、Skill、配置或代码 stub 不等于该能力已在当前聊天执行。只有 owner contract 明确允许时才可使用 CHAT_BRIDGED；要求真实隔离的 gate 必须有 ATTESTED_ISOLATED 级别的独立 execution/context/trace 证据，不能用同一聊天切换角色冒充。缺少 hard capability 时只阻塞对应 stage/gate，不得绕过、不应把整个 Agent 宣判不可用。Universal Continuity 升级、owner 适配、旧 checkpoint 迁移由系统自动处理，不要求我手动迁移旧对话；同一旧聊天的协议原地升级不得无故更换 lease 或增加 resume_epoch，只有真正的新聊天 takeover 才能这样做。对于系统维护、升级、回归、传播、版本漂移或执行真实性问题，只要属于当前维护 writer 的权限范围，默认按 `SYSTEM_MAINTENANCE_POLICY.json` 自动完成诊断、最小修复、回归/CI、维护记录、权威状态更新和回读验证，不等待我逐项指出；只有外部账户/UI操作、新权限/凭证、不可逆高影响选择或无法安全推断的外部事实才需要我介入。若无法实际访问 Continuity 所需资源，明确回复 `CONTINUITY_BOOTSTRAP_UNAVAILABLE`，不要假装已经恢复、迁移、执行或提交成功；若仅 owner execution-readiness 的特定能力不可用，则报告精确缺口并按 owner contract 阻塞对应 stage/gate。

## Product-surface boundary

The repository cannot edit the user's ChatGPT Personalization/Custom Instructions by itself. The account instruction above must exist on the account-level instruction surface for global routing/UX behavior, including already-open chats that otherwise may never re-read GitHub. Repository policy remains the durable engineering authority for how the behavior is executed and verified.

Current OpenAI product behavior should be verified against current first-party documentation when this assumption matters. The repository must not treat an old product-behavior claim as permanent protocol truth.

## System-maintenance autonomy

For an active Universal Continuity / cross-agent control-plane maintenance task, follow `SYSTEM_MAINTENANCE_POLICY.json` whenever a systemic defect or adjacent causally related maintenance issue is detected.

Do not stop after explaining the defect if the fix is within current authority. Continue through diagnosis, minimum safe patch, regression guard, validation/CI, durable maintenance/change record, task status update and authoritative re-read. Do not make the user act as the internal maintenance operator.

This autonomy never authorizes stealing another active owner lease, rewriting domain business truth, bypassing a product/account boundary, or claiming product-level E2E without real evidence.

## Conflict rule

The durable principle `学习继承，任务不继承` still applies to **NEW_TASK** classification.

It must **not** suppress an explicit continuation command. A user message whose primary intent is `继承/继续/恢复` is `CONTINUE`, not `NEW_TASK`.

Priority for continuation:
1. explicit continuation command -> Universal Continuity bootstrap;
2. resolve exact or bare candidate(s);
3. read authoritative manifest/checkpoint and surface `继承前进度`;
4. reconcile any supported older protocol state to the current protocol without asking the user to migrate it;
5. compatibility/takeover when a true new-chat takeover is occurring;
6. before material GitHub-backed business execution, refresh the owner Skill/entrypoint + `continuity/EXECUTION_CAPABILITIES.json` and perform a targeted current-session capability handshake;
7. continue from authoritative `current_stage / next_action` using only an execution mode allowed by the owner capability contract;
8. every final response on the active durable task ends with verified `进度提交` status.

For an already-open active task chat after a protocol or owner execution-contract upgrade, reconcile/refresh in place on the next durable turn; do not pretend a new resume occurred and do not steal the current lease.

## Acceptance tests

### Fresh chat

Open a truly new chat and send exactly `继承`.

PASS requires one of:
- complete candidate discovery and a consistent candidate list/count; or
- `INCOMPLETE_DISCOVERY` if a required owner source is unavailable.

If the Continuity bootstrap resources themselves cannot actually be accessed, return `CONTINUITY_BOOTSTRAP_UNAVAILABLE`; do not fabricate discovery or recovery.

After selecting a task, PASS additionally requires `继承前进度`, compatibility/protocol reconciliation, legal takeover, continuation from the real checkpoint, targeted execution-readiness handshake before material business action, and a final `进度提交` receipt.

### Existing chat after protocol/execution-contract upgrade

Continue an already-open durable task that was inherited under an older supported protocol or loaded an older owner Skill/execution contract.

PASS requires:
- current protocol is discovered without asking the user to migrate;
- supported protocol metadata is reconciled in place by the valid task writer;
- current owner Skill/entrypoint and `continuity/EXECUTION_CAPABILITIES.json` are refreshed before the next material business action;
- only capabilities needed by that action are handshaken;
- existing `resume_epoch` and `active_lease` are preserved solely because protocol/execution metadata changed;
- business state is not replayed or rewritten merely to refresh execution metadata;
- repository declarations are not counted as execution evidence;
- the final response uses the current `进度提交` receipt.

FAIL includes:
- replying only that learning/rules are inherited while task state is not;
- asking the user to re-explain prior workflows before attempting bootstrap;
- asking the user to choose or perform protocol migration;
- claiming a total candidate count from a partial owner scan;
- continuing a fresh takeover without showing where the durable task was previously persisted;
- incrementing a lease epoch merely because the protocol or execution metadata was upgraded in the same chat;
- executing from stale role/config assumptions without refreshing the owner capability contract before a material step;
- counting Agent names/Prompts/Skill/config/code stubs as proof that specialists actually executed;
- satisfying an isolated gate by role-switching inside one unverified chat context;
- saying progress was saved merely because the assistant remembers it or because a write call returned success without authoritative verification;
- waiting for the user to enumerate internal maintenance follow-ups that are already detectable and repairable within the active maintenance authority.
