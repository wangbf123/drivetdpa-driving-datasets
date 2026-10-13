# A–D 开环实验分析报告（NuScenes 全量，最终版）

这是 `drivetdpa_abcd_nuscenes_20260930` 的**权威、论文级分析报告**，覆盖 A1–A4（偏好消融）、B1–B4（模态消融）、C1–C2（动作层消融）、D1–D2（Talk2BEV 消融）。相较 2026-09-30 早期版本（`reports/abcd_按实验指导_20260930/`），本版经过**深度数据挖掘 + 三次自我修正**，是可支撑论文结论的定稿。

## 文件

| 文件 | 内容 |
|---|---|
| [`ANALYSIS_REPORT.md`](./ANALYSIS_REPORT.md) | **主报告**（中文，236 行）：摘要、行为塌缩三层证据、ADE 误差归因、机制、A/B/C/D 消融、条件、局限、可支撑主张、后续建议、附录 |
| [`analysis_findings.json`](./analysis_findings.json) | 机器可读结论（17 个字段）：动作构成、塌缩、横向/纵向位移、误差归因、think 复述、场景感知检验、独立验证等 |
| [`results_summary.json`](./results_summary.json) | 12 配置汇总统计（mean±std / 95% t 区间 / 条件分解 / 配对检验） |
| [`ABCD_DATA_ANALYSIS.md`](./ABCD_DATA_ANALYSIS.md) | pipeline 自动生成的原始汇总报告 |

## 核心结论（六条强支撑主张）

| # | 结论 |
|---|---|
| **S1** | surrogate 偏好优化（A2/A3/A4）相对 SFT **无精度增益**；场景感知检验下 A1–A4 **统计不可区分**（p≥0.36，CI 跨 0） |
| **S2** | 模型**整类丢弃转向动作** + **几乎从不刹车**，塌缩**与场景无关**（9/9 场景 100% 直行） |
| **S3** | **主导误差是纵向（不会刹车）**：GT 刹车样本 ADE ≈10.1–11.2m（2× 均值），转向样本仅 ≈5.0m |
| **S4** | BEV 是 RAT **输出合规性**的必要输入（去 BEV：parse 1.00→0.61） |
| **S5** | Action 层独立贡献轨迹精度（去掉 ADE +22%） |
| **S6** | think 为**复述式**（85.4% 8-gram 逐字来自输入），非机动推理 |

## 三次关键修正（诚实记录）

1. **正则 bug**：早期脚本正则未匹配实际段落标题 `### Correct action:`，误报"GT 零转向样本"；修正后 held-out 实为 **52/180** 含转向。
2. **归因修正**：主失效从"不转弯"改为"**不刹车/不停车**"（刹车样本驱动超额误差）。
3. **统计修正（最重要）**：逐样本 Wilcoxon 曾报 A2/A4 "显著更差"，但**反保守**（忽略场景聚类）；场景感知复测（n=9 场景配对 + cluster bootstrap）显示 **A1–A4 无差异**。论文须用场景感知统计。

原始 run 数据见 [`experiments/runs/drivetdpa_abcd_nuscenes_20260930/`](../../experiments/runs/drivetdpa_abcd_nuscenes_20260930/)。
