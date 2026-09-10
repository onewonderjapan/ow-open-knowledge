# agent-cultivation — AI Agent Cultivation Methodology

How do you *grow* an AI agent/skill/workflow instead of just writing one? This is the standard we distilled after running the same improvement loop across four business lines (image production, business AI, MV production, LoRA training): a cultivation loop (real task → pitfall log → three-layer consolidation → golden-sample recycling), a training guide for agents already in production, a startup standard for new agent projects, and the data classification rules that make it all safe.

## Contents

| File | What it covers |
|------|----------------|
| [AGENT育成標準.md](AGENT育成標準.md) | **The core standard.** Five principles, the cultivation loop, three-layer consolidation (code / skill / memory), QC discipline — with mermaid diagrams |
| [既存AGENT訓練ガイド.md](既存AGENT訓練ガイド.md) | How to improve an agent that is already running: offline exercise ("exam" cases), golden-sample recycling, regression verification |
| [新プロジェクトSTARTUP標準.md](新プロジェクトSTARTUP標準.md) | Startup standard for new agent projects: skeleton, what to do on day one |
| [AI研究会-学習と業務適用の基礎.md](AI研究会-学習と業務適用の基礎.md) | Study-group material: learning foundations and applying them to business work |
| [FLOW.md](FLOW.md) | The ai-stack pipeline flow plus the skill-growth loop — the full picture |
| [PHASE0-RESULTS.md](PHASE0-RESULTS.md) | Results of Phase 0 (baseline verification) |
| [PITFALLS.md](PITFALLS.md) | Pitfall log: symptom / root cause / fix (e.g. CJK-username cache issues) |
| [data-classification.md](data-classification.md) | Data classification template: L1/L2/L3 levels + prohibited-data list |
| [workbench-skills/](workbench-skills/) | Personal workbench skill set (daily-start, weekly-check, … + a coach agent) |

## Recommended reading order

1. **[AGENT育成標準.md](AGENT育成標準.md)** — the global picture of the cultivation loop
2. **[既存AGENT訓練ガイド.md](既存AGENT訓練ガイド.md)** — concrete improvement techniques
3. **[新プロジェクトSTARTUP標準.md](新プロジェクトSTARTUP標準.md)** — follow this when starting a new project
4. **[data-classification.md](data-classification.md)** — clear the data-safety gate before touching real data
5. The rest as needed: study-group material, the full flow, the pitfall log

## Notes

- Documents keep their original wording — Japanese, Chinese, or a mix of both, sometimes within the same paragraph. That is how the team actually writes, so we kept it rather than translating it away. Filenames are original too.
- [data-classification.md](data-classification.md) is a ready-to-adopt template: swap in your team's roles and tool list.
- For a runnable companion implementation, see [../ai-stack/](../ai-stack/).
