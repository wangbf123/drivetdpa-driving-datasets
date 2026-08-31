# DriveTDPA Driving Datasets

Datasets and experiment artifacts for the DriveTDPA autonomous-driving pipeline.

The pipeline is:

```text
CARLA sensors -> ROS Bridge -> Autoware -> dynamic BEV -> Talk2BEV
-> DriveTDPA -> preference selector -> Autoware control -> CARLA feedback
```

This repository is the public index for data, examples, schemas, metrics, and reproducibility material. Large raw files are stored in object storage or a dataset platform; this repository stores their version, location, checksum, and documentation.

## Dataset versions

| Version | Source | Purpose | Status |
| --- | --- | --- | --- |
| `dataset-sil-v0.1` | Software-in-the-loop | No-CARLA pipeline validation | Planned |
| `dataset-carla-v0.1` | CARLA | Sensor-to-control closed-loop evaluation | Planned |
| `dataset-preference-v0.1` | Rollouts | Chosen/rejected trajectory pairs | Planned |

Each released dataset version has a JSONL manifest in [`manifests/`](manifests/), a SHA256 checksum for every downloadable artifact, and a record of the source, code version, model version, and configuration version.

## Data collected per scene

| Pipeline stage | Example data |
| --- | --- |
| CARLA | Front camera image, LiDAR point cloud, ego pose and speed |
| ROS Bridge | Timestamped ROS 2 topics and TF transforms |
| Autoware | Localization, detected objects, route, planned trajectory, control command |
| Dynamic BEV | Lanes, route, ego vehicle, objects, occupancy, traffic-light state |
| Talk2BEV | Structured scene facts and natural-language scene description |
| DriveTDPA | Reasoning, action, predicted 3-second trajectory, latency |
| Preference selector | Candidate trajectories, scores, chosen and rejected trajectories |
| Closed-loop result | Control command at `t`, ego state and scene context at `t+1` |

The record format is documented in [`schemas/`](schemas/). A compact example is in [`examples/scene_000001/`](examples/scene_000001/).

## Storage policy

| Content | Location |
| --- | --- |
| Source code, schemas, manifests, reports, examples | This GitHub repository |
| Full camera/LiDAR sequences, ROS 2 bags, large maps, videos | Object storage |
| Model checkpoints and training datasets | Object storage or a model/dataset platform |

Do not commit API keys, access keys, private endpoints, credentials, full raw sensor dumps, or model checkpoints to this repository.

## Downloading a released scene

When a manifest contains a real artifact URL, download and verify it with:

```bash
bash scripts/download_dataset.sh \
  --manifest manifests/dataset-carla-v0.1.jsonl \
  --scene scene_000001 \
  --output ./data
```

The example manifest contains placeholders only. It is not a downloadable dataset release.

## Repository layout

```text
manifests/   Dataset and artifact indexes
schemas/     JSON schemas and field definitions
examples/    Small, non-sensitive example records
reports/     Metrics, figures, and release notes
scripts/     Download and integrity-check utilities
```

## Data provenance

Every scene must declare one of the following sources:

```text
sil     Software-in-the-loop data, without real-time CARLA execution
carla   CARLA simulation data
real    Data captured from a real vehicle or public real-world dataset
```

Predicted trajectories must not be labelled as ground truth. Preference judges must not receive ground-truth labels, rewards, or ranking fields as input.
