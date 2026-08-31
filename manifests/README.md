# 数据清单（Manifest）

每一行 JSONL 索引一个 CARLA 场景或场景级发布文件。正式条目统一使用 `source: "carla"`，数据集版本以 `dataset-carla` 开头。

索引至少记录 `dataset_version`、`scene_id`、`source`、`status`、文件 URI、字节数和 SHA256。场景 manifest 还需要保留 CARLA 配置、软件和模型版本、ROS Topic 以及关联记录路径。

当前 `*.example.jsonl` 故意使用占位符。只有当文件上传并完成校验后才能替换为真实值。URI 应使用不含凭据的 HTTPS 地址或稳定 OSS 对象路径，禁止提交签名 URL、AccessKey 和 Secret。
