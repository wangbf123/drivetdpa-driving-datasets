# A–G 实验最终数据

[项目首页](../../README.md) · [最终数据与报告总入口](../../FINAL_RESULTS.md) · [开环 / 闭环动态图解](../../docs/experiment_flows_zh.md)

本目录按「实验 A–G」**一个实验一个目录**，汇总全实验矩阵的最终结果数据：

- **A–D**：NuScenes 开环消融（最终版 `abcd_full_20260930`，全量 scene-disjoint，180 held-out，A 组 3 seeds）。
- **E / F / G**：CARLA 实时闭环（语音指令 / 环境鲁棒性 / Talk2BEV 场景理解）。

权威分析报告见 [`reports/abcd_final/`](../../reports/abcd_final/) 与 [`reports/efg_final/`](../../reports/efg_final/)。

## 状态矩阵

| 实验 | 含义 | 状态 | 数据目录 |
|---|---|---|---|
| A | 偏好优化消融（A1_SFT / A2_physics / A3_jpo / A4_vldpo） | ✅ PASS | [`A/`](./A/) |
| B | 模态消融（B1 图像+文本 … B4 图像+语音+BEV） | ⚠️ B1/B2 PARTIAL，B3/B4 PASS | [`B/`](./B/) |
| C | 动作层消融（C1 R→T / C2 R→A→T） | ✅ PASS | [`C/`](./C/) |
| D | Talk2BEV 消融（D1 无 / D2 有） | ⚠️ D1 PARTIAL，D2 PASS | [`D/`](./D/) |
| E | 语音指令闭环（5 类指令 × 10 trial） | ✅ PASS 50/50 | [`E/`](./E/) |
| F | 环境鲁棒性闭环（5 场景 × 5 指令） | ✅ PASS 25/25 | [`F/`](./F/) |
| G | Talk2BEV 场景理解（真实 InternVL，54 条） | ✅ PASS 54/54 | [`G/`](./G/) |

## 目录结构

- `A/`：每个子实验含 `seed17/ seed23/ seed42/` 三个 seed 的 `metrics.json`（ADE/FDE 等）与 `predictions.jsonl`（模型输出）。
- `B/`–`D/`：每个子实验含 `metrics.json` + `predictions.jsonl`。
- `E/`：`experiment_e_results.csv` + `experiment_e_summary.json`（5 指令 × 10 trial）。
- `F/`：`experiment_f_results.csv` + `experiment_f_summary.json`（5 场景 × 5 指令）。
- `G/`：`summary.json` + `audit/`（54 条场景理解审计 + 时间线）+ `g_bag/metadata.yaml` + 运行日志。

## 诚实边界（一句话）

E/F/G 证明的是「闭环系统端到端可执行、执行幅度可重复、对天气稳健、真实模型能理解场景」；它们**不证明**任何单组件的消融贡献，也**不证明**模型轨迹规划质量。A–D 观察到的「行为塌缩」（几乎不转弯、不刹车）须与 E/F/G 的「闭环 100% 成功」**合并**陈述，才能给出诚实、完整的论文叙事。详见 [`reports/efg_final/EFG_ANALYSIS_REPORT.md`](../../reports/efg_final/EFG_ANALYSIS_REPORT.md) §6 与 [`reports/abcd_final/ANALYSIS_REPORT.md`](../../reports/abcd_final/ANALYSIS_REPORT.md)。

## 数据来源

| 组 | 来源 |
|---|---|
| A–D | `drivetdpa_experiments/abcd_full_20260930/eval/`（全量 scene-disjoint 最终版） |
| E | `autonomous_driving/results/experiment_e/` |
| F | `drivetdpa_experiments/runs/F_env_run2/` |
| G | `drivetdpa_experiments/runs/G_talk2bev_env_20261021/` |
