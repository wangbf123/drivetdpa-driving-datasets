#!/usr/bin/env python3
"""Generate deterministic SHA256 entries without following symlinks."""

import argparse
import hashlib
from pathlib import Path


def digest(path):
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


parser = argparse.ArgumentParser()
parser.add_argument("paths", nargs="+", type=Path)
parser.add_argument("--output", type=Path)
args = parser.parse_args()
files = []
for path in args.paths:
    if path.is_symlink():
        continue
    if path.is_file():
        files.append(path)
    elif path.is_dir():
        files.extend(item for item in path.rglob("*") if item.is_file() and not item.is_symlink())
lines = [f"{digest(path)}  {path.as_posix()}" for path in sorted(set(files), key=lambda p: p.as_posix())]
payload = "\n".join(lines) + ("\n" if lines else "")
if args.output:
    args.output.write_text(payload, encoding="utf-8")
else:
    print(payload, end="")
