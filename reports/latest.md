# 最新实验报告

[返回项目首页](../README.md) · [A–G FINAL 数据与报告](../FINAL_RESULTS.md) · [报告版本索引](README.md) · [中文目录与时间线](../docs/project_guide_zh.md)

> 更新时间：2026-10-25（CARLA 闭环 E/F/G + NuScenes 开环 A–D，最终版）

## CARLA 闭环实验 E / F / G（`drivetdpa_experiments/runs/*` + `autonomous_driving/results/experiment_e/`）

这是 DriveTDPA 全实验矩阵中**唯一端到端跑通的闭环证据**，覆盖：

- **E 语音指令闭环**：5 指令 × 10 trial = **50/50 = 100%**
- **F 环境鲁棒性闭环**：5 场景 × 5 指令 = **25/25 = 100%**
- **G Talk2BEV 场景理解**：真实 InternVL 模型 54/54 消息审计 PASS

**权威报告**：[`efg_final/EFG_ANALYSIS_REPORT.md`](efg_final/EFG_ANALYSIS_REPORT.md)
**机器可读结论**：[`efg_final/analysis_findings.json`](efg_final/analysis_findings.json)

**核心结论**：闭环系统端到端可执行、执行幅度高度可重复且转向对称（LEFT `+37.63±0.47°` /
RIGHT `−36.91±0.56°`）、对雨/雾/夜/逆光稳健、真实 InternVL 能正确理解场景。**但** 100%
成功是「系统集成 + 显式动作映射」的产物，不是「轨迹回归质量」的证明——E/F 的动作来自语音
指令的规则解析，模型只做「离散动作→连续轨迹」展开，因此 A–D 观察到的「行为塌缩」在闭环中
被绕过而非被推翻。二者合并陈述才完整。

## NuScenes A–D 开环消融（`drivetdpa_abcd_nuscenes_20260930`）

A1–A4（偏好消融）、B1–B4（模态消融）、C1–C2（动作层消融）、D1–D2（Talk2BEV 消融），
NuScenes scene-disjoint 切分（2523 训练 / 180 held-out / 9 场景）。

**权威报告**：[`abcd_final/ANALYSIS_REPORT.md`](abcd_final/ANALYSIS_REPORT.md)
**机器可读结论**：[`abcd_final/analysis_findings.json`](abcd_final/analysis_findings.json)

**核心结论**：模型学会了 RAT 协议格式与「前进」意图，但发生**行为类别塌缩**——整类丢弃
转向（VEER 输出 0 次）、几乎从不刹车；**主导误差是纵向（不会停车）**；surrogate 偏好优化
（A2/A3/A4）相对 SFT 在场景感知统计下**无显著差异**；动作层有独立价值（去 ADE +22%）。

## 完整证据链（开环 + 闭环）

1. 离线消融（A–D）证明**组件价值**：动作层 +22% 精度、BEV 保合规、但模型塌缩（不转弯/不刹车）。
2. 闭环系统（E/F/G）证明**端到端可用**：动作→轨迹→执行链确定、可重复、对天气稳健。
3. 二者合并：RAT 分层把「意图→离散动作→连续轨迹」显式分解——意图来源可靠时忠实执行（闭环验证），
   意图来源不可靠时暴露塌缩（开环验证）。

## CARLA 偏好实验（历史）

最新 CARLA run：[`carla_pref_20260902T082921Z_seed30`](../experiments/runs/carla_pref_20260902T082921Z_seed30/run_manifest.json) —— 非实时闭环重跑，官方 Talk2BEV entrypoint 仍按 manifest 保持 BLOCKED。
