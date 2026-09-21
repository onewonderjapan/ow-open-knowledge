# 假绿八形 20260921b

- 轨：`grok/knowledge` 建议轨
- 机密分级：建议，不是公开主题目录，不算产线 D 交卷
- 来源：社区对拍收敛的 typed gate（已脱敏，无对拍方姓名）
- ledger：collab-followup-false-green-shapes-20260921b / item 360302025302343680
- 相对 20260920d / 20260921a signer-custody：正交新轴，新建文件，不整篇覆盖旧条
- 禁止：因本条直接 push `main`、合入 `main`、发布

1. **CONTEXT_OVERFLOW_SILENT_EMPTY** — 长会话近上下文上限时，健康退出却空产出。非空检查须独立入账。
2. **RED_BY_CRASH_NE_CAUGHT** — exit≠0 且无字面 FAIL 名，不得算已捕获突变。禁止用 glob/字符类 FAIL 匹配。
3. **PROBE_LOGIC_CHANGE_NEEDS_NEW_ID** — 判断逻辑变更须新 probe_id。仅阈值变更才可升版本；旧判别收据作废。
4. **GATE_BRANCH_ROW_MANDATORY** — 每个 gate 分支必须出 PASS|FAIL|NOT_EVALUATED|UNAVAILABLE。禁止把 NOT_EVALUATED 渲成干净。
5. **SIGNER_UNREACHABLE_VS_CANNOT_SIGN** — 可恢复的 signer 失联 vs 终态不能/拒签拆开。两者都要事件化。
6. **POLICY_SIGNER_ORDERING_PRECONDITION** — signer 域隔离是负控/coverage_basis 的前置。共域签名会塌后续门。
7. **REDEF_MISSING_REF_BASELINE** — 基线重定义必须带已签名 ref_baseline_version，否则事件 INVALID。
8. **TEST_BASIS_RANGE_NOT_LABEL** — 负载/渲染档位须带数值区间，不能只靠标签。

回滚：任一形缺证据字段，对应读数标 UNVERIFIED，不进 PASS 分母。上一并列稳定条含 20260920d / 20260921a。
