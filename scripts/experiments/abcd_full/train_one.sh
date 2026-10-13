#!/usr/bin/env bash
# Train a single A-D configuration for a single seed.
#
#   CONFIG      A1_SFT | A2_physics | A3_jpo | A4_vldpo
#   SEED        integer training seed
#   MODEL_PATH  input checkpoint (base for A1; A1 checkpoint for A2/A3/A4)
#   META_PATH   meta.json for the dataset (train_sft for A1; pref meta for A2/A3/A4)
#   OUTPUT_DIR  where the checkpoint is written
#
# A1 uses SFT (internvl_chat_finetune.py); A2/A3/A4 use preference training
# (internvl_chat_tpo.py) starting from the A1 checkpoint of the same seed, so
# the A-class ablation isolates the preference-optimization stage.
set -euo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-/mnt/workspace/autonomous_driving}"
CURRENT_PATH="$PROJECT_ROOT/internvl_chat_gpt_oss"
CONFIG="${CONFIG:?CONFIG required}"
SEED="${SEED:-42}"
MODEL_PATH="${MODEL_PATH:?MODEL_PATH required}"
META_PATH="${META_PATH:?META_PATH required}"
OUTPUT_DIR="${OUTPUT_DIR:?OUTPUT_DIR required}"
MAX_STEPS="${MAX_STEPS:-200}"
MASTER_PORT="${MASTER_PORT:-34360}"

mkdir -p "$OUTPUT_DIR"
cd "$CURRENT_PATH"
export PYTHONPATH="$CURRENT_PATH:${PYTHONPATH:-}"
export USE_TCS_LOADER=0
export LAUNCHER=pytorch
export WANDB_MODE=disabled
export PYTHONWARNINGS="ignore::pydantic.warnings.UnsupportedFieldAttributeWarning"
export TF_CPP_MIN_LOG_LEVEL=3

if [[ "$CONFIG" == "A1_SFT" ]]; then
  torchrun --standalone --nnodes=1 --nproc-per-node=1 --master-port="$MASTER_PORT" \
    "$CURRENT_PATH/internvl/train/internvl_chat_finetune.py" \
    --model_name_or_path "$MODEL_PATH" \
    --conv_style "internvl2_5" \
    --use_fast_tokenizer False \
    --output_dir "$OUTPUT_DIR" \
    --meta_path "$META_PATH" \
    --force_image_size 448 \
    --max_dynamic_patch 4 \
    --down_sample_ratio 0.5 \
    --drop_path_rate 0.0 \
    --min_num_frame 1 \
    --max_num_frame 1 \
    --freeze_llm False \
    --freeze_mlp False \
    --freeze_backbone True \
    --vision_select_layer -1 \
    --dataloader_num_workers 2 \
    --bf16 True \
    --max_steps "$MAX_STEPS" \
    --per_device_train_batch_size 1 \
    --gradient_accumulation_steps 1 \
    --save_strategy "steps" \
    --save_steps "$MAX_STEPS" \
    --save_total_limit 1 \
    --learning_rate 1e-5 \
    --weight_decay 0.01 \
    --warmup_ratio 0.03 \
    --lr_scheduler_type "cosine" \
    --logging_steps 1 \
    --max_seq_length 4096 \
    --do_train True \
    --grad_checkpoint True \
    --gradient_checkpointing True \
    --dynamic_image_size True \
    --use_thumbnail True \
    --ps_version 'v2' \
    --use_custom_flash_attn False \
    --report_to "none" \
    --use_packed_ds False \
    --remove_unused_columns False \
    --loss_reduction "square" \
    --seed "$SEED" \
    2>&1 | tee -a "$OUTPUT_DIR/training_log.txt"
else
  # A2_physics / A3_jpo / A4_vldpo -> preference (TPO) training.
  torchrun --standalone --nnodes=1 --nproc-per-node=1 --master-port="$MASTER_PORT" \
    "$CURRENT_PATH/internvl/train/internvl_chat_tpo.py" \
    --model_name_or_path "$MODEL_PATH" \
    --output_dir "$OUTPUT_DIR" \
    --meta_path "$META_PATH" \
    --conv_style internvl2_5 \
    --use_fast_tokenizer False \
    --force_image_size 448 \
    --down_sample_ratio 0.5 \
    --dynamic_image_size True \
    --use_thumbnail True \
    --max_dynamic_patch 4 \
    --min_num_frame 1 \
    --max_num_frame 1 \
    --freeze_llm False \
    --freeze_mlp False \
    --freeze_backbone True \
    --vision_select_layer -1 \
    --max_length 8192 \
    --truncation_mode keep_end \
    --bf16 True \
    --do_train \
    --per_device_train_batch_size 1 \
    --gradient_accumulation_steps 1 \
    --learning_rate 1e-6 \
    --warmup_ratio 0.05 \
    --lr_scheduler_type linear \
    --weight_decay 0.0 \
    --max_steps "$MAX_STEPS" \
    --logging_steps 1 \
    --save_strategy steps \
    --save_steps "$MAX_STEPS" \
    --save_total_limit 1 \
    --dataloader_num_workers 2 \
    --remove_unused_columns False \
    --seed "$SEED" \
    --grad_checkpoint True \
    --report_to none \
    2>&1 | tee -a "$OUTPUT_DIR/training_log.txt"
fi

echo "TRAIN_PASS config=$CONFIG seed=$SEED output=$OUTPUT_DIR"
