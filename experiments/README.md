# 实验数据导航

[返回项目首页](../README.md) · [A–G 最终成果](../FINAL_RESULTS.md) · [报告导航](../reports/README.md) · [目录与时间线](../docs/project_guide_zh.md)

## 优先阅读：A–G 最终实验数据

**首选入口：[ag_final/ · 一个实验一个目录](ag_final/README.md)**。按组目录于 **2026-10-26** 发布；数据的实验日期与报告日期另行标注，不把目录发布日当作重新运行实验的日期。

| 实验 | 已发布数据 | 对应最终报告 | 数据范围 |
| --- | --- | --- | --- |
| **A–D · NuScenes 开环** | [A](ag_final/A/) · [B](ag_final/B/) · [C](ag_final/C/) · [D](ag_final/D/)：共 20 份指标与 20 份预测；[旧最终包](runs/drivetdpa_abcd_nuscenes_20260930/)继续提供 held-out 与 SHA256 | [A–D 最终主报告](../reports/abcd_final/ANALYSIS_REPORT.md) | 2026-09-30 全量结果；图像、完整原始 NuScenes 和 checkpoint 不在仓库 |
| **E · 语音指令执行** | [50 次 trial CSV](ag_final/E/experiment_e_results.csv) · [summary](ag_final/E/experiment_e_summary.json) | [E–G 最终主报告](../reports/efg_final/EFG_ANALYSIS_REPORT.md) | 已发布逐条指令、success、起点 / 峰值 / 末端速度、转角变化 |
| **F · 环境鲁棒性** | [25 次 trial CSV](ag_final/F/experiment_f_results.csv) · [summary](ag_final/F/experiment_f_summary.json) | [E–G 最终主报告](../reports/efg_final/EFG_ANALYSIS_REPORT.md) | 已发布逐场景 / 指令结果与动作幅度；晴空基线有跨 trial 状态残留 |
| **G · 场景理解审计** | [54 条消息时间线](ag_final/G/audit/lvlm_scene_context_timeline.jsonl) · [audit](ag_final/G/audit/lvlm_scene_context_audit.json) · [summary / 日志 / bag metadata](ag_final/G/) | [E–G 最终主报告](../reports/efg_final/EFG_ANALYSIS_REPORT.md) | 已发布消息内容与 hash / 身份审计；只有 bag 元信息，未发布其引用的 `.db3` |

> E/F/G 数据在 `ag_final/E`、`F`、`G`，汇总分析在 `reports/efg_final/`。`runs/carla_pref_*` 是历史 recorded-seed 偏好实验，不应混作 E/F/G 实时闭环数据。完整图像、权重和完整 rosbag 并未全部入库，服务器来源见[实验矩阵](../docs/experiment_matrix_zh.md)。

## 按时间查找版本

以下区分**数据目录发布日期、实验记录日期与报告定稿日期**，按可识别日期倒序排列；完整时间线见[项目时间线](../docs/project_guide_zh.md)。

| 时间 / 阶段 | 入口 | 中文说明 | 阅读建议 |
| --- | --- | --- | --- |
| **2026-10-26 · A–G 按组数据发布** | **[ag_final/](ag_final/README.md)** | A–D 分组指标与预测；E/F 逐次 CSV 与 summary；G timeline / audit / summary / 日志 / bag metadata | **按实验组找数据先看这里**；不代表当天重新运行实验 |
| 2026-10-25 · E–G 报告发布 | [最终报告与汇总](../reports/efg_final/) | G 源目录含 `20261021`，E/F 未单独标精确实验日期 | 结合新入库逐次数据阅读；不据 G 目录名推定 E/F 时间 |
| 2026-10-13 · A–D 报告更新与全量包发布 | [A–D 最终报告](../reports/abcd_final/README.md) | 对 09-30 全量结果进行最终整理与统计解释 | 结论引用场景感知统计后的主报告 |
| **2026-09-30 · A–D final 数据记录** | [`drivetdpa_abcd_nuscenes_20260930`](runs/drivetdpa_abcd_nuscenes_20260930/) | scene-disjoint 全量切分：训练 2523 样本 / 841 场景；held-out 180 样本 / 9 场景 | 查 held-out、切分与 SHA256 时使用 |
| 2026-09-24 · A–D pilot | [`drivetdpa_abcd_nuscenes_20260924`](runs/drivetdpa_abcd_nuscenes_20260924/) | 450 训练样本、20 评估样本、单评估场景 | 用于了解早期试验，不替代 final |
| 2026-09-15 · 阻塞快照 | [`blocked_runs/`](blocked_runs/) | 15 个 A–G 配置包，记录当时缺少真实可审计输出的原因，manifest 为 `BLOCKED` | 历史记录，不是成功结果；[状态解释](../docs/experiment_matrix_zh.md) |
| 2026-08-31—09-02 · CARLA 历史偏好实验 | [`runs/carla_pref_*`](runs/) · [机器索引](index.jsonl) | 995 个已录制 CARLA 种子上的真实模型多采样、judge 与 loader 审计包 | 与 A–G 开环 / 实时闭环成果分开查阅 |

## 如何浏览 A–G 分组目录

```text
ag_final/
├── A/   偏好优化：A1–A4，各 seed17 / seed23 / seed42
├── B/   模态消融：B1–B4，各 metrics.json + predictions.jsonl
├── C/   动作层消融：C1–C2，各 metrics.json + predictions.jsonl
├── D/   Talk2BEV 消融：D1–D2，各 metrics.json + predictions.jsonl
├── E/   50 次指令 trial CSV + summary
├── F/   25 次环境 / 指令 trial CSV + summary
└── G/   54 条消息 timeline、audit、summary、日志、bag metadata
```

