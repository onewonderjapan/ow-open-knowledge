---
id: 20260905-judge-human-calibration-rerun
title: "观众语言模型评审 ↔ 人审相关性持续校准（规则 6–9 生效后复测）"
tags: [research]
created: 2026-09-05
updated: 2026-09-06
summary: "实验已执行（batch_s1_v1，11 卡人审 11 对局 finalized 2026-09-06）：规则 6–9 生效后 judge↔human 相关性 legacy 近似 −0.036 / 标准 Spearman −0.118——相关性「归零」但未由负转正，未达预注册 ≥0.3 阈值，首轮证伪口径（≤0）命中；历史序列更新为 0.384/−0.85/+0.85/−0.25/−0.625/0.1/−0.04，仍在震荡带内。机评前二遇冷与首届呼应（J 人审 0 胜、D park）。混杂因素：规则生效与评委池换为 GLM-5.3 同时发生，结论引用必须携带。"
lang: zh
type: experiment
scope: public
source: knowledge-base@8256ce7
related: [20260904-video-gen-model-pilot, 20260905-pet-tournament-physics-rerun]
---

# 观众语言模型评审 ↔ 人审相关性持续校准（规则 6–9 生效后复测）

> Summary: 实验已执行（batch_s1_v1）：规则 6–9 生效后 judge↔human 相关性 legacy −0.036 / 标准 −0.118，归零未转正、未达 ≥0.3，首轮证伪口径命中；机评前二（J/D）人审遇冷与首届呼应；评委池换为 GLM-5.3 与规则生效同时发生，属混杂因素。

## Context

本实验选自 [internal path] 选题 L-03（方向①：MV 导演模式）。

已有背景（来自证据笔记，非本实验产出）：

- director_training 历史 6 届 judge↔human Spearman 逐届为 0.384 / -0.85 / +0.85 / -0.25 / -0.625 / 0.1，正负载荡、机评第一多次未过人审；规则 6–9（痛点真实性 / 受众半径 / 台词体例 / 旁白用量管制）已于 2026-08-16 批准写入 CONTRACT 附录、下届 rubric 生效（见证据链第一条）。
- batch_s1_v1 的 11 张节拍表已有三评委均值分且编辑修订已完成，唯独缺人审 pairwise 配对（见证据链第二条）；机评侧另按总控 2026-09-06 改道决定以 GLM-5.3 三独立槽重跑（L-03a，rubric=rules_6_to_9）。

## 假设

评委 rubric 加装规则 6–9 四条反向约束后，judge↔human Spearman 从历史 6 届的 -0.85~+0.85 震荡转为持续为正（机评分可用于粗排序）。

- 证伪口径：规则生效后首轮 Spearman ≤0，或滚动后两届中相关性再度转负，即假设不成立。
- 本假设来自 backlog L-03 的假设草稿，执行前不得当作已验证事实引用。

## 方法（预注册 + 实际执行）

1. 取 digest 中同 11 张已修订节拍表，按 L-03a 编排的 11 对局链式对阵做人审 pairwise（每人恰 2 场，封顶机制照旧）。实际执行：2026-09-06T23:16 finalize，11 对局 + 11 disposition（1 park）。
2. 与机评三评委均值分排序计算 Spearman 双口径（legacy 近似 agreement + 标准 Spearman tie-corrected）。
3. 同口径滚动后两届锦标赛，形成规则生效前后的对照序列（待后续届次）。
4. 执行登记：卡片清单、逐对胜负、计算中间值——见 [internal path]。

## 数据（实测，2026-09-06）

- 人审 pairwise 11 对局：p1 A>B、p2 C>B、p3 D>C、p4 E>D、p5 F>E、p6 F>G、p7 H>G、p8 I>H、p9 I>J、p10 K>J、p11 K>A（字母映射见 machine_review/label_map.json）。人审胜场：F/I/K=2，A/C/D/E/H=1，B/G/J=0。
- Disposition：11 卡全 select 唯一例外 D（sc_20260816-194140-c）= park。
- 机评（GLM-5.3 三槽均值，rubric=rules_6_to_9）：J 8.83 > D 8.33 > C 8.25 > K 8.17 > B 7.50 > H 7.25 > A=F=I 7.08 > E 6.92 > G 5.83（胜负驱动前四 J>K>D>C 与均值序一致）。
- **相关性双口径：legacy 近似 agreement = −0.036（Σd²=228）；标准 Spearman（tie-corrected）= −0.118**（n=11）。历史序列更新为 0.384 / −0.85 / +0.85 / −0.25 / −0.625 / 0.1 / **−0.04**。

## 结论（2026-09-06 回填）

- **假设本届不成立（首轮证伪口径命中）**：规则 6–9 生效后相关性归零（legacy −0.036 / 标准 −0.118）但未由负转正、未达 ≥0.3；机评分本届不可用于粗排序。序列仍在历史震荡带内，「持续为正」需后两届滚动检验。
- 逐届震荡的结构性观察（本届新增证据）：机评前二遇冷跨届重现——J（机评第一，单人独角戏、机评全维度高分）人审 0 胜；D（机评第二）人审 park。人审偏好协作多任务线（F/I/K 全部 2 胜），机评的 canon 维度重扣（F/I 撞禁写清单）未被人审跟随——**两套评价体系的分歧轴仍在**，具体是「独角戏 vs 协作戏」还是「禁写清单扣分权重」，需下届设计区分实验。
- 必须随结论引用的混杂因素：规则 6–9 生效与评委池换为 GLM-5.3（原火山系面板，arkcli 已废弃）**同时发生**，相关性变化不能单独归因于规则；下届沿用 GLM-5.3 池可部分分离该因素。
- Confidence：low → medium（有实测数据，但 n=11 单届 + 混杂因素，证据强度为方向性排除「已转正」而非精确估计）。

## 证据链

- 历史 6 届 Spearman 序列与规则 6–9 的批准记录：`20260817-learning`（learning，director_training 学习日志：各 cycle 人审裁决、校准发现与规则批准原文）。
- 11 卡三评委均值分与修订完成状态：`20260817-digest`（digest，batch_s1_v1 观众语言模型评审合订本：三评委逐卡意见、均值分与编辑修订记录）。

## 复现性说明（reproducible: yes 的依据）

- 机评逐卡三槽分（machine_review/ranking.json）、人审逐对与 disposition（human_review/review_session.json，finalized 2026-09-06）、双口径复算过程（human_review/spearman_agreement.md）均已归档；第三方按归档材料可复算 −0.036（legacy）与 −0.118（标准）。
- review_session.json 的 judge_human_spearman 字段保持 finalize 原样（null），以 spearman_agreement.md 档案为准。

## 说明与局限

- n=11 且人审胜场仅 0/1/2 三档（链式编排每人 2 场），人审侧排序粒度粗，相关性估计方差大；结论是「未转正」的方向性排除，不是精确相关性估计。
- 评委池混杂因素见结论段；后两届滚动（预注册第 3 步）仍未执行，对照序列未闭合。
- 人审由总控执行（2026-09-06），本页如实记录其 finalized 数据；机评与本页计算由施工层完成。

## Related

- [视频生成模型小样评测：同组提示词的稳定性对比](video-gen-model-pilot.md) — supports：实验类笔记的字段规范与预注册写法来源。
- [物理常识规则生效后锦标赛机评 ↔ 人审复测](pet-tournament-physics-rerun.md) — see-also：姊妹管线（pet_drama）的同型实验，其「规则生效后转正」结果与本页「未转正」形成跨管线对照。
