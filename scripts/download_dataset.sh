#!/usr/bin/env bash
set -euo pipefail

manifest=''
scene=''
output=''

while [ "$#" -gt 0 ]; do
  case "$1" in
    --manifest) manifest="$2"; shift 2 ;;
    --scene) scene="$2"; shift 2 ;;
    --output) output="$2"; shift 2 ;;
    *) echo "Unknown argument: $1" >&2; exit 2 ;;
  esac
done

if [ -z "$manifest" ] || [ -z "$scene" ] || [ -z "$output" ]; then
  echo "Usage: $0 --manifest FILE --scene SCENE_ID --output DIRECTORY" >&2
  exit 2
fi

echo "Dataset download is intentionally disabled until a signed release manifest is published."
echo "Requested manifest: $manifest"
echo "Requested scene: $scene"
echo "Requested output: $output"
echo "Implement the downloader only after artifact URIs and SHA256 values are released."
