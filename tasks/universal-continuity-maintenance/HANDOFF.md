# 跨对话继承系统建设与维护｜Handoff

- task_id: `continuity:universal-continuity-maintenance`
- task_class: `SYSTEM_INFRA`
- owner: `UNIVERSAL_CONTINUITY_HARNESS`
- status: `ACTIVE`
- contract: `CONTINUITY_V3_7`
- current_stage: `SYSTEM_MAINTENANCE_ACTIVE`
- current writer lease: `lease-8ecdf71e-46b3-4e7d-b2ea-61ee05c6d654`
- resume_epoch: `8`
- manifest_version: `76`
- completed controller run: `chat-product-entry-and-internal-executor-boundary-v66-2026-10-13`
- controller status: `COMPLETE` revision `25`
- corrective validation after real reopen: Universal GitHub Actions `38342571980` / job `115116638109` — risk-tiered audit PASS, Agent architecture harness PASS, full pytest PASS
- user-facing `COMMITTED` still requires this closure checkpoint itself to be published with current-HEAD CAS, its post-publish CI observed, and final authoritative surfaces reread.

## v66：统一为“一个 ChatGPT Agent 入口，执行模式内部处理”

本轮修复的是跨 owner 产品边界：`OWNER_NATIVE`、`GITHUB_CHAT / CHAT_BRIDGED`、deterministic tool、isolated external 等属于内部执行、证据和 assurance 标签，不是用户需要选择的“路线”。正常产品形态保持为：

`用户 -> ChatGPT -> 匹配的 BUSINESS Agent / Skill -> 系统内部 capability handshake / executor selection -> 该 owner 唯一 canonical workflow/SOP -> owner 声明的持久化与证据边界`

对当前 architecture manifest `1.3` 的 BUSINESS owner，`product_interface` 固定为：

- `interaction_surface = CHATGPT`
- `entry_model = SINGLE_OWNER_ENTRY`
- `execution_mode_selection = SYSTEM_INTERNAL`
- `business_contract_model = SINGLE_CANONICAL_OWNER_WORKFLOW`

因此正常任务中不得要求用户选择 `OWNER_NATIVE`、`GITHUB_CHAT`、Python、MCP、plugin 或其他 execution plane。内部能力差异可以降低 assurance、让严格 hard gate 保持 OPEN/BLOCKED，但不能偷偷换 SOP、改 TaskContract、缩减 required outputs 或制造第二套业务工作流。

GitHub `main` 继续是工程/规则/Continuity 权威；具体业务运行状态/checkpoint 的权威位置仍由各 owner 自己声明。本轮没有把 BUSINESS truth 搬到 Universal，也没有新增必须部署的 MCP/server/service。

## 已同步的当前 BUSINESS owners

### Financial Writing Agent

当前 head：`6494cd58a93d82f7fc6849803b6b7493cf66443f`

- `continuity/AGENT_MANIFEST.json` 已是 architecture manifest `1.3` 并声明统一 product interface。
- `skills/financial-writing-agent/SKILL.md` 明确正常只有一个 ChatGPT Financial 入口，不再让用户选择 `OWNER_NATIVE / GITHUB_CHAT / Python / MCP / plugin`。
- OWNER_NATIVE 与 GITHUB_CHAT 继续作为内部 execution/evidence adapter，共享 canonical `TaskContract`、默认 DUAL、stage graph、revision/invalidation 和 Word 输出合同。
- GITHUB_CHAT 的 `CHAT_SELF_REVIEW` assurance 边界没有被抬高；owner-native / provider-attested 认证仍需真实证据。

### A-share Market Agent

当前 head：`651d97533cd62d34dc230f0b5047715074ab1803`

- manifest 已是 `1.3`。
- Skill 明确一个 ChatGPT 产品入口，runtime/cutover/CHAT_BRIDGED/MCP 等是系统内部 readiness/evidence 机制。
- 原 `cutover_status.json`、market-day Runtime authority 和 GitHub Continuity 边界保持不变；缺少 hard capability 只阻塞对应 gate，不改业务 SOP。

### Novel Writing Agent

当前 head：`46606fee061a5cf5421a5d0ef145a5955fd66760`

- manifest 已是 `1.3`，明确 `CHAT_BRIDGED` 是内部 execution/assurance label。
- 原 Skill 没有要求用户选择执行路线，因此没有为了形式统一再做高成本 hot-path 重写。
- 已知 Skill size drift 和 provider-attestation 边界保持原状态。

### Video Growth Agent

当前 head：`8f7d0cfb8121fc1a06e1e3a24c1167649d4def94`

- manifest 已是 `1.3`，明确普通 `CHAT_BRIDGED` 与严格 `ATTESTED_ISOLATED` review 是同一 Video Growth 产品内部不同 assurance class，不是用户选择的两套路线。
- 原严格 isolated-review 要求没有被弱化。
- 已知 Skill size drift 仍是原有 drift，不被本轮假装关闭。

本轮没有取得任何 BUSINESS task lease，没有改写文章、market-day 决策、小说 Canon/project state 或视频项目业务真值。

