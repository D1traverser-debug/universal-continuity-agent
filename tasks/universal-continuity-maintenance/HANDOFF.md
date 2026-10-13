# 跨对话继承系统建设与维护｜Handoff

- task_id: `continuity:universal-continuity-maintenance`
- task_class: `SYSTEM_INFRA`
- owner: `UNIVERSAL_CONTINUITY_HARNESS`
- status: `ACTIVE`
- contract: `CONTINUITY_V3_7`
- current_stage: `SYSTEM_MAINTENANCE_ACTIVE`
- current writer lease: `lease-8ecdf71e-46b3-4e7d-b2ea-61ee05c6d654`
- resume_epoch: `8`
- manifest_version: `69`
- current controller run: `user-proposal-independence-and-main-cas-v65-2026-10-13`
- current controller status: `ACTIVE` revision `18`, reopened to `M7_IMPLEMENTATION_AND_SUPERSESSION` by M10 second-order review
- latest green hosted validation: GitHub Actions `38329561028` — risk-tiered audit PASS, Agent architecture harness PASS, full pytest PASS

## 本轮确认并修复的核心问题

### 1. 不得把用户的想法、疑问或类比自动当成决定

现有冷路径维护政策本来已经规定：用户提出的 mechanism 不是默认 canonical，必须区分用户目标/约束与用户提出的办法，并挑战用户和助手的初始方案。但本轮仍出现了真实复发：用户只是问“你觉得怎么做”，系统就顺势创建 PR-first branch，把一个候选方案推成了实施方向。

因此这次没有再创建一套重复政策，而是把最小不变量提升到 `ENTRYPOINT.md` 热路径：

> Questions, suggestions, analogies, or tentative ideas are candidates, not authority. Do not infer approval; assess independently before acting unless explicitly instructed.

详细分类、证据、替代方案和 adoption 规则仍由 `SYSTEM_MAINTENANCE_POLICY.json` 负责。用户的明确目标/约束仍是高权威输入，但“顺着用户猜一个方案然后直接执行”不再合法。

### 2. Universal `main` 保持唯一工程权威，material write 使用 HEAD-CAS

此前把 `main protected=false` 单独标成 HIGH，是把多人/多独立 writer 仓库的威胁模型套到了当前 `SINGLE_ACTIVE_CHAT` 总控模型上。该结论已撤回。

当前模型不是 PR-first。Universal material control-plane mutation 的标准路径由 `PROGRESS_OBSERVABILITY_POLICY.json` 约束：

1. 写前 reread 当前 `main` HEAD；
2. 校验当前 active `lease_id / resume_epoch`；
3. reread 本次操作所需的精确 authority；
4. systemic/non-trivial maintenance 还必须由 controller 放行 `MATERIAL_PATCH`；
5. 基于刚观测到的 HEAD 构造一个 tree 和一个 commit；
6. 只用 `update_ref(force=false, expected_sha=observed_head)` 推进 `main`；
7. 如果 HEAD 已变化，立即 abort，重新读取 HEAD / lease / authority 并重新判断，禁止 replay 或 force 旧 commit；
8. 写后 reread `main`，观察 CI，再 reread authoritative task state 后才允许 `COMMITTED`。

这轮实际 checkpoint 与实现已经使用了这条 HEAD-level CAS 路径，而不是普通 contents 覆盖。

### 3. PR-first 实验没有成为架构

本轮曾创建实验分支 `continuity/pr-first-mutation-gate-v65`。这是错误威胁模型下产生的候选实验；它没有 merge，也不是 authoritative implementation。当前架构明确：`PR-first` 和 branch protection **不是 `SINGLE_ACTIVE_CHAT` 模型的默认要求**。

如果未来 writer 模型真的变成多人、多个独立 Agent、机器人或外部服务可并发写入，再重新评估 GitHub-side branch protection / ruleset / permission gate。那是新的威胁模型决定，不是当前 `main protected=false` 自动等于 HIGH。

当前 assurance ceiling 仍需诚实保留：active-lease + HEAD-CAS 能防 stale/concurrent compliant writer 覆盖，但无法物理阻止一个本来就有 GitHub 写权限、且故意无视协议的 authorized writer。当前没有证据要求为这种更强威胁模型增加 PR 生命周期。

## 本轮真实验证与 reopen

- 第一版热路径规则写得过长，CI `38329213434` 真实失败：risk-tiered audit PASS、Agent architecture PASS、pytest `298 passed / 1 failed`；唯一失败是 `ENTRYPOINT.md` 8447 bytes 超过 8192-byte hot-path budget。
- controller 因此 M8→M7 reopen，没有放宽预算，而是把热路径规则压缩成一句，详细语义继续留在冷路径 policy。
- 修正后的 CI `38329561028` 全绿：risk-tiered audit PASS、Agent architecture harness PASS、full pytest PASS。
- M10 二阶检查随后发现本 HANDOFF 仍保留旧的 “unprotected main = HIGH” 结论，因此再次 M10→M7 reopen。当前这次修改就是移除该 stale threat-model conclusion，并让 `SYSTEM_BLUEPRINT.md` 与已验证的 mutation contract 对齐。

## 与此前 v63 修复的关系

此前已完成的两项修复继续有效：

- ChatGPT automation/task existence、enabled state、scheduler liveness 属于 external product state；依赖现时状态的判断必须 live reread。用户主动删除核心监控不得被自动逆转。
- `manifest_version` 是 task mutation/CAS lineage；`latest_meta_maintenance_run_ref` 是最近真正完成的 formal proof。普通 task mutation 不要求二者 exact equality，也不得为了追版本号伪造 formal proof。

## 仍然 OPEN 的真实边界

- `HARNESS_STATUS.json` 内旧 monitor-enabled 字段仍是历史 lower-authority cache；不得覆盖 live product reread 或 task manifest，下次安全 rebuild 时收敛即可。
- 历史 issue #12 只保留原始 silent enabled→disabled provenance 未解；本次用户主动删除不是复发证据。
- `independent_meta_semantic_review` 仍 OPEN：CI/回归证明 scoped structural correctness，不证明独立语义判断与 live outcome。
- formal controller-meta promotion 仍 OPEN；只能使用 genuinely COMPLETE trace，不能倒填历史。
- Financial current-head architecture revalidation 与 fresh-chat DUAL 3-output retest 仍 OPEN；本 SYSTEM_INFRA 任务不取得 BUSINESS lease，不修改 BUSINESS truth。

## 后续原则

默认不要再把“用户提出一个办法”解释为“用户已经决定采用”。先独立判断目标、证据、替代方案和适用威胁模型，再行动。

Universal 当前继续直接维护 `main`；material control-plane write 使用 active lease + observed-HEAD CAS + CI + authoritative reread。只有当 writer topology / permission threat model 真实变化时，才重新评估 PR-first 或 GitHub-side protection。