E/F CSV 可直接按 `command` 或 `scene` 查看执行与速度 / 转角；G 时间线包含描述、模型身份和输入 / 输出 hash。[G 审计 JSON](ag_final/G/audit/lvlm_scene_context_audit.json)记录了源 bag 和时间线的 hash。`g_bag/metadata.yaml` 只描述 bag 结构，其引用的 `g_bag_0.db3` 未发布，不能用元信息文件代替完整 bag 回放。

## 原 A–D 最终发布包：切分与校验入口

原 `runs/drivetdpa_abcd_nuscenes_20260930/` 路径保留，便于按既有报告引用追溯与校验。按组查看指标优先使用上方 `ag_final/`，核对切分与 SHA256 使用下表。

| 文件 / 子目录 | 中文说明 |
| --- | --- |
| [README](runs/drivetdpa_abcd_nuscenes_20260930/README.md) | 实验设计、配置、规模和已知边界 |
| [experiment_matrix.json](runs/drivetdpa_abcd_nuscenes_20260930/experiment_matrix.json) | 12 个配置的机器可读指标矩阵 |
| [metrics/](runs/drivetdpa_abcd_nuscenes_20260930/metrics/) | 原始发布包指标；A 类按 seed 区分，B/C/D 各配置一份 |
| [predictions/](runs/drivetdpa_abcd_nuscenes_20260930/predictions/) | 原始发布包逐样本 think、actions、trajectory、raw_text 及指标 |
| [heldout/](runs/drivetdpa_abcd_nuscenes_20260930/heldout/) | held-out 输入、scene-disjoint 切分清单和元数据；图像本身不在仓库 |
| [SHA256SUMS](runs/drivetdpa_abcd_nuscenes_20260930/SHA256SUMS) | **该原发布包**内文件的完整性校验和，不扩展声明为覆盖整个 ag_final |

## 本地校验

在仓库根目录执行。工具仅需 Python 3.9+ 标准库；NuScenes 的文件完整性使用 `sha256sum` 检查。

**CARLA 历史实验包：**

```bash
python scripts/validate_experiment.py experiments/runs/carla_pref_*
```

验证器检查文件大小与 SHA256、CARLA 图片来源、`mock=false` 模型身份、真实 judge、零 fallback、非空且不同的 chosen/rejected，以及 loader 结果。

**两份 NuScenes 数据包：**

```bash
(cd experiments/runs/drivetdpa_abcd_nuscenes_20260930 && sha256sum --check SHA256SUMS)
(cd experiments/runs/drivetdpa_abcd_nuscenes_20260924 && sha256sum --check SHA256SUMS)
```

SHA256 通过表示对应原发布包的文件与其清单一致，不代表重新运行训练或验证科学结论；该清单不是整个 `ag_final/` 的统一校验清单。

> 当前 `validate_experiment.py experiments/runs` 会把 NuScenes 汇总清单当作 CARLA artifact 清单解析，触发 `AttributeError`；它**不会自动跳过 NuScenes**。请使用上面的分类型命令。E/F 逐次 CSV 和 G timeline / audit 可直接查看与复核已发布字段；完整图像、权重和 bag `.db3` 不在仓库，仍不能仅靠这些文件重新执行完整模型推理与仿真。

## CARLA 历史偏好包的目录说明

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

## 在采集服务器运行

完整采集依赖仓库之外的 DriveTDPA 主项目、模型 checkpoint、CARLA 种子数据及相应服务。下列 `/mnt/workspace/` 路径是原采集服务器示例，不是当前仓库自带环境；发布与推送选项会写入远程仓库，应由维护者按需启用。

<details>
<summary>展开原有单轮、持续采集与导入说明</summary>

自动实验脚本位于 DriveTDPA 主项目的 `scripts/experiments/`。单轮实验会依次执行
CARLA bag 种子提取、真实模型健康检查、多 seed rollout、安全门控、真实 VLM judge、
TPO loader 审计、manifest 生成、导入、Git commit 和 push：

完整的模型启动、单轮和持续运行、状态检查、停止、恢复及故障判断命令见
[《DriveTDPA 自动实验运行手册》](../docs/automated_experiment_guide_zh.md)。

```bash
cd /mnt/workspace/autonomous_driving
SEED_BASE=91000 \
PUBLISH_RESULTS=1 \
PUSH_RESULTS=1 \
bash scripts/experiments/run_carla_data_experiment.sh
```

持续采集示例在每轮完成后等待 30 秒，并递增 seed：

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

创建 `/mnt/workspace/drivetdpa_experiments/STOP` 后，runner 会在当前轮结束时停止；完整
的立即停止命令见运行手册。
完整 rosbag 和模型权重只保留在采集服务器，不由该流程提交到 Git。
每轮数据通过后会先完成本地导入和 commit，再单独尝试 push。GitHub 凭据暂时不可用时
记录 `PUSH_BLOCKED` 并在下一轮重试，不会中止数据采集或把实验本身误标成失败。

已经完成且 `run_manifest.json` 为 `PASS` 的本机 run 也可手动导入：

```bash
cd /mnt/workspace/drivetdpa-driving-datasets
python scripts/import_experiment.py \
  --source-run /mnt/workspace/drivetdpa_experiments/runs/<run_id> \
  --repository /mnt/workspace/drivetdpa-driving-datasets
python scripts/validate_experiment.py experiments/runs/carla_pref_*
```

</details>
