# 自动化实验数据

`runs/` 保存可直接审阅的小型实验包，`index.jsonl` 是机器可读总索引。每个 run 来自
一个 SHA256 匹配的 CARLA 前视相机帧和 Talk2BEV-compatible 场景上下文，之后重新
执行真实 DriveTDPA 多 seed rollout、候选安全门控、真实 VLM judge 和当前 TPO
loader。

## 在采集服务器运行

自动实验脚本位于 DriveTDPA 主项目的 `scripts/experiments/`。单轮实验会依次执行
CARLA bag 种子提取、真实模型健康检查、多 seed rollout、安全门控、真实 VLM judge、
TPO loader 审计、manifest 生成、导入、Git commit 和 push：

```bash
cd /mnt/workspace/autonomous_driving
SEED_BASE=91000 \
PUBLISH_RESULTS=1 \
PUSH_RESULTS=1 \
bash scripts/experiments/run_carla_data_experiment.sh
```

持续采集默认每 30 分钟运行一轮，并递增 seed：

```bash
nohup env \
  INTERVAL_SECONDS=1800 \
  MAX_RUNS=0 \
  PUBLISH_RESULTS=1 \
  PUSH_RESULTS=1 \
  bash /mnt/workspace/autonomous_driving/scripts/experiments/run_continuous_carla_data.sh \
  >/mnt/workspace/drivetdpa_experiments/continuous.stdout.log 2>&1 &
echo $! >/mnt/workspace/drivetdpa_experiments/continuous.pid
```

创建 `/mnt/workspace/drivetdpa_experiments/STOP` 后，runner 会在当前轮结束时停止。
完整 rosbag 和模型权重只保留在采集服务器，不由该流程提交到 Git。
每轮数据通过后会先完成本地导入和 commit，再单独尝试 push。GitHub 凭据暂时不可用时
记录 `PUSH_BLOCKED` 并在下一轮重试，不会中止数据采集或把实验本身误标成失败。

已经完成且 `run_manifest.json` 为 `PASS` 的本机 run 也可手动导入：

```bash
python scripts/import_experiment.py \
  --source-run /mnt/workspace/drivetdpa_experiments/runs/<run_id> \
  --repository /mnt/workspace/drivetdpa-driving-datasets
python scripts/validate_experiment.py experiments/runs
```

## 验证全部 run

```bash
python scripts/validate_experiment.py experiments/runs
```

验证器检查每个文件的大小和 SHA256、CARLA 图片来源、`mock=false` 模型身份、
`real_judge_evidence=true`、零 fallback、chosen/rejected 非空且不同，以及 loader
结果。任何一项不满足都会非零退出。

## 单个 run 目录

```text
carla_front.png          小型 CARLA 前视图
scene_context.json       Talk2BEV-compatible LVLM + structured BEV 场景上下文
source_manifest.json     rosbag topic、消息时间和源文件 SHA256
model_health.json        真实模型身份
rollout_group.jsonl      同一输入的多 seed 候选
preference_pairs.jsonl   chosen/rejected 训练记录
preference_audit.jsonl   judge、门控和 fallback 审计
preference_stats.json    汇总指标
loader_audit.json        当前 TPO loader 实际读取结果
run_manifest.json        本 run 状态、范围和全部文件 SHA256
```

当前 run 使用已录制 CARLA 数据作为种子，每轮模型推理是新的，但不是实时车辆闭环
重跑。完整 rosbag 不进入 Git；其哈希保留在 `source_manifest.json`，后续可迁移到对象
存储。
