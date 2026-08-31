# Dataset manifests

One JSON object is stored per line. A release manifest lists the scene metadata and every artifact needed to retrieve or reproduce that scene.

Required fields:

```text
dataset_version, scene_id, source, duration_sec, created_at,
code_commit, model_version, config_version, artifacts
```

Each artifact must include `kind`, `uri`, `bytes`, and `sha256`. Use an HTTPS URL, OSS URI, or a documented dataset-platform URI. Never place credentials in a `uri`.
