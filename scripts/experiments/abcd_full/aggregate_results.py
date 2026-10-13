#!/usr/bin/env python3
"""Aggregate A-D experiment eval results into paper-grade statistics + report.

Reads eval/<config>[/seed<seed>]/metrics.json + predictions.jsonl for all 12
configurations, computes mean +/- std and 95% t-intervals across training seeds
(A-class), a day/rain/night condition breakdown, paired Wilcoxon tests for the
key ablations, and the two qualitative analyses the guide asks for (C: R->A
direction mismatches, D: scene-reference rate). Writes results_summary.json and
ABCD_DATA_ANALYSIS.md under --output-root/report.
"""
from __future__ import annotations

import argparse
import json
import math
from collections import defaultdict
from pathlib import Path
from typing import Any

import numpy as np
from scipy import stats

CONFIGS_A = ["A1_SFT", "A2_physics", "A3_jpo", "A4_vldpo"]
CONFIGS_BCD = [
    "B1_image_text", "B2_image_speech", "B3_image_text_bev", "B4_image_speech_bev",
    "C1_R_to_T", "C2_R_to_A_to_T", "D1_no_talk2bev", "D2_talk2bev",
]
CONFIG_LABELS = {
    "A1_SFT": "A1 SFT", "A2_physics": "A2 SFT+Physics", "A3_jpo": "A3 SFT+JPO",
    "A4_vldpo": "A4 SFT+JPO+VL-DPO", "B1_image_text": "B1 Image+Text",
    "B2_image_speech": "B2 Image+Speech(proxy)", "B3_image_text_bev": "B3 Image+Text+BEV",
    "B4_image_speech_bev": "B4 Image+Speech+BEV", "C1_R_to_T": "C1 R->T",
    "C2_R_to_A_to_T": "C2 R->A->T", "D1_no_talk2bev": "D1 no Talk2BEV",
    "D2_talk2bev": "D2 Talk2BEV",
}
METRIC_KEYS = [
    "ADE_m", "FDE_m", "Goal", "A_to_T_consistency", "R_to_A_consistency", "TMC",
    "scene_reference_rate", "scene_reference_correct_rate", "parse_success_rate",
    "Lat_ms_mean", "ADE_common", "ADE_worstcase",
]


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(l) for l in path.read_text().splitlines() if l.strip()]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def t_ci(values: list[float], conf: float = 0.95) -> dict[str, float | None]:
    values = [v for v in values if v is not None]
    if not values:
        return {"mean": None, "std": None, "lo": None, "hi": None, "n": 0}
    arr = np.array(values, dtype=float)
    mean = float(arr.mean())
    std = float(arr.std(ddof=1)) if len(arr) > 1 else 0.0
    n = len(arr)
    if n >= 2 and std > 0:
        tcrit = stats.t.ppf(1 - (1 - conf) / 2, df=n - 1)
        se = std / math.sqrt(n)
        lo, hi = mean - tcrit * se, mean + tcrit * se
    else:
        lo, hi = mean, mean
    return {"mean": mean, "std": std, "lo": lo, "hi": hi, "n": n}


def paired_wilcoxon(a: list[float], b: list[float]) -> dict[str, Any]:
    """Wilcoxon signed-rank test + Cohen's d on paired per-sample values."""
    pairs = [(x, y) for x, y in zip(a, b) if x is not None and y is not None]
    if len(pairs) < 5:
        return {"n_pairs": len(pairs), "statistic": None, "p_value": None, "cohens_d": None, "note": "insufficient pairs"}
    x = np.array([p[0] for p in pairs], dtype=float)
    y = np.array([p[1] for p in pairs], dtype=float)
    try:
        stat, p = stats.wilcoxon(x, y, alternative="two-sided")
    except Exception:
        stat, p = float("nan"), float("nan")
    d = (x - y).mean() / ((x - y).std(ddof=1) or 1.0)
    return {"n_pairs": int(len(pairs)), "statistic": float(stat), "p_value": float(p),
            "cohens_d": float(d)}


# --------------------------------------------------------------------------- #
# Direction helpers for the C qualitative analysis
# --------------------------------------------------------------------------- #
def think_direction(think: str) -> str | None:
    t = (think or "").lower()
    if any(k in t for k in ("turn left", "veer left", "move left", "左转", "向左")):
        return "LEFT"
    if any(k in t for k in ("turn right", "veer right", "move right", "右转", "向右")):
        return "RIGHT"
    if any(k in t for k in ("straight", "follow lane", "直行", "保持车道", "forward")):
        return "STRAIGHT"
    return None


def trajectory_direction(traj: list[list[float]] | None) -> str | None:
    if not traj or len(traj) == 0:
        return None
    x6 = traj[-1][0]
    if x6 > 0.5:
        return "RIGHT"
    if x6 < -0.5:
        return "LEFT"
    return "STRAIGHT"


