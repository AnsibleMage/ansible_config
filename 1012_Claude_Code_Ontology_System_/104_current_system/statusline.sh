#!/bin/bash
# Claude Code StatusLine - Custom Display Script
# 2-line status with colored progress bars

INPUT=$(cat)

# JSON parsing with jq (fallback defaults)
MODEL=$(echo "$INPUT" | jq -r '.model.display_name // "Unknown"')
DURATION_MS=$(echo "$INPUT" | jq -r '.cost.total_duration_ms // 0' | cut -d. -f1)
COST=$(echo "$INPUT" | jq -r '.cost.total_cost_usd // 0')
INPUT_TOKENS=$(echo "$INPUT" | jq -r '.context_window.total_input_tokens // 0' | cut -d. -f1)
OUTPUT_TOKENS=$(echo "$INPUT" | jq -r '.context_window.total_output_tokens // 0' | cut -d. -f1)
CACHE_TOKENS=$(echo "$INPUT" | jq -r '.context_window.current_usage.cache_read_input_tokens // 0' | cut -d. -f1)
CTX_USED_PCT=$(echo "$INPUT" | jq -r '.context_window.used_percentage // 0' | cut -d. -f1)
CTX_SIZE=$(echo "$INPUT" | jq -r '.context_window.context_window_size // 200000' | cut -d. -f1)
CTX_INPUT=$(echo "$INPUT" | jq -r '.context_window.current_usage.input_tokens // 0' | cut -d. -f1)

# Colors
GREEN="\033[32m"
YELLOW="\033[33m"
RED="\033[31m"
BLUE="\033[34m"
MAGENTA="\033[35m"
CYAN="\033[36m"
WHITE="\033[37m"
BOLD="\033[1m"
RESET="\033[0m"
DIM="\033[2m"

# Convert tokens to k format (1234 -> 1.2k, 500 -> 500)
to_k() {
  local n=${1:-0}
  if [ "$n" -ge 1000000 ] 2>/dev/null; then
    printf "%.1fM" "$(echo "scale=1; $n / 1000000" | bc)"
  elif [ "$n" -ge 1000 ] 2>/dev/null; then
    printf "%.1fk" "$(echo "scale=1; $n / 1000" | bc)"
  else
    printf "%d" "$n"
  fi
}

# Convert ms to HH:MM:SS
ms_to_time() {
  local ms=${1:-0}
  local total_sec=$((ms / 1000))
  local h=$((total_sec / 3600))
  local m=$(( (total_sec % 3600) / 60 ))
  local s=$((total_sec % 60))
  printf "%02d:%02d:%02d" "$h" "$m" "$s"
}

# Get ANSI color by percentage (green < 50, yellow < 75, red >= 75)
get_color() {
  local pct=${1:-0}
  if [ "$pct" -lt 50 ] 2>/dev/null; then
    echo -ne "$GREEN"
  elif [ "$pct" -lt 75 ] 2>/dev/null; then
    echo -ne "$YELLOW"
  else
    echo -ne "$RED"
  fi
}

# Progress bar: 16 chars, filled=█ empty=░
progress_bar() {
  local pct=${1:-0}
  # Clamp to 0-100
  [ "$pct" -gt 100 ] 2>/dev/null && pct=100
  [ "$pct" -lt 0 ] 2>/dev/null && pct=0
  local filled=$((pct * 16 / 100))
  local empty=$((16 - filled))
  local bar=""
  for ((i=0; i<filled; i++)); do bar+="█"; done
  for ((i=0; i<empty; i++)); do bar+="░"; done
  echo -n "$bar"
}

# === Format values ===
TOTAL_TOKENS=$((INPUT_TOKENS + OUTPUT_TOKENS + CACHE_TOKENS))
IN_K=$(to_k "$INPUT_TOKENS")
OUT_K=$(to_k "$OUTPUT_TOKENS")
CACHE_K=$(to_k "$CACHE_TOKENS")
TOTAL_K=$(to_k "$TOTAL_TOKENS")
DURATION_FMT=$(ms_to_time "$DURATION_MS")
COST_FMT=$(printf "%.2f" "$COST")

# Context bar
CTX_USED_K=$(to_k "$CTX_INPUT")
CTX_TOTAL_K=$(to_k "$CTX_SIZE")
CTX_COLOR=$(get_color "$CTX_USED_PCT")
CTX_BAR=$(progress_bar "$CTX_USED_PCT")

# Cost color (dynamic: green < $5, yellow < $15, red >= $15)
get_cost_color() {
  local cost_cents=$(echo "$1 * 100" | bc | cut -d. -f1)
  cost_cents=${cost_cents:-0}
  if [ "$cost_cents" -lt 500 ] 2>/dev/null; then
    echo -ne "$GREEN"
  elif [ "$cost_cents" -lt 1500 ] 2>/dev/null; then
    echo -ne "$YELLOW"
  else
    echo -ne "$RED"
  fi
}
COST_COLOR=$(get_cost_color "$COST")

# === Output 2 lines ===
# Line 1: Model, Duration, Cost, Token details
printf "🤖 %b%b%s%b %b│%b ⏱ %b%s%b %b│%b 💰 %b\$%s%b %b│%b 📊 %b%s%b %b%s%b %b%s%b %b%b%s%b\n" \
  "$BOLD" "$CYAN" "$MODEL" "$RESET" \
  "$DIM" "$RESET" \
  "$DIM" "$DURATION_FMT" "$RESET" \
  "$DIM" "$RESET" \
  "$COST_COLOR" "$COST_FMT" "$RESET" \
  "$DIM" "$RESET" \
  "$BLUE" "$IN_K" "$RESET" \
  "$MAGENTA" "$OUT_K" "$RESET" \
  "$CYAN" "$CACHE_K" "$RESET" \
  "$BOLD" "$WHITE" "$TOTAL_K" "$RESET"

# Line 2: Context usage
printf "📐 Context: %b%s%b/%s (%b%s%%%b) %b%s%b\n" \
  "$BOLD" "$CTX_USED_K" "$RESET" \
  "$CTX_TOTAL_K" \
  "$CTX_COLOR" "$CTX_USED_PCT" "$RESET" \
  "$CTX_COLOR" "$CTX_BAR" "$RESET"
