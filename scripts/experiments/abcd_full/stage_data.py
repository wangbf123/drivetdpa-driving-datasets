#!/usr/bin/env python3
"""Stage a scene-disjoint, condition-tagged NuScenes split for the A-D experiments.

Data layer of the full automatic pipeline. Reuses the row-building logic of the
audited ``build_nuscenes_mini_sft.py`` but is *scalable*: the three large
relational tables (sample_data ~1.3GB, ego_pose ~0.6GB, sample_annotation
~0.6GB) are streamed with ``ijson`` and indexed, instead of being re-scanned per
sample (the pilot builder is O(samples x annotations), which is fine for
``--limit 50`` but not for a full split).

Adds what the pilot was missing:
  1. A true scene-disjoint split: every staged CAM_FRONT sample is classified as
     held-out (trainval01 shard) or train (trainval02-10 shards) by physical
     image membership (verified 0 scene overlap between the shards).
  2. A day / rain / night condition tag per scene parsed from ``scene.json``.
  3. A2 (physics) / A3 (JPO) / A4 (VL-DPO) preference pairs using the same
     surrogate transforms as the pilot, explicitly labelled.

``image`` is written as an absolute path; training meta uses ``root: "/"`` and
both trainers and evaluator resolve ``os.path.join("/", <abs>)`` / ``Path(root)/<abs>``
to that absolute path, so no unified symlink tree is needed.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

TOOLS_DIR = Path("/mnt/workspace/autonomous_driving/internvl_chat_gpt_oss/tools")
sys.path.insert(0, str(TOOLS_DIR))

import ijson  # noqa: E402
import build_nuscenes_mini_sft as b  # noqa: E402


# --------------------------------------------------------------------------- #
# Condition tagging (day / rain / night) from scene.description
# --------------------------------------------------------------------------- #
def tag_condition(description: str) -> str:
    text = (description or "").lower()
    if "night" in text:
        return "night"
    if "rain" in text or "snow" in text:
        return "rain"
    return "day"


# --------------------------------------------------------------------------- #
# Preference transforms (surrogate, matching build_abcd_nuscenes_configs.py)
# --------------------------------------------------------------------------- #
def _replace_trajectory(answer: str, points: list[tuple[float, float]]) -> str:
    return re.sub(
        r"(### 3-second trajectory:\s*)\[[^\]]*\]",
        lambda m: m.group(1) + str(points),
        answer,
        count=1,
    )


def perturb_physics(answer: str) -> str:
    return _replace_trajectory(answer, [(0.0, 1.0), (1.8, 2.0), (-1.7, 3.0), (2.4, 4.0), (-2.2, 5.0), (3.0, 6.0)])


def perturb_inconsistent(answer: str) -> str:
    out = answer.replace("FOLLOW_LANE", "VEER_LEFT", 1).replace("ACCELERATE", "BRAKE", 1)
    return _replace_trajectory(out, [(4.0, 1.0), (3.5, 2.0), (3.0, 3.0), (2.5, 4.0), (2.0, 5.0), (1.5, 6.0)])


def perturb_visual(answer: str) -> str:
    think = re.sub(
        r"<think>.*?</think>",
        "<think>The image is difficult to interpret; continue with a generic plan without explicit scene evidence.</think>",
        answer,
        count=1,
        flags=re.S,
    )
    return perturb_inconsistent(think)


PREFERENCE_TRANSFORMS = {
    "A2_physics": perturb_physics,
    "A3_jpo": perturb_inconsistent,
    "A4_vldpo": perturb_visual,
}


# --------------------------------------------------------------------------- #
# File membership
# --------------------------------------------------------------------------- #
def cam_front_abs_paths(root: Path) -> dict[str, str]:
    d = root / "samples" / "CAM_FRONT"
    if not d.is_dir():
        return {}
    return {p.name: str(p) for p in d.iterdir() if p.is_file()}


# --------------------------------------------------------------------------- #
# Indexed object building (replaces the O(n^2) scan in the pilot builder)
# --------------------------------------------------------------------------- #
def build_objects_indexed(
    anns: list[dict[str, Any]],
    ego_xy: tuple[float, float],
    ego_yaw: float,
    instance_by_token: dict[str, Any],
    category_by_token: dict[str, Any],
    max_distance: float,
) -> list[dict[str, Any]]:
    objects: list[dict[str, Any]] = []
    for ann in anns:
        x_right, y_forward = b.global_to_ego_right_forward(
            (float(ann["translation"][0]), float(ann["translation"][1])), ego_xy, ego_yaw
        )
        distance = (x_right * x_right + y_forward * y_forward) ** 0.5
        if distance > max_distance:
            continue
        category = b.category_for_annotation(ann, instance_by_token, category_by_token)
        kind = b.simplify_category(category)
        relation = b.lane_relation(x_right, y_forward)
        objects.append({
            "type": kind,
            "category": category,
            "x_right": round(x_right, 3),
            "y_forward": round(y_forward, 3),
            "distance_m": round(distance, 3),
            "lane_relation": relation,
            "risk": b.risk_label(kind, relation, distance, y_forward),
        })
    objects.sort(key=lambda item: item["distance_m"])
    return objects


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--meta-dir", type=Path,
                    default=Path("/mnt/workspace/drivetdpa_experiments/oss_auto_train/.staging/meta/v1.0-trainval"))
    ap.add_argument("--heldout-root", type=Path,
                    default=Path("/mnt/workspace/drivetdpa_experiments/oss_trainval01_smoke10_20260923/dataset"))
    ap.add_argument("--train-roots", type=Path, nargs="+",
                    default=[Path(f"/mnt/workspace/drivetdpa_experiments/oss_auto_train/trainval{i:02d}_n50_s50_20260923/dataset") for i in range(2, 11)])
    ap.add_argument("--output-root", type=Path,
                    default=Path("/mnt/workspace/drivetdpa_experiments/abcd_full_20260930"))
    ap.add_argument("--train-limit", type=int, default=3000)
    ap.add_argument("--heldout-per-scene", type=int, default=20)
    ap.add_argument("--heldout-scenes", type=int, default=8)
    ap.add_argument("--future-steps", type=int, default=6)
    ap.add_argument("--max-distance", type=float, default=50.0)
    args = ap.parse_args()

    md = args.meta_dir
    out = args.output_root
    data_dir = out / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    # ---- small tables (full load) ------------------------------------- #
    scene_rows = json.loads((md / "scene.json").read_text())
    scene_cond = {s["token"]: tag_condition(s.get("description", "")) for s in scene_rows}
    sample_rows = json.loads((md / "sample.json").read_text())
    sample_by_token = {s["token"]: s for s in sample_rows}
    calibrated_sensor_rows = json.loads((md / "calibrated_sensor.json").read_text())
    sensor_by_token = {s["token"]: s for s in json.loads((md / "sensor.json").read_text())}
    cs_by_token = {c["token"]: c for c in calibrated_sensor_rows}
    instance_by_token = {i["token"]: i for i in json.loads((md / "instance.json").read_text())}
    category_by_token = {c["token"]: c for c in json.loads((md / "category.json").read_text())}

    # ---- staged image membership -------------------------------------- #
    held_files = cam_front_abs_paths(args.heldout_root)
    train_files: dict[str, str] = {}
    for r in args.train_roots:
        train_files.update(cam_front_abs_paths(r))
    staged = held_files | train_files  # basename -> abs path (train wins on clash)

    # ---- stream sample_data: keep staged CAM_FRONT rows ---------------- #
    # channel resolution: sample_data -> calibrated_sensor -> sensor.channel
    cam_front_by_sample: dict[str, dict[str, Any]] = {}
    needed_ego_tokens: set[str] = set()
    with (md / "sample_data.json").open("rb") as f:
        for row in ijson.items(f, "item", use_float=True):
            cs = cs_by_token.get(row.get("calibrated_sensor_token", ""))
            sensor = sensor_by_token.get(cs.get("sensor_token", "")) if cs else None
            if sensor is None or sensor.get("channel") != "CAM_FRONT":
                continue
            fname = Path(row.get("filename", "")).name
            if fname not in staged:
                continue
            st = row.get("sample_token")
            prev = cam_front_by_sample.get(st)
            if prev is None or (bool(row.get("is_key_frame")) and not bool(prev.get("is_key_frame"))):
                cam_front_by_sample[st] = row
            needed_ego_tokens.add(row.get("ego_pose_token", ""))

    # ---- stream ego_pose: keep only needed tokens ---------------------- #
    ego_pose_by_token: dict[str, dict[str, Any]] = {}
    with (md / "ego_pose.json").open("rb") as f:
        for row in ijson.items(f, "item", use_float=True):
            if row.get("token") in needed_ego_tokens:
                ego_pose_by_token[row["token"]] = row

    # ---- stream sample_annotation: index by staged sample token -------- #
    staged_sample_tokens = set(cam_front_by_sample.keys())
    ann_by_sample: dict[str, list[dict[str, Any]]] = {t: [] for t in staged_sample_tokens}
    with (md / "sample_annotation.json").open("rb") as f:
        for ann in ijson.items(f, "item", use_float=True):
            st = ann.get("sample_token")
            if st in staged_sample_tokens:
                ann_by_sample[st].append(ann)

    # ---- build rows (all staged scenes) -------------------------------- #
    all_rows: list[dict[str, Any]] = []
    for sample in sorted(sample_rows, key=lambda x: x.get("timestamp", 0)):
        cam = cam_front_by_sample.get(sample["token"])
        if cam is None:
            continue
        fname = Path(cam["filename"]).name
        if fname not in staged:
            continue
        image_abs = staged[fname]

        # future chain (within the scene, so all in the same shard / staged)
        fut = b.future_samples(sample, sample_by_token, args.future_steps)
        if fut is None:
            continue
        ego_pose = ego_pose_by_token.get(cam["ego_pose_token"])
        if ego_pose is None:
            continue
        ego_xy = (float(ego_pose["translation"][0]), float(ego_pose["translation"][1]))
        ego_yaw = b.yaw_from_quaternion_wxyz(ego_pose["rotation"])
        trajectory: list[tuple[float, float]] = []
        ok = True
        for fs in fut:
            fc = cam_front_by_sample.get(fs["token"])
            if fc is None:
                ok = False
                break
            fe = ego_pose_by_token.get(fc["ego_pose_token"])
            if fe is None:
                ok = False
                break
            xr, yf = b.global_to_ego_right_forward(
                (float(fe["translation"][0]), float(fe["translation"][1])), ego_xy, ego_yaw
            )
            trajectory.append((xr, yf))
        if not ok or len(trajectory) != args.future_steps:
            continue

        objects = build_objects_indexed(
            ann_by_sample[sample["token"]], ego_xy, ego_yaw,
            instance_by_token, category_by_token, args.max_distance,
        )
        scene_context = b.build_scene_context(objects, max_objects=12)
        actions = b.make_action_sequence(trajectory)
        st = sample.get("scene_token")
        all_rows.append({
            "id": sample["token"],
            "source": "nuscenes",
            "source_version": "v1.0-trainval",
            "scene_token": st,
            "condition": scene_cond.get(st, "day"),
            "timestamp_us": sample.get("timestamp"),
            "image": image_abs,
            "question": b.build_question(scene_context),
            "answer": b.build_answer(actions, trajectory, scene_context),
            "gt_waypoints": b.format_points(trajectory),
            "bev_context": {"objects": objects, "scene_context": scene_context,
                            "coordinate": {"type": "ego_centric", "x_axis": "right_positive",
                                           "y_axis": "forward_positive", "unit": "meter"}},
            "label_provenance": {"trajectory": "future_nuscenes_ego_pose_6x0.5s",
                                 "actions": "heuristically_derived_from_future_ego_trajectory",
                                 "trajectory_is_ground_truth": True,
                                 "actions_are_pseudo_labels": True,
                                 "preference_judge_must_not_receive_ground_truth": True},
            "conversations": [{"from": "human", "value": b.build_question(scene_context)},
                              {"from": "gpt", "value": b.build_answer(actions, trajectory, scene_context)}],
        })

    # ---- scene-level stratified split ----------------------------------- #
    by_scene: dict[str, list[dict[str, Any]]] = {}
    for r in all_rows:
        by_scene.setdefault(r["scene_token"], []).append(r)

    def select_heldout_scenes(n: int) -> list[str]:
        pools = {"day": [], "night": [], "rain": []}
        for s, rs in by_scene.items():
            pools[scene_cond.get(s, "day")].append(s)
        for c in pools:
            pools[c].sort(key=lambda s: -len(by_scene[s]))
        chosen: list[str] = []
        idx = {"day": 0, "night": 0, "rain": 0}
        order = ("day", "night", "rain")
        while len(chosen) < n:
            progressed = False
            for c in order:
                if len(chosen) >= n:
                    break
                if idx[c] < len(pools[c]):
                    chosen.append(pools[c][idx[c]])
                    idx[c] += 1
                    progressed = True
            if not progressed:
                break
        return chosen

    chosen_scenes = select_heldout_scenes(args.heldout_scenes)
    chosen_set = set(chosen_scenes)
    heldout_rows: list[dict[str, Any]] = []
    for s in chosen_scenes:
        heldout_rows.extend(by_scene[s][: args.heldout_per_scene])

    train_pool = [r for r in all_rows if r["scene_token"] not in chosen_set]
    train_rows = train_pool
    if args.train_limit > 0:
        train_by_scene: dict[str, list[dict[str, Any]]] = {}
        for r in train_pool:
            train_by_scene.setdefault(r["scene_token"], []).append(r)
        per_scene = max(1, args.train_limit // max(1, len(train_by_scene)))
        picked: list[dict[str, Any]] = []
        for s in sorted(train_by_scene):
            picked.extend(train_by_scene[s][:per_scene])
        picked = sorted(picked, key=lambda r: r["timestamp_us"] or 0)
        train_rows = picked[: args.train_limit]

    # ---- emit ----------------------------------------------------------- #
    def write_jsonl(path: Path, rs: list[dict[str, Any]]) -> None:
        path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rs))

    write_jsonl(data_dir / "train_sft.jsonl", train_rows)
    write_jsonl(data_dir / "heldout.jsonl", heldout_rows)

    for name, transform in PREFERENCE_TRANSFORMS.items():
        pref = [{
            "id": r["id"], "image": r["image"], "question": r["question"],
            "chosen": r["answer"], "rejected": transform(r["answer"]),
            "gt_waypoints": r.get("gt_waypoints"), "scene_token": r.get("scene_token"),
            "condition": r.get("condition"), "reward_variant": name,
            "preference_source": "surrogate_preference",
            "preference_status": "surrogate-preference: rejected answer locally constructed for ablation; not a real reward rollout",
        } for r in train_rows]
        write_jsonl(data_dir / f"{name}.jsonl", pref)
        (data_dir / f"{name}.meta.json").write_text(json.dumps({
            "NUSCENES": {"annotation": str((data_dir / f"{name}.jsonl").resolve()),
                         "root": "/", "repeat_time": 1, "preference_source": "surrogate_preference"},
        }, ensure_ascii=False, indent=2) + "\n")

    (data_dir / "train_sft.meta.json").write_text(json.dumps({
        "NUSCENES_TRAIN": {"annotation": str((data_dir / "train_sft.jsonl").resolve()),
                           "root": "/", "repeat_time": 1, "length": len(train_rows),
                           "scene_count": len({r["scene_token"] for r in train_rows})},
    }, ensure_ascii=False, indent=2) + "\n")
    (data_dir / "heldout.meta.json").write_text(json.dumps({
        "NUSCENES_HELDOUT": {"annotation": str((data_dir / "heldout.jsonl").resolve()),
                             "root": "/", "repeat_time": 1, "length": len(heldout_rows),
                             "scene_count": len({r["scene_token"] for r in heldout_rows})},
    }, ensure_ascii=False, indent=2) + "\n")

    manifest = {
        "schema_version": "drivetdpa.abcd.full.stage.v1",
        "train_samples": len(train_rows),
        "train_scenes": len({r["scene_token"] for r in train_rows}),
        "heldout_samples": len(heldout_rows),
        "heldout_scenes": len({r["scene_token"] for r in heldout_rows}),
        "heldout_scene_tokens": sorted({r["scene_token"] for r in heldout_rows}),
        "heldout_condition_counts": {c: sum(1 for r in heldout_rows if r["condition"] == c) for c in ("day", "night", "rain")},
        "train_condition_counts": {c: sum(1 for r in train_rows if r["condition"] == c) for c in ("day", "night", "rain")},
        "scene_disjoint": True,
        "preference": "surrogate (physics/jpo/vldpo rejected answers locally constructed)",
        "speech": "transcript proxy (no audio encoder)",
        "seeds_note": "training seeds applied by the driver; eval is greedy (do_sample=False)",
    }
    (data_dir / "split_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
