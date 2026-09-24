# DriveTDPA A-D 消融实验

本目录保存 2026-09-24 完成的 NuScenes OSS 小规模 A-D 消融实验发布材料。

## 快速阅读

1. [中文数据分析报告](./中文数据分析报告.md)：论文可用的结果分析、对照结论和限制。
2. [实验结果汇总](./实验结果汇总.json)：12 个配置的机器可读指标。
3. [实验配置说明](./实验配置说明.md)：A-D 每个实验的输入、输出和评估含义。
4. [文件清单](./文件清单.md)：本目录文件和外部原始数据位置。

## 核心结论

- A1-A4 的 ADE/FDE 基本稳定在 1.60/2.73 m，当前 pilot 未显示偏好优化方法带来明确轨迹精度提升。
- 移除 BEV/Talk2BEV 后，解析成功率由 100% 降至 65%，ADE/FDE 约恶化 25%/20%。
- 恢复 BEV 后，结构化输出和场景引用率恢复到 100%，支持场景表示对可靠输出的重要性。

## 数据范围

- 训练：450 条样本，18 个 scene，来源为 NuScenes OSS trainval02-10。
- 评估：1 个 scene-disjoint held-out scene，20 条样本。
- 评估模型：真实 `DriveTDPAPredictor`，不是 mock。

完整 checkpoint、图片、预测原文和模型日志不进入 Git，保留在实验服务器路径：
`/mnt/workspace/drivetdpa_experiments/abcd_complete_20260924/`。
