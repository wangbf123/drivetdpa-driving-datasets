# A–G FINAL · 最终实验数据与报告

[返回首页](README.md) · [开环 / 闭环动态图解](docs/experiment_flows_zh.md) · [中文目录与时间线](docs/project_guide_zh.md) · [报告索引](reports/README.md) · [实验数据索引](experiments/README.md)

> **最终成果总入口**：先选实验组，再查看数据与对应报告。**[A–G 按实验分组的最终数据](experiments/ag_final/README.md)** 已于 2026-10-26 入库整理，含 E/F 逐次 CSV 与 G 审计时间线。A–D 最终报告更新于 **2026-10-13**；E–G 最终报告发布于 **2026-10-25**。时间线与历史版本见[中文指南](docs/project_guide_zh.md#timeline)。

**[A–D 最终数据](#abcd-data)** · **[E–G 最终汇总](#efg-data)** · **[最终报告](#final-reports)** · **[原始材料范围](#source-data)**

## 01 · A–G 实验对应关系

| 组别 | 实验问题 | 最终数据入口 | 最终报告 |
| --- | --- | --- | --- |
| **A · 偏好优化** | SFT、Physics、JPO、VL-DPO 如何影响轨迹？ | [A 组数据](experiments/ag_final/A/)：A1–A4 各 3 seed 的指标与预测 | [A–D 主报告](reports/abcd_final/ANALYSIS_REPORT.md) |
| **B · 输入模态** | 图像、文本/语音转写代理与 BEV 有何作用？ | [B 组数据](experiments/ag_final/B/)：B1–B4 指标与预测 | [A–D 主报告](reports/abcd_final/ANALYSIS_REPORT.md) |
| **C · 动作层** | R→T 与 R→A→T 如何影响轨迹？ | [C 组数据](experiments/ag_final/C/)：C1–C2 指标与预测 | [A–D 主报告](reports/abcd_final/ANALYSIS_REPORT.md) |
| **D · Talk2BEV 消融** | 去掉场景描述后，精度和输出合规性如何变化？ | [D 组数据](experiments/ag_final/D/)：D1–D2 指标与预测 | [A–D 主报告](reports/abcd_final/ANALYSIS_REPORT.md) |
| **E · 语音指令闭环** | 五类指令能否驱动车辆执行？ | [E 逐次 CSV](experiments/ag_final/E/experiment_e_results.csv) · [汇总 JSON](experiments/ag_final/E/experiment_e_summary.json)；50 次执行 | [E–G 主报告](reports/efg_final/EFG_ANALYSIS_REPORT.md) |
| **F · 环境鲁棒性** | 五种天气/光照下，指令执行表现如何？ | [F 逐次 CSV](experiments/ag_final/F/experiment_f_results.csv) · [汇总 JSON](experiments/ag_final/F/experiment_f_summary.json)；25 次执行 | [E–G 主报告](reports/efg_final/EFG_ANALYSIS_REPORT.md) |
| **G · 场景理解** | 真实模型能否在 CARLA 相机输入上产出有效场景描述？ | [G 审计时间线](experiments/ag_final/G/audit/lvlm_scene_context_timeline.jsonl) · [审计结果](experiments/ag_final/G/audit/lvlm_scene_context_audit.json)；54 条消息 | [E–G 主报告](reports/efg_final/EFG_ANALYSIS_REPORT.md) |

完整配置、状态与证据边界见 [A–G 实验矩阵](docs/experiment_matrix_zh.md)。

<a id="abcd-data"></a>

## 02 · A–D 最终实验数据

**按组浏览：[A](experiments/ag_final/A/) · [B](experiments/ag_final/B/) · [C](experiments/ag_final/C/) · [D](experiments/ag_final/D/)**

原始发布包与校验和：[`drivetdpa_abcd_nuscenes_20260930`](experiments/runs/drivetdpa_abcd_nuscenes_20260930/)。分组目录提供更直观的配置浏览，原包保留 held-out、切分清单和 SHA256。

数据记录日期为 **2026-09-30**，全量数据发布与最终报告整理于 **2026-10-13**。训练 2523 样本 / 841 场景；held-out 180 样本 / 9 场景，训练与评估场景不重叠。

| 想看什么 | 直接打开 | 中文说明 |
| --- | --- | --- |
| 配置与实验信息 | [experiment_matrix.json](experiments/runs/drivetdpa_abcd_nuscenes_20260930/experiment_matrix.json) · [run_manifest.json](experiments/runs/drivetdpa_abcd_nuscenes_20260930/run_manifest.json) | 12 个配置、切分信息与发布记录 |
| **逐配置指标** | **[metrics/](experiments/runs/drivetdpa_abcd_nuscenes_20260930/metrics/)** | 20 份指标；A 类各 3 seed，B/C/D 各单份 |
| **逐样本预测** | **[predictions/](experiments/runs/drivetdpa_abcd_nuscenes_20260930/predictions/)** | 20 份 JSONL，含 RAT 输出及逐样本指标 |
| 评估输入与切分 | [heldout/](experiments/runs/drivetdpa_abcd_nuscenes_20260930/heldout/) | held-out 输入、scene-disjoint 清单和训练/偏好数据元信息 |
| 文件完整性 | [SHA256SUMS](experiments/runs/drivetdpa_abcd_nuscenes_20260930/SHA256SUMS) | 已发布文件的逐文件校验和 |
| **可直接阅读的数据表** | **[ABCD_DATA_ANALYSIS.md](reports/abcd_final/ABCD_DATA_ANALYSIS.md)** | pipeline 生成的指标汇总；解释与最终统计结论以主报告为准 |
| 汇总统计 / 结论 | [results_summary.json](reports/abcd_final/results_summary.json) · [analysis_findings.json](reports/abcd_final/analysis_findings.json) | 汇总数值与最终分析结论分别保存 |

完整图像、checkpoint 和训练集正文未随此小型包全部入库。`heldout.jsonl` 中的图像路径需要外部数据；部分 metrics 沿用了旧 pilot 的 `limits` 文案，实际切分以 [split_manifest.json](experiments/runs/drivetdpa_abcd_nuscenes_20260930/heldout/split_manifest.json) 为准，详见[数据包说明](experiments/runs/drivetdpa_abcd_nuscenes_20260930/README.md)。

<a id="efg-data"></a>

## 03 · E–G 最终实验数据与汇总

**汇总目录：[`reports/efg_final/`](reports/efg_final/README.md)** · 报告发布于 **2026-10-25**

| 想看什么 | 直接打开 | 中文说明 |
| --- | --- | --- |
| **E 逐次执行** | **[50 条 CSV](experiments/ag_final/E/experiment_e_results.csv)** · [E summary](experiments/ag_final/E/experiment_e_summary.json) | 按 trial / command 记录 success、速度与偏航 |
| **F 逐次执行** | **[25 条 CSV](experiments/ag_final/F/experiment_f_results.csv)** · [F summary](experiments/ag_final/F/experiment_f_summary.json) | 按 scene / command 记录执行结果 |
| **G 审计与时间线** | **[54 条消息记录](experiments/ag_final/G/audit/lvlm_scene_context_timeline.jsonl)** · [审计 JSON](experiments/ag_final/G/audit/lvlm_scene_context_audit.json) · [目录](experiments/ag_final/G/) | 模型身份、消息有效性、hash 与运行日志；bag 只含元数据 |
| **最终统计数据** | **[results_summary.json](reports/efg_final/results_summary.json)** | E 按指令分解、F 按场景/指令分解、G 审计字段 |
| **可直接阅读的数据表** | **[EFG_DATA_ANALYSIS.md](reports/efg_final/EFG_DATA_ANALYSIS.md)** | 成功率、速度、转向幅度、环境对比及限制 |
| 结构化结论 | [analysis_findings.json](reports/efg_final/analysis_findings.json) | 结构化主张、数据依据与边界 |

报告记录 E **50/50**、F **25/25** 指令执行通过，G **54/54** 消息审计通过。E/F 无对照组、动作词汇与判据范围有限，F 的晴空基线包含跨 trial 状态残留；G 的上游官方 Talk2BEV entrypoint 未执行、BEV 对象为空。详细解释见[最终主报告](reports/efg_final/EFG_ANALYSIS_REPORT.md)。

**已入库 E/F 逐次 CSV 与 summary，以及 G 审计 JSON、逐消息时间线、运行日志和 bag 元数据。完整 bag 数据库与完整相机序列未入库。** 分组最终数据见 [`experiments/ag_final/`](experiments/ag_final/README.md)；外部来源见下方。

<a id="final-reports"></a>

## 04 · A–G 最终实验报告

| 阅读顺序 | 报告 | 重点 |
| --- | --- | --- |
| **1 · 开环消融** | **[A–D 最终分析报告](reports/abcd_final/ANALYSIS_REPORT.md)** | 行为塌缩、误差归因、场景感知统计、逐组消融与限制 |
| **2 · 闭环与场景理解** | **[E–G 最终分析报告](reports/efg_final/EFG_ANALYSIS_REPORT.md)** | 指令执行、动作可重复性、环境分解、场景审计与跨组解释 |
| 3 · 配合中文说明 | [A–D 中文解读](docs/nuscenes_abcd_experiment_zh.md) · [实验数据字典](docs/EXPERIMENT_DATA_DICTIONARY_ZH.md) | 先理解术语，再核对原始指标 |

**引用时的版本选择**：结论优先引用两份 Final 主报告，同时注明数据包或汇总 JSON。A–D 的旧 pilot、自动生成汇总表与最终主报告有统计和解释上的差别，使用主报告中场景感知检验后的结论。

**两份报告合并阅读**：A–D 度量轨迹回归精度，E/F 度量离散动作执行，G 度量场景消息审计；三类指标应分别表述。闭环成功率不能直接用作轨迹精度提升或组件消融收益的证明。

<a id="source-data"></a>

## 05 · 原始材料范围与校验

以下服务器路径来自现有报告/清单，仅用于追溯，**不是本仓库内目录或公开下载链接**。

| 材料 | 已入库内容 | 原始来源 |
| --- | --- | --- |
| A–D | 小型实验发布包、逐样本预测、指标与评估输入 | `/mnt/workspace/drivetdpa_experiments/abcd_full_20260930/`；完整图像/权重需另行准备 |
| E | [逐次 CSV 与 summary](experiments/ag_final/E/)、汇总指标、数据表和分析报告 | `/mnt/workspace/autonomous_driving/results/experiment_e/` |
| F | [逐次 CSV 与 summary](experiments/ag_final/F/)、汇总指标、数据表和分析报告 | `/mnt/workspace/drivetdpa_experiments/runs/F_env_run2/` |
| G | [审计时间线、日志与 bag 元数据](experiments/ag_final/G/)、数据表和分析报告；无完整 bag 数据库 | `/mnt/workspace/drivetdpa_experiments/runs/G_talk2bev_env_20261021/` |

A–D 最终发布包可在仓库根目录检查：

```bash
(cd experiments/runs/drivetdpa_abcd_nuscenes_20260930 && sha256sum --check SHA256SUMS)
```

E/F 可浏览逐次 CSV；G 可核对审计时间线与 audit 中记录的 hash。完整 bag 与图像不在库，不能仅凭元数据重新运行完整仿真实验。校验范围见[实验数据目录](experiments/README.md)。

---

[返回首页](README.md) · [版本时间线](docs/project_guide_zh.md#timeline) · [历史报告](reports/README.md#history) · [中文文档](docs/README.md)