def r_vs_t_mismatch(row: dict[str, Any]) -> bool | None:
    pred = row.get("prediction", {})
    rt = think_direction(pred.get("think", ""))
    tt = trajectory_direction(pred.get("trajectory"))
    if rt is None or tt is None:
        return None
    return rt != tt


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--eval-root", type=Path, required=True)
    ap.add_argument("--output-root", type=Path, required=True)
    ap.add_argument("--seeds", type=str, default="42 17 23")
    ap.add_argument("--heldout", type=Path, required=True)
    args = ap.parse_args()
    seeds = args.seeds.split()

    report_dir = args.output_root / "report"
    report_dir.mkdir(parents=True, exist_ok=True)

    # condition mapping from the held-out input
    cond_by_id: dict[str, str] = {}
    cond_by_scene: dict[str, str] = {}
    for r in load_jsonl(args.heldout):
        cond_by_id[r["id"]] = r.get("condition", "day")
        cond_by_scene[r["scene_token"]] = r.get("condition", "day")

    # ---- collect eval results ------------------------------------------- #
    def collect(config: str) -> list[tuple[str | None, dict, list]]:
        out = []
        if config in CONFIGS_A:
            for s in seeds:
                d = args.eval_root / config / f"seed{s}"
                if (d / "metrics.json").exists():
                    out.append((s, load_json(d / "metrics.json"), load_jsonl(d / "predictions.jsonl")))
        else:
            d = args.eval_root / config
            if (d / "metrics.json").exists():
                out.append((None, load_json(d / "metrics.json"), load_jsonl(d / "predictions.jsonl")))
        return out

    results: dict[str, list] = {c: collect(c) for c in CONFIGS_A + CONFIGS_BCD}
    present = {c for c, v in results.items() if v}

    # ---- per-config summary (mean +/- std / CI across seeds) ------------- #
    summary: dict[str, Any] = {}
    for config in present:
        rows = results[config]
        mets = [r[1]["metrics"] for r in rows]
        entry: dict[str, Any] = {"label": CONFIG_LABELS[config], "n_runs": len(rows)}
        for key in METRIC_KEYS:
            vals = [m.get(key) for m in mets]
            entry[key] = t_ci(vals)
        summary[config] = entry

    # ---- day / rain / night breakdown (A-class, pooled across seeds) ----- #
    def per_condition_metrics(config: str) -> dict[str, dict[str, float | None]]:
        """Pool per-sample ADE/FDE/parse across seeds, grouped by condition."""
        per: dict[str, list[dict]] = defaultdict(list)
        for _seed, _m, preds in results[config]:
            for row in preds:
                cond = cond_by_id.get(row.get("id")) or cond_by_scene.get(row.get("scene_token"), "day")
                per[cond].append(row)
        out: dict[str, dict[str, float | None]] = {}
        for cond in ("day", "night", "rain"):
            rs = per.get(cond, [])
            ades = [r["ade_m"] for r in rs if r.get("ade_m") is not None]
            fdes = [r["fde_m"] for r in rs if r.get("fde_m") is not None]
            parse = sum(bool(r.get("parse_ok")) for r in rs) / len(rs) if rs else None
            out[cond] = {
                "n": len(rs),
                "ADE_m": float(np.mean(ades)) if ades else None,
                "FDE_m": float(np.mean(fdes)) if fdes else None,
                "parse_success_rate": parse,
            }
        return out

    conditions: dict[str, Any] = {}
    for config in CONFIGS_A:
        if config in present:
            conditions[config] = per_condition_metrics(config)

    # ---- per-sample vectors for paired tests ----------------------------- #
    def per_sample_ade(config: str) -> list[float]:
        """Pool ADE across seeds by sample id (aligned by id)."""
        by_id: dict[str, list[float]] = defaultdict(list)
        for _seed, _m, preds in results[config]:
            for r in preds:
                if r.get("ade_m") is not None:
                    by_id[r["id"]].append(r["ade_m"])
        ids = sorted(by_id)
        return [float(np.mean(by_id[i])) for i in ids]

    tests: dict[str, Any] = {}
    for a, b_, label in [("A1_SFT", "A2_physics", "A1 vs A2 (physics)"),
                         ("A1_SFT", "A3_jpo", "A1 vs A3 (JPO)"),
                         ("A1_SFT", "A4_vldpo", "A1 vs A4 (VL-DPO)")]:
        if a in present and b_ in present:
            tests[label] = paired_wilcoxon(per_sample_ade(a), per_sample_ade(b_))
    if "D1_no_talk2bev" in present and "D2_talk2bev" in present:
        tests["D1 no-BEV vs D2 Talk2BEV (ADE)"] = paired_wilcoxon(per_sample_ade("D1_no_talk2bev"), per_sample_ade("D2_talk2bev"))
    if "B1_image_text" in present and "B3_image_text_bev" in present:
        tests["B1 Image-Text vs B3 Image-Text+BEV (ADE)"] = paired_wilcoxon(per_sample_ade("B1_image_text"), per_sample_ade("B3_image_text_bev"))

    # ---- qualitative analyses -------------------------------------------- #
    qual: dict[str, Any] = {}
    for config in ("C1_R_to_T", "C2_R_to_A_to_T"):
        if config not in present:
            continue
        n_total = 0
        n_mismatch = 0
        examples: list[dict] = []
        for _seed, _m, preds in results[config]:
            for r in preds:
                mm = r_vs_t_mismatch(r)
                if mm is None:
                    continue
                n_total += 1
                if mm:
                    n_mismatch += 1
                    if len(examples) < 5:
                        pred = r.get("prediction", {})
                        examples.append({"id": r.get("id"), "think": pred.get("think", "")[:160],
                                         "trajectory": pred.get("trajectory")})
        qual[config] = {"r_vs_t_mismatch_rate": n_mismatch / n_total if n_total else None,
                        "r_vs_t_evaluable": n_total, "mismatch_examples": examples}

    scene_ref = {}
    for config in present:
        m = results[config][0][1]["metrics"]
        scene_ref[config] = {"scene_reference_rate": m.get("scene_reference_rate"),
                             "scene_reference_correct_rate": m.get("scene_reference_correct_rate")}

    summary_json = {
        "schema_version": "drivetdpa.abcd.full.report.v1",
        "seeds": seeds,
        "present_configs": sorted(present),
        "missing_configs": sorted(set(CONFIGS_A + CONFIGS_BCD) - present),
        "summary": summary,
        "conditions": conditions,
        "paired_tests": tests,
        "qualitative": qual,
        "scene_reference": scene_ref,
    }
    (report_dir / "results_summary.json").write_text(json.dumps(summary_json, ensure_ascii=False, indent=2) + "\n")

    # ---- markdown report -------------------------------------------------- #
    lines: list[str] = []
    lines.append("# A-D 实验完整结果（NuScenes scene-disjoint 全量 pipeline）\n")
    lines.append(f"- seeds: {seeds}\n- 已评估配置: {len(present)}/{len(CONFIGS_A) + len(CONFIGS_BCD)}\n\n")
    lines.append("## 总体结果（mean ± std across seeds；A 类 95% t 区间）\n")
    lines.append("| 配置 | ADE (m) | FDE (m) | Goal | Parse | A→T | Scene ref | Lat(ms) |")
    lines.append("|---|---|---|---|---|---|---|---|")
    for config in CONFIGS_A + CONFIGS_BCD:
        if config not in present:
            continue
        e = summary[config]
        def fmt(key):
            v = e.get(key, {})
            m = v.get("mean")
            if m is None:
                return "-"
            return f"{m:.4f}±{v.get('std', 0):.4f}"
        lines.append(
            f"| {e['label']} | {fmt('ADE_m')} | {fmt('FDE_m')} | {fmt('Goal')} | {fmt('parse_success_rate')} | "
            f"{fmt('A_to_T_consistency')} | {fmt('scene_reference_rate')} | {fmt('Lat_ms_mean')} |"
        )
    lines.append("\n## Day / Rain / Night 条件（A 类）\n")
    lines.append("| 配置 | 条件 | n | ADE (m) | FDE (m) | Parse |")
    lines.append("|---|---|---|---|---|---|")
    for config in CONFIGS_A:
        if config not in conditions:
            continue
        for cond in ("day", "night", "rain"):
            c = conditions[config][cond]
            ade = f"{c['ADE_m']:.4f}" if c["ADE_m"] is not None else "-"
            fde = f"{c['FDE_m']:.4f}" if c["FDE_m"] is not None else "-"
            pr = f"{c['parse_success_rate']:.2f}" if c["parse_success_rate"] is not None else "-"
            lines.append(f"| {CONFIG_LABELS[config]} | {cond} | {c['n']} | {ade} | {fde} | {pr} |")
    lines.append("\n## 配对检验（Wilcoxon signed-rank，ADE）\n")
    lines.append("| 对比 | n_pairs | p | Cohen's d |")
    lines.append("|---|---|---|---|")
    for label, t in tests.items():
        p = f"{t['p_value']:.4g}" if isinstance(t.get("p_value"), float) else "-"
        d = f"{t['cohens_d']:.3f}" if isinstance(t.get("cohens_d"), float) else "-"
        lines.append(f"| {label} | {t['n_pairs']} | {p} | {d} |")
    lines.append("\n## 定性分析\n")
    for config, q in qual.items():
        lines.append(f"- **{CONFIG_LABELS[config]}** R↔T 方向不一致率: {q['r_vs_t_mismatch_rate']:.3f} "
                     f"（可评估 {q['r_vs_t_evaluable']} 条）" if q['r_vs_t_mismatch_rate'] is not None else f"- **{config}**: 无可评估样本")
    lines.append("\n## 边界说明\n")
    lines.append("- 偏好数据为 surrogate（本地构造 rejected），语音为转写 proxy，评估为 greedy（do_sample=False）。")
    lines.append("- A 类跨训练 seed 汇报；B/C/D 为单 checkpoint 协议消融。")
    lines.append("- parse 失败本身是结果的一部分；ADE_common / ADE_worstcase 见 metrics.json。")
    (report_dir / "ABCD_DATA_ANALYSIS.md").write_text("\n".join(lines) + "\n")

    print(json.dumps(summary_json, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
