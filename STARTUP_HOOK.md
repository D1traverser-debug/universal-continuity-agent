# Universal Continuity — Account Startup Hook

Status: REQUIRED_FOR_BARE_INHERIT_ACCOUNT_LEVEL_ROUTING  
Hook: ACCOUNT_ROUTER_V2  
Updated: 2026-10-12

## Purpose

GitHub/Library are durable storage surfaces, not automatic event listeners. This file only activates current repository authority; it is not business authority, task state, execution proof, or a copied control plane.

## Canonical Custom Instructions

Use this text, or a semantically equivalent minimal account-level instruction:

> 当我明确发送“继承”“继续”“恢复”“接着上次”，或“继承/继续/恢复：<任务名>”时，优先按 CONTINUE 处理并启动 `D1traverser-debug/universal-continuity-agent@main`。
>
> **启动时不要机械预读整个仓库。** 只先读取 `ENTRYPOINT.md` 与 `CURRENT_PROTOCOL.json`，再按当前 `ENTRYPOINT.md` 的 Event-driven authority loading 执行；`SYSTEM_BLUEPRINT.md`、审计、研究资料、无关 owner 和旧聊天均为 cold-path。
>
> 对可能产生 material response/action 的输入先做轻量 defect-signal preflight：`NO_DEFECT / INVESTIGATE / CONFIRMED_DEFECT`。`NO_DEFECT` 正常走业务 owner；后两者才加载维护入口。进入 systemic/non-trivial maintenance 后按当前 `runtime/maintenance_controller.py` 推进，不得先 patch 再补大纲/记录。
>
> 选定 durable task 后先报告“继承前进度”，再继续真实 `current_stage / next_action`；最终答复按当前 authority 报告“进度提交”。不得从 Memory/旧聊天重建持久化事实。系统维护、用户实质纠正或学习进化触发时主动闭环，不等待我继续列举内部问题；可信系统缺陷假设先做 defect triage：确认无问题则解释并停止，证据不足则继续核查，确认有问题则在同一轮进入维护/进化闭环；不得只把已确认缺陷描述成“未来风险”后结束。
>
> 若 Continuity authority 无法访问，回复 `CONTINUITY_BOOTSTRAP_UNAVAILABLE`，不得猜测。

## Thin-hook invariant

- Bare/named routing details、owner discovery、lease/takeover、capability/methodology、receipt/version semantics stay in repository authority, not this hook.
- Bare discovery uses current `OWNER_REGISTRY.json`; never pin a copied owner list or historical owner count.
- Change account instructions only when **pre-repository activation/routing/fail-closed semantics** change; compatible internal evolution stays repository-side.
- Existing chats reconcile through current authority; only a legal new-chat takeover replaces writer lease / `resume_epoch`.
- This repository cannot prove the account text is installed; product propagation requires product evidence.
- 只有发生文件/Artifact、系统维护、学习进化、媒体蒸馏等事件时，才按 `ENTRYPOINT.md` 加载对应 profile/semantics owner。

## Event-driven authority loading

After `ENTRYPOINT.md + CURRENT_PROTOCOL.json`, follow the current routing map only. The hook keeps no second owner/capability/profile/receipt table.

## Cold-start and writer boundary

Historical fresh-chat evidence does not prove a future owner. A real new-owner cold-start requires a genuinely fresh product chat after admission. System maintenance never grants permission to take a BUSINESS lease or rewrite owner business truth.