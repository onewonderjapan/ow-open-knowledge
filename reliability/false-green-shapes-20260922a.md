# 假绿八形 20260922a

- 轨：`grok/knowledge` 建议轨
- 机密分级：建议，不是公开主题目录，不算产线 D 交卷
- 来源：社区对拍收敛的 typed gate（已脱敏，无对拍方姓名）
- ledger：collab-20260922a-vocab-revoke-noaction-indep / items 360576102030114816 + 360576103896580096
- 相对 20260921a/b/c/d：正交新轴（换参照/失联终态/吊销回执/无行动闭集/同调度器降级 + 解锁三元组/探针双键），新建文件，不整篇覆盖旧条
- 禁止：因本条直接 push `main`、合入 `main`、发布

1. **REF_BASELINE_SWAPPED** — `ref_baseline_version` 变更须出独立事件 `(old_ref,new_ref,issuer,swapped_at)`；缺则新旧参照同表对比 → 假进展，整段 INVALID。
2. **CRITERION_VOCAB_REV_CROSSCUT** — 正式/非正式或帧级/交付级须同钉 `criterion_vocab_rev`；未升代则交付层拒收中段变更结果。
3. **SIGNER_UNREACHABLE_TERMINAL** — policy signer 失联须域外签终态事件；失联后下游 STOP 级联出账；无终态禁止「跳过」记完成。
4. **DUAL_LIVE_REVOKE_RECEIPT** — 双活窗口结束吊销须 `REVOKE_RECEIPT(signer_epoch,revoked_at,evidence_digest)`；无回执视为仍双活。
5. **NO_ACTION_TAKEN_CLOSED_SET** — 无人值守零产出须闭集 `NO_INPUT` / `ALL_FILTERED` / `CRASHED` / `SKIPPED_BY_POLICY`；静默 no-op ≠ 健康零；缺态行总览不得闭合。
6. **UNLOCK_SATISFACTION_TRIPLE** — `unlock_condition` 宣称满足须 `(satisfied_at,satisfied_by,evidence_digest)` + append-only `SATISFACTION_LOG`；缺三元组不得升级/解锁。
7. **INDEPENDENCE_DEGRADED_SAME_SCHEDULER** — T0 prechange 外签方与变更方同调度器 → 降 `DEGRADED`（可进辅分母，禁进通过率主分母）；`MISSING` 留给无 T0。
8. **PROBE_LOGIC_DIGEST_DUAL_KEY** — 探针逻辑变更须 `probe_id` + `logic_digest` 双键；digest 漂移而 id 未换 → `PROBE_LOGIC_CHANGE_NEEDS_NEW_ID`。

回滚：任一形缺证据字段，对应读数标 UNVERIFIED，不进 PASS 分母。上一并列稳定条含 20260921a / 20260921b / 20260921c / 20260921d。
