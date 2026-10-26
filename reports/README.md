# 实验报告导航｜A–G 最终版优先

[项目首页](../README.md) · [A–G 最终成果](../FINAL_RESULTS.md) · [中文目录与时间线](../docs/project_guide_zh.md)

先看最终版报告，再按需回查历史材料。A–D 是 NuScenes 开环消融，E/F/G 是 CARLA 闭环与场景理解；两类指标需分别解释。

## ⭐ 最终报告与数据

| 实验 | 主报告：解释结果与边界 | 数据：查看表格和汇总 | 发布 / 更新日期 |
| --- | --- | --- | --- |
| **A–D · NuScenes 开环消融** | [最终分析报告](abcd_final/ANALYSIS_REPORT.md) · [目录说明](abcd_final/README.md) | [A–G 分组数据入口](../experiments/ag_final/README.md) · [数据表](abcd_final/ABCD_DATA_ANALYSIS.md) · [汇总 JSON](abcd_final/results_summary.json) · [结论 JSON](abcd_final/analysis_findings.json) | **2026-10-13**，报告深化更新 |
| **E/F/G · CARLA 闭环与场景理解** | [最终分析报告](efg_final/EFG_ANALYSIS_REPORT.md) · [目录说明](efg_final/README.md) | [E 逐次数据](../experiments/ag_final/E/) · [F 逐次数据](../experiments/ag_final/F/) · [G 审计与日志](../experiments/ag_final/G/) · [数据表](efg_final/EFG_DATA_ANALYSIS.md) · [汇总 JSON](efg_final/results_summary.json) | **2026-10-25**，报告发布 |

A–G 逐组结果集中在 [`experiments/ag_final/`](../experiments/ag_final/README.md)：A–D 含逐配置指标和预测，E/F 含逐次 CSV 与汇总 JSON，G 含 54 条时间线、审计、汇总及运行日志。A–D 的[原运行包](../experiments/runs/drivetdpa_abcd_nuscenes_20260930/)另外保留 held-out 与 SHA256；G 的 bag 仅发布 metadata，完整图像、模型权重和完整 rosbag 仍需外部准备，详见 [E/F/G 发布边界](efg_final/README.md)。

> **阅读口径**：A–D 的最终结论以 `abcd_final/ANALYSIS_REPORT.md` 为准，其中场景感知统计修正了自动数据表中的逐样本检验解释；E/F/G 的最终结论以 `efg_final/EFG_ANALYSIS_REPORT.md` 为准。闭环执行成功率不能等同于轨迹预测精度。

<a id="history"></a>

## 按时间回看版本

以下按**报告发布 / 更新日期倒序**排列。日期来自 Git 记录（北京时间），不使用检出文件的修改时间；实验数据日期另列。

| 报告版本 | 发布 / 更新日期 | 数据范围与用途 |
| --- | --- | --- |
| [E/F/G 最终版](efg_final/README.md) | **2026-10-25** | E 50 次、F 25 次执行试验；G 54 条场景理解审计。报告未统一提供三组精确实验日期 |
| [A–D 最终版](abcd_final/README.md) | **2026-10-13** | `20260930` 全量发布包：2523 训练样本 / 180 held-out 样本 / 9 场景 |
| [A–D 按实验指导整理版](abcd_按实验指导_20260930/README.md) | **2026-09-30** | 仍基于 **09-24 pilot**：450 训练样本 / 20 held-out 样本；目录日期表示整理日期 |
| [A–D 初版 pilot](abcd_20260924/README.md) | **2026-09-24** | 单场景小规模试验；供追溯早期配置和结论，不替代最终版 |

[最新状态摘要](latest.md)用于快速了解结论和限制。完整版本演进与项目目录说明见[中文阅读指南](../docs/project_guide_zh.md)。

## 文件类型怎么读

| 文件 | 中文说明 |
| --- | --- |
| `*ANALYSIS_REPORT.md` | 人工整理的最终实验分析：依据、逐组比较、机制、局限与论文结论 |
| `*DATA_ANALYSIS.md` | 数据表和分组统计；解释与最终分析报告配合阅读 |
| `results_summary.json` | 机器可读指标汇总，便于后续分析 |
| `analysis_findings.json` | 机器可读分析结论与审计边界 |

`figures/` 和 `metrics/` 当前仅预留目录，尚无已发布图表或指标文件；实际指标入口见上方 final 汇总与分组数据。部分运行日志已随 G 发布，完整图像、视频、模型权重及完整 rosbag 不随当前轻量结果包发布。示例数值不能作为正式测量结果。

---

[返回项目首页](../README.md) · [浏览 A–G 最终成果](../FINAL_RESULTS.md)
