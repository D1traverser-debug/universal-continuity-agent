# 跨对话继承系统建设与维护｜Handoff

- task_id: `continuity:universal-continuity-maintenance`
- task_class: `SYSTEM_INFRA`
- display_name_zh: `跨对话继承系统建设与维护`
- domain: `CONTINUITY`
- owner: `UNIVERSAL_CONTINUITY_HARNESS`
- status: `ACTIVE`
- resume_visibility: `EXPLICIT_ONLY`
- contract: `CONTINUITY_V3_6`

## Current truth
- 工程真源：`D1traverser-debug/universal-continuity-agent@main`。
- v3.6 的当前能力与验证状态以 `HARNESS_STATUS.json` 为准。
- 恢复链规则以 `CONTEXT_RECOVERY_POLICY.json` 为准。
- 媒体学习与证据规则以 `MEDIA_DISTILLATION_PROTOCOL.md` 为准；这里不重复其历史细节。
- 2026-10-09 的真实恢复案例确认：本任务保持 `EXPLICIT_ONLY`，不会进入裸继承的默认 USER 候选；用户明确要求继续 Universal Continuity 后可直接路由本任务。
- 本轮审计发现旧 handoff 重复了已存在于权威 artifacts 的大量细节，因此按 v3.6 的短 handoff 与 artifact 引用优先原则进行收敛。

## Current stage
`V3_6_PROGRESSIVE_CONTEXT_RECOVERY_ACTIVE`

## Next action
继续横向审计其余 required owner 的 handoff/checkpoint，检查简洁性、权威来源、当前执行真相与 artifact 引用质量；只修复有明确证据的问题。

## Exact artifacts for next action
- `CONTEXT_RECOVERY_POLICY.json`
- `OWNER_REGISTRY.json`
- `BARE_INHERIT_DISCOVERY.json`
- `HARNESS_STATUS.json`
- 各 required owner 的当前 `TASK_INDEX` 与按需读取的 handoff/checkpoint

## Recovery rule
本任务是系统基础设施维护任务，不进入普通裸 `继承` 默认 USER 候选。仅在用户明确要求继续、维护或升级 Universal Continuity / 继承系统 / 跨对话继承系统时恢复。
