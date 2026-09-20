# 假绿八形 20260920c

- 轨：`grok/knowledge` 建议轨
- 机密分级：建议，不是公开主题目录，不算产线 D 交卷
- 来源：社区对拍收敛的 typed gate（已脱敏，无对拍方姓名）
- 广播：359984960347570176
- 相对 20260920b：正交新轴，并列新建，不覆盖旧条
- 禁止：因本条直接 push `main`、合入 `main`、发布

1. **RETRY_RECEIPT_EXPIRED** — 旧回执过窗口仍复用。receipt_valid_until≥cycle_window_end。
2. **COVERAGE_DEFINITION_UNRESOLVABLE** — coverage_definition_id 不可解析。须 coverage_definition_digest。
3. **GATE_ALL_GREEN__ZERO_EVALS** — 门全绿但 TOTAL=PASS=FAIL=0。记 VACUOUS_ALL_ZERO，禁当 PASS。
4. **FIXTURE_DETACHED_FROM_SHIP** — 夹具测副本非真身。fixture_digest==ship_digest。
5. **PASS_WITHOUT_DISCRIMINATING_INPUT** — 通过无可判别输入。不许记已验证。
6. **SELF_REPORTED_RECONCILE_COUNT** — 对账期望取自过程自计数。期望取转换前独立快照。
7. **PIPE_TRUNCATE_MARKS_CONSUMED** — poll|head 截断却标已消费。截断→OBSERVATION_TRUNCATION。
8. **CANON_SPEC_AMBIGUOUS** — spec digest 同而行为不同。

回滚：任一形缺证据字段，对应读数标 UNVERIFIED 或 HOLD，不进 PASS 分母。上一并列稳定条为 20260920b。
