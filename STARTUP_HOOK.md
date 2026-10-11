# Universal Continuity — Account Startup Hook

Status: REQUIRED_FOR_BARE_INHERIT_ACCOUNT_LEVEL_ROUTING  
Hook: ACCOUNT_ROUTER_V2  
Updated: 2026-10-11

## Purpose

GitHub and ChatGPT Library are durable storage/discovery surfaces, **not automatic event listeners**. This file defines only the account-level trigger into current repository authority. It is not business authority, task storage, execution proof, or a copy of the evolving control plane.

## Canonical Custom Instructions

Use the following text, or a semantically equivalent minimal account-level instruction:

> 当我明确发送“继承”“继续”“恢复”“接着上次”，或“继承/继续/恢复：<任务名>”时，优先按 CONTINUE 处理并启动 `D1traverser-debug/universal-continuity-agent@main`。
>
> **启动时不要机械预读整个仓库。** 只先读取 `ENTRYPOINT.md` 与 `CURRENT_PROTOCOL.json`，然后按当前 `ENTRYPOINT.md` 的 Event-driven authority loading 执行；`SYSTEM_BLUEPRINT.md`、审计、研究资料、无关 owner 和旧聊天均为 cold-path。
>
> 不得从 Memory/旧聊天重建持久化事实。系统维护、用户实质纠正或学习进化触发时，按当前仓库 authority 主动闭环，不等待我继续列举内部问题；有 durable task 时按当前仓库规则在 material safe point 持久化并回读。
>
> 若 Continuity authority 无法访问，回复 `CONTINUITY_BOOTSTRAP_UNAVAILABLE`，不得猜测。

## Thin-hook invariant

- Account-level Custom Instructions only activate the current repository authority. Bare/named routing details, owner discovery, lease/takeover, capability readiness, methodology, learning, progress receipts and version compatibility remain in the repository and must not be copied into the account hook.
- Change account-level Custom Instructions only when **pre-repository activation/routing/fail-closed semantics** change. Compatible internal protocol/profile/policy evolution must not force account-instruction churn.
- Existing/open chats reconcile through current repository authority. True takeover semantics remain in `ENTRYPOINT.md` and the task authority.
- This repository cannot prove that the account-level text is actually installed. Product-surface propagation requires product evidence when relevant.
- 只有发生文件/Artifact、系统维护、学习进化、媒体蒸馏等事件时，才按 `ENTRYPOINT.md` 加载对应 profile/semantics owner；不要把这些规则复制进固定启动 prompt。

## Event-driven authority loading

After `ENTRYPOINT.md + CURRENT_PROTOCOL.json`, follow only the current `ENTRYPOINT.md` routing map. The account hook does not maintain a second owner list, capability list, profile list, receipt algorithm or protocol migration table.

## Cold-start and writer boundary

Historical fresh-chat evidence does not prove a future owner. A real new-owner cold-start still requires a genuinely fresh product chat after admission. An active writer reconciles supported changes in place; only a legal new-chat takeover replaces the writer lease. System maintenance never grants permission to take a BUSINESS lease or rewrite owner business truth.
