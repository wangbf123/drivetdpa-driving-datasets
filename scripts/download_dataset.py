#!/usr/bin/env python3
"""Download released HTTPS artifacts selected from a JSONL manifest."""

import argparse
import hashlib
import json
import sys
import urllib.request
from pathlib import Path
from urllib.parse import urlsplit


parser = argparse.ArgumentParser()
parser.add_argument("manifest", type=Path)
parser.add_argument("--scene", required=True)
parser.add_argument("--output", type=Path, required=True)
args = parser.parse_args()
records = [json.loads(line) for line in args.manifest.read_text(encoding="utf-8").splitlines() if line.strip()]
selected = [row for row in records if row.get("scene_id") == args.scene]
if not selected:
    sys.exit(f"No manifest entry for scene {args.scene}")
args.output.mkdir(parents=True, exist_ok=True)
for index, row in enumerate(selected):
    uri = row.get("artifact_uri") or row.get("uri", "")
    expected = row.get("sha256", "")
    if "REPLACE_" in uri or expected == "REPLACE_WITH_SHA256":
        sys.exit("Manifest contains placeholders; no released artifact is available")
    parsed = urlsplit(uri)
    if parsed.scheme == "oss":
        sys.exit("oss:// downloads require ossutil or a published HTTPS URL")
    if parsed.scheme != "https" or parsed.username or parsed.password:
        sys.exit("Only credential-free HTTPS artifact URLs are accepted")
    target = args.output / (Path(parsed.path).name or f"artifact_{index}")
    with urllib.request.urlopen(uri, timeout=60) as response, target.open("wb") as output:
        while chunk := response.read(1024 * 1024):
            output.write(chunk)
    actual = hashlib.sha256(target.read_bytes()).hexdigest()
    if actual != expected:
        target.unlink(missing_ok=True)
        sys.exit(f"SHA256 mismatch for {target.name}")
    if row.get("bytes", target.stat().st_size) != target.stat().st_size:
        target.unlink(missing_ok=True)
        sys.exit(f"Byte-size mismatch for {target.name}")
    print(f"PASS {target}")
