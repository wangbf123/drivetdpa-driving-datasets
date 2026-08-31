# DriveTDPA CARLA Driving Datasets

Public dataset portal for the CARLA-based DriveTDPA autonomous-driving pipeline. It connects synchronized simulator sensors, Autoware state, dynamic BEV context, Talk2BEV descriptions, DriveTDPA predictions, preference selection, control commands, and next-frame feedback into auditable scene records.

> Repository status: **schema and example release**. Records under `examples/` are format examples, not benchmark results or ground truth. Full CARLA captures will be published as versioned object-storage releases and indexed here.

## End-to-end pipeline

```text
CARLA camera / LiDAR / GNSS / IMU / vehicle state
  -> CARLA ROS Bridge
  -> Autoware localization / perception / map / route
  -> dynamic BEV
  -> Talk2BEV scene facts and description
  -> DriveTDPA reasoning / action / 3-second trajectory
  -> preference selector chooses a safe candidate
  -> Autoware planning and control
  -> CARLA vehicle actuation
  -> next CARLA frame and closed-loop metrics
```

All official records use `source: "carla"`. Preference pairs are generated from multiple DriveTDPA rollouts for the **same CARLA frame**, not unrelated prompts.

## What one frame contains

| Stage | Example artifact | Typical format |
| --- | --- | --- |
| CARLA sensors | Front RGB image, LiDAR scan, ego pose | JPG/PNG, PCD/BIN, JSON |
| ROS Bridge | Synchronized topics and TF | rosbag2 DB3/MCAP |
| Autoware | Objects, localization, route, trajectory, control | ROS 2 messages / JSON export |
| Dynamic BEV | Ego-centric objects, occupancy and lane relation | JSON, PNG |
| Talk2BEV | Structured facts and scene description | JSON/JSONL |
| DriveTDPA | Reasoning, 3-step action, 6-point trajectory, latency | JSON/JSONL |
| Preference selector | Candidates, scores, chosen and rejected trajectories | JSON/JSONL |
| Closed loop | Control at frame `t`, state and outcome at `t+1` | JSON/JSONL |

See [the data dictionary](docs/data_dictionary.md) and [the connected example scene](examples/scene_000001/manifest.json).

## Dataset releases

| Dataset | Contents | Status |
| --- | --- | --- |
| `dataset-carla-v0.1` | CARLA, Autoware, BEV, Talk2BEV and DriveTDPA frames | Planned |
| `dataset-carla-preference-v0.1` | Candidate groups and preference pairs from CARLA rollouts | Planned |
| `dataset-carla-closed-loop-v0.1` | Control-to-next-frame episodes and metrics | Planned |

`Planned` reserves a schema and release location; it does not claim that a full capture has been uploaded or validated.

## Repository layout

```text
docs/                 Architecture, collection protocol, fields and ROS topics
datasets/             Reserved release locations and storage conventions
manifests/            Machine-readable scene and artifact indexes
schemas/              JSON Schemas for validation
examples/             Small CARLA-format example scene
reports/              Experiment summaries, metrics and figures
scripts/              Validation, checksums and verified downloads
```

## Quick validation

Python 3.9+ is sufficient; the tools use only the standard library.

```bash
python scripts/validate_dataset.py examples/scene_000001/manifest.json
python scripts/generate_checksums.py examples/scene_000001
```

Download commands become active when a release manifest contains real HTTPS artifact URLs:

```bash
python scripts/download_dataset.py manifests/dataset-carla-v0.1.example.jsonl \
  --scene scene_000001 --output data
```

Placeholder URLs are rejected intentionally.

## Storage and access

GitHub stores documentation, schemas, compact examples, manifests, checksums, figures and reports. Large camera sequences, LiDAR, rosbag2 files, maps, videos and checkpoints belong in Alibaba Cloud OSS or a public dataset platform. Every published object must have a byte size and SHA256 digest in its manifest. See [storage and release policy](docs/storage_and_release.md).

## Data integrity and ground truth

- Simulator state, collision signals and configured CARLA routes may be labelled ground truth when provenance is retained.
- Model descriptions, reasoning, actions and trajectories are predictions, never ground truth.
- A preference judge must not receive reward, rank, future ground truth or chosen/rejected labels as input.
- Invalid, non-finite, colliding or out-of-bounds trajectories cannot be selected.
- Every frame uses stable `dataset_version`, `scene_id`, `frame_id` and CARLA timestamp identifiers.

## Documentation

- [Architecture](docs/architecture.md)
- [CARLA data collection](docs/data_collection.md)
- [Data dictionary](docs/data_dictionary.md)
- [ROS 2 topics](docs/ros_topics.md)
- [Storage and releases](docs/storage_and_release.md)
- [Contributing data](CONTRIBUTING.md)
