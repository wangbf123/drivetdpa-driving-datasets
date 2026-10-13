# DriveTDPA 数据集与实验仓库

> DriveTDPA 项目的数据门户：**CARLA 自动驾驶数据规范与采集** + **NuScenes A–D 开环消融实验**的完整数据、分析与报告。

![NuScenes A-D](https://img.shields.io/badge/experiment-NuScenes%20A%E2%80%93D-blue)
![CARLA](https://img.shields.io/badge/source-CARLA-orange)
![InternVL](https://img.shields.io/badge/model-InternVL%203.5--1B-blueviolet)
![status](https://img.shields.io/badge/status-pre--release-yellow)

## 目录

- [最新：NuScenes A–D 开环消融实验](#nuscenes-a-d-开环消融实验)
- [CARLA 数据集门户](#carla-数据集门户)
- [仓库目录](#仓库目录)
- [快速校验](#快速校验)
- [数据怎么存](#数据怎么存)
- [数据真实性规则](#数据真实性规则)
- [详细文档](#详细文档)

---

## NuScenes A–D 开环消融实验

**这是本仓库当前最完整的实验成果**（`drivetdpa_abcd_nuscenes_20260930`），对照实验指导在 NuScenes 上完成 A/B/C/D 四组开环消融。

**一句话结论**：模型学会了 RAT 协议的**格式**与"前进"意图，但发生**行为类别塌缩**——整类丢弃转向、几乎从不刹车；**主导误差是纵向（不会停车）**；surrogate 偏好优化（A2/A3/A4）相对 SFT **无精度增益**（场景感知统计下 A1–A4 不可区分）。

| 入口 | 说明 |
|---|---|
| [📄 主报告](reports/abcd_final/ANALYSIS_REPORT.md) | 论文级分析（行为塌缩三层证据、误差归因、场景感知统计、三次修正） |
| [📊 机器可读结论](reports/abcd_final/analysis_findings.json) | 17 个结构化字段，可直接引用 |
| [📦 原始 run 数据](experiments/runs/drivetdpa_abcd_nuscenes_20260930/) | 20 份 metrics + predictions + held-out 集 + SHA256 |
| [📖 中文说明](docs/nuscenes_abcd_experiment_zh.md) | 面向中文读者的完整解读 |
| [🔧 复现脚本](scripts/experiments/abcd_full/) | 数据切分 → 训练 → 评估 → 报告，可断点续跑 |

**六条强支撑主张**：① A1–A4 无显著差异；② 整类丢弃转向 + 从不刹车（与场景无关）；③ 误差主因是刹车；④ BEV 是输出合规必要输入；⑤ Action 层独立贡献 +22%；⑥ think 是复述而非推理。

---

## CARLA 数据集门户

本仓库同时是 CARLA 自动驾驶实验的数据门户：将仿真传感器、Autoware 状态、动态 BEV、Talk2BEV 场景描述、DriveTDPA 轨迹预测、偏好选择、控制指令和下一帧反馈串联成可追踪、可验证、可复现的场景记录。

> 当前状态：**数据规范、格式示例和自动实验预发布数据**。`examples/` 仅用于说明格式；`experiments/runs/` 保存已经过真实模型、真实 judge、loader 和 SHA256 校验的小型 CARLA recorded-seed 实验包。它们不是完整实时闭环数据集，也不能视为 Ground Truth。

### 项目完整链路

```text
CARLA 相机 / LiDAR / GNSS / IMU / 车辆状态
  -> CARLA ROS Bridge
  -> Autoware 定位 / 感知 / 地图 / 路由
  -> 动态 BEV
  -> Talk2BEV 场景事实和文字描述
  -> DriveTDPA 推理 / 动作 / 3 秒轨迹
  -> preference selector 选择安全候选轨迹
  -> Autoware 规划与控制
  -> CARLA 车辆执行
  -> 下一帧 CARLA 状态与闭环指标
```

本仓库正式数据均使用 `source: "carla"`。偏好对来自**同一个 CARLA 场景、同一帧输入**的多次 DriveTDPA rollout，不会将无关输入或伪造数据混合成偏好样本。

### 每一帧包含什么

| 链路阶段 | 数据示例 | 常见文件格式 |
| --- | --- | --- |
| CARLA 传感器 | 前视 RGB、LiDAR、车辆位姿和速度 | JPG/PNG、PCD/BIN、JSON |
| ROS Bridge | 带时间戳的 ROS 2 Topic 和 TF | rosbag2 DB3/MCAP |
| Autoware | 定位、目标、路由、规划轨迹和控制指令 | ROS 2 消息、JSON 导出 |
| 动态 BEV | 自车、目标、占用栅格、车道关系和风险 | JSON、PNG |
| Talk2BEV | 结构化场景事实和自然语言描述 | JSON/JSONL |
| DriveTDPA | 推理、3 步动作、6 点轨迹和延迟 | JSON/JSONL |
| 偏好选择器 | 候选轨迹、评分、chosen/rejected | JSON/JSONL |
| 闭环结果 | `t` 时刻控制与 `t+1` 时刻车辆反馈 | JSON/JSONL |

字段说明见[数据字典](docs/data_dictionary.md)，完整关联示例见[场景示例](examples/scene_000001/manifest.json)。

### 计划发布的数据集

| 数据集版本 | 内容 | 状态 |
| --- | --- | --- |
| `dataset-carla-v0.1` | CARLA、Autoware、BEV、Talk2BEV 和 DriveTDPA 多模态帧 | 计划中 |
| `dataset-carla-preference-v0.1` | CARLA 场景候选轨迹组和偏好对 | 计划中 |
| `dataset-carla-closed-loop-v0.1` | 控制指令到下一帧反馈的闭环片段和指标 | 计划中 |
| `dataset-carla-preference-experiment-v0.1` | 已录制 CARLA 种子上的真实模型多采样和偏好选择 | 自动持续采集中 |

“计划中”表示已经预留数据规范和发布位置，不表示完整数据已经采集或通过验证。

## 仓库目录

```text
docs/                  架构、采集协议、字段说明、中文说明和 ROS Topic
datasets/              正式数据集发布位置和存储约定
manifests/             场景及大文件的机器可读索引
schemas/               用于自动校验的 JSON Schema
examples/              小型 CARLA 格式示例场景
reports/               实验汇总、指标和图表（含 NuScenes A–D 分析报告）
experiments/           自动实验 run、机器可读索引和逐文件校验和
scripts/               数据校验、校验和、下载与 A–D 复现脚本
```

## 快速校验

工具只依赖 Python 3.9+ 标准库：

```bash
python scripts/validate_dataset.py examples/scene_000001/manifest.json
python scripts/generate_checksums.py examples/scene_000001
python scripts/validate_experiment.py experiments/runs
```

自动采集、持续运行、停止和导入命令见
[《DriveTDPA 自动实验运行手册》](docs/automated_experiment_guide_zh.md)，实验文件说明见
[`experiments/README.md`](experiments/README.md)。

正式清单填写真实 HTTPS 下载地址后，可按场景下载并自动验证 SHA256：

```bash
python scripts/download_dataset.py manifests/dataset-carla-v0.1.example.jsonl \
  --scene scene_000001 --output data
```

示例清单仍是占位符，下载工具会主动拒绝，避免误认为已经发布正式数据。

## 数据怎么存

GitHub 保存文档、Schema、小型示例、manifest、校验和、图表和报告。完整相机序列、点云、rosbag2、地图、视频和模型权重应存入阿里云 OSS 或公开数据集平台。每个正式文件必须在 manifest 中记录文件大小和 SHA256。具体规则见[存储与发布规范](docs/storage_and_release.md)。

## 数据真实性规则

- CARLA 仿真器状态、碰撞信号和配置好的路线可以作为 Ground Truth，但必须保留来源和配置。
- 模型生成的场景描述、推理、动作和轨迹都是预测结果，不能标为 Ground Truth。
- 偏好判断模型不能看到 reward、rank、未来真值或 chosen/rejected 标签。
- 非有限数值、发生碰撞或越界的轨迹不能被 preference selector 选中。
- 所有数据使用稳定的 `dataset_version`、`scene_id`、`frame_id` 和 CARLA 时间戳进行关联。

## 详细文档

- [系统架构](docs/architecture.md)
- [CARLA 数据采集流程](docs/data_collection.md)
- [数据字典](docs/data_dictionary.md)
- [ROS 2 Topic 清单](docs/ros_topics.md)
- [存储与发布规范](docs/storage_and_release.md)
- [NuScenes A–D 实验中文说明](docs/nuscenes_abcd_experiment_zh.md)
- [数据贡献说明](CONTRIBUTING.md)
