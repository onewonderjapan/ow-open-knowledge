# 阶段② 决策 / 执行 (Decide / Act)

**目标**：依据当前策略与本轮输入产出决策；模拟模式下记账。

## 步骤
1. 读取 `state/strategy.md`（当前逻辑）与 `state/portfolio.json`（当前状态）。
2. 结合 `runs/<run-key>/inputs/` 产出决策，写 `runs/<run-key>/decisions.json`：
   - 每条决策含：标的、动作、数量/权重、**理由**、触发该决策的策略条款引用。
3. 校验风险约束（如 `params.max_position_pct` 单仓上限）。
4. **paper 模式**：把成交写入 `state/ledger.jsonl`（append，带 `run_key`/`ts`），
   并据此更新 `state/portfolio.json` 快照。
5. **live 模式**：命中确认门（`gates.real_order`）→ 停下，产出待确认清单交人工，**不自动下单**。

## 产出
- `runs/<run-key>/decisions.json`
- （paper）`state/ledger.jsonl` 追加、`state/portfolio.json` 更新

## 约束
- 每条决策必须可追溯到 strategy 的具体条款（便于④改善时归因）。
- 风险约束优先于收益动机。
