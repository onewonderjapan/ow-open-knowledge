# 假绿八形 20260921c

- 轨：`grok/knowledge` 建议轨
- 机密分级：建议，不是公开主题目录，不算产线 D 交卷
- 来源：社区对拍收敛的 typed gate（已脱敏，无对拍方姓名）
- ledger：collab-20260921a-signer-custody-coverage-type / item 360347971570630656
- 相对 20260921a/b：正交新轴，新建文件，不整篇覆盖旧条
- 禁止：因本条直接 push `main`、合入 `main`、发布

1. **ALERT_CRED_DOMAIN_SEPARATION** — 执行签名域 ≠ 告警主体域。同域禁止 CLEARED，只允 ESCALATED_UNANSWERED；CLEAR 绑定当前 signer_epoch。
2. **PIN_UNLOCK_CONDITION_MANDATORY** — 版本钉须含 (component, pinned_version, pinned_at, unlock_condition)。unlock_condition 须可机检。
3. **AGGREGATION_CHANGE_FORCES_PROBE_ID** — AND/OR/加权聚合变更属逻辑变更 → 新 probe_id。digest 须覆盖聚合节点。
4. **UPGRADE_TRIGGER_OWNED** — 升级待办须含 (trigger_condition, owner_role, revalidation_gate)。禁止无主「改天再升」。
5. **CRITERION_VER_MISMATCH_UNKNOWN** — criterion_version 须与裁决同算。不匹配 → UNKNOWN，不得复用旧 pass。
6. **DENOM_FREEZE_SOURCE_SIGN** — 冻结分母须 source_id + freeze_at + issuer_sign，否则守恒门可绕。
7. **CLOCK_ANCHOR_MONOTONIC** — clock_anchor 相对前次须单调序号。序号回滚 ⇒ 钟被调；禁止跨调整排序。
8. **MIXED_GENERATION_EXPECT_LENGTH** — 溢出/空产出须有上游 expect_length/非空契约。违约单独列账，不得并入成功。

回滚：任一形缺证据字段，对应读数标 UNVERIFIED，不进 PASS 分母。上一并列稳定条含 20260921a / 20260921b。
