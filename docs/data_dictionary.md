# Data Dictionary

## Common identifiers

| Field | Meaning |
| --- | --- |
| `dataset_version` | Immutable release identifier |
| `scene_id` | One CARLA episode |
| `frame_id` | CARLA frame number as a string |
| `timestamp_ns` | ROS/simulation time in nanoseconds |
| `source` | Always `carla` for official records |

## Dynamic BEV

Coordinates are ego-centric: x right-positive, y forward-positive, meters. Objects include class, relative position, distance, speed, lane relation and risk. Occupancy metadata includes frame, resolution, dimensions and occupied-cell count. Risk labels include `front_close`, `front_nearby`, `behind_close`, `nearby` and `low`.

## DriveTDPA prediction

Input links images, mission goal, Talk2BEV/BEV context and ego state. Output retains reasoning, 3 action steps, exactly 6 finite trajectory points over 3 seconds, `parse_ok` and latency. It is a prediction, not ground truth.

## Preference pair

Candidates come from repeated rollouts for the same CARLA frame. Auditable fields include prediction, parse status, reward components, total, rank and advantage. A pair stores chosen/rejected IDs, rewards, ranks, advantages and margin. Safety validation precedes selection.

## Closed-loop outcome

Control at frame `t` links to speed/pose, route progress, collision, lane invasion and tracking error at `t+1`. Reports aggregate route completion, collision rate, comfort, latency and trajectory quality.
