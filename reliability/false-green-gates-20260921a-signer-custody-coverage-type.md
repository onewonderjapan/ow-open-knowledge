# 假绿门 20260921a · signer / custody / coverage / type

- 轨：`grok/knowledge` 建议轨
- 机密分级：建议，不是公开主题目录，不算产线 D 交卷
- 来源：社区对拍收敛的 typed gate（已脱敏，无对拍方姓名）
- 广播 T2：360210380221317120 / plan collab-20260921a-signer-custody-coverage-type
- 形态：五门（非八形）
- 相对 20260919d / 20260920d：正交新轴，新建文件，不整篇覆盖旧八形
- 禁止：因本条直接 push `main`、合入 `main`、发布

1. **POLICY_SIGNER_UNREACHABLE** — signer 失联默认 HOLD_UNTIL_SIGNER_RESTORE。仅 lease 写明才 VOID。
2. **PRECHANGE_DENOM_MISSING** — 变更前分母须消费方 T0 外签快照。变更方旧快照不得用。
3. **ALERT_MAX_AGE_SELF_CLEAR** — max_age 自清的 executor 不得是被告警方。到期升 ESCALATED_UNANSWERED。
4. **COVERAGE_DEFINITION_BASIS** — 仅 independent_observer 进通过率分母。
5. **TYPE_DOMAIN_MIXED** — canonicalizer 须覆盖键类型域。混域拒比较。

回滚：任一门缺证据字段，对应读数标 UNVERIFIED 或 HOLD，不进 PASS 分母。
