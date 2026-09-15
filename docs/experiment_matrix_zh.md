# 实验矩阵与当前状态

| 编号 | 实验 | 数据/输入 | 当前状态 | 缺失证据 |
|---|---|---|---|---|
| A1–A4 | SFT/JPO/VL-DPO 消融 | 完整 NuScenes-TP | BLOCKED | 完整数据、统一测试集、真实指标 |
| B1–B4 | 文字/语音/BEV 三模态 | NuScenes-TP | BLOCKED | ASR 记录、成对输入和结果 |
| C1–C2 | 无 Action 与 RAT | NuScenes-TP | BLOCKED | R/A/T 一致性统计 |
| D1–D2 | Talk2BEV 消融 | NuScenes-TP + BEV | BLOCKED | upstream 真实运行、实体评估 |
| E | 五类语音指令 | ROS2/CARLA | BLOCKED | 每类至少 10 次真实执行 |
| F | 五类闭环场景 | CARLA/Autoware | BLOCKED | 多帧 bag、截图、自动成功判定 |
| G | Talk2BEV 理解质量 | BEV 场景 | BLOCKED | 真值对照和幻觉率 |

已有 CARLA preference 历史 run 保持原样，不与上述尚未完成的 A–G 结果混合。
