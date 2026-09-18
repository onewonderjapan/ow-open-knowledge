# 假绿八形 20260918d

- 轨：`grok/knowledge` 建议轨
- 机密分级：建议，不是公开主题目录，不算产线 D 交卷
- 来源：社区对拍收敛的 typed gate（已脱敏，无对拍方姓名）
- 相对 20260918c：新码，不覆盖旧条
- 禁止：因本条直接 push `main`、合入 `main`、发布

1. **SHADOW_ENV_COINIT_NONATOMIC** — 阴影枚举与 PMREM 同 init 闭包却称单格回滚。整段用 rollback_unit_id；标 COINIT_NONATOMIC。
2. **MIGRATE_SHADOW_COMPARE_REQUIRED** — 「能渲染」当迁移通过。固定相机灯光对比 digest，并与 env、toneMapping、outputColorSpace 同捆；缺则 PROVISIONAL。
3. **WEIGHTS_REV_DIGEST_PAIR_REQUIRED** — 只报 rev 或只报 digest。强制 (rev, digest, epoch)；单向漂移 WEIGHTS_DESYNC；签发方等于被报表方则 UNPROVEN。
4. **REENTRY_GATE_REV_SILENT_SWAP** — reentry_gate_rev 变更无可见 diff。强制 gate_diff_digest，且 diff 签发方不得等于持有方；缺则仍 HOLD。
5. **BUSINESS_STATE_HASH_NE_ENVELOPE** — 业务态 hash 与回执信封 hash 互代。双层分列并同签；互代则 UNVERIFIED。
6. **EMPTY_REASON_MUST_BE_CLOSED_SET** — EMPTY 原因自由文本进机器判定。改闭集枚举；未知则 UNSTATED 加 UNMAPPED_REASON。
7. **CANONICALIZER_VERSION_REQUIRED** — 跨引擎比对无 canonicalizer_version。禁跨引擎绿；撞车策略显式 HARD_REJECT，或 PROVISIONAL 加窗长。
8. **AUTH_REVOKED_BUT_SIG_OK** — 签名有效但授权窗缺失或过期仍信任。sig_valid 且未授权单列，禁信任绿。

回滚：任一形缺证据字段，对应读数标 UNVERIFIED 或 HOLD，不进 PASS 分母。上一稳定 batch 为 20260918c。
