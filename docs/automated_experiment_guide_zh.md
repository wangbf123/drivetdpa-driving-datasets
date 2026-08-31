# DriveTDPA 自动实验运行手册

本文说明如何在采集服务器启动、观察、停止和验证 DriveTDPA CARLA 偏好数据实验。
当前自动流程使用已经审计的 CARLA rosbag 作为场景种子，每轮重新执行真实模型推理，
不要求实时 CARLA 保持在线。

## 路径和前提

默认路径：

```text
主项目        /mnt/workspace/autonomous_driving
本机实验数据  /mnt/workspace/drivetdpa_experiments
公开数据仓库  /mnt/workspace/drivetdpa-driving-datasets
模型接口      http://127.0.0.1:18000
```

先确认模型接口来自真实 checkpoint：

```bash
curl --fail --silent --show-error http://127.0.0.1:18000/health
```

返回值必须同时包含 `"ok": true`、`"mock": false` 和非空的
`model_identity.model_path`。如果接口没有运行，可执行：

```bash
cd /mnt/workspace/autonomous_driving

setsid -f /usr/local/bin/python3 \
  internvl_chat_gpt_oss/tools/drivetdpa_predict_server.py \
  --host 127.0.0.1 \
  --port 18000 \
  --model-path internvl_chat_gpt_oss/work_dirs/smoke_dpo_single_a10_20260620_161511 \
  --dtype bf16 \
  --max-new-tokens 256 \
  >/mnt/workspace/drivetdpa_experiments/model-server.log 2>&1
```

模型已经在线时不要重复启动同一端口的服务。

## 单轮实验

`SEED_BASE` 应使用尚未采用的采样 seed。执行一轮并自动导入、提交和推送：

```bash
cd /mnt/workspace/autonomous_driving

SEED_BASE=96000 \
PUBLISH_RESULTS=1 \
PUSH_RESULTS=1 \
bash scripts/experiments/run_carla_data_experiment.sh
```

命令最后输出 `PASS: /mnt/workspace/drivetdpa_experiments/runs/<run_id>` 才表示该轮
通过。任何阶段失败都会非零退出，并在 run 目录写入 `failure.json`，失败产物不会导入
公开仓库。

## 持续自动运行

先确认没有旧 runner：

```bash
pgrep -af '^bash scripts/experiments/run_continuous_carla_data.sh$' || true
```

下面的配置在每轮完成后等待 30 秒，持续运行并自动推送。DSW 环境使用独立 session，
避免启动终端退出后回收后台进程：

```bash
cd /mnt/workspace/autonomous_driving

setsid -f env \
  INTERVAL_SECONDS=30 \
  MAX_RUNS=0 \
  START_SEED=96000 \
  SEED_STRIDE=1000 \
  PUBLISH_RESULTS=1 \
  PUSH_RESULTS=1 \
  bash scripts/experiments/run_continuous_carla_data.sh \
  >/mnt/workspace/drivetdpa_experiments/continuous.stdout.log 2>&1

sleep 2
pgrep -f '^bash scripts/experiments/run_continuous_carla_data.sh$' \
  | tail -n 1 \
  >/mnt/workspace/drivetdpa_experiments/continuous.pid
```

主要参数：

| 参数 | 含义 |
| --- | --- |
| `INTERVAL_SECONDS` | 一轮完成后等待秒数；30 秒约可达到每小时 50 轮 |
| `MAX_RUNS` | 最大尝试轮数；0 表示持续运行 |
| `START_SEED` | 第一轮采样 seed |
| `SEED_STRIDE` | 每轮 seed 增量 |
| `PUBLISH_RESULTS` | 1 表示导入本地公开数据仓库并 commit |
| `PUSH_RESULTS` | 1 表示向 GitHub `main` 推送 |

每轮依次执行：

```text
CARLA rosbag 图片/场景哈希匹配
-> 真实模型多 seed rollout
-> 候选解析和安全门控
-> 真实 VLM judge
-> chosen/rejected 偏好对
-> 当前 TPO loader 实际读取
-> SHA256 manifest
-> 本地数据仓库导入和 commit
-> GitHub push
```

## 查看状态和日志

检查 runner：

```bash
runner_pid=$(cat /mnt/workspace/drivetdpa_experiments/continuous.pid)
ps -p "$runner_pid" -o pid,stat,etime,cmd
```

查看轮次状态：

```bash
tail -f /mnt/workspace/drivetdpa_experiments/continuous.log
```

正常发布的一轮依次出现 `PASS` 和 `PUSH_PASS`。`PUSH_BLOCKED` 表示实验和本地提交
已经完成，但 GitHub 暂时不可达或没有权限，runner 会在下一轮重试。查看单轮详细日志：

```bash
ls -lt /mnt/workspace/drivetdpa_experiments/logs | head
tail -f /mnt/workspace/drivetdpa_experiments/logs/<run_id>.log
```

## 停止和恢复

创建停止文件并结束当前等待，可让 runner 立即正常退出；已有数据不会删除：

```bash
touch /mnt/workspace/drivetdpa_experiments/STOP

runner_pid=$(cat /mnt/workspace/drivetdpa_experiments/continuous.pid)
pkill -TERM -P "$runner_pid" sleep 2>/dev/null || true
```

确认已经退出：

```bash
ps -p "$runner_pid" -o pid,stat,cmd
```

恢复时重新执行“持续自动运行”命令，并将 `START_SEED` 设置为上一次 seed 加
`SEED_STRIDE`。runner 启动时会清除旧的 `STOP` 文件。

## 验证和数据位置

本机完整 run：

```text
/mnt/workspace/drivetdpa_experiments/runs/<run_id>/
```

公开小型数据：

```text
/mnt/workspace/drivetdpa-driving-datasets/experiments/runs/<run_id>/
```

离线验证所有已发布 run：

```bash
cd /mnt/workspace/drivetdpa-driving-datasets
python scripts/validate_experiment.py experiments/runs
git status --short --branch
```

GitHub 页面：

```text
https://github.com/wangbf123/drivetdpa-driving-datasets/tree/main/experiments/runs
```

## 真实性边界

- 当前流程从已录制 CARLA bag 取种子；模型候选和偏好判断每轮都会重新推理。
- 重复不同 seed 会增加偏好样本，但不会增加道路场景多样性。
- 当前 run 不是本轮实时 CARLA 车辆闭环，也不是 Ground Truth。
- Talk2BEV-compatible LVLM 已执行；官方 Talk2BEV entrypoint 仍为
  `BLOCKED_NOT_EXECUTED`。
- 源 CARLA 仍为 lavapipe 软件渲染，GPU 渲染状态保持 `BLOCKED_LAVAPIPE`。
- 若要采集新道路场景，必须先恢复 CARLA SSH 隧道、RPC/streaming 端口和实时 ROS
  传感器消息，再录制新的可审计 rosbag。
