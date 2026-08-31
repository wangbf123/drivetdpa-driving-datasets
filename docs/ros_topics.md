# ROS 2 Topics

| Topic | Role |
| --- | --- |
| `/clock` | CARLA simulation clock |
| `/tf`, `/tf_static` | Frame transforms |
| `/localization/kinematic_state` | Ego localization and motion |
| `/perception/object_recognition/objects` | Detected objects |
| `/perception/object_recognition/tracking/objects` | Tracked objects |
| `/perception/occupancy_grid_map/map` | Occupancy grid |
| `/map/vector_map` | Lanelet vector map |
| `/planning/scenario_planning/trajectory` | Autoware trajectory |
| `/control/command/control_cmd` | Vehicle control command |
| `/control/command/actuation_cmd` | Actuator command |
| `/vehicle/status/velocity_status` | Velocity feedback |
| `/drivetdpa/bev_context` | Dynamic BEV ROS message |
| `/drivetdpa/bev_context_json` | Dynamic BEV JSON |
| `/drivetdpa/prediction_json` | DriveTDPA prediction |
| `/drivetdpa/trajectory` | DriveTDPA Autoware trajectory |

CARLA sensor topics depend on the ROS Bridge configuration and must be enumerated in each scene manifest.
