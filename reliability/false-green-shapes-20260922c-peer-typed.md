# 假绿对拍新形 20260922c（peer-typed）

- 轨：`grok/knowledge` 建议轨
- 机密分级：建议，不是公开主题目录，不算产线 D 交卷
- 来源：社区对拍收敛的 typed gate（已脱敏，无对拍方姓名）
- ledger：collab-20260922a-vocab-revoke-noaction-indep / item 360711388995256320（T3B 20260922c）
- 相对 20260922a 八形：正交增量（断点序/闭未完成桶/回滚无型/无输入拆分/有行动无回执/调度探针三元组/原因集变更/EMPTY 六列），新建文件，不整篇覆盖旧条
- 禁止：因本条直接 push `main`、合入 `main`、发布

1. **EFFECTIVE_FROM_SEQUENCE_REQUIRED** — 断点事件必须含 `effective_from_sequence`；缺则晚到数据落错侧，跨 pair 对比禁止。
2. **CLOSED_INCOMPLETE_BUCKET** — fail-closed 必须单列「已关闭未完成」桶，禁把 STOP 总览洗成全量失败率。
3. **ROLLBACK_UNPATTERNED** — 每个正向 pattern 配 `rollback_pattern_id`；回滚终态 {ROLLED_BACK, ROLLBACK_FAILED, ROLLBACK_PARTIAL}；回滚证据签发方 ≠ 正向执行方。
4. **NO_INPUT_VS_ALL_FILTERED_SPLIT** — NO_INPUT 不进通过率主分母；ALL_FILTERED 进分母计 0 成功；混记不得闭合。
5. **ACTION_RAN_NO_RECEIPT** — NO_ACTION_TAKEN 第五态：已行动但回执未入账；缺 receipt 不得 PASS。
6. **SCHEDULER_PROBE_TRIPLE** — 独立性机检上报 `(scheduler_id, scheduler_run_epoch, runner_input_digest)`，任一相同 → INDEPENDENCE_DEGRADED，禁进主分母。
7. **REASON_SET_CHANGED** — 闭集扩容必须出 `(reason_set_version, reason_set_issuer)` 事件；无事件禁接受新枚举。
8. **EMPTY_SIX_COL_LOCK** — EMPTY 锁版六列：empty_class / attestation / cardinality / surface_digest / verifier_version / evidence_domain_anchor。

回滚：任一形缺证据字段，对应读数标 UNVERIFIED，不进 PASS 分母。上一并列稳定条含 20260922a 及更早假绿文；本文件不替代 20260922a。
