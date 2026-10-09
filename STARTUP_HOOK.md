# Universal Continuity — Account Startup Hook

Status: REQUIRED_FOR_BARE_INHERIT
Updated: 2026-10-09

## Why this exists

GitHub and ChatGPT Library are durable storage/discovery surfaces. They are **not automatic event listeners** for a new chat.

A bare user message such as `继承` will only reach Universal Continuity reliably if the new chat has an account-level instruction that tells ChatGPT to invoke the continuity bootstrap. Without that hook, ChatGPT may answer from generic Memory/past-chat context instead and never query GitHub/Library.

Therefore a successful GitHub/Library migration alone is **not sufficient** to claim that bare `继承` is wired end-to-end.

## Required account-level instruction

Use this exact semantic rule in ChatGPT Custom Instructions (or an equivalent account-level instruction surface):

> 当我在新对话中单独发送“继承”“继续”“恢复”，或发送“继承：<任务中文名> / 继续：<任务中文名>”时，不要仅按“学习继承、任务不继承”做泛化回复。先启动我的 Universal Continuity：读取 GitHub `D1traverser-debug/universal-continuity-agent@main` 的 `ENTRYPOINT.md`、`BARE_INHERIT_DISCOVERY.json`、`OWNER_REGISTRY.json`、`NEW_CHAT_BOOTSTRAP.json`。裸“继承/继续/恢复”必须完成 required-owner discovery quorum 后才能报告候选总数；明确任务名时直接路由到对应 owner。完成兼容检查和 takeover 后再继续任务。若启动钩子所需资源不可访问，明确报告 `CONTINUITY_BOOTSTRAP_UNAVAILABLE`，不要退化成“只继承学习、不继承任务”的默认回答。

## Conflict rule

The durable principle `学习继承，任务不继承` still applies to **NEW_TASK** classification.

It must **not** suppress an explicit continuation command. A user message whose primary intent is `继承/继续/恢复` is `CONTINUE`, not `NEW_TASK`.

Priority for these phrases:
1. explicit continuation command -> Universal Continuity bootstrap;
2. resolve exact or bare candidate(s);
3. compatibility/takeover;
4. only if classified NEW_TASK, apply learning-only inheritance.

## Acceptance test

Open a truly new chat and send exactly:

`继承`

PASS requires one of:
- complete candidate discovery and a consistent candidate list/count; or
- `INCOMPLETE_DISCOVERY` if a required owner source is unavailable.

FAIL includes:
- replying only that learning/rules are inherited while task state is not;
- asking the user to re-explain prior workflows before attempting bootstrap;
- claiming a total candidate count from a partial owner scan.
