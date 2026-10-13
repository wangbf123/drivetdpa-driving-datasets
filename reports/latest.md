# 最新实验报告

> 更新时间：2026-09-30（NuScenes A–D 全量消融，最终版）

## NuScenes A–D 开环消融（`drivetdpa_abcd_nuscenes_20260930`）

这是当前最完整、可支撑论文结论的实验成果。A1–A4（偏好消融）、B1–B4（模态消融）、
C1–C2（动作层消融）、D1–D2（Talk2BEV 消融）在 NuScenes scene-disjoint 切分（2523 训练 /
180 held-out / 9 场景）上完成。

**权威报告**：[`abcd_final/ANALYSIS_REPORT.md`](abcd_final/ANALYSIS_REPORT.md)
**机器可读结论**：[`abcd_final/analysis_findings.json`](abcd_final/analysis_findings.json)
**原始数据**：[`../experiments/runs/drivetdpa_abcd_nuscenes_20260930/`](../experiments/runs/drivetdpa_abcd_nuscenes_20260930/)

**核心结论**：模型学会了 RAT 协议格式与"前进"意图，但发生**行为类别塌缩**——整类丢弃
转向（20 个 eval 输出 `VEER` 0 次）、几乎从不刹车；**主导误差是纵向（不会停车）**；
surrogate 偏好优化（A2/A3/A4）相对 SFT 在场景感知统计下**无显著差异**。

## CARLA 偏好实验

最新 CARLA run：[`carla_pref_20260902T082921Z_seed30`](../experiments/runs/carla_pref_20260902T082921Z_seed30/run_manifest.json)

```text
STATUS=PASS
SOURCE=carla
CANDIDATE_COUNT=7
ACCEPTED_CANDIDATES=2
PREFERENCE_PAIRS=1
FALLBACK_SAMPLES=0
JUDGE_CONFIDENCE=0.95
```

该 run 使用已录制 CARLA 相机/场景种子重新执行真实 DriveTDPA 多次采样、安全门控、真实
VLM judge 和 TPO loader。它不是实时 CARLA 车辆闭环重跑。官方 Talk2BEV entrypoint 与
NVIDIA GPU 渲染状态仍按 manifest 保持 BLOCKED。机器可读索引见
[`experiments/index.jsonl`](../experiments/index.jsonl)。
