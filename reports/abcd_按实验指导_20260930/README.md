# DriveTDPA A-D 实验报告与分析

本目录按照《DriveTDPA 实验指导》整理当前 A-D 开环实验的实测结果。

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

## 核心结果

- A1-A4 均达到 100% 结构化解析成功率和 100% A→T 一致性。
- A1-A4 的 ADE 为 1.5953-1.5995 m，FDE 为 2.7289-2.7402 m。
- B3/B4 加入 BEV 后解析成功率均为 100%，高于 B1/B2 的 65%/60%。
- D2 加入 Talk2BEV 后，ADE 相对 D1 下降 19.75%，FDE 下降 16.91%，解析成功率提高 35 个百分点。
