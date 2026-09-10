---
name: CHANGE-ME-workflow-name
description: 一句话说明"何时触发·做什么"。例：每日金融分析与模拟投资闭环——收盘后评估昨日决策并小步改善策略，开盘前采集行情并产出当日模拟操作。
---

# <工作流名称>

> 遵循仓库 [STANDARD.md](../STANDARD.md)。默认 `paper` 模式，命中确认门即停下问人。

## 用途 / 触发
- 何时用：<cron 每日调用 / 手动 `/<name>`>
- 目标：<这个闭环要达成什么>

## 前置检查
1. 读取 `config.yml`：确认 `mode`（paper/live）、本轮属于哪个阶段组合。
2. 计算 run-key = 今天日期；若 `runs/<run-key>/` 已存在 → 按 §P1 幂等处理（跳过或加后缀续跑）。
3. 读取 `state/strategy.md`（当前逻辑）与 `state/portfolio.json`（当前状态）。

## 阶段① 采集 —— 详见 [steps/1-ingest.md](steps/1-ingest.md)
- 拉取本轮外部输入，落盘 `runs/<run-key>/inputs/`。只读，不改 state。

## 阶段② 决策/执行 —— 详见 [steps/2-decide.md](steps/2-decide.md)
- 依据 strategy + 本轮输入产出决策 → `runs/<run-key>/decisions.json`。
- paper 模式：把模拟操作写入 `state/ledger.jsonl`，更新 `state/portfolio.json`。

## 阶段③ 评估/采点 —— 详见 [steps/3-evaluate.md](steps/3-evaluate.md)
- 对**过去**的决策用后续真实行情打分 → 追加 `state/scorecard.jsonl`。

## 阶段④ 改善/学习 —— 详见 [steps/4-improve.md](steps/4-improve.md)
- 依据 scorecard 证据，对 `strategy.md` 做一次带理由、可回滚的小步修订，并追加变更日志。

## 收尾
1. 写 `runs/<run-key>/report.md`（本轮做了什么·为什么·评分·策略是否改动）。
2. 确认所有 state 更新已落盘。
3. 若有命中确认门的动作（真实下单/发送等）→ **停下**，向人汇报待确认，不自动执行。

## 失败处理与幂等
- 任一阶段失败：记录到 report.md，保留已完成阶段的产物，不污染 state。
- 重跑安全：以 run-key 判重；只追加文件天然幂等去重需带 run-key 字段。
