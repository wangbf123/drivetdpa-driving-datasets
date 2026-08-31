# Architecture

The dataset is organized around CARLA scenes and timestamped frames. A scene is one reproducible episode with a CARLA town, route, weather, traffic seed, sensor suite, Autoware configuration and model versions.

## Identity and synchronization

- `scene_id` identifies an episode.
- `frame_id` identifies a CARLA simulation frame.
- `timestamp_ns` is the ROS/simulation timestamp in nanoseconds.
- Every BEV, description, prediction, preference decision and control result retains these identifiers.
- Control at frame `t` links to ego state, events and route progress at frame `t+1`.

## Processing layers

1. CARLA produces sensor observations and authoritative simulator state.
2. CARLA ROS Bridge publishes synchronized ROS 2 messages.
3. Autoware provides localization, perception, map, route, planning and control state.
4. Dynamic BEV converts the scene into ego-centric structured context.
5. Talk2BEV produces auditable scene facts and a textual description.
6. DriveTDPA predicts reasoning, a 3-step action and a 3-second trajectory with 6 points.
7. The preference selector compares candidates from the same input and selects a valid trajectory.
8. Autoware/CARLA execute control and produce the next-frame outcome.

Raw references and compact derived records are retained so every result is traceable to its CARLA frame.
