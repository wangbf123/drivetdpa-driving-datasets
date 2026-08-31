# 数据字典

## 公共标识字段

| 字段 | 含义 |
| --- | --- |
| `dataset_version` | 不可变的数据集发布版本 |
| `scene_id` | 一次 CARLA 场景实验 |
| `frame_id` | CARLA 仿真帧编号 |
| `timestamp_ns` | ROS/仿真纳秒时间戳 |
| `source` | 正式数据固定为 `carla` |

## 动态 BEV

坐标系以自车为中心，x 轴向右为正，y 轴向前为正，单位为米。目标字段包含类别、相对位置、距离、速度、车道关系和风险等级。占用栅格包含坐标系、分辨率、宽高和占用单元数量。当前风险值包括 `front_close`、`front_nearby`、`behind_close`、`nearby` 和 `low`。

## DriveTDPA 预测

输入关联相机路径、任务目标、Talk2BEV/BEV 场景上下文和自车状态。输出保留推理文本、3 个动作步骤、3 秒内恰好 6 个有限数值轨迹点、`parse_ok` 和模型延迟。该结果属于模型预测，不是 Ground Truth。

## 偏好对

候选来自同一个 CARLA 帧的多次 rollout。可审计字段包括预测内容、解析状态、奖励分量、总奖励、排名和 advantage。偏好对记录 chosen/rejected ID、奖励、排名、advantage 和差值。任何候选必须先通过安全检查才能被选中。

## 闭环结果

`t` 帧控制指令关联到 `t+1` 帧的车辆速度、位置、路线进度、碰撞、压线和轨迹跟踪误差。场景报告汇总路线完成率、碰撞率、舒适性、延迟和轨迹质量。
