#!/usr/bin/env bash
# DriveTDPA A-D full experiment pipeline (resumable, automatic).
#
# Stages the scene-disjoint / day-rain-night split, trains the A-class ablation
# (A1 SFT, A2 physics, A3 JPO, A4 VL-DPO) with N training seeds, evaluates all
# 12 configurations (A1-A4, B1-B4, C1-C2, D1-D2) with the real predictor, and
# produces the statistical report. Every step is idempotent: a completed step
# (checkpoint with model.safetensors, or eval metrics.json) is skipped on re-run.
#
# Usage:
#   SEEDS="42 17 23" MAX_STEPS=200 TRAIN_LIMIT=3000 \
#     bash scripts/experiments/abcd_full/run_abcd_full.sh
set -euo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-/mnt/workspace/autonomous_driving}"
OUTPUT_ROOT="${OUTPUT_ROOT:-/mnt/workspace/drivetdpa_experiments/abcd_full_20260930}"
BASE_MODEL="${BASE_MODEL:-$PROJECT_ROOT/InternVL3_5-1B}"
SEEDS="${SEEDS:-42 17 23}"
MAX_STEPS="${MAX_STEPS:-200}"
TRAIN_LIMIT="${TRAIN_LIMIT:-3000}"
HELDOUT_SCENES="${HELDOUT_SCENES:-9}"
HELDOUT_PER_SCENE="${HELDOUT_PER_SCENE:-20}"
EVAL_MAX_NEW_TOKENS="${EVAL_MAX_NEW_TOKENS:-1024}"

SCRIPTS="$PROJECT_ROOT/scripts/experiments/abcd_full"
DATA_DIR="$OUTPUT_ROOT/data"
CKPT_DIR="$OUTPUT_ROOT/checkpoints"
EVAL_DIR="$OUTPUT_ROOT/eval"
REPORT_DIR="$OUTPUT_ROOT/report"
LOG_DIR="$OUTPUT_ROOT/logs"
mkdir -p "$DATA_DIR" "$CKPT_DIR" "$EVAL_DIR" "$REPORT_DIR" "$LOG_DIR"

STAGE_SCRIPT="$SCRIPTS/stage_data.py"
TRAIN_SCRIPT="$SCRIPTS/train_one.sh"
EVALUATOR="$PROJECT_ROOT/scripts/experiments/evaluate_nuscenes_rat.py"
SERVER="$PROJECT_ROOT/internvl_chat_gpt_oss/tools/drivetdpa_predict_server.py"
PYTHON_BIN="${PYTHON_BIN:-/usr/local/bin/python3}"

HELDOUT_INPUT="$DATA_DIR/heldout.jsonl"
# dataset-root is irrelevant with absolute image paths, but must exist.
DATASET_ROOT="$OUTPUT_ROOT"

log() { echo "[abcd_full] $*"; }

# --------------------------------------------------------------------------- #
# 1. Stage data (idempotent)
# --------------------------------------------------------------------------- #
if [[ -f "$DATA_DIR/split_manifest.json" ]]; then
  log "stage: already staged -> $DATA_DIR/split_manifest.json"
else
  log "stage: building split (train_limit=$TRAIN_LIMIT heldout_scenes=$HELDOUT_SCENES)"
  "$PYTHON_BIN" "$STAGE_SCRIPT" \
    --output-root "$OUTPUT_ROOT" \
    --train-limit "$TRAIN_LIMIT" \
    --heldout-scenes "$HELDOUT_SCENES" \
    --heldout-per-scene "$HELDOUT_PER_SCENE" \
    2>&1 | tee "$LOG_DIR/stage.log"
  log "stage: done"
fi

# --------------------------------------------------------------------------- #
# 2. Train A-class (A1 first, then A2/A3/A4 from A1 of the same seed)
# --------------------------------------------------------------------------- #
train_if_missing() {
  local config="$1" seed="$2" model="$3" meta="$4"
  local out="$CKPT_DIR/$config/seed$seed"
  if [[ -f "$out/model.safetensors" ]]; then
    log "train: SKIP $config seed$seed (checkpoint exists)"
    return
  fi
  log "train: $config seed$seed <- $model"
  CONFIG="$config" SEED="$seed" MODEL_PATH="$model" META_PATH="$meta" \
    OUTPUT_DIR="$out" MAX_STEPS="$MAX_STEPS" MASTER_PORT="$((34400 + seed))" \
    bash "$TRAIN_SCRIPT" 2>&1 | tee "$LOG_DIR/train_${config}_seed${seed}.log"
  [[ -f "$out/model.safetensors" ]] || { log "train: FAILED $config seed$seed"; exit 1; }
}

