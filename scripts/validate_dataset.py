#!/usr/bin/env python3
"""Validate DriveTDPA CARLA JSON, JSONL, and connected example scenes."""

import argparse
import json
import math
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit

SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
PLACEHOLDERS = {"REPLACE_WITH_SHA256", "REPLACE_WITH_RELEASE_URL"}


def load_records(path):
    if path.suffix == ".jsonl":
        return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    return [json.loads(path.read_text(encoding="utf-8"))]


def finite_tree(value, where, errors):
    if isinstance(value, float) and not math.isfinite(value):
        errors.append(f"{where}: non-finite number")
    elif isinstance(value, dict):
        for key, child in value.items():
            finite_tree(child, f"{where}.{key}", errors)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            finite_tree(child, f"{where}[{index}]", errors)


def validate_uri(uri, where, errors):
    if uri in PLACEHOLDERS or uri.startswith("oss://REPLACE/"):
        return
    parsed = urlsplit(uri)
    if parsed.username or parsed.password or any(k in uri.lower() for k in ("access_key", "secret", "signature=")):
        errors.append(f"{where}: URI appears to contain credentials")
    if parsed.scheme not in ("https", "oss"):
        errors.append(f"{where}: artifact URI must use https or oss")


def validate_record(record, where, errors):
    if "source" in record and record["source"] != "carla":
        errors.append(f"{where}: source must be carla")
    if "dataset_version" in record and not record["dataset_version"].startswith("dataset-carla"):
        errors.append(f"{where}: dataset_version must start with dataset-carla")
    for key in ("artifact_uri", "uri"):
        if key in record:
            validate_uri(record[key], f"{where}.{key}", errors)
    if "sha256" in record and record["sha256"] != "REPLACE_WITH_SHA256" and not SHA256_RE.fullmatch(record["sha256"]):
        errors.append(f"{where}.sha256: expected 64 lowercase hex characters")
    output = record.get("output", {})
    if "trajectory" in output and len(output["trajectory"]) != 6:
        errors.append(f"{where}.output.trajectory: expected exactly 6 points")
    if "action_steps" in output and len(output["action_steps"]) != 3:
        errors.append(f"{where}.output.action_steps: expected exactly 3 steps")
    candidates = record.get("candidates")
    if candidates is not None:
        ids = {candidate.get("candidate_id") for candidate in candidates}
        if len(candidates) < 2:
            errors.append(f"{where}.candidates: expected at least 2 candidates")
        if record.get("chosen") not in ids or record.get("rejected") not in ids:
            errors.append(f"{where}: chosen/rejected must reference candidate IDs")
        if record.get("chosen") == record.get("rejected"):
            errors.append(f"{where}: chosen and rejected must differ")
        if not record.get("selection", {}).get("safety_validated", False):
            errors.append(f"{where}.selection: safety_validated must be true")
    finite_tree(record, where, errors)


def validate_scene(manifest, path, errors):
    required = ("dataset_version", "scene_id", "source", "status", "carla", "records", "artifacts")
    for key in required:
        if key not in manifest:
            errors.append(f"{path}:{key}: missing required field")
    if manifest.get("source") != "carla":
        errors.append(f"{path}: source must be carla")
    if manifest.get("carla", {}).get("synchronous_mode") is not True:
        errors.append(f"{path}: CARLA synchronous_mode must be true")
    base = path.parent
    for relative in manifest.get("records", []):
        child = base / relative
        if not child.is_file():
            errors.append(f"{path}: referenced record missing: {relative}")
            continue
        for record in load_records(child):
            validate_record(record, str(child), errors)
            if "scene_id" in record and record["scene_id"] != manifest.get("scene_id"):
                errors.append(f"{child}: scene_id does not match manifest")
    for index, artifact in enumerate(manifest.get("artifacts", [])):
        validate_record(artifact, f"{path}.artifacts[{index}]", errors)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", type=Path)
    args = parser.parse_args()
    errors = []
    checked = 0
    for path in args.paths:
        if not path.is_file():
            errors.append(f"{path}: file not found")
            continue
        try:
            records = load_records(path)
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{path}: {exc}")
            continue
        checked += len(records)
        for record in records:
            validate_record(record, str(path), errors)
            if path.name == "manifest.json":
                validate_scene(record, path, errors)
    if errors:
        print("FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"PASS: validated {checked} top-level record(s); CARLA provenance and linked scene records are consistent")
    return 0


if __name__ == "__main__":
    sys.exit(main())
