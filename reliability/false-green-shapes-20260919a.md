# 假绿八形 20260919a

- 轨：`grok/knowledge` 建议轨
- 机密分级：建议，不是公开主题目录，不算产线 D 交卷
- 来源：社区对拍收敛的 typed gate（已脱敏，无对拍方姓名）
- 相对 20260918d：新码，并列新建，不覆盖旧条
- 禁止：因本条直接 push `main`、合入 `main`、发布

1. **MEMBERSHIP_UNATTESTED** — 被计数集合由被计量方自圈。需域外 membership_digest。
2. **DEDUP_SURFACE_OPAQUE** — 去重只报「0重复」。必报 cardinality_before/after、submit_count、dedupe_key_set_digest。
3. **FAULT_DOMAIN_DATA_SOURCE_REQUIRED** — fault_domain 缺数据来源方维。补第四维 data_source_party。
4. **BLOCKER_ID_POLICY_ORDINAL_PAIR** — blocker 易漂移。用 (policy_rev, rule_ordinal)。
5. **FREQUENCY_EXPECTED_TICK_DIGEST** — 无 expected_tick_set。契约 tick 与 RAW_GAP；插值仅可视化。
6. **BATCH_EXECUTION_UNPROVEN** — 单条都绿无整批证明。batch_execution_receipt 加负控位图。
7. **CUSTOM_DOMAIN_NO_DENOMINATOR** — 自定义证据域无独立分母仍聚合。三件齐才准入。
8. **INPUT_REJECT_IN_QUALITY_DENOMINATOR** — 质量分母含输入合同失败。INPUT_REJECT 独立桶。

回滚：任一形缺证据字段，对应读数标 UNVERIFIED 或 HOLD，不进 PASS 分母。上一并列稳定条为 20260918d。
