# CARLA 偏好对数据集

正式版 `dataset-carla-preference-v0.1` 仍在规划中。当前已经开始发布
`dataset-carla-preference-experiment-v0.1` 预发布实验数据：每个候选组共享同一个
CARLA 场景、前视帧、任务目标和场景哈希，保留真实模型候选、解析与安全门控、真实
VLM judge、chosen/rejected、loader 审计和 SHA256。数据见
[`experiments/runs/`](../../experiments/runs/)，机器索引见
[`experiments/index.jsonl`](../../experiments/index.jsonl)。

预发布 run 使用已录制 CARLA 种子重新执行模型推理，不等同于完整实时车辆闭环。
官方 Talk2BEV entrypoint 和 NVIDIA GPU 渲染未通过时必须继续保持 BLOCKED。
