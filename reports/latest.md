# 最新自动实验报告

更新时间：2026-09-01T23:24:13.539155+00:00

最新 run：[`carla_pref_20260901T232343Z_seed775000`](../experiments/runs/carla_pref_20260901T232343Z_seed775000/run_manifest.json)

```text
STATUS=PASS
SOURCE=carla
CANDIDATE_COUNT=4
ACCEPTED_CANDIDATES=4
PREFERENCE_PAIRS=3
FALLBACK_SAMPLES=0
JUDGE_CONFIDENCE=0.95
```

该 run 使用已录制 CARLA 相机/场景种子重新执行真实 DriveTDPA 多次采样、
安全门控、真实 VLM judge 和 TPO loader。它不是实时 CARLA 车辆闭环重跑。
官方 Talk2BEV entrypoint 与 NVIDIA GPU 渲染状态仍按 manifest 保持 BLOCKED。

当前共发布 664 个自动实验 run。机器可读索引见
[`experiments/index.jsonl`](../experiments/index.jsonl)。
