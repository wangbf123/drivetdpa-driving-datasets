#!/usr/bin/env python3
"""将本机 DriveTDPA 自动实验的小型产物导入公共数据仓库。"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


FILES = {
    "carla_front": "seed/carla_front.png",
    "scene_context": "seed/scene_context.json",
    "source_manifest": "seed/source_manifest.json",
    "model_health": "model_health.json",
    "rollout_group": "rollout_group.jsonl",
    "preference_pairs": "preference_pairs.jsonl",
    "preference_audit": "preference_audit.jsonl",
    "preference_stats": "preference_stats.json",
    "loader_audit": "loader_audit.json",
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def atomic_text(path: Path, value: str) -> None:
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(value, encoding="utf-8")
    os.replace(temporary, path)


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON 根节点必须是对象: {path}")
    return value


def update_index(repository: Path) -> list[dict[str, Any]]:
    runs_root = repository / "experiments" / "runs"
    records = []
    for manifest_path in sorted(runs_root.glob("*/run_manifest.json")):
        value = load_json(manifest_path)
        records.append(
            {
                "run_id": value["run_id"],
                "created_at": value["created_at"],
                "status": value["status"],
                "source": value["source"],
                "dataset_version": value["dataset_version"],
                "candidate_count": value.get("metrics", {}).get("candidate_count"),
                "accepted_candidates": value.get("metrics", {}).get(
                    "accepted_candidates"
                ),
                "preference_pairs": value.get("metrics", {}).get(
                    "preference_pairs"
                ),
                "fallback_samples": value.get("metrics", {}).get(
                    "fallback_samples"
                ),
                "judge_confidence": value.get("metrics", {}).get(
                    "judge_confidence"
                ),
                "manifest": str(manifest_path.relative_to(repository)),
                "manifest_sha256": sha256_file(manifest_path),
            }
        )
    index_path = repository / "experiments" / "index.jsonl"
    atomic_text(
        index_path,
        "".join(
            json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n"
            for record in records
        ),
    )
    return records


def update_reports(repository: Path, records: list[dict[str, Any]]) -> None:
    latest = records[-1] if records else None
    lines = [
        "# 最新自动实验报告",
        "",
        f"更新时间：{datetime.now(timezone.utc).isoformat()}",
        "",
    ]
    if latest is None:
        lines.append("目前还没有通过导入器发布的真实实验 run。")
    else:
        lines.extend(
            [
                f"最新 run：[`{latest['run_id']}`](../{latest['manifest']})",
                "",
                "```text",
                f"STATUS={latest['status']}",
                f"SOURCE={latest['source']}",
                f"CANDIDATE_COUNT={latest['candidate_count']}",
                f"ACCEPTED_CANDIDATES={latest['accepted_candidates']}",
                f"PREFERENCE_PAIRS={latest['preference_pairs']}",
                f"FALLBACK_SAMPLES={latest['fallback_samples']}",
                f"JUDGE_CONFIDENCE={latest['judge_confidence']}",
                "```",
                "",
                "该 run 使用已录制 CARLA 相机/场景种子重新执行真实 DriveTDPA 多次采样、",
                "安全门控、真实 VLM judge 和 TPO loader。它不是实时 CARLA 车辆闭环重跑。",
                "官方 Talk2BEV entrypoint 与 NVIDIA GPU 渲染状态仍按 manifest 保持 BLOCKED。",
                "",
                f"当前共发布 {len(records)} 个自动实验 run。机器可读索引见",
                "[`experiments/index.jsonl`](../experiments/index.jsonl)。",
            ]
        )
    atomic_text(repository / "reports" / "latest.md", "\n".join(lines) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-run", type=Path, required=True)
    parser.add_argument("--repository", type=Path, required=True)
    args = parser.parse_args()

    source_manifest_path = args.source_run / "run_manifest.json"
    if not source_manifest_path.is_file():
        raise SystemExit(f"缺少 run manifest: {source_manifest_path}")
    manifest = load_json(source_manifest_path)
    if manifest.get("status") != "PASS" or manifest.get("source") != "carla":
        raise SystemExit("只允许导入通过全部检查的 CARLA run")
    run_id = str(manifest.get("run_id", "")).strip()
    if not run_id or Path(run_id).name != run_id:
        raise SystemExit("run_id 非法")

    output = args.repository / "experiments" / "runs" / run_id
    if output.exists():
        raise SystemExit(f"拒绝覆盖已经发布的不可变 run: {output}")
    output.mkdir(parents=True)
    try:
        artifacts = {}
        for name, relative in FILES.items():
            source = args.source_run / relative
            if not source.is_file():
                raise FileNotFoundError(source)
            destination = output / Path(relative).name
            shutil.copy2(source, destination)
            artifacts[name] = {
                "relative_path": destination.name,
                "bytes": destination.stat().st_size,
                "sha256": sha256_file(destination),
            }
        public_manifest = dict(manifest)
        public_manifest["publication"] = {
            "repository": "https://github.com/wangbf123/drivetdpa-driving-datasets",
            "relative_run_path": str(output.relative_to(args.repository)),
            "large_source_bag_published": False,
            "note": "完整 rosbag 未提交 Git；源文件哈希保留在 source_manifest.json。",
        }
        public_manifest["artifacts"] = artifacts
        atomic_text(
            output / "run_manifest.json",
            json.dumps(public_manifest, ensure_ascii=False, indent=2, sort_keys=True)
            + "\n",
        )
    except Exception:
        shutil.rmtree(output)
        raise

    records = update_index(args.repository)
    update_reports(args.repository, records)
    print(
        json.dumps(
            {
                "status": "PASS",
                "run_id": run_id,
                "output": str(output),
                "published_runs": len(records),
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
