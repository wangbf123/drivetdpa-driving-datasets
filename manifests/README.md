# Dataset Manifests

Each JSONL line indexes one CARLA scene or one scene-level release artifact. All official entries use `source: "carla"` and a version beginning with `dataset-carla`.

Required index fields are `dataset_version`, `scene_id`, `source`, `status`, artifact URI, byte size and SHA256. Scene manifests additionally retain CARLA scenario settings, software/model versions, ROS topics and connected record paths.

The `*.example.jsonl` files deliberately contain placeholders. Replace them only after artifacts are uploaded and checksummed. Use credential-free HTTPS URLs or stable OSS object keys; never commit signed URLs, access keys or secrets.
