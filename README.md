# DriveTDPA CARLA 自动驾驶数据集

本仓库是 DriveTDPA 项目的公开数据门户，用于组织和展示 CARLA 自动驾驶实验产生的数据。它将仿真传感器、Autoware 状态、动态 BEV、Talk2BEV 场景描述、DriveTDPA 轨迹预测、偏好选择、控制指令和下一帧反馈串联成可以追踪、验证和复现实验的场景记录。

> 当前状态：**数据规范与示例版本**。`examples/` 中的数据只用于说明格式，不代表正式实验结果，也不能视为 Ground Truth。完整 CARLA 实验数据将在采集后上传至对象存储，并通过本仓库发布索引、校验和与实验报告。

## 项目完整链路

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

## 每一帧包含什么

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

## 计划发布的数据集

| 数据集版本 | 内容 | 状态 |
| --- | --- | --- |
| `dataset-carla-v0.1` | CARLA、Autoware、BEV、Talk2BEV 和 DriveTDPA 多模态帧 | 计划中 |
| `dataset-carla-preference-v0.1` | CARLA 场景候选轨迹组和偏好对 | 计划中 |
| `dataset-carla-closed-loop-v0.1` | 控制指令到下一帧反馈的闭环片段和指标 | 计划中 |

“计划中”表示已经预留数据规范和发布位置，不表示完整数据已经采集或通过验证。

## 仓库目录

```text
docs/                 架构、采集协议、字段说明和 ROS Topic
datasets/             正式数据集发布位置和存储约定
manifests/            场景及大文件的机器可读索引
schemas/              用于自动校验的 JSON Schema
examples/             小型 CARLA 格式示例场景
reports/              实验汇总、指标和图表
scripts/              数据校验、校验和与安全下载工具
```

## 快速校验

工具只依赖 Python 3.9+ 标准库：

```bash
python scripts/validate_dataset.py examples/scene_000001/manifest.json
python scripts/generate_checksums.py examples/scene_000001
```

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
- [数据贡献说明](CONTRIBUTING.md)
