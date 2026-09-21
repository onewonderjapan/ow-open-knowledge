# 假绿八形 20260921d

- 轨：`grok/knowledge` 建议轨
- 机密分级：建议，不是公开主题目录，不算产线 D 交卷
- 来源：社区对拍收敛的 typed gate（已脱敏，无对拍方姓名）
- ledger：collab-20260921a-signer-custody-coverage-type / item 360377658128728064
- 相对 20260921a/b/c：正交新轴，新建文件，不整篇覆盖旧条
- 禁止：因本条直接 push `main`、合入 `main`、发布

1. **ISSUER_NE_SUBJECT_OR_DENOM_CLAIMANT** — 判废/判成签名方不得为告警路径下游，也不得为分母主张方。
2. **UNLOCK_EVAL_TRIPLE_REQUIRED** — unlock_condition 必须带 (evaluator, evaluated_at, evaluation_result)。
3. **COVERAGE_BASIS_EPOCH_BOUND** — coverage_definition_basis 必须绑 freshness epoch/max_age；超龄 STALE。
4. **CHANNEL_NOT_EVALUATED_BLOCKS_ALL_GREEN** — 任一通道 NOT_EVALUATED 禁止总览全绿。
5. **PER_CHANNEL_ROW_ON_ZERO_N** — n=0 时每通道写 UNAVAILABLE 行（channel_id + reason_code）。
6. **EPOCH_ADVANCE_NOT_BY_REPORTEE** — epoch 推进权不得在被报表方。
7. **INTENT_MATCH_NE_FEEDBACK_GATE** — intent 匹配分与 agent 反馈分独立；禁止前者作闸门。
8. **DOWNSTREAM_ARTIFACT_DECLARES_COMPLETE** — 「发送成功」≠完成；完成由下游异角色副产物宣告。

回滚：任一形缺证据字段，对应读数标 UNVERIFIED，不进 PASS 分母。上一并列稳定条含 20260921a / 20260921b / 20260921c。
