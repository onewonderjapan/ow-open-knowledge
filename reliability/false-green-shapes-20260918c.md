# 假绿八形 20260918c

- 轨：`grok/knowledge` 建议轨
- 机密分级：建议，不是公开主题目录，不算产线 D 交卷
- 来源：社区对拍收敛的 typed gate（已脱敏；对拍方仅角色标签 A–G，无姓名）
- 相对 20260918b：新码，非重复
- 禁止：因本条直接 push `main`、合入 `main`、发布

1. **META_VALIDATOR_COLOCATED** — 多写入点同故障域致一致性检查恒真。分域写入；同域记 UNTRUSTED_SELF_CHECK；故意不一致正控仍绿则 VALIDATOR_DEAD。
2. **NC_NEVER_FIRED_IS_UNKNOWN** — 负控从未触发仍报通过。未触发记 UNKNOWN；last_fired_at 加窗口过期则 SENSOR_STALE。
3. **INDUCED_SINGLE_FIELD_HOLD** — 仅缺一必填仍放行。诱导负例期望 HARD_HOLD；仍绿则 GATE_SOFTENED。
4. **GRAY_ZONE_BY_EVIDENCE_DOMAIN** — 按条目隔离灰区致跨域拼绿。按证据域隔离并带 evidence_domain_anchor；无锚则 CROSS_DOMAIN_UNANCHORED。
5. **ZERO_REJECT_MULTI_WINDOW_AUDIT** — 单次 0% 拒绝当健康。最小样本加连续窗触发审计；审计窗须仍可弄红 must-fail。
6. **DESENSITIZE_CLAIM_NEEDS_SIGNER** — 脱敏声明自签。脱敏头 signer 不得等于 executor，否则禁入共享池。
7. **GATE_BIPOLAR_NC** — 门禁缺 must-pass / must-fail 成对。成对负控加 readback；must-fail 后分母仍增则 GATE_LEAK。
8. **CHANGE_MATRIX_REQUIRED** — 多变因同升版无归因矩阵。要 api_rev 与 path 矩阵；缺则 UNATTRIBUTED_BLACK；CI 挡住已删枚举。

回滚：任一形缺证据字段，对应读数不得进 PASS 分母。
