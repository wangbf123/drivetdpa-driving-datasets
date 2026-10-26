# E–G 闭环实验分析报告（CARLA 实时，最终版）

[项目首页](../../README.md) · [A–G 最终成果](../../FINAL_RESULTS.md) · [报告总目录](../README.md) · [中文目录与时间线](../../docs/project_guide_zh.md)

> **最终版 · 优先阅读**｜报告发布：**2026-10-25**（Git 记录，北京时间）。这不是三组实验统一的执行日期；[G 的运行汇总](../../experiments/ag_final/G/summary.json)记录 `2026-10-21T19:52:00+08:00`，E/F 的精确运行日期需结合原始来源核对。

**阅读顺序：[最终报告](EFG_ANALYSIS_REPORT.md) → [数据表](EFG_DATA_ANALYSIS.md) → [汇总 JSON](results_summary.json) → [结论 JSON](analysis_findings.json)。**

**逐次数据：[E 指令执行 CSV](../../experiments/ag_final/E/experiment_e_results.csv) · [F 环境执行 CSV](../../experiments/ag_final/F/experiment_f_results.csv) · [G 场景消息时间线](../../experiments/ag_final/G/audit/lvlm_scene_context_timeline.jsonl) · [A–G 数据总目录](../../experiments/ag_final/README.md)。**

