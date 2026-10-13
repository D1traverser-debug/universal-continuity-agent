# 跨对话继承系统建设与维护｜Handoff

- task_id: `continuity:universal-continuity-maintenance`
- owner: `UNIVERSAL_CONTINUITY_HARNESS`
- status: `ACTIVE`
- manifest_version: `103`
- resume_epoch: `9`
- active lease: `lease-350c8bbe-08cf-47e7-8116-0537f9c9ad67`
- current controller: `main-mutation-mechanical-enforcement-v70-2026-10-13`
- controller status: `BLOCKED revision 12 / M7_IMPLEMENTATION_AND_SUPERSESSION`

## 当前结论

用户要求暂不执行生产重构，先把总控系统按功能逐项反查。功能覆盖审计已经完成：共归纳 18 个当前总控功能域；此前 G01–G30 已触及所有主要功能域，没有发现一个完整的大功能从未被审视过。

但 `research/system_architecture_library/23_refactor_execution_plan.md` 不能原样作为实施清单。开始重构前必须显式补齐这些落点：G27 context compaction、G29 runtime/protocol/provider compatibility、G30/G22 evaluation-promotion lifecycle、G24 writer-model transition trigger，以及 G03 inter-owner interaction、G04 environment/substrate、G23 multiple-fault、G20/G21 coupling/toil、G14 fitness-function map。

详细证据：`audits/ARCHITECTURE_FUNCTION_COVERAGE_CROSSCHECK_V70_2026-10-13.md`。

## 本轮新可靠性事故

保存上述审计时，material `main` 再次误走 direct file mutation，产生 commit `b0dd89ffdc43876951cfb430d57ea6b0eb1e4792` 并错误改动 README。当前 writer 随即停止该路径，重新读取 HEAD，并使用 Git Data + `expected_sha` CAS 恢复 README、保留功能审计；恢复 commit 为 `240029ddf6168d6a55a9af05357330a3a49cf167`，随后权威回读确认 README 已恢复。

这证明 v69 的 ENTRYPOINT 文字 guard 不是机械 enforcement。该失败类再次定为 `RECURRED_AFTER_FIX`，必须提升到 tool/repository permission 层；不得再通过增加提示语或 exact-text regression 宣称关闭。当前暴露的 GitHub connector 没有 repository rules/branch-protection 的管理写操作，所以 prevention 真实状态为 OPEN/BLOCKED。

事故状态：`audits/MAIN_MUTATION_RECURRENCE_V70_2026-10-13.json`。

## v65 direct-main / PR-first 回归锚点

当前模型不是 PR-first。

active lease + observed-HEAD CAS + CI + authoritative reread

实验分支 `continuity/pr-first-mutation-gate-v65` 没有 merge，也不是 authoritative implementation。

这些锚点描述当前 authority 与历史实验边界；它们不表示 convention-only PR-first、提示语或回归文案可以替代本轮已证明缺失的机械 enforcement。

## next_action

现在不执行生产架构重构。后续用户明确要求继续重构时：

1. 先回读当前 authority；
2. 先解决或重新决策 material-main 的机械 enforcement 边界；
3. 把功能覆盖审计中的九项显式补入 refactor design；
4. 对版本敏感 Agent runtime 事实重新观察；
5. 再从修订后的最小设计进入 M7，而不是照搬旧 plan 23。
