# 假绿八形 20260918b

- 轨：`grok/knowledge` 建议轨
- 机密分级：建议，不是公开主题目录，不算产线 D 交卷
- 来源：社区对拍收敛的 typed gate（已脱敏，无对拍方姓名）
- 禁止：因本条直接 push `main`、合入 `main`、发布

1. **GRAY_ZONE_HELD** — 灰区相似度不进任一层通过率；GRAY_FLOOD 回结构预检。
2. **INTERSECTION_EMPTY_MUST_RED** — 「交集为空仍健康」必须附可弄红的负控，否则 UNATTESTED。
3. **RECEIPT_ISSUER_NE_EXECUTOR** — 收据签发方不得等于执行方；四元组两两不等才算 VERIFIED。
4. **ROSTER_DELTA_UNVERIFIED** — 名单增量须 shot_digest + rules_rev + 消费方反签。
5. **FALLBACK_UNEXPLAINED** — fallback 必须含 trigger_code；缺则不得当成功降级。
6. **RESTORE_REQUIRES_RECEIPT** — 解冻或恢复须显式反签回执，禁止静默变绿。
7. **INSPECTED_VS_DECLARED** — 受检计数与外签清单基数成对；部分扫描标 SCOPE_PARTIAL。
8. **SAMPLE_UNANCHORED** — 关键帧抽样须带 frame index；缺锚不得报几何健康。

回滚：任一形缺证据字段，对应读数标 UNVERIFIED 或 HOLD，不进 PASS 分母。
