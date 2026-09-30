# DriveTDPA A-D 实验数据（NuScenes OSS）

本目录保存 2026-09-24 完成的 DriveTDPA A-D 实验运行结果。数据来自 NuScenes OSS，按实验指导组织为 A、B、C、D 四组共 12 个配置。

## 数据规模

| 项目 | 数量 |
| --- | ---: |
| 训练样本 | 450 条 |
| 训练场景 | 18 个 scene |
| 评估样本 | 20 条 |
| 评估场景 | 1 个 scene |
| 实验配置 | 12 个 |

训练阶段使用真实模型训练与推理链路；评估结果中的 `mock` 字段为 `false`。原始运行目录为 `/mnt/workspace/drivetdpa_experiments/abcd_complete_20260924`，本目录仅发布可复核的小型结果产物。

## 目录结构

```text
experiments/runs/drivetdpa_abcd_nuscenes_20260924/
├── README.md
├── run_manifest.json       # 运行元数据与发布信息
├── experiment_matrix.json  # A-D 配置矩阵
├── SHA256SUMS              # 所有文件的 SHA256 校验值
├── metrics/                # 每个配置一份指标 JSON
├── predictions/            # 每个配置逐样本预测 JSONL
└── logs/                   # 每个配置的推理服务日志
```

## 实验配置

| 组别 | 配置 | 中文含义 |
| --- | --- | --- |
| A | A1_SFT | SFT 基线 |
| A | A2_physics | 物理约束训练 |
| A | A3_jpo | JPO 偏好优化 |
| A | A4_vldpo | VL-DPO 偏好优化 |
| B | B1_image_text | 图像 + 文本输入 |
| B | B2_image_speech | 图像 + 语音转写输入 |
| B | B3_image_text_bev | 图像 + 文本 + BEV |
| B | B4_image_speech_bev | 图像 + 语音转写 + BEV |
| C | C1_R_to_T | 直接从场景表征到轨迹 |
| C | C2_R_to_A_to_T | 场景表征到动作再到轨迹 |
| D | D1_no_talk2bev | 不使用 Talk2BEV |
| D | D2_talk2bev | 使用 Talk2BEV |

完整的输入模式、输出协议和组别说明见 [`experiment_matrix.json`](experiment_matrix.json)。

## 文件映射

- `metrics/<配置>.json`：ADE、FDE、Goal、解析成功率、场景引用率、延迟等评估指标。
- `predictions/<配置>.jsonl`：与指标文件对应的逐样本模型输出。
- `logs/<配置>.server.log`：该配置推理服务的运行日志。
- `run_manifest.json`：数据来源、规模、配置数量和发布路径等机器可读元数据。
- `SHA256SUMS`：对本目录全部文件进行完整性校验。

## 相关报告

中文实验报告与 A-D 分组分析位于 [`reports/abcd_按实验指导_20260930/`](../../../reports/abcd_按实验指导_20260930/)。

## 发布边界

本目录只包含指标、逐样本预测、日志和元数据，便于 GitHub 上浏览和复现实验记录；模型 checkpoint、图像、点云、原始 NuScenes 文件及训练压缩包仍保留在 OSS/工作空间，不随本目录提交。