for seed in $SEEDS; do
  train_if_missing A1_SFT "$seed" "$BASE_MODEL" "$DATA_DIR/train_sft.meta.json"
  a1="$CKPT_DIR/A1_SFT/seed$seed"
  train_if_missing A2_physics "$seed" "$a1" "$DATA_DIR/A2_physics.meta.json"
  train_if_missing A3_jpo      "$seed" "$a1" "$DATA_DIR/A3_jpo.meta.json"
  train_if_missing A4_vldpo     "$seed" "$a1" "$DATA_DIR/A4_vldpo.meta.json"
done

# --------------------------------------------------------------------------- #
# 3. Evaluate
# --------------------------------------------------------------------------- #
declare -A MODES=(
  [A1_SFT]=full
  [A2_physics]=full
  [A3_jpo]=full
  [A4_vldpo]=full
  [B1_image_text]=image_text
  [B2_image_speech]=image_speech
  [B3_image_text_bev]=full
  [B4_image_speech_bev]=full_speech
  [C1_R_to_T]=trajectory_only
  [C2_R_to_A_to_T]=full
  [D1_no_talk2bev]=no_bev
  [D2_talk2bev]=full
)

REF_SEED="${REF_SEED:-$(echo "$SEEDS" | awk '{print $1}')}"

eval_one() {
  local name="$1" model="$2" mode="$3" out="$4" port="$5"
  if [[ -f "$out/metrics.json" ]]; then
    log "eval: SKIP $name (metrics.json exists)"
    return
  fi
  mkdir -p "$out"
  log "eval: $name mode=$mode port=$port"
  "$PYTHON_BIN" "$SERVER" --model-path "$model" --host 127.0.0.1 --port "$port" \
    --dtype bf16 --max-new-tokens "$EVAL_MAX_NEW_TOKENS" > "$out/server.log" 2>&1 &
  local spid=$!
  local healthy=""
  for _ in $(seq 1 180); do
    if curl -fsS --max-time 2 "http://127.0.0.1:$port/health" >/dev/null 2>&1; then healthy=1; break; fi
    if ! kill -0 "$spid" 2>/dev/null; then break; fi
    sleep 5
  done
  if [[ -z "$healthy" ]]; then
    log "eval: FAILED server for $name (see $out/server.log)"
    kill "$spid" 2>/dev/null || true
    exit 1
  fi
  "$PYTHON_BIN" "$EVALUATOR" \
    --input "$HELDOUT_INPUT" --dataset-root "$DATASET_ROOT" \
    --predict-url "http://127.0.0.1:$port/predict" \
    --health-url "http://127.0.0.1:$port/health" \
    --input-mode "$mode" --output "$out/predictions.jsonl" --report "$out/metrics.json" \
    2>&1 | tee "$LOG_DIR/eval_${name}.log"
  kill "$spid" 2>/dev/null || true
  wait "$spid" 2>/dev/null || true
}

port=18100
# A-class: each training seed's checkpoint gets its own eval.
for config in A1_SFT A2_physics A3_jpo A4_vldpo; do
  for seed in $SEEDS; do
    eval_one "${config}_seed${seed}" "$CKPT_DIR/$config/seed$seed" "${MODES[$config]}" \
      "$EVAL_DIR/$config/seed$seed" "$port"
    port=$((port + 1))
  done
done

# B/C/D: protocol ablations on the A4 reference checkpoint.
a4_ref="$CKPT_DIR/A4_vldpo/seed$REF_SEED"
for config in B1_image_text B2_image_speech B3_image_text_bev B4_image_speech_bev \
             C1_R_to_T C2_R_to_A_to_T D1_no_talk2bev D2_talk2bev; do
  eval_one "$config" "$a4_ref" "${MODES[$config]}" "$EVAL_DIR/$config" "$port"
  port=$((port + 1))
done

# --------------------------------------------------------------------------- #
# 4. Aggregate + report
# --------------------------------------------------------------------------- #
log "aggregate: building statistics and report"
"$PYTHON_BIN" "$SCRIPTS/aggregate_results.py" \
  --eval-root "$EVAL_DIR" --output-root "$OUTPUT_ROOT" \
  --seeds "$SEEDS" --heldout "$HELDOUT_INPUT" 2>&1 | tee "$LOG_DIR/aggregate.log"

log "PIPELINE_PASS output_root=$OUTPUT_ROOT"
