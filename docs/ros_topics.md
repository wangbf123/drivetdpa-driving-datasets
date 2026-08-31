# ROS 2 Topic 清单

| Topic | 作用 |
| --- | --- |
| `/clock` | CARLA 仿真时钟 |
| `/tf`、`/tf_static` | 坐标系变换 |
| `/localization/kinematic_state` | 自车定位和运动状态 |
| `/perception/object_recognition/objects` | 感知目标 |
| `/perception/object_recognition/tracking/objects` | 跟踪目标 |
| `/perception/occupancy_grid_map/map` | 占用栅格地图 |
| `/map/vector_map` | Lanelet 矢量地图 |
| `/planning/scenario_planning/trajectory` | Autoware 规划轨迹 |
| `/control/command/control_cmd` | 车辆控制指令 |
| `/control/command/actuation_cmd` | 执行器指令 |
| `/vehicle/status/velocity_status` | 车辆速度反馈 |
| `/drivetdpa/bev_context` | 动态 BEV ROS 消息 |
| `/drivetdpa/bev_context_json` | 动态 BEV JSON |
| `/drivetdpa/prediction_json` | DriveTDPA 预测结果 |
| `/drivetdpa/trajectory` | DriveTDPA 输出的 Autoware 轨迹 |

CARLA 相机、LiDAR、GNSS、IMU 和车辆状态 Topic 会随 CARLA ROS Bridge 传感器配置变化，因此每个场景必须在 manifest 中保存实际录制的完整 Topic 清单。
