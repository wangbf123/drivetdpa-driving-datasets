# 项目目录中文指南与版本时间线

[返回首页](../README.md) · [A–G FINAL](../FINAL_RESULTS.md) · [全部中文文档](README.md)

这份指南按“**最终成果 → 支撑数据 → 历史版本 → 采集与开发**”组织阅读入口。首页展示当前 Final 版本；历史文件按时间回溯，保留原路径以便核对报告引用和 SHA256。

## 1 · 三条推荐阅读路线

| 目的 | 路线 |
| --- | --- |
| **快速理解项目** | [首页](../README.md) → [A–G FINAL](../FINAL_RESULTS.md) → 选择对应主报告 |
| **动态看懂实验链路** | [开环 / 闭环动态图解](experiment_flows_zh.md) → [交互播放版](experiment_flows.html) → 查看每个节点的输入、处理与输出 |
| **核对论文证据** | [A–G 实验矩阵](experiment_matrix_zh.md) → [A–D 主报告](../reports/abcd_final/ANALYSIS_REPORT.md) / [E–G 主报告](../reports/efg_final/EFG_ANALYSIS_REPORT.md) → 数据表与 JSON → 发布包 / 原始来源说明 |
| **采集或复现实验** | [系统架构](architecture.md) → [自动实验手册](automated_experiment_guide_zh.md) → [复现脚本说明](../scripts/experiments/abcd_full/README.md) → [校验与贡献要求](../CONTRIBUTING.md) |

## 2 · 每个目录放什么

