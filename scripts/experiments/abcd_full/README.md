# DriveTDPA 实验 A–D 全量自动训练管线

对照《DriveTDPA 实验指导》"第二步：开环实验（NuScenes-TP）"的 A/B/C/D 四组实验，
在完整的 NuScenes trainval 数据集上自动完成 **数据切分 → 训练 → 评估 → 统计报告** 的
全流程。所有步骤可断点续跑（幂等），进程中断后重跑会自动跳过已完成的 checkpoint / eval。

## 脚本

| 脚本 | 作用 |
| --- | --- |
| `stage_data.py` | 构建 scene-disjoint + day/rain/night 标签的训练/held-out 切分，生成 SFT 与偏好（A2/A3/A4 surrogate）JSONL + meta.json |
| `train_one.sh` | 训练单个配置 × 单个 seed（A1 走 SFT；A2/A3/A4 从同 seed 的 A1 checkpoint 走 TPO 偏好训练） |
| `run_abcd_full.sh` | 总驱动：stage → train（12 个 checkpoint）→ eval（20 次）→ aggregate → report |
| `aggregate_results.py` | 汇总统计：mean±std、95% t 区间、day/rain/night 分组、Wilcoxon 配对检验、定性分析（C 的 R↔T 方向不一致、D 的场景引用率） |

## 运行

```bash
cd /mnt/workspace/autonomous_driving
SEEDS="42 17 23" MAX_STEPS=200 TRAIN_LIMIT=3000 \
HELDOUT_SCENES=9 HELDOUT_PER_SCENE=20 \
  bash scripts/experiments/abcd_full/run_abcd_full.sh
```

### 关键参数

| 参数 | 默认 | 含义 |
| --- | --- | --- |
| `SEEDS` | `42 17 23` | 训练 seed（A 类每个配置训 3 个 checkpoint） |
| `MAX_STEPS` | `200` | 每个 checkpoint 的训练步数 |
| `TRAIN_LIMIT` | `3000` | 训练样本上限（按场景均匀采样） |
| `HELDOUT_SCENES` / `HELDOUT_PER_SCENE` | `9` / `20` | held-out 场景数 / 每场景样本数 |
| `EVAL_MAX_NEW_TOKENS` | `1024` | 评估解码长度 |

## 输出（`/mnt/workspace/drivetdpa_experiments/abcd_full_20260930/`）

```text
data/            train_sft.jsonl / heldout.jsonl / A{2,3,4}_*.jsonl + meta + split_manifest.json
checkpoints/     <CONFIG>/seed<seed>/model.safetensors
eval/            <CONFIG>[/seed<seed>]/metrics.json + predictions.jsonl
report/          results_summary.json + ABCD_DATA_ANALYSIS.md
logs/            stage / train_* / eval_* / aggregate.log
```

## 设计说明（与 pilot 的差异 / 边界）

- **切分**：按 scene（850 场景）做 stratified 切分，held-out 9 个场景覆盖 day/night/rain 各 3，
  与训练场景 scene-disjoint（无泄漏）。pilot 只用 1 个 held-out scene。
- **规模**：训练 2523 样本 / 841 场景，held-out 180 样本；pilot 为 450/20。
- **A 类消融正确性**：A2/A3/A4 都从同 seed 的 A1（SFT）checkpoint 继续偏好训练，
  隔离"偏好优化阶段"的影响。
- **评估为 greedy**（`do_sample=False`），因此 seed 方差来自训练而非推理采样；
  A 类汇报跨 3 个训练 seed 的 mean±std 与 95% t 区间。
- **偏好数据为 surrogate**：A2/A3/A4 的 rejected 由本地脚本构造（物理不平滑 / 动作不一致 /
  弱场景证据），不是官方 reward rollout；论文需明确措辞。
- **语音为转写 proxy**：B2/B4 用文本转写代理，无音频编码器；论文需明确。
- **ADE 已修正**：评估器输出 `ADE_common`（两组合法样本）与 `ADE_worstcase`（解析失败罚 10m），
  parse 失败本身作为 `parse_success_rate` 报告，避免选择偏置。
- **已知边界**：`Unsup` 未计算（无 support ontology）、`TMC` 为 A→T 代理（R→A 仅在 think
  含显式方向意图时计分）、`R_to_A_consistency` 在无方向标注的样本上为 null。
