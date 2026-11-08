# 知识笔记索引 / Index

共 5 篇。由 `kb export-public` 生成，请勿手改。

| id | title | summary | lang | updated | path |
|---|---|---|---|---|---|
| `20260925-codegen-2d-landscape` | 代码生成 2D：高星 repo 与官方 skill 方法论 | 代码生成 2D 五层盘点（as-of 2026-09-25）：最高星的是「AI 可靠生成的目标格式」库（mermaid 90.4k / excalidraw 132.9k / manim 94.2k）；官方 skill 方法论样本 anthropics/skills（178.1k）是先写美学宣言再用 canvas/p5.js 表达的两段式，强调不锁创意、craftsmanship、原创避版权。 | zh | 2026-09-25 | [presales-research/codegen-2d-landscape.md](presales-research/codegen-2d-landscape.md) |
| `20260906-gebiz-window-ledger` | 新加坡 GeBIZ 投标窗口分布实测（8 周观察，L-20） | 8 周窗口观察第 1 周：台账已建（[internal path]），首批 4 个 IT 类机会窗口 12.85/24.91/≈9(粗)/12.99 天，中位数初值 ≈12.9 天、≤14 天占比 3/4，与假设方向一致但 n=4 不足以判定；每周由轮询会话从 digest 追加，8 周后出分布报告。 | zh | 2026-09-06 | [presales-research/gebiz-window-ledger.md](presales-research/gebiz-window-ledger.md) |
| `20260925-gh-research-framework` | GitHub 高星 repo 定期调查框架（3D 渲染与代码生成 2D） | 本主题的调查规程：对象是 AI 做视觉产出（3D 渲染 / 代码生成 2D）的高星 repo；口径用 GitHub API 当日实测星数；知识按「引擎层→神经渲染→生成式→接口层（skill/MCP）」分类轴归类，每轮刷新盘点笔记而非新建。 | zh | 2026-09-25 | [presales-research/gh-research-framework.md](presales-research/gh-research-framework.md) |
| `20260925-render-3d-landscape` | 3D 画面渲染：高星 repo 路线图与方法论 | 3D 渲染高星 repo 四层盘点（as-of 2026-09-25，GitHub API 实测）：实时引擎 three.js 115.9k 一枝独秀且日更；神经渲染主线已收敛到 3DGS 工具链；生成式 3D 研究 repo 普遍「发论文即冻结」；AI×3D 的增量在 MCP/skill 接口层而非新算法库。 | zh | 2026-09-25 | [presales-research/render-3d-landscape.md](presales-research/render-3d-landscape.md) |
| `20260905-judge-human-calibration-rerun` | 观众语言模型评审 ↔ 人审相关性持续校准（规则 6–9 生效后复测） | 实验已执行（batch_s1_v1，11 卡人审 11 对局 finalized 2026-09-06）：规则 6–9 生效后 judge↔human 相关性 legacy 近似 −0.036 / 标准 Spearman −0.118——相关性「归零」但未由负转正，未达预注册 ≥0.3 阈值，首轮证伪口径（≤0）命中；历史序列更新为 0.384/−0.85/+0.85/−0.25/−0.625/0.1/−0.04，仍在震荡带内。机评前二遇冷与首届呼应（J 人审 0 胜、D park）。混杂因素：规则生效与评委池换为 GLM-5.3 同时发生，结论引用必须携带。 | zh | 2026-09-06 | [qa-gates/judge-human-calibration-rerun.md](qa-gates/judge-human-calibration-rerun.md) |
