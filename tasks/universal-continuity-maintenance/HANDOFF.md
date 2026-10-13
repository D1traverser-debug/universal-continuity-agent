# 跨对话继承系统建设与维护｜Handoff

- task_id: `continuity:universal-continuity-maintenance`
- task_class: `SYSTEM_INFRA`
- owner: `UNIVERSAL_CONTINUITY_HARNESS`
- status: `ACTIVE`
- current_stage: `SYSTEM_MAINTENANCE_ACTIVE`
- current writer lease: `lease-8ecdf71e-46b3-4e7d-b2ea-61ee05c6d654`
- resume_epoch: `8`
- manifest_version: `88`
- current controller run: `human-readable-durable-revision-v68-2026-10-13`
- controller status: `ACTIVE` revision `14` at `M8_MULTI_LAYER_VALIDATION`
- prepatch audit: `audits/HUMAN_READABLE_DURABLE_REVISION_V68_PREPATCH_2026-10-13.json`

## v68 设计结论

用户要解决的是“我看不懂你每次提交到底是哪一版”，不是把 Git 换成 SVN。已学习 SVN、Git tag / `git describe` 与 CalVer 后，Universal 采用派生的人类修订号：

`UC-YYYYMMDD-rN`

其中日期来自权威持久化时间的日历日期，`rN` 直接复用已有 monotonic `manifest_version`。因此没有 daily counter、没有每日归零、没有新的 revision registry、没有 Git history scan，也不会用 tag 给每个 checkpoint 再造一层身份。

技术 namespace 继续分开：

- Git SHA = 精确不可变工程身份；
- protocol 3.7 = 兼容语义；
- manifest_version = durable task/CAS 单调状态序列；
- controller revision = 单次维护 run 内部轨迹；
- Human Durable Revision = 用户显示层，派生而非权威。

## 第一次 M8 真实失败并 reopen

CI `38363727516 / 115183763873`：control-plane audit PASS、Agent architecture PASS，但 full pytest `317 passed / 2 failed`。

失败项不是版本格式本身：

1. controller M7 implementation receipt 缺少 maintenance policy 要求的 `prepatch_checkpoint` 绑定；
2. 重写 HANDOFF 时丢掉了既有 single-writer 回归锚点 `当前模型不是 PR-first`。

因此 controller 已真实 reopen 到 M7，再修回 M8。Human Durable Revision 设计未改，只修过程/回归表面。

## receipt 行为

- `COMMITTED`：显示新持久化修订号；
- `NO_MATERIAL_CHANGE`：号不变，并明确“版本未变”；
- `COMMIT_FAILED`：不造新号，最多显示上一个已验证修订；
- `STALE_WRITER`：不造新号；
- 继承时先显示 takeover 前的已持久化修订号。

## 这是不是维护系统专用？

不是。它属于 durable progress receipt 的通用显示层。但本轮**只在 Universal 自己先试运行**。未来 Financial / A股 / Novel / Video 若采用，只能映射到各自已经存在的 monotonic durable owner version 和稳定 scope code；不会建一个 5 仓库共用的中央流水号。

## 复杂度控制

没有新增 root policy / registry / Agent / service；没有扩大 ENTRYPOINT；没有新增 hot-path 远程调用。只扩展现有 `PROGRESS_OBSERVABILITY_POLICY.json`、`VERSION_LIFECYCLE_POLICY.json`，加一个纯确定性 `runtime/human_revision.py` 和 focused tests。

## v65 direct-main / PR-first 回归锚点

当前模型不是 PR-first。

Universal material compliant writes 继续使用 active lease + observed-HEAD CAS + CI + authoritative reread。PR-first 和 branch protection 不是当前 `SINGLE_ACTIVE_CHAT` 威胁模型下的默认要求；unprotected `main` 本身不是 HIGH defect。

实验分支 `continuity/pr-first-mutation-gate-v65` 没有 merge，也不是 authoritative implementation。

## 下一步

重新跑 M8 全量 CI；任何失败继续 reopen。通过后做 M9 propagation review（不写四个 BUSINESS repo）、M10 二阶检查、M11 closure 与 post-closure CI/reread。