[动态看懂闭环执行与反馈](../../docs/experiment_flows_zh.md#closed-execution) · [单次 trial 时序](../../docs/experiment_flows_zh.md#closed-sequence) · [交互版逐步播放](../../docs/experiment_flows.html#closed-loop)

这是 DriveTDPA **闭环实验 E / F / G** 的权威、论文级分析报告，覆盖：

- **E** 语音指令闭环（5 类指令 × 10 trial，CARLA 实时）
- **F** 环境鲁棒性闭环（5 天气/光照场景 × 5 指令，CARLA 实时）
- **G** Talk2BEV 场景理解（真实 InternVL 模型 + CARLA 实时相机，54 条场景理解）

三组实验共享同一条真实链路：语音 / 轨迹指令 → 真实 InternVL 模型 → RAT（Reasoning→Action→Trajectory）→ YAML → ROS2 → Autoware E2E 控制 → CARLA 车辆执行。**这是全实验矩阵（A–G）中唯一端到端跑通的闭环证据**，与 A–D 的开环轨迹精度消融（NuScenes，ADE/FDE）互补。

> 与 A–D 报告的关键区别：A–D 用 ADE/FDE 度量"轨迹准不准"，E/F/G 用**执行成功率**度量"闭环系统是否按指令动作"。两者回答的是不同层级的问题，详见 [`EFG_ANALYSIS_REPORT.md`](./EFG_ANALYSIS_REPORT.md) §6。

## 文件

| 文件 | 内容 |
|---|---|
| [`EFG_ANALYSIS_REPORT.md`](./EFG_ANALYSIS_REPORT.md) | **主报告**（中文，11 节 + 3 附录）：实验依据、指标中文说明、E/F/G 逐组深挖（实验问题/数据对比/执行质量/机制/对论文价值）、三组共同边界、**跨组联动（为何 A–D 塌缩但 E/F 100%）**、局限、可支撑主张、论文结构建议、后续建议 |
| [`analysis_findings.json`](./analysis_findings.json) | 机器可读结论：执行成功率、动作幅度一致性、天气场景分解、审计字段、边界 |
| [`results_summary.json`](./results_summary.json) | E/F/G 三组汇总统计（per-command / per-scene / 审计指标） |
| [`EFG_DATA_ANALYSIS.md`](./EFG_DATA_ANALYSIS.md) | 数据报告（数据表、per-command/per-scene 分解、定性分析、边界说明） |

## 核心结论（六条主张，区分"强支撑 / 弱支撑"）

| # | 结论 | 强度 |
|---|---|---|
| **C1** | DriveTDPA 全链路（语音→InternVL→RAT→YAML→ROS2→Autoware E2E→CARLA）是**可运行、可执行的集成系统**；E+F 共 75/75 trials 全部通过，G 54/54 消息全部通过审计 | **强** |
| **C2** | 闭环执行**幅度高度可重复**：LEFT `+37.63±0.47°`、RIGHT `-36.91±0.56°`、SPEED_UP `+1.78±0.04 m/s`、SLOW_DOWN `-1.23±0.04 m/s`，说明 E2E 控制链（trajectory_follower→shift_decider→external_cmd_selector→vehicle_cmd_gate→raw_vehicle_cmd_converter）确定性、标定良好 | **强** |
| **C3** | 指令执行**对天气/光照稳健**：rain/fog/night/glare 四场景动作幅度与 clear_noon 基线几乎一致（LEFT ≈+36°、RIGHT ≈-34°、SPEED_UP 峰值 ≈2.89 m/s、SLOW_DOWN 末端 ≈0.4 m/s） | **强** |
| **C4** | 真实 InternVL 模型（2.12GB checkpoint，`mock=false`，hash 审计）在 CARLA 实时相机上产出 **Talk2BEV 兼容的场景理解**，正确识别道路布局 / 车道线 / 行人 / 静态物体，跨 5 场景 54 条全部无错误 | **强** |
| **C5** | 闭环 100% 成功是**"系统集成 + 显式动作映射"的产物，而非"轨迹回归质量"的证明**：E/F 的动作来自语音指令的离散动作解析（规则映射），不经过模型自由形式的轨迹回归，因此 A–D 观察到的"行为塌缩（不转弯/不刹车）"在闭环中被动作层显式化解 | **强（机制）** |
| **C6** | E/F **无对照组、判据宽松、词汇量极小**，**不能**支撑"语音优于文本""BEV 在闭环有用"等组件级消融结论；G 的 BEV 对象为空、上游 Talk2BEV entrypoint 未执行 | **弱（需复测）** |

## 诚实边界（一句话）

E/F/G 证明的是**"闭环系统端到端可执行、执行幅度可重复、对天气稳健、真实模型能理解场景"**；它们**不证明**任何单组件的消融贡献（无对照组），也**不证明**模型的轨迹规划质量（判据是离散动作执行、非轨迹精度）。100% 成功率含"判据宽松"的贡献，必须与 A–D 的"行为塌缩"结论**合并**陈述，才能给出诚实、完整的论文叙事。

## 原始数据位置与发布边界

本目录保存**分析报告、数据表与汇总 JSON**，逐次结果已发布至 [`experiments/ag_final/`](../../experiments/ag_final/README.md)：

| 实验 | 已发布的逐次数据与审计材料 |
| --- | --- |
| E | [50 行执行结果 CSV](../../experiments/ag_final/E/experiment_e_results.csv) · [汇总 JSON](../../experiments/ag_final/E/experiment_e_summary.json) |
| F | [25 行执行结果 CSV](../../experiments/ag_final/F/experiment_f_results.csv) · [汇总 JSON](../../experiments/ag_final/F/experiment_f_summary.json) |
| G | [54 条场景消息时间线](../../experiments/ag_final/G/audit/lvlm_scene_context_timeline.jsonl) · [模型与消息审计](../../experiments/ag_final/G/audit/lvlm_scene_context_audit.json) · [运行汇总](../../experiments/ag_final/G/summary.json) · [录制日志](../../experiments/ag_final/G/record.log) · [天气日志](../../experiments/ag_final/G/weather.log) |

G 的 [`g_bag/`](../../experiments/ag_final/G/g_bag/) 当前仅有 `metadata.yaml`，其引用的 `g_bag_0.db3` 未入库。完整 rosbag、相机图像与模型权重仍在外部保存，不能仅凭 metadata 重放 bag。

以下服务器路径用于追溯原始来源，不是当前云环境目录或公开下载入口：

- E：`/mnt/workspace/autonomous_driving/results/experiment_e/`
- F：`/mnt/workspace/drivetdpa_experiments/runs/F_env_run2/`
- G：`/mnt/workspace/drivetdpa_experiments/runs/G_talk2bev_env_20261021/`

完整实验时间线见[中文目录与时间线](../../docs/project_guide_zh.md)。

---

[返回 A–G 最终成果](../../FINAL_RESULTS.md) · [继续看 A–D 最终版](../abcd_final/README.md)