| 目录 / 文件 | 中文用途 | 从哪里开始看 |
| --- | --- | --- |
| **[FINAL_RESULTS.md](../FINAL_RESULTS.md)** | **A–G 最终成果总入口**；按组别关联最终数据、报告、汇总与原始来源 | 先选 A–D 或 E–G |
| **[reports/](../reports/README.md)** | **结论与分析**；最终主报告、数据分析表、统计 JSON 与旧版报告 | 当前结论看 `abcd_final/`、`efg_final/` |
| **[experiments/](../experiments/README.md)** | **实验数据与证据包**；已发布运行记录、机器索引和历史阻塞材料 | 按组看 `ag_final/A/` 至 `G/`；A–D 原包及校验和在 `runs/drivetdpa_abcd_nuscenes_20260930/` |
| [docs/](README.md) | 中文文档：阅读导航、实验矩阵、字段字典、架构、采集与发布规范 | [文档索引](README.md) |
| [scripts/](../scripts/) | 校验、下载、导入、生成校验和与 A–D 训练/评估辅助脚本 | 离线校验从[首页命令](../README.md#validation)开始 |
| [examples/](../examples/scene_000001/manifest.json) | 小型 CARLA 场景格式示例，关联帧、BEV、预测、偏好和指标 | `scene_000001/manifest.json` |
| [schemas/](../schemas/) | JSON Schema：规定场景清单、帧、BEV、模型预测、偏好对及实验包的结构 | 根据待核对文件选择 `.schema.json` |
| [manifests/](../manifests/README.md) | 场景及外部大文件清单约定；现有 `.example.jsonl` 含下载占位符 | 先看 README，确认正式地址与 SHA256 |
| [datasets/](../datasets/README.md) | 正式 CARLA 数据集发布位置与规划 | `carla/`、`preference/`、`closed_loop/` 均有用途说明 |
| [CONTRIBUTING.md](../CONTRIBUTING.md) | 数据提交要求：来源、版本、校验和、敏感信息与实验说明 | 贡献数据前阅读 |

### 报告目录：先看 Final，再看历史

```text
reports/
├── README.md                      报告导航：Final 入口与历史版本
├── latest.md                      最新实验状态摘要
├── efg_final/                     E–G 最终版（2026-10-25 发布）
│   ├── EFG_ANALYSIS_REPORT.md      主报告：结论、机制、边界与论文价值
│   ├── EFG_DATA_ANALYSIS.md        数据表：按指令、场景与审计字段分解
│   ├── results_summary.json        汇总数值
│   └── analysis_findings.json      结构化分析结论
├── abcd_final/                    A–D 最终版（2026-10-13 更新）
│   ├── ANALYSIS_REPORT.md          主报告：场景感知统计与最终解释
│   ├── ABCD_DATA_ANALYSIS.md        pipeline 生成的数据汇总
│   ├── results_summary.json        配置汇总数值
│   └── analysis_findings.json      结构化分析结论
├── abcd_按实验指导_20260930/       历史整理版，数据仍为 09-24 pilot
├── abcd_20260924/                 历史 pilot 初版
├── figures/                       图表预留目录，当前没有发布图表
└── metrics/                       指标预留目录，实际 final JSON 在对应 final 目录
```

### 实验目录：区分三类记录

```text
experiments/
├── README.md                      实验数据导航与校验方法
├── index.jsonl                    CARLA 自动实验的机器可读索引
├── ag_final/                      按 A–G 分组的最终数据（2026-10-26 入库整理）
│   ├── A/ … D/                    各配置 / seed 的指标与预测
│   ├── E/、F/                     逐次 CSV 与 summary
│   └── G/                         审计时间线、日志及 bag 元数据
├── runs/
│   ├── drivetdpa_abcd_nuscenes_20260930/   A–D 最终发布包，180 held-out 样本
│   ├── drivetdpa_abcd_nuscenes_20260924/   A–D 历史 pilot，20 held-out 样本
│   └── carla_pref_*/              995 个历史偏好实验包（recorded-seed）
└── blocked_runs/                  2026-09-15 的 A–G 阻塞快照
```

E–G 的逐次执行与审计数据保存在 **[`experiments/ag_final/E/`](../experiments/ag_final/E/)、[F/](../experiments/ag_final/F/)、[G/](../experiments/ag_final/G/)**；最终分析汇总位于 **[`reports/efg_final/`](../reports/efg_final/README.md)**。完整相机序列和 bag 数据库仍在外部保存。`blocked_runs/` 是早期记录，其状态不能代表后续 Final 的进展。

<a id="timeline"></a>

## 3 · 按时间回溯项目

以下按日期倒序，便于先找到最新成果。日期依据为 Git 提交记录、run manifest 的 `created_at` 或运行目录标识；**实验记录时间与报告发布时间分别标注**，不以检出后的文件修改时间排序。带时区的日期按北京时间理解。

| 时间 | 类型 | 发生了什么 | 对应文件 |
| --- | --- | --- | --- |
| **2026-10-26** | **数据归档发布** | 按 A–G 分组发布最终数据，新增 E/F 逐次 CSV、G 审计时间线与日志 | [ag_final 数据目录](../experiments/ag_final/README.md) |
| **2026-10-25** | **报告发布** | 发布 E–G 最终报告、数据汇总与结构化结论 | [E–G Final](../reports/efg_final/README.md) |
| 2026-10-21 | G 运行记录 | G summary 的 `created_at` 为 10-21；不能据此推定 E/F 的运行日期 | [G summary](../experiments/ag_final/G/summary.json) |
| **2026-10-13** | **数据发布 / 报告更新** | 发布 09-30 全量 A–D 实验包；独立 `abcd_final/` 并深化报告 | [A–D Final](../reports/abcd_final/README.md) · [最终数据包](../experiments/runs/drivetdpa_abcd_nuscenes_20260930/) |
| 2026-09-30 | 实验包记录 | 全量 A–D manifest 记录时间为 09-30；2523 训练样本、180 held-out 样本、9 个评估场景 | [run_manifest.json](../experiments/runs/drivetdpa_abcd_nuscenes_20260930/run_manifest.json) |
| 2026-09-30 | 历史报告整理 | 按实验指导重排旧 pilot 结果，仍使用 09-24 的 450 训练 / 20 held-out 数据 | [历史按指导版](../reports/abcd_按实验指导_20260930/README.md) |
| 2026-09-24 | pilot 记录 / 报告发布 | 单场景 A–D pilot，450 训练样本、20 held-out 样本 | [历史数据包](../experiments/runs/drivetdpa_abcd_nuscenes_20260924/) · [历史报告](../reports/abcd_20260924/README.md) |
| 2026-09-15 | 历史阻塞快照 | 记录当时 A–G 缺失的证据与阻塞状态 | [blocked_runs/](../experiments/blocked_runs/) · [实验矩阵中的历史说明](experiment_matrix_zh.md) |
| 2026-08-31—09-02（运行目录日期） | 历史数据积累 | CARLA recorded-seed 偏好实验包；与 E/F 实时指令闭环区分 | [实验数据说明](../experiments/README.md) |

### 容易混淆的两个“09-30”

| 入口 | 实际内容 | 当前用途 |
| --- | --- | --- |
| `reports/abcd_按实验指导_20260930/` | **09-24 单场景 pilot** 的报告整理版 | 查看历史写法与早期分析 |
| `experiments/runs/drivetdpa_abcd_nuscenes_20260930/` | **09-30 全量 scene-disjoint** 实验发布包 | 配合 `reports/abcd_final/` 核对最终结论 |

A–D pilot 与全量版的样本范围、统计处理和部分结论不同。历史文件保留其原始语境；引用当前结论时，从 Final 入口进入。

## 4 · 文件名怎么读

| 名称 / 格式 | 中文含义 |
| --- | --- |
| `final` | 当前仓库指定的最终分析版本；不表示完整外部原始数据都已入库 |
| `run` / `run_id` | 一次实验运行或一组发布记录的标识 |
| `pilot` | 小规模预实验，需与全量评估分开比较 |
| `manifest` | 文件、来源、状态、版本与校验信息的清单 |
| `metrics` | 指标数值；A–D 实际逐配置文件在最终数据包的 `metrics/` |
| `predictions` | 逐样本模型输出，通常为一行一条的 JSONL |
| `results_summary.json` | 汇总统计数值 |
| `analysis_findings.json` | 解释、主张及其证据与边界 |
| `SHA256SUMS` | 文件完整性校验清单；迁移或改动包内文件会影响校验 |
| `BLOCKED` | 对应记录当时缺少必要条件或证据，不能作为成功实验结果使用 |

## 5 · 目录整理原则

- **首页优先 Final**：先给最终数据和报告入口，再呈现规范与历史记录。
- **索引按时间组织**：最新版本在前，保留实验日期、整理日期与发布日期的区别。
- **报告和数据互相可查**：报告索引、实验索引、Final 总入口均可回到首页和中文指南。
- **原始文件保留路径**：不为视觉排序重命名数据包；通过中文导航树与版本表提升可读性，同时保留既有引用和校验和。
- **预留与已发布内容标清楚**：格式示例、正式数据集规划、历史阻塞包、最终汇总各有说明。

---

[返回首页](../README.md) · [A–G FINAL](../FINAL_RESULTS.md) · [报告索引](../reports/README.md) · [实验数据索引](../experiments/README.md) · [文档索引](README.md)
