# 跨对话继承系统建设与维护｜Handoff

- task_id: `continuity:universal-continuity-maintenance`
- task_class: `SYSTEM_INFRA`
- owner: `UNIVERSAL_CONTINUITY_HARNESS`
- status: `ACTIVE`
- current_stage: `SYSTEM_MAINTENANCE_ACTIVE`
- current writer lease: `lease-8ecdf71e-46b3-4e7d-b2ea-61ee05c6d654`
- resume_epoch: `8`
- manifest_version: `87`
- current controller run: `human-readable-durable-revision-v68-2026-10-13`
- controller status: `ACTIVE` revision `12` at `M8_MULTI_LAYER_VALIDATION`
- prepatch audit: `audits/HUMAN_READABLE_DURABLE_REVISION_V68_PREPATCH_2026-10-13.json`

## v68 目标

用户指出当前对外同时出现 `manifest_version`、controller revision、protocol version、Git SHA，难以理解“这次到底是什么版本”，并建议参考 SVN/日期序列。目标不是把 Git 改成 SVN，而是建立一个**用户看得懂、又不增加第二套权威状态**的修订号。

## 学习与设计结论

- SVN 的 `rN` 好用，是因为每次集中式仓库提交都有一个全局递增自然数；这个特性不应生搬硬套到多个 Git 仓库。
- Git SHA 继续是精确不可变工程身份；Git tag 只适合重要发布点，不应每次 checkpoint 都打 tag。
- CalVer 日期能让人快速知道“什么时候”，但单独日期不能区分同一天多次提交。
- 因此 Universal 先试运行：`UC-YYYYMMDD-rN`。
- `YYYYMMDD` 来自已经权威持久化的 `updated_at/persisted_at` 日期；`rN` 直接复用已经存在的 `manifest_version`（未来 owner 可映射到自己的 monotonic durable version）。
- **不新增 daily counter、不做每日归零、不扫 Git history、不新增 revision registry、不把标签写回 manifest 形成第二份真值。**

当前 prepatch 状态 `manifest_version=86` 对应的示例是 `UC-20261013-r86`。本次实现 checkpoint 持久化后，用户可见修订号应由新 manifest 动态派生，而不是硬编码保存。

## 放在哪一层

这不是“维护系统专用版本号”，而是**durable progress receipt 的显示层**：

- `Git SHA`：机器/工程精确定位；
- `protocol 3.7`：兼容语义；
- `manifest_version`：任务状态/CAS 的单调序列；
- `controller revision`：一次维护 run 内部轨迹；
- `Human Durable Revision`：给用户看的派生标签。

所以主要落在现有 `PROGRESS_OBSERVABILITY_POLICY.json` 与 `VERSION_LIFECYCLE_POLICY.json`，没有新建 root policy。

## 已实现，待 M8

- `PROGRESS_OBSERVABILITY_POLICY.json` → schema 1.1，定义 human revision 的 receipt 行为；
- `VERSION_LIFECYCLE_POLICY.json` → schema 1.1，明确 Git / protocol / durable state / controller / human revision 五个 namespace；
- `runtime/human_revision.py` → 纯确定性 O(1) 格式化/派生；
- `tests/test_human_revision.py` → 覆盖同日多次、跨日不归零、时区不偷偷换日、非法 scope/version fail closed、namespace separation；
- 没有改 `ENTRYPOINT.md`，避免为了显示层再次消耗 hot-path budget；
- 没有改 BUSINESS owner 状态。

## 下一步

M8 跑 Universal control-plane audit、Agent architecture harness、full pytest。失败就 reopen。通过后只做 propagation review：确认未来其他 Agent 可以复用规则，但**本轮不自动给四个 BUSINESS repo 写入新格式**。先让 Universal 自己跑稳，再决定是否推广。

## 顺手纠正的旧状态

v67 closure 后的 GitHub Actions `38360976886 / 115174841711` 已经 PASS；此前 manifest 仍写着 `POST_CLOSURE_CI_REQUIRED`。本轮在不改变 v67事实的前提下，已把该 lower-level status 纠正为 `POST_CLOSURE_CI_PASS`。

## 边界

- 不把 Human Revision 当 Git SHA、protocol 或业务版本。
- 不允许跨 5 个 repo 共用一个中央计数器；那会引入锁、竞争和单点。
- `NO_MATERIAL_CHANGE` 不加号；`COMMIT_FAILED/STALE_WRITER` 不造新号。
- 回滚也生成新的持久状态版本；旧号永不复用。
- 非权威 branch / scratch 不发行用户修订号。
