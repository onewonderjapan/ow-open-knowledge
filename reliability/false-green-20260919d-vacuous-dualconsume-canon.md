# 假绿八形 20260919d · vacuous / dual-consume / canon

- 轨：`grok/knowledge` 建议轨
- 机密分级：建议，不是公开主题目录，不算产线 D 交卷
- 来源：社区对拍收敛的 typed gate（已脱敏，无对拍方姓名）
- LEDGER：359653920567459840 / collab-20260919d-vacuous-dualconsume-lease-canon
- 相对 20260919c：新轴，并列新建，不覆盖旧条
- 禁止：因本条直接 push `main`、合入 `main`、发布

1. **VACUOUS_PASS_PCT_FORBIDDEN** — 比率分母=0 禁渲染 100% 绿。出 VACUOUS_PASS/UNDECIDABLE 并随值出分母。
2. **ZERO_ASSERTION_TYPE_CLOSED** — 分母=0 须闭集原因。issuer ≠ 读面板方。
3. **DUAL_CONSUMER_SILENT_DROP** — 同 epoch 同资源只允许一个消费者。空 feed ≠ 成功。
4. **LEDGER_ROW_MISSING_NE_PASS** — ledger 缺行 = NOT_EVALUATED，永不默认 PASS。
5. **TIMEOUT_CANCEL_FIELD_SPLIT** — timeout 与 cancel 分字段，不得折成合法 EMPTY。
6. **HOLD_NO_TIMEOUT_AUTOFLIP** — HOLD 禁超时自动转 PASS/FAIL。
7. **CANON_SPEC_SEPARATE_SIGN** — canonicalizer_spec_digest 与 payload_digest 分签。
8. **EXEMPTION_AGE_BOUND_HARD** — 例外 open epochs 超 upper_bound 必须红。

回滚：任一形缺证据字段，对应读数标 UNVERIFIED 或 HOLD，不进 PASS 分母。上一并列稳定条为 20260919c。
