<div align="center">

# DriveTDPA · 数据与实验

**A–G 最终实验成果 · 中文报告 · 可追溯数据**

从 NuScenes 开环消融，到 CARLA 闭环执行与场景理解。

![A–D 开环实验](https://img.shields.io/badge/A–D-NuScenes_开环-2563eb)
![E–G 闭环与场景理解](https://img.shields.io/badge/E–G-CARLA_闭环与场景理解-059669)
![报告状态](https://img.shields.io/badge/报告-Final-7c3aed)

**[A–G FINAL 总入口](FINAL_RESULTS.md)** · **[开环 / 闭环动态图解](docs/experiment_flows_zh.md)** · **[中文目录与时间线](docs/project_guide_zh.md)** · **[全部文档](docs/README.md)**

</div>

---

## ⭐ A–G 最终成果

首次阅读请从这里开始。**数据看左列，结论看右列**；历史版本在下方单独索引。

| 实验 | 最终实验数据 / Final | 最终实验报告 / Final |
| --- | --- | --- |
| **A–D · NuScenes 开环消融**<br>偏好优化、输入模态、动作层、Talk2BEV | **[按 A–D 分组的最终数据](experiments/ag_final/README.md)**<br>20 份指标 + 20 份预测 · [held-out 与 SHA256 原包](experiments/runs/drivetdpa_abcd_nuscenes_20260930/)<br>[汇总 JSON](reports/abcd_final/results_summary.json) · [数据分析表](reports/abcd_final/ABCD_DATA_ANALYSIS.md) | **[A–D 最终分析报告](reports/abcd_final/ANALYSIS_REPORT.md)**<br>[报告目录](reports/abcd_final/README.md) · [结构化结论](reports/abcd_final/analysis_findings.json)<br>报告更新：**2026-10-13** |
| **E–G · CARLA 闭环与场景理解**<br>语音指令、环境鲁棒性、Talk2BEV 理解 | **[E / F / G 最终数据](experiments/ag_final/README.md)**<br>E：50 条 CSV · F：25 条 CSV · G：54 条审计时间线<br>[汇总 JSON](reports/efg_final/results_summary.json) · [数据分析表](reports/efg_final/EFG_DATA_ANALYSIS.md) · [原始材料位置说明](FINAL_RESULTS.md#source-data) | **[E–G 最终分析报告](reports/efg_final/EFG_ANALYSIS_REPORT.md)**<br>[报告目录](reports/efg_final/README.md) · [结构化结论](reports/efg_final/analysis_findings.json)<br>报告发布：**2026-10-25** |

> **数据范围**：[`experiments/ag_final/`](experiments/ag_final/README.md) 按 A–G 分组展示最终数据：A–D 指标与预测、E/F 逐次 CSV、G 审计时间线与日志均已入库；完整图像、模型权重和 bag 数据仍需外部准备。原 A–D 发布包保留供 SHA256 校验，详见 [FINAL 总入口](FINAL_RESULTS.md)。

### 先了解这三点

- **A–D 看轨迹精度与组件作用**：最终报告记录了转向/刹车行为塌缩；场景感知统计下，A1–A4 无显著精度差异。
- **E–G 看闭环执行与场景理解**：报告记录 E 50/50、F 25/25 执行通过，G 54/54 消息审计通过；结果受测试范围与判据约束。
- **两组结果需要合并阅读**：E/F 的显式动作映射支持指令执行，不能据此认定 A–D 中的轨迹回归问题已经解决。

## 🔄 开环与闭环 · 动态流程图

**[详细流程图与闭环时序 →](docs/experiment_flows_zh.md)** · **[交互播放版 HTML →](docs/experiment_flows.html)**

两条链路分别展示数据准备、模型处理、输出评价与车辆反馈。SVG 的虚线箭头可流动；交互版支持 **播放 / 暂停、上一步 / 下一步、节点详情、速度和缩放**。GitHub 展示 HTML 源码时，下载该单文件后用浏览器打开，无需安装依赖。动画演示流程，不连接实时实验服务。

<details open>
<summary><strong>展开开环 A–D：数据 → 场景切分 → 训练消融 → 预测 → 真值对比 → 最终报告</strong></summary>

![A–D 开环动态流程图](docs/assets/open_loop_flow.svg)

[查看训练分支](docs/experiment_flows_zh.md#open-training) · [查看推理、失败分流与最终统计](docs/experiment_flows_zh.md#open-evaluation)

</details>

<details open>
<summary><strong>展开闭环 E/F：指令 → 动作 → 轨迹 → Autoware → CARLA → 状态反馈；附 G 审计支路</strong></summary>

![E/F 闭环执行与 G 场景理解动态流程图](docs/assets/closed_loop_flow.svg)

[查看控制反馈与判据](docs/experiment_flows_zh.md#closed-execution) · [查看单次 trial 时序](docs/experiment_flows_zh.md#closed-sequence) · [查看 G 场景理解审计](docs/experiment_flows_zh.md#scene-audit)

</details>

## 🧭 怎么阅读这个项目

| 你的目的 | 推荐入口 | 下一步 |
| --- | --- | --- |
| **快速看最终成果** | [A–G FINAL 总入口](FINAL_RESULTS.md) | 选择实验组 → 数据表 → 主报告 |
| **看懂开环与闭环链路** | [动态流程图与详细图解](docs/experiment_flows_zh.md) | 训练 / 推理分支 → 控制反馈 → 时序与节点说明 |
| **看懂每个目录** | [中文目录与时间线](docs/project_guide_zh.md) | 按目录用途或版本日期查找 |
| **写论文 / 引用结论** | [A–D 报告](reports/abcd_final/ANALYSIS_REPORT.md) / [E–G 报告](reports/efg_final/EFG_ANALYSIS_REPORT.md) | 同时核对统计方法、结论边界和对应数据 |
| **核对实验配置与字段** | [A–G 实验矩阵](docs/experiment_matrix_zh.md) | [实验数据字典](docs/EXPERIMENT_DATA_DICTIONARY_ZH.md) |
| **检查或复用数据** | [实验数据目录](experiments/README.md) | [快速校验](#validation) |
| **准备采集 / 复现** | [自动实验运行手册](docs/automated_experiment_guide_zh.md) | [A–D 复现脚本说明](scripts/experiments/abcd_full/README.md) |

## 🗂️ 项目目录 · 中文速览

以下按推荐阅读顺序排列；GitHub 的文件列表仍按名称排序。

```text
drivetdpa-driving-datasets/
├── README.md                 项目首页：优先展示 A–G 最终成果
├── FINAL_RESULTS.md          A–G 最终数据、报告与来源的统一入口
├── reports/                  分析报告与统计汇总
│   ├── efg_final/            E–G 最终报告与数据汇总（2026-10-25 发布）
│   ├── abcd_final/           A–D 最终报告与数据汇总（2026-10-13 更新）
│   ├── abcd_按实验指导_20260930/  历史整理版，使用 09-24 pilot 数据
│   └── abcd_20260924/        历史单场景 pilot 报告
├── experiments/              实验发布数据、索引与历史阻塞记录
│   ├── ag_final/             A–G 分组最终数据（指标、预测、CSV、审计）
│   ├── runs/                 A–D 两个原始发布包 + CARLA 历史偏好实验包
│   └── blocked_runs/         2026-09-15 的阻塞记录
├── docs/                     中文导览、实验说明、数据字典与采集规范
├── scripts/                  数据校验、下载、导入与 A–D 复现脚本
├── examples/                 CARLA 格式示例（用于理解字段）
├── schemas/                  场景、预测、偏好对等 JSON Schema
├── manifests/                大文件清单示例与索引约定
├── datasets/                 正式数据集规划与发布位置说明
└── CONTRIBUTING.md           数据贡献与真实性要求
```

完整说明见 **[项目目录中文指南](docs/project_guide_zh.md)**。

## 🕒 版本顺序 · 最新在前

日期区分实验记录与报告发布，不使用本机文件修改时间判断版本。

| 日期 | 阶段 | 阅读入口 |
| --- | --- | --- |
| **2026-10-26** | **A–G 最终数据按组归档**：补齐 E/F CSV 与 G 审计时间线 | [A–G 分组数据](experiments/ag_final/README.md) |
| **2026-10-25** | **E–G 最终报告发布**：闭环执行、环境鲁棒性与场景理解 | [E–G Final](reports/efg_final/README.md) |
| **2026-10-13** | **A–D 全量数据发布与最终报告更新**：数据记录日期为 09-30 | [A–D Final](reports/abcd_final/README.md) |
| 2026-09-30 | A–D 全量实验包记录；同时整理了基于旧 pilot 的按指导版报告 | [全量数据](experiments/runs/drivetdpa_abcd_nuscenes_20260930/) · [历史整理版](reports/abcd_按实验指导_20260930/README.md) |
| 2026-09-24 | A–D 单场景 pilot：450 训练样本、20 held-out 样本 | [历史报告](reports/abcd_20260924/README.md) |
| 2026-09-15 及之前 | A–G 阻塞记录、CARLA recorded-seed 偏好实验积累 | [历史说明](docs/project_guide_zh.md#timeline) |

**[查看详细时间线与版本对应关系 →](docs/project_guide_zh.md#timeline)**

<a id="validation"></a>

## ✅ 快速校验

离线工具只依赖 **Python 3.9+ 标准库**。在仓库根目录执行：

```bash
# CARLA 格式示例及关联记录
python scripts/validate_dataset.py examples/scene_000001/manifest.json

# 历史 CARLA 偏好实验包
python scripts/validate_experiment.py experiments/runs/carla_pref_*

# A–D 最终发布包的文件完整性
(cd experiments/runs/drivetdpa_abcd_nuscenes_20260930 && sha256sum --check SHA256SUMS)
```

当前验证器仅适用于 CARLA run；直接传入整个 `experiments/runs` 会因 NuScenes 清单格式不同而报错。更多校验说明见 [实验数据目录](experiments/README.md)。文件校验通过表示发布文件完整，重新训练和仿真仍需外部主项目、图像、权重及运行环境。

<details>
<summary><strong>CARLA 数据集规划与真实性约定</strong></summary>

### 数据集规划

仓库还维护 CARLA 传感器 → ROS Bridge → Autoware → BEV → Talk2BEV → DriveTDPA → 控制反馈的数据规范。

| 发布位置 | 内容 | 当前范围 |
| --- | --- | --- |
| [datasets/carla/](datasets/carla/README.md) | 传感器、Autoware、BEV、Talk2BEV 与模型预测 | 完整数据集计划中 |
| [datasets/preference/](datasets/preference/README.md) | 同帧多候选轨迹与偏好对 | 完整数据集计划中；小型历史实验包已在 `experiments/runs/` |
| [datasets/closed_loop/](datasets/closed_loop/README.md) | 控制指令与下一帧反馈 | 完整数据集计划中；E–G 汇总见 Final 入口 |

`examples/` 是格式示例；`manifests/*.example.jsonl` 含下载占位符，下载工具会拒绝这些占位地址。CARLA 偏好历史包使用 recorded-seed，不代表实时车辆闭环重跑。

### 存储与来源

Git 保存文档、Schema、小型示例、实验发布包、清单与报告；完整图像、点云、rosbag、视频和模型权重放在对象存储或实验服务器。正式文件需记录大小和 SHA256，见 [存储与发布规范](docs/storage_and_release.md)。

- CARLA 仿真器状态可作为真值，但需保留来源和配置；模型预测、推理和场景描述应标明其预测性质。
- 偏好对来自同一 CARLA 场景、同一帧的候选；judge 不应接触 reward、rank 或未来真值等泄漏字段。
- 非有限数值、碰撞或越界轨迹应被安全门控排除；记录需用版本、场景、帧和时间戳关联。
- NuScenes A–D 与 CARLA 数据使用各自的来源和清单格式，查看时需区分。

</details>

---

**[A–G FINAL](FINAL_RESULTS.md)** · [报告索引](reports/README.md) · [实验数据索引](experiments/README.md) · [中文文档](docs/README.md) · [贡献说明](CONTRIBUTING.md)
