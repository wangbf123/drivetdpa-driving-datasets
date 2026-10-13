# DriveTDPA A–D 开环消融实验（NuScenes，全量 pipeline）

> `run_id`: `drivetdpa_abcd_nuscenes_20260930` · 状态：**PASS** · source：`nuscenes`（v1.0-trainval）

这是 DriveTDPA 在 NuScenes 上按《实验指导》"第二步：开环实验（NuScenes-TP）"运行的 **A/B/C/D 四组消融** 完整数据。对比 2026-09-24 的单场景 pilot，本 run 使用 **scene-disjoint 全量切分**（训练 2523 样本 / 841 场景，held-out 180 样本 / 9 场景，day·night·rain 各 3）。

## 一句话结论

模型学会了 RAT 协议的**格式**与"前进"意图（parse≈1.0、Goal≈0.9、A→T=1.0），但发生了**行为类别塌缩**：整类丢弃转向动作（20 个 eval 输出 `VEER` **0 次**）、几乎从不刹车/停车；**主导误差是纵向（不会停车）而非横向（不会转弯）**。A 类 surrogate 偏好优化（A2/A3/A4）相对 SFT（A1）在场景感知统计下**无显著差异**。详见 [`reports/abcd_final/ANALYSIS_REPORT.md`](../../../reports/abcd_final/ANALYSIS_REPORT.md)。

## 目录结构

```text
experiment_matrix.json   12 配置 × 关键指标（机器可读，含 seed 信息）
metrics/                 20 份 metrics.json（A 类每 seed 一份；B/C/D 单份）
predictions/             20 份 predictions.jsonl（每条含 think/actions/trajectory/raw_text + 逐样本指标）
heldout/                 heldout.jsonl（180 条评估输入）+ split_manifest + 各 meta.json
SHA256SUMS               上述全部文件的 SHA256 校验和
```

## 实验配置

| 组 | 配置 | 含义 | 训练 |
|---|---|---|---|
| A（偏好消融） | `A1_SFT` | SFT 基线 | 200 步 lr1e-5 |
| | `A2_physics` | SFT + 物理约束偏好（surrogate） | 从 A1 同 seed 继续 200 步 lr1e-6 |
| | `A3_jpo` | SFT + 联合偏好（surrogate） | 同上 |
| | `A4_vldpo` | SFT + VL-DPO 偏好（surrogate） | 同上 |
| B（输入模态） | `B1 image+text` / `B2 image+speech` / `B3 +BEV` / `B4 speech+BEV` | 去/加 BEV、语音转写代理 | 用 A4 seed42 checkpoint |
| C（动作层） | `C1 R→T` / `C2 R→A→T` | 去掉 / 保留 Action 层 | 用 A4 seed42 checkpoint |
| D（Talk2BEV） | `D1 no` / `D2 yes` | 去/加 Talk2BEV 场景描述 | 用 A4 seed42 checkpoint |

- A 类每个配置训练 3 个 seed（42/17/23），`metrics/` 与 `predictions/` 用 `_seed<id>` 区分。
- B/C/D 为单 checkpoint 协议消融，不带 seed 后缀，共用 A4 `seed42` 参考 checkpoint。

## 指标说明

`ADE_m`/`FDE_m`（米，越小越好）、`Goal`（前向奖励，越大越好）、`parse_success_rate`（六点轨迹解析成功率）、`A_to_T_consistency`（动作→轨迹一致）、`scene_reference_rate`（场景引用）、`Lat_ms_mean`（延迟）。完整定义见 `metrics/*.json` 的 `metric_notes`，汇总统计见 `reports/abcd_final/results_summary.json`。

## 已知边界（论文必须声明）

- 偏好对为 **surrogate**（本地构造 rejected，非真实 reward rollout）。
- 语音为**转写 proxy**，无真实音频编码器。
- 评估为 **greedy**（`do_sample=False`），A 类方差仅来自训练 seed。
- 训练 **200 步 / 1B** 模型，结论是"该预算下的塌缩"。
- held-out 仅 **9 场景**（每类 3），适合方向性消融，不适合绝对性能声明。
- 动作标签为**启发式伪标签** → "不输出 VEER" 是相对该伪标签的结论。

> ⚠️ `metrics/*.json` 内 `limits` 字段是评估器沿用的单场景 pilot 样板文字（"single scene pilot / not a final paper result"），**与本 run 的 9 场景 scene-disjoint 切分不符**，属已知陈旧文案；实际切分以 `heldout/split_manifest.json` 与 `experiment_matrix.json` 的 `split` 为准。

## 复现

数据由以下脚本产出（`scripts/experiments/abcd_full/`）：

```bash
cd /mnt/workspace/autonomous_driving
SEEDS="42 17 23" MAX_STEPS=200 TRAIN_LIMIT=3000 \
HELDOUT_SCENES=9 HELDOUT_PER_SCENE=20 \
  bash scripts/experiments/abcd_full/run_abcd_full.sh
```

> `heldout/heldout.jsonl` 中的 `image` 字段为本地/OSS 绝对路径，图像本身不在本仓库。
