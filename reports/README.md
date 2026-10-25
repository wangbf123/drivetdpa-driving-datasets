# 实验报告

该目录只保存体积较小、方便审查的发布结果。

## 目录

| 路径 | 内容 |
|---|---|
| [`latest.md`](latest.md) | 最新实验状态和已知限制 |
| [`efg_final/`](efg_final/) | **CARLA 闭环实验 E/F/G 最终分析**（权威、论文级，含执行可重复性、环境稳健性、Talk2BEV 场景理解与跨组联动） |
| [`abcd_final/`](abcd_final/) | **NuScenes A–D 开环消融最终分析**（权威、论文级，含场景感知统计与三次修正） |
| [`abcd_按实验指导_20260930/`](abcd_按实验指导_20260930/) | A–D 实验的按实验指导核对版（早于 abcd_final 的深度挖掘） |
| [`abcd_20260924/`](abcd_20260924/) | A–D 单场景 pilot 报告 |
| `metrics/*.json` | 碰撞率、ADE、FDE、延迟等机器可读指标 |
| `figures/*.png` | 精选 BEV、轨迹和对比图 |

## 说明

- **NuScenes A–D 的权威结论以 [`abcd_final/ANALYSIS_REPORT.md`](abcd_final/ANALYSIS_REPORT.md) 为准**；
  早期目录保留作为历史记录。
- **CARLA 闭环 E/F/G 的权威结论以 [`efg_final/EFG_ANALYSIS_REPORT.md`](efg_final/EFG_ANALYSIS_REPORT.md) 为准**；
  与 A–D 合并阅读可得完整「开环消融 + 闭环系统」证据链。
- 完整运行日志、视频和原始数据放在对象存储，并从不可变的 CARLA manifest 链接。
  示例数值不能当作正式测量结果；每份报告必须说明使用的数据集、代码、模型和 CARLA 场景版本。
