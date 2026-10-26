# 中文文档导航

[返回项目首页](../README.md) · [A–G 最终成果](../FINAL_RESULTS.md) · [项目目录与时间线](project_guide_zh.md)

先读最终结果，再按需要查实验解释、数据字段或采集流程。历史状态与最终报告分开阅读，避免把早期阻塞记录当成当前结论。

## 从这里开始

| 阅读顺序 | 文档 | 解决什么问题 |
| --- | --- | --- |
| ① | [项目目录与时间线](project_guide_zh.md) | 每个目录存什么；历史版本与 final 如何对应 |
| ② | [A–G 最终数据与报告入口](../FINAL_RESULTS.md) | 找最终报告、已发布数据和可复核的汇总 |
| ③ | [实验矩阵与证据状态](experiment_matrix_zh.md) | A–G 各组研究什么；目前有哪些证据和限制 |
| ④ | [NuScenes A–D 中文说明](nuscenes_abcd_experiment_zh.md) | 看懂开环消融、指标及最终结论 |
| ⑤ | [开环 / 闭环详细动态流程图](experiment_flows_zh.md) | 流动箭头、训练与评估分支、车辆控制反馈、单次 trial 时序；附可播放交互版 |

## 看实验、读数据

| 文档 / 入口 | 中文说明 |
| --- | --- |
| [A–D 最终分析报告](../reports/abcd_final/ANALYSIS_REPORT.md) | NuScenes 全量开环消融，含行为塌缩、误差归因与场景感知统计 |
| [E–G 最终分析报告](../reports/efg_final/EFG_ANALYSIS_REPORT.md) | CARLA 实时闭环执行、环境鲁棒性和场景理解；含与 A–D 的联系及局限 |
| [实验数据目录](../experiments/README.md) | 最终 / pilot 数据、CARLA 历史包、校验方法及服务器侧复现入口 |
| [实验数据字典](EXPERIMENT_DATA_DICTIONARY_ZH.md) | 指标、状态和实验包文件的中文含义；具体可用字段以对应 run 和最终报告为准 |
| [CARLA 数据字典](data_dictionary.md) | 场景、帧、预测、偏好对和闭环关联字段 |
| [数据集发布目录](../datasets/README.md) | 正式 CARLA 数据集的规划与预发布说明；与已发布实验结果分开管理 |

## 理解系统与采集流程

| 文档 | 中文说明 | 建议阅读顺序 |
| --- | --- | --- |
| [系统架构](architecture.md) | 场景与帧如何关联，各模块如何串联 | 先了解全貌 |
| [CARLA 数据采集流程](data_collection.md) | 采集前配置、采集中记录与采集后检查 | 再看数据产生过程 |
| [ROS 2 Topic 清单](ros_topics.md) | 仿真时钟、定位、感知、规划和控制消息 | 调试或接入时查阅 |
| [自动实验运行手册](automated_experiment_guide_zh.md) | 采集服务器上的模型启动、单轮 / 持续运行、停止与排障 | 有主项目、模型和种子数据时使用 |
| [存储与发布规范](storage_and_release.md) | GitHub 与对象存储的分工、校验和及发布约定 | 提交新数据前阅读 |
| [数据贡献说明](../CONTRIBUTING.md) | 来源、真实性、隐私和提交要求 | 发起贡献前阅读 |

> 本仓库主要发布文档、实验结果和轻量校验工具。运行完整模型训练或 CARLA / Autoware 采集需要外部 DriveTDPA 主项目、模型及数据；服务器绝对路径仅用于记录来源。
