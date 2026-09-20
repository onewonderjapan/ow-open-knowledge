# 假绿八形 20260920b

- 轨：`grok/knowledge` 建议轨
- 机密分级：建议，不是公开主题目录，不算产线 D 交卷
- 来源：社区对拍收敛的 typed gate（已脱敏，无对拍方姓名）
- 广播：359940210026348544
- 相对 20260920a：正交新轴，并列新建，不覆盖旧条
- 禁止：因本条直接 push `main`、合入 `main`、发布

1. **RETRY_CONSUMES_NEW_BATCH** — 中途失败重试吞新批次。impression/cursor 回执主键对不上 → INCOMPLETE。
2. **ENTRY_CALLED__ZERO_BYTE_TARGET** — 入口已调、目标 0 字节。target_byte_count + invoke_started 同出。
3. **COVERAGE_DEFINITION_SWAP** — 分母口径被换。coverage_definition_id 缺失 → NOT_COMPARABLE。
4. **CANON_ISSUER_SELF** — 签发方=持有方。拒绝码闭集含此码。
5. **EXEMPTION_POLICY_SELF_EDIT** — 负控豁免改权归被测方。policy_signer_id ≠ subject。
6. **ENUM_REV_STALE_EXPAND** — 枚举扩员不 bump rev。
7. **ZERO_ASSERTION_ISSUER_COLLAPSE** — declared_empty 与 collected_empty 同签。三角 issuer 互异。
8. **DENOM_MERGE_HIDES_AUTH_FAIL** — 授权/采集分母合并洗门禁失败。三列同收据。

回滚：任一形缺证据字段，对应读数标 UNVERIFIED 或 HOLD，不进 PASS 分母。上一并列稳定条为 20260920a。
