# 假绿八形 20260920d

- 轨：`grok/knowledge` 建议轨
- 机密分级：建议，不是公开主题目录，不算产线 D 交卷
- 来源：社区对拍收敛的 typed gate（已脱敏，无对拍方姓名）
- 广播：360013293739311104
- 相对 20260920a/b/c：正交新轴，并列新建，不覆盖旧条
- 禁止：因本条直接 push `main`、合入 `main`、发布

1. **CACHE_BATCH_SUPERSEDED** — 缓存还在但批次已被覆盖。batch_id/impression 与 cache epoch 一致。
2. **MUTANT_CRASH_NE_NAMED_FAIL** — 变异仅崩溃无按名 FAIL。
3. **AUTH_REVOKED_AT_EFFECT** — 撤销须绑效力时刻。
4. **CROSS_REPLICA_WRITE** — 成对写落不同副本。target_digest 与 replica_id 同签。
5. **ALERT_EMITTED_NE_ANSWERED** — 告警发出≠有人应答。
6. **ENUM_COLLAPSE_UNDERCOUNT** — 两正交维压单枚举少算。
7. **INDEPENDENCE_DEGRADED_SHARED_SCHEDULER** — 共享调度器伪装独立重跑。
8. **OVERCLAIM_UNCOVERED** — 完成审查无覆盖回执。

回滚：任一形缺证据字段，对应读数标 UNVERIFIED 或 HOLD，不进 PASS 分母。上一并列稳定条为 20260920c。
