# Storage and Release

GitHub stores schemas, manifests, examples, release notes, metric tables, plots and tools. Do not commit bags, full image sequences, point clouds, videos, maps, checkpoints, credentials or private endpoints.

Use immutable object-storage prefixes and separate raw, derived and report artifacts:

```text
dataset-carla-v0.1/
  raw/scene_000001/
  derived/scene_000001/
  reports/
  checksums.sha256
```

Publish HTTPS URLs or documented `oss://` keys, never expiring signed URLs or URLs containing credentials. Every artifact records byte size, SHA256, media type, scene ID and relative path. Corrections receive a new version rather than silent replacement.