## 验证与真实 reopen

第一版共享 contract 实现错误地把 `AGENT_ARCHITECTURE_CONTRACT` schema 从 `1.1` 提到 `1.2`，并让旧 architecture manifest `1.2` 也强制要求新字段。Universal CI `38340563667` / job `115110366042` 暴露该兼容性回归。当时 controller 仍处于 M7，因此直接在 M7 修正：

- contract schema 保持 `1.1`；
- 新 product-interface 要求由 owner architecture manifest `1.3` 承载；
- legacy `1.2` 继续兼容。

修正后 Universal CI `38341336266` / `115112770288` 全绿；跨 owner propagation + observation cache checkpoint `d2f27c2bbaa1b560222326f4662e9ccd8d85f929` 的 CI `38341968555` / `115114761598` 再次全绿。

第一次 closure commit `f3002de18e284c583ca820eda6ad8d2208e5621a` 的 post-publish CI `38342327005` / `115115871171` 又发现真实回归：Handoff 重写保留了 v65 的含义，却删掉回归测试保护的精确 anchors。COMPLETE 因此被撤销，controller revision `20` 正式 reopen 到 M7。

修复 commit `fe33b1f50759a7e20be24c9bf59138df030d338a` 恢复了 anchors；其 corrective CI `38342571980` / `115116638109` 全绿。随后重新完成 M7→M11，controller 以 revision `25` 关闭。这次轨迹保留真实 reopen，不把失败 closure 当成已完成。

四个 private owner 的 push workflow 都创建了 run，但均没有分配 runner：

- Financial `38341448831 / 115113123995`
- A-share `38341477686 / 115113214854`
- Novel `38341498059 / 115113278000`
- Video `38341521415 / 115113349788`

这些 job 都是 `steps=[]`, `runner_id=0`。因此只能记录 `RUNNER_NOT_EXECUTED`，不能称 owner CI PASS，也不能把它误判成代码测试失败证据。

## v65 direct-main / PR-first 回归锚点

当前模型不是 PR-first。

Universal material compliant writes 继续使用 active lease + observed-HEAD CAS + CI + authoritative reread；`main protected=false` 本身不是当前 `SINGLE_ACTIVE_CHAT` 威胁模型下的 HIGH defect。

实验分支 `continuity/pr-first-mutation-gate-v65` 没有 merge，也不是 authoritative implementation；它仍无 PR，除非未来 writer topology / permission threat model 出现新的真实证据，否则不得自动 promotion。

## 二阶复核结论

- 没有新建第二套业务工作流。
- 没有让 MCP/plugin 成为强制依赖；它们仍只是可选内部工具连接方式。
- 没有删除 executor label；保留其 assurance/evidence/fail-closed 价值，删除的是“让用户选路线”的产品语义。
- 没有降低 Financial `CHAT_SELF_REVIEW`、Video strict isolation 等已有 assurance 边界。
- 没有改变 owner-specific business state authority。
- architecture manifest `1.2` 后向兼容继续成立。
- 四个 owner 的 main head 已在 corrective validation 后重新读取并保持上述值。
- private owner CI runner 未执行的限制继续明确保留。

当前 assurance ceiling：

`STRUCTURAL_PRODUCT_INTERFACE_CONFORMANCE_PLUS_UNIVERSAL_REGRESSION_AND_CORRECTIVE_CI_PASS__PRIVATE_OWNER_CI_EXECUTION_NOT_OBSERVED__NO_LIVE_BUSINESS_QUALITY_OR_OUTCOME_PROOF`

## 继续保持 OPEN 的边界

- Financial fresh-chat DUAL 3-output retest 与 current-head business execution/architecture revalidation 仍由 Financial owner 完成；本轮没有冒充业务实测已经通过。
- `independent_meta_semantic_review` / live outcome assurance 仍 OPEN。
- formal controller-meta promotion 仍 OPEN；不得为了匹配最新 manifest_version 伪造 chronology。
- `HARNESS_STATUS.json` 里的历史 monitor cache 下次安全 rebuild 时再收敛；它不是 live product-state authority。
- 历史 issue #12 只保留最早 silent enabled→disabled provenance 未解；用户后来的主动删除不是 recurrence。
- 对故意绕过协议的 authorized GitHub writer，当前 single-writer + HEAD-CAS 仍只声明既有 assurance ceiling，不自动升级到 PR-first/branch-protection 威胁模型。

## 继承时的默认理解

用户正常只是在 ChatGPT 使用对应 Agent。不要再把内部 runtime/executor/assurance 名称解释成用户需要选择的“入口”或“路线”。只有用户主动询问执行保证、诊断真实 blocker，或确实需要外部授权/产品决策时，才暴露这些内部差异。

跨 owner 的产品边界以后优先由共享 `AGENT_ARCHITECTURE_CONTRACT.json` / `EXECUTION_READINESS_CONTRACT.json` 约束，再做最小 owner-local 传播，避免每个 Agent 自己长出一套解释。

此前 v65 的用户方案独立判断规则、direct-main HEAD-CAS、PR-first 非默认架构仍全部有效；不得回退。
