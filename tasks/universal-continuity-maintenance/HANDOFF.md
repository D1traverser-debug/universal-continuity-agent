# 跨对话继承系统建设与维护｜Handoff

- task_id: `continuity:universal-continuity-maintenance`
- task_class: `SYSTEM_INFRA`
- owner: `UNIVERSAL_CONTINUITY_HARNESS`
- status: `ACTIVE`
- current_stage: `SYSTEM_MAINTENANCE_ACTIVE`
- current writer lease: `lease-8ecdf71e-46b3-4e7d-b2ea-61ee05c6d654`
- resume_epoch: `8`
- manifest_version: `91`
- completed controller run: `human-readable-durable-revision-v68-2026-10-13`
- controller status: `COMPLETE` revision `22`
- final audit: `audits/HUMAN_READABLE_DURABLE_REVISION_V68_FINAL_2026-10-13.json`
- final M8 validation: GitHub Actions `38364980981` / job `115187832418` — control-plane audit PASS, Agent architecture PASS, full pytest PASS

## v68 最终方案

用户以后不需要把 `manifest_version`、controller revision、protocol 和 Git SHA 当成同一种“版本号”理解。

Universal 先采用一个给人看的 **Human Durable Revision**：

`UC-YYYYMMDD-rN`

例如本 checkpoint 根据当前权威状态派生为 `UC-20261013-r91`。这个字符串**不存成第二份权威字段**；每次展示时从已经加载的权威 `updated_at + manifest_version` 现场派生。

### 五个 namespace 分工

- Git SHA：精确不可变工程定位。
- protocol `3.7`：协议兼容语义。
- `manifest_version`：任务/CAS 的单调 durable-state sequence。
- controller revision：单次维护流程内部轨迹。
- Human Durable Revision：用户可读显示层。

## 为什么不是照搬 SVN / daily counter

SVN 的 `rN` 依赖集中式 repository-wide commit stream。当前体系是多个 Git repo + 多个 owner/task durable streams。若做全局 `r1234` 或 `R20261013.001`，必须新建中央计数器、锁、每日 reset/timezone 规则、跨 repo 协调和故障恢复，这会增加总控耦合与竞争面。

所以：

- 不建中央 revision registry；
- 不建 daily counter，不每日归零；
- 不遍历 Git history 算号；
- 不为每个 checkpoint 打 Git tag；
- 不为显示字段扩张核心 TaskMetadata/业务状态 schema；
- 不在 ENTRYPOINT 加规则，也不增加 startup preload。

`YYYYMMDD` 只提供日期上下文；同一个 revision scope 内真正表示先后的仍是 `rN`。内部 checkpoint、lease/control-state durability 可能让号码出现跳号，这是允许的，不补号、不复用。

## 使用范围

这**不是维护系统专用概念**，而是 durable progress/resume receipt 的通用显示规则；但 v68 只在 Universal 自己先落地。

未来 Financial / A-share / Novel / Video 若采用，必须各自先证明：

1. 已经有适合该 revision stream 生命周期的 monotonic durable version；
2. 有不会让用户混淆的稳定 scope code；
3. 不跨 scope 比较数字大小；
4. 若没有合适 sequence，宁可暂时不显示，也不能为显示效果临时发明一套计数器。

本轮只读检查了四个 BUSINESS owner 的 architecture surface，并没有取得 BUSINESS lease、没有改它们的业务状态。Video 当前任务已可看到 `manifest_version: 20`，说明某些 owner 未来可以自然映射；其他 owner 仍需 owner-scoped mapping review，不能假设完全一样。

## Receipt 行为

- `COMMITTED`：显示新验证后的 Human Durable Revision；
- `NO_MATERIAL_CHANGE`：显示同一个版本并明确“未变”；
- `COMMIT_FAILED`：不造新号，只能引用上一个已验证版本；
- `STALE_WRITER`：不造新号；
- 继承：takeover 前先显示原有持久化 revision。
- 回滚/revert：是新的 durable state，因此得到新的 `rN`；旧号永不复用。

## 验证过程

v68 有 3 次真实 reopen：

- `38363727516 / 115183763873`：`317 passed / 2 failed`；
- `38363967497 / 115184549077`：全绿，但二阶审查发现 stored derived label 与 owner scope/adoption 边界问题，因此主动 reopen；
- `38364713013 / 115186953138`：`321 passed / 1 failed`，剩一个历史 handoff regression anchor；
- 最终 `38364980981 / 115187832418`：control-plane、Agent architecture、full pytest 全部 PASS。

最终审计还覆盖了同日多次、跨日、时区展示、时间戳异常、跳号、rollback、NO_MATERIAL_CHANGE、COMMIT_FAILED、STALE_WRITER、scope collision、owner 缺少 sequence、branch/scratch、Git tag、协议/Git namespace 混淆和性能问题。

## Anti-bloat 结论

当前实现只扩展既有 `PROGRESS_OBSERVABILITY_POLICY.json` 和 `VERSION_LIFECYCLE_POLICY.json`，新增一个纯确定性 `runtime/human_revision.py` 与 focused tests。计算是 O(1)，来自当前任务本来就要读取的 metadata；**不会为了显示一个版本号遍历 Git、遍历五个 Agent、查全局 registry 或额外调用远程服务。**

## v65 direct-main / PR-first regression anchor

当前模型不是 PR-first。

Universal material compliant writes continue to use active lease + observed-HEAD CAS + CI + authoritative reread. PR-first and branch protection are not default requirements under the current `SINGLE_ACTIVE_CHAT` threat model; unprotected `main` alone is not a HIGH defect.

实验分支 `continuity/pr-first-mutation-gate-v65` **没有 merge，也不是 authoritative implementation**；它仍是 unmerged / no-PR / non-authoritative experimental branch。

## 保留边界

v68 只解决版本可读性与 namespace 混淆。v67 已知的 Novel/Video owner-local drift、Financial fresh-chat DUAL 业务实测、private owner CI 未执行、independent semantic/live-outcome assurance、formal controller-meta promotion、历史 monitor provenance 和 tool-limited branch cleanup 仍按各自边界 OPEN，不被这个新版本号掩盖。
