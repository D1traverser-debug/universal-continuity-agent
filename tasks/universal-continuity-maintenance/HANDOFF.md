# 跨对话继承系统建设与维护｜Handoff

- task_id: `continuity:universal-continuity-maintenance`
- task_class: `SYSTEM_INFRA`
- owner: `UNIVERSAL_CONTINUITY_HARNESS`
- status: `ACTIVE`
- contract: `CONTINUITY_V3_7`
- current_stage: `SYSTEM_MAINTENANCE_ACTIVE`
- current writer lease: `lease-8ecdf71e-46b3-4e7d-b2ea-61ee05c6d654`
- resume_epoch: `8`
- manifest_version: `71`
- completed controller run: `user-proposal-independence-and-main-cas-v65-2026-10-13`
- controller status: `COMPLETE` revision `23`
- implementation/alignment validation: GitHub Actions `38330150551` / job `115077831629` — risk-tiered audit PASS, Agent architecture harness PASS, full pytest PASS
- final user-facing `COMMITTED` still requires live reread of the published closure checkpoint and its post-publish CI; this handoff does not treat a stored run id as perpetual current truth.

## 本轮完成的进化

### 1. 用户提出的办法不再被自动当成决定

本轮暴露了一个真实复发：冷路径政策早已规定用户提出的 mechanism 不是默认 canonical，但实际对话中仍出现“用户只是问/提想法 → 系统顺势采纳 → 直接开始实施”的行为。

因此没有再新建重复 policy，而是在 `ENTRYPOINT.md` 增加最小热路径不变量：

> Questions, suggestions, analogies, or tentative ideas are candidates, not authority. Do not infer approval; assess independently before acting unless explicitly instructed.

含义是：
- 用户明确目标、约束、纠错仍是高权威输入；
- 用户提出的具体做法、类比、猜测、疑问先作为 candidate；
- 不得为了显得配合就揣测“用户已经同意这个方案”；
- 先独立检查事实、目标、替代方案、失败模式和适用边界；
- 只有证据/authority gate 支持，或用户明确决定/指令，才执行。

详细分类和 adoption 规则继续由 `SYSTEM_MAINTENANCE_POLICY.json` 持有，避免把 ENTRYPOINT 堆成大 prompt。

### 2. Universal 继续直接维护 `main`，但 material write 改成 HEAD-level CAS

此前把 `main protected=false` 单独标成 HIGH，是错误地套用了多人/多独立 writer 的威胁模型。当前 repo 的 writer model 是 `SINGLE_ACTIVE_CHAT`，因此该 HIGH 结论已从架构和 handoff 撤销。

当前标准 material mutation 路径：

1. reread 当前 `main` HEAD；
2. verify 当前 active `lease_id / resume_epoch`；
3. reread 本次操作需要的精确 authority；
4. systemic/non-trivial maintenance 由 controller 放行 `MATERIAL_PATCH`；
5. 基于刚观测的 HEAD 构造一个 tree + commit；
6. 只允许 `update_ref(force=false, expected_sha=observed_head)` 推进 `main`；
7. HEAD mismatch 时 abort，重新读取 HEAD / lease / authority，禁止 replay/force stale commit；
8. 写后 reread `main`、观察 CI、再 reread authoritative task state，才允许 `COMMITTED`。

该规则由 `PROGRESS_OBSERVABILITY_POLICY.json` 持有，并由 `tests/test_user_proposal_and_main_mutation_integrity.py` 回归保护。

### 3. PR-first 不是当前默认架构

当前模型不是 PR-first。实验分支 `continuity/pr-first-mutation-gate-v65` 没有 merge，也不是 authoritative implementation；它没有 PR，不得因为已经存在就自动 promotion。

`SYSTEM_BLUEPRINT.md` 现在明确：在 `SINGLE_ACTIVE_CHAT` 模型下，Universal `main` 是唯一工程权威；material compliant writes 使用 active lease + observed-HEAD CAS + CI + reread。PR-first / branch protection 只有在 writer topology、权限或威胁模型真实变化时再评估。

保证边界也明确：HEAD-CAS 能防 stale/concurrent compliant writer 覆盖；它不能物理阻止一个本来就有 GitHub 写权限、且故意无视协议的 authorized writer。当前没有证据要求为这种更强威胁模型增加 PR 生命周期。

## 真实 controller / CI 轨迹

本 run 完整经过 M0→M11，并有两次真实 reopen：

1. 第一版 ENTRYPOINT 规则过长，CI `38329213434` / job `115074858091`：risk-tiered audit PASS、Agent architecture PASS、pytest `298 passed / 1 failed`。唯一失败是 ENTRYPOINT 8447 bytes > 8192-byte budget。controller M8→M7 reopen，压缩热路径规则而没有放宽预算。
2. 修正后 CI `38329561028` 全绿。
3. M10 二阶检查发现旧 HANDOFF 仍写着 “unprotected main = HIGH / mutation gateway or branch protection”，会让下一次继承重新拿到错误威胁模型，因此 M10→M7 reopen。
4. 对齐后的 authoritative implementation/checkpoint CI `38330150551` / `115077831629` 全绿：risk-tiered audit PASS、Agent architecture harness PASS、full pytest PASS。
5. M9 确认该变化是 Universal control-plane invariant，不需要取得任何 BUSINESS lease、修改任何 BUSINESS truth 或复制 owner-local rule。
6. M10 复核确认：旧 HIGH 文案已删除；PR-first 实验没有 PR 且非 authority；direct-main CAS 与 architecture/handoff 对齐；HARNESS monitor booleans 仍被限定为 lower-authority historical cache；独立语义/live outcome 保证仍未被夸大。

## 仍然 OPEN 的真实边界

- `HARNESS_STATUS.json` 内旧 monitor-enabled 字段仍是 rebuildable lower-authority historical cache；不得覆盖 live product reread 或 task manifest，下次安全 rebuild 时收敛。
- 历史 issue #12 只保留原始 silent enabled→disabled provenance 未解；本次用户主动删除不是复发证据。
- `independent_meta_semantic_review` 仍 OPEN：CI/回归证明 scoped structural correctness，不证明独立语义判断或 live outcome。
- formal controller-meta promotion 仍 OPEN；当前已有 genuinely COMPLETE trace 可供评估，但不得为了追版本号伪造 chronology。
- Financial current-head architecture revalidation 与 fresh-chat DUAL 3-output retest 仍 OPEN；由 Financial owner authority 完成。

## 后续默认原则

- 不要把用户的 suggestion/question/analogy/tentative idea 自动解释成 approval 或 architecture decision。
- 先独立判断，再执行；明确用户指令除外。
- Universal 当前继续直接维护 `main`，material write 使用 active lease + observed-HEAD CAS + CI + authoritative reread。
- `main protected=false` 本身不再被定为当前 HIGH defect；如果 writer topology/permission threat model 变化，再重新评估 GitHub-side protection。
- 不取得 BUSINESS lease，不改写 BUSINESS truth。
