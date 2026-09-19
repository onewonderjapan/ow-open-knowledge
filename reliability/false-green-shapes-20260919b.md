# 假绿八形 20260919b

- 轨：`grok/knowledge` 建议轨
- 机密分级：建议，不是公开主题目录，不算产线 D 交卷
- 来源：社区对拍收敛的 typed gate（已脱敏，无对拍方姓名）
- 相对 20260919a：新码，并列新建，不覆盖旧条
- 禁止：因本条直接 push `main`、合入 `main`、发布

1. **FALSE_GREEN_FP_COST_UNTRACKED** — 只报抓到不报误杀。必报 (TP, FP, precision_proxy)。
2. **DEDUP_CARDINALITY_QUAD_REQUIRED** — 去重缺四元基数。缺任一即 DEDUP_SURFACE_OPAQUE。
3. **SCAN_SCOPE_REQUIRED** — 无扫描面声明。batch receipt 强制 scan_scope。
4. **DATA_SOURCE_REGISTRY_PRIMARY** — 数据来源仅推导。登记为主、推导旁证。
5. **FALLBACK_INVISIBLE** — 降级不可观测。typed reason_code + degradation_flag。
6. **THRESHOLD_REV_FORWARD_ONLY** — 阈值无 diff/回溯重判。threshold_rev 前向生效。
7. **DENOM_ISSUER_NE_EXECUTOR** — 分母自签或缺 clock_anchor。issuer≠executor + issuer_epoch。
8. **ZERO_FOLD_KEY_MISMATCH** — 读错键折成合法零。零值必带读取表达式+顶层键断言。

回滚：任一形缺证据字段，对应读数标 UNVERIFIED 或 HOLD，不进 PASS 分母。上一并列稳定条为 20260919a。
