# DriveTDPA 实验数据字典（中文）

本文件是所有实验表格的唯一字段来源。数据包没有真实输出时必须标记 `BLOCKED`，不能用空值或模拟值冒充实验结果。

| 文件/字段 | 中文含义 | 来源 | 允许状态/单位 |
|---|---|---|---|
| `manifest.json.status` | 实验整体状态 | 实验运行器和验收脚本 | `PASS/BLOCKED/FAIL` |
| `dataset` | 数据集名称、版本、路径 | 数据集挂载和运行配置 | 文本 |
| `model_checkpoint` | 模型权重目录或版本 | 模型服务启动参数 | 路径/commit |
| `predictions.jsonl` | 每帧模型 RAT 输出 | DriveTDPA 推理服务 | 一行一帧 |
| `events.jsonl` | 输入、输出、错误和状态事件 | ROS2/模型/实验运行器日志 | JSONL |
| `ADE` | 预测轨迹平均位移误差 | 预测轨迹与标注轨迹 | 米，越低越好 |
| `FDE` | 最后预测点位移误差 | 预测轨迹与标注轨迹 | 米，越低越好 |
| `Goal` | mission goal 完成率/误差 | 目标解析与轨迹终点 | 率或米 |
| `R_A_consistency` | 推理与动作一致率 | RAT 解析器 | 0–1 |
| `A_T_consistency` | 动作与轨迹方向一致率 | RAT 解析器和轨迹 | 0–1 |
| `TMC` | 三模态一致性宏平均 | R/A/T 三项一致性 | 0–1 |
| `collision_rate` | 碰撞率 | CARLA/Autoware 事件 | 率 |
| `offroad_rate` | 越界率 | 车辆轨迹和地图 | 率 |
| `TTC_p05` | 最小 5% 分位碰撞时间 | 车辆状态/障碍物 | 秒 |
| `latency_p50/p95/p99` | 推理端到端延迟分位数 | 时间戳事件 | 毫秒 |
| `voice_asr_accuracy` | 语音识别正确率 | WAV 与人工参考文本 | 率 |
| `mission_goal_success` | 语音目标执行成功率 | mission_goal 与车辆状态 | 率 |
| `talk2bev_entity_precision/recall` | 场景实体准确率/召回率 | BEV 真值与 Talk2BEV 输出 | 率 |
| `talk2bev_hallucination_rate` | 场景幻觉率 | BEV 真值核对 | 率 |

## 表格来源约定

- `metrics.json`：机器可读最终指标；没有真实样本时只能是 `BLOCKED`。
- `predictions.jsonl`：DriveTDPA 原始模型输出，不放手工改写结果。
- `events.jsonl`：ROS2 topic、ASR、BEV、车辆状态和错误事件。
- `manifest.json`：实验配置、数据版本、checkpoint、commit、随机种子和硬件环境。
- `checksums.sha256`：实验包内所有文件的 SHA256，来源是本次运行产生的原始文件。
- `screenshots/`：仅保存真实 RViz/CARLA 截图；没有闭环运行时保持空目录并在 manifest 写明原因。
