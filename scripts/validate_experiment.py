#!/usr/bin/env python3
"""离线验证自动实验 run 的关联、真实性标记和 SHA256。"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path, jsonl: bool = False):
    if jsonl:
        return [
            json.loads(line)
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
    return json.loads(path.read_text(encoding="utf-8"))


def validate_run(run_dir: Path) -> list[str]:
    errors = []
    manifest_path = run_dir / "run_manifest.json"
    if not manifest_path.is_file():
        return [f"{run_dir}: 缺少 run_manifest.json"]
    manifest = load_json(manifest_path)
    if manifest.get("status") != "PASS":
        errors.append(f"{run_dir}: status 不是 PASS")
    if manifest.get("source") != "carla":
        errors.append(f"{run_dir}: source 不是 carla")
    if manifest.get("run_id") != run_dir.name:
        errors.append(f"{run_dir}: run_id 与目录名不一致")
    for name, artifact in manifest.get("artifacts", {}).items():
        path = run_dir / artifact.get("relative_path", "")
        if not path.is_file():
            errors.append(f"{run_dir}: 缺少 artifact {name}")
            continue
        if path.stat().st_size != artifact.get("bytes"):
            errors.append(f"{path}: 文件大小不一致")
        if sha256_file(path) != artifact.get("sha256"):
            errors.append(f"{path}: SHA256 不一致")

    required = {
        "source": run_dir / "source_manifest.json",
        "health": run_dir / "model_health.json",
        "stats": run_dir / "preference_stats.json",
        "audit": run_dir / "preference_audit.jsonl",
        "pairs": run_dir / "preference_pairs.jsonl",
        "loader": run_dir / "loader_audit.json",
    }
    if any(not path.is_file() for path in required.values()):
        return errors
    source = load_json(required["source"])
    health = load_json(required["health"])
    stats = load_json(required["stats"])
    audits = load_json(required["audit"], jsonl=True)
    pairs = load_json(required["pairs"], jsonl=True)
    loader = load_json(required["loader"])
    image = run_dir / "carla_front.png"
    expected_image_hash = source.get("selected", {}).get("image_sha256")
    if not image.is_file() or sha256_file(image) != expected_image_hash:
        errors.append(f"{run_dir}: CARLA 图片与源 manifest 哈希不一致")
    identity = health.get("model_identity", {})
    if health.get("ok") is not True or health.get("mock") is not False:
        errors.append(f"{run_dir}: model health 没有证明 mock=false")
    if identity.get("mock") is not False or not identity.get("model_path"):
        errors.append(f"{run_dir}: 缺少真实模型身份")
    if stats.get("status") != "PASS" or stats.get("real_judge_evidence") is not True:
        errors.append(f"{run_dir}: preference stats 未通过真实 judge 检查")
    if stats.get("fallback_samples") != 0:
        errors.append(f"{run_dir}: preference 存在 fallback")
    if not audits or any(item.get("fallback") is not False for item in audits):
        errors.append(f"{run_dir}: audit 缺失或包含 fallback")
    if not pairs:
        errors.append(f"{run_dir}: 没有 preference pair")
    for pair in pairs:
        if pair.get("chosen_candidate_id") == pair.get("rejected_candidate_id"):
            errors.append(f"{run_dir}: chosen/rejected ID 相同")
        if not pair.get("chosen") or not pair.get("rejected"):
            errors.append(f"{run_dir}: chosen/rejected 文本为空")
    if loader.get("status") != "PASS":
        errors.append(f"{run_dir}: TPO loader audit 未通过")
    scope = manifest.get("scope", {})
    if scope.get("official_talk2bev_entrypoint") != "BLOCKED_NOT_EXECUTED":
        errors.append(f"{run_dir}: official Talk2BEV 状态被错误提升")
    if scope.get("live_vehicle_closed_loop_in_this_run") is not False:
        errors.append(f"{run_dir}: recorded-seed 实验被错误标为实时闭环")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path)
    args = parser.parse_args()
    errors = []
    checked = 0
    for path in args.paths:
        run_dirs = sorted(path.glob("*/run_manifest.json")) if path.is_dir() and path.name == "runs" else []
        if run_dirs:
            for manifest in run_dirs:
                errors.extend(validate_run(manifest.parent))
                checked += 1
        else:
            errors.extend(validate_run(path))
            checked += 1
    if errors:
        print("FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"PASS: 已验证 {checked} 个自动实验 run")
    return 0


if __name__ == "__main__":
    sys.exit(main())
