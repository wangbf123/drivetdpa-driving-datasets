# A–G 实验矩阵与证据状态

[返回中文文档导航](README.md) · [A–G 最终成果](../FINAL_RESULTS.md) · [项目目录与时间线](project_guide_zh.md)

以下按当前仓库的 **final 报告和已发布产物** 整理。报告给出的实验状态、原始数据是否入库、尚未完成的对照实验是三个不同问题，分别列出。2026-09-15 的 `BLOCKED` 包保留在文末作为历史记录。

## 当前最终成果

**数据目录更新：2026-10-26**。[`experiments/ag_final/`](../experiments/ag_final/README.md)按 A–G 分组发布数据，现为首选浏览入口；旧 `runs/` 发布包保留切分与校验和。E/F 逐次 CSV、G 时间线与审计已入库，完整图像、权重和 rosbag `.db3` 仍需外部材料。

| 编号 | 实验问题 | 已有证据与入口 | 仍需区分的边界 |
| --- | --- | --- | --- |
| **A1–A4** | 偏好优化相对 SFT 是否改善轨迹？ | [A 组最终数据](../experiments/ag_final/A/)（2026-09-30 全量结果）；4 配置 × 3 seed，含指标与预测；[最终分析](../reports/abcd_final/ANALYSIS_REPORT.md) | 偏好对是 surrogate，训练预算 200 步；场景感知检验下 A1–A4 无显著差异 |
| **B1–B4** | 文本、语音代理、BEV 输入有何作用？ | [B 组最终数据](../experiments/ag_final/B/)：4 个模态配置；[最终分析](../reports/abcd_final/ANALYSIS_REPORT.md) | 语音使用文本转写 proxy，无真实音频编码器；不能据此评价 ASR |
| **C1–C2** | 中间 Action 层是否有独立价值？ | [C 组最终数据](../experiments/ag_final/C/)：R→T 与 R→A→T 的开环预测对照；[最终分析](../reports/abcd_final/ANALYSIS_REPORT.md) | 单 checkpoint 协议消融，结论对应本实验预算与评估集 |
| **D1–D2** | 加入 Talk2BEV 场景描述有何作用？ | [D 组最终数据](../experiments/ag_final/D/)：有 / 无场景描述的开环预测对照；[最终分析](../reports/abcd_final/ANALYSIS_REPORT.md) | 场景引用率不等于实体精确率 / 召回率，也不证明官方上游完整执行 |
| **E** | 五类语音指令能否驱动闭环执行？ | [E 的逐次 CSV](../experiments/ag_final/E/experiment_e_results.csv)和[分组汇总](../experiments/ag_final/E/experiment_e_summary.json)记录 5 指令 × 10 trial，50/50 成功；[最终分析](../reports/efg_final/EFG_ANALYSIS_REPORT.md) | 逐次结果表已入库，完整传感器序列和控制日志仍非全部发布；无文本对照，不能证明语音优于文本 |
| **F** | 天气 / 光照是否影响闭环指令执行？ | [F 的逐次 CSV](../experiments/ag_final/F/experiment_f_results.csv)和[分组汇总](../experiments/ag_final/F/experiment_f_summary.json)记录 5 场景 × 5 指令，25/25 成功 | 逐次结果表已入库；晴空基线有跨 trial 状态残留；成功率衡量离散动作执行 |
| **G** | 真实模型是否能输出可审计的场景理解？ | [G 时间线](../experiments/ag_final/G/audit/lvlm_scene_context_timeline.jsonl)与[审计 JSON](../experiments/ag_final/G/audit/lvlm_scene_context_audit.json)记录 54/54 有效消息、真实模型身份、审计 PASS | 时间线 / audit / 日志与 bag metadata 已入库，完整 `.db3` 未入库；BEV 对象为空，官方 Talk2BEV 上游入口仍为 `BLOCKED_NOT_EXECUTED`；不等于完整实体真值评估 |

A–D 最终数据采用 scene-disjoint 切分：训练 2523 样本 / 841 场景，held-out 180 样本 / 9 场景。A–D 的 ADE/FDE 衡量轨迹误差，E/F 的成功率衡量按指令执行；E/F 的显式动作映射不能用来证明模型自由轨迹回归质量。完整解释见两份最终主报告。

## 数据在哪里

| 内容 | 仓库可直接浏览 | 外部原始来源与范围 |
| --- | --- | --- |
| A–D 最终结果 | [ag_final/A–D 分组入口](../experiments/ag_final/README.md)；[旧发布包的 heldout 与 SHA256](../experiments/runs/drivetdpa_abcd_nuscenes_20260930/) | 图像、完整 NuScenes 原始数据和 checkpoint 不随仓库发布 |
| E 最终结果 | [逐次 CSV 与 summary](../experiments/ag_final/E/) | 来源 `/mnt/workspace/autonomous_driving/results/experiment_e/`；完整传感器 / 控制原始序列并未全部发布 |
| F 最终结果 | [逐次 CSV 与 summary](../experiments/ag_final/F/) | 来源 `/mnt/workspace/drivetdpa_experiments/runs/F_env_run2/`；完整原始运行材料仍在外部 |
| G 最终结果 | [54 条 timeline、audit、summary、日志和 bag 元信息](../experiments/ag_final/G/) | 来源 `/mnt/workspace/drivetdpa_experiments/runs/G_talk2bev_env_20261021/`；`g_bag/metadata.yaml` 引用的 `.db3` 未入库，不能完整回放 |
| E–G 分析 | [数据报告与汇总 JSON](../reports/efg_final/) | 结合上述逐次数据与主报告阅读，不能据成功率推定完整规划质量 |
| CARLA 偏好历史实验 | [995 个 recorded-seed 实验包](../experiments/README.md) | 保留真实模型、judge、loader 和哈希审计，不等同于 E/F/G 实时闭环 |

服务器路径是来源记录，不是仓库下载链接。正式 CARLA 数据集的三个发布目录仍为[规划 / 预发布状态](../datasets/README.md)。

## 历史快照：2026-09-15 的阻塞记录

以下记录对应 [`experiments/blocked_runs/`](../experiments/blocked_runs/) 中 2026-09-15 生成的实验包；其 manifest 的状态保持 `BLOCKED`。它们记录当时的证据缺口，不代表上述 final 报告的当前状态，也不能作为成功实验结果引用。

| 编号 | 当时计划 | 历史状态 | 当时记录的缺失证据 |
| --- | --- | --- | --- |
| A1–A4 | SFT/JPO/VL-DPO 消融 | BLOCKED | 完整数据、统一测试集、真实指标 |
| B1–B4 | 文字/语音/BEV 三模态 | BLOCKED | ASR 记录、成对输入和结果 |
| C1–C2 | 无 Action 与 RAT | BLOCKED | R/A/T 一致性统计 |
| D1–D2 | Talk2BEV 消融 | BLOCKED | upstream 真实运行、实体评估 |
| E | 五类语音指令 | BLOCKED | 每类至少 10 次真实执行 |
| F | 五类闭环场景 | BLOCKED | 多帧 bag、截图、自动成功判定 |
| G | Talk2BEV 理解质量 | BLOCKED | 真值对照和幻觉率 |

早期目标中尚未被最终证据覆盖的部分仍应保留为限制，例如真实音频对照、官方 Talk2BEV 上游与实体真值评估。历史 CARLA preference run 与 A–G final 结果分别归档。
