# 假绿八形 20260919c

- 轨：`grok/knowledge` 建议轨
- 机密分级：建议，不是公开主题目录，不算产线 D 交卷
- 来源：社区对拍收敛的 typed gate（已脱敏，无对拍方姓名）
- 相对 20260919a/b：新码，并列新建，不覆盖旧条
- 禁止：因本条直接 push `main`、合入 `main`、发布

1. **TRUNCATION_AXIS_UNSPLIT** — 网关硬截断与模型 length 共用一码。拆 TRANSPORT vs MODEL。
2. **POS_CTRL_EPOCH_ALIGNED** — 正控按墙钟而非 handoff epoch。未随 epoch 出现即 SILENT_POS_CTRL_MISSING。
3. **BLOCKER_MIGRATE_QUAD** — 跨 rev 按名合并 blocker。要 (from_rev,to_rev,old_ord,new_ord)。
4. **SCHEMA_VIOLATION_NE_QUALITY** — schema 拒收进质量分母。只进 INPUT 合同层。
5. **BASELINE_SAME_ASSET_SIGMA** — 完播对照用平台同期基线。用同素材历史 σ。
6. **REGISTRY_EFFECTIVE_AT** — 来源登记无生效时刻。判定按数据产生时刻。
7. **RECON_ZERO_TRAP** — 对账零差当健康。必声明 zero_flip_red_rule。
8. **CANONICAL_QUAD_SER_ORDER** — 四元 digest 无规范化。固定键序/无空白/禁浮点。

回滚：任一形缺证据字段，对应读数标 UNVERIFIED 或 HOLD，不进 PASS 分母。上一并列稳定条为 20260919b。
