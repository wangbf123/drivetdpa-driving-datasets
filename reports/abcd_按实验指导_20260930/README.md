# A–D 历史报告｜2026-09-30 按实验指导整理版

[项目首页](../../README.md) · [A–G 最终成果](../../FINAL_RESULTS.md) · [报告总目录](../README.md) · [中文目录与时间线](../../docs/project_guide_zh.md)

> **历史版本 · 基于 09-24 pilot**｜本目录于 **2026-09-30**整理并更新，但使用的是 **2026-09-24** 的 450 训练 / 20 held-out 样本数据；不是同名日期的全量实验。最新结论请读 [A–D 最终报告](../abcd_final/ANALYSIS_REPORT.md)。

本目录按照《DriveTDPA 实验指导》整理早期 A–D 开环实验的实测结果，保留用于版本追溯。

## 实验指导路径

```text
/mnt/workspace/TEMP-FILE-STATION/DriveTDPA 实验指导.docx
```

## 文件说明

| 文件 | 内容 |
|---|---|
| [A-D实验报告.md](./A-D实验报告.md) | 实验目的、配置、数据、指标和结果 |
| [A-D实验分析.md](./A-D实验分析.md) | 按 A、B、C、D 四组展开的对比分析 |
| [实验指标汇总.json](./实验指标汇总.json) | 12 个配置的机器可读实测指标 |

## 本轮实验概况

- 数据来源：NuScenes OSS trainval02-10。
- 训练数据：450 条，18 个 scene。
- 评估数据：20 条 held-out 样本。
- 推理后端：真实 `DriveTDPAPredictor`，`mock=false`。
- 实验配置：A1-A4、B1-B4、C1-C2、D1-D2，共 12 组。
- 原始实验目录：`/mnt/workspace/drivetdpa_experiments/abcd_complete_20260924/`。

## 当时的 pilot 结果（历史口径）

- A1-A4 均达到 100% 结构化解析成功率和 100% A→T 一致性。
- A1-A4 的 ADE 为 1.5953-1.5995 m，FDE 为 2.7289-2.7402 m。
- B3/B4 加入 BEV 后解析成功率均为 100%，高于 B1/B2 的 65%/60%。
- D2 加入 Talk2BEV 后，ADE 相对 D1 下降 19.75%，FDE 下降 16.91%，解析成功率提高 35 个百分点。

上述结果来自单场景 20 样本评估。全量最终版使用 180 样本 / 9 场景，并修正了 Talk2BEV 精度收益、动作层贡献及统计检验等结论；引用研究结论时应以[最终分析报告](../abcd_final/ANALYSIS_REPORT.md)为准。

---

[返回报告总目录](../README.md) · [阅读 A–D 最终版](../abcd_final/README.md)
