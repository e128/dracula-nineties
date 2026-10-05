#!/usr/bin/env bash
set -euo pipefail

# Truecolor (24-bit) projections of dracula-nineties.css's dark :root tokens, computed the
# same way mermaid-palette.json documents its own hex projections: oklch() through
# Oklab -> linear sRGB, gamut-clipped. Recompute with
# `python3 .github/palette-check.py --dump` if dracula-nineties.css's :root values move.
#
# The progress bar's three grades are --data-1, --data-2 and --purple. It read --link for
# the middle grade until v2.1.0, but --data-1 and --link are now the same upstream cyan
# (#8be9fd), which collapsed grades one and two into one colour. --data-2 keeps three
# distinct steps. --link is still the timer's colour.
PURPLE='189;147;249'    # --purple  #bd93f9
LINK='139;233;253'      # --link    #8be9fd
LABEL='192;192;192'     # --label   #c0c0c0
MUTED='128;128;128'     # --muted   #808080
RULE='102;102;102'      # --rule-light #666666
GREEN='80;250;123'      # --green   #50fa7b
ORANGE='255;184;108'    # --orange  #ffb86c
RED='255;85;85'         # --red     #ff5555
PINK='255;121;198'      # --pink    #ff79c6
DATA1='139;233;253'     # --data-1  #8be9fd
DATA2='255;121;198'     # --data-2  #ff79c6

DATA=$(cat)

# Extract fields via single jq call
IFS=$'\t' read -r CLI_VERSION MODEL MODEL_ID DIR PCT DURATION_MS ADDED REMOVED < <(
    echo "$DATA" | jq -r '[
        (.version // ""),
        (.model.display_name // "Claude"),
        (try (.model.id // "unknown") catch "unknown"),
        (.cwd // "~" | split("/") | last),
        (try (
    if (.context_window.remaining_percentage // null) != null then
      100 - (.context_window.remaining_percentage | floor)
    elif (.context_window.context_window_size // 0) > 0 then
      (((.context_window.current_usage.input_tokens // 0) +
        (.context_window.current_usage.cache_creation_input_tokens // 0) +
        (.context_window.current_usage.cache_read_input_tokens // 0)) * 100 /
       .context_window.context_window_size) | floor
    else 0 end
  ) catch 0),
        (.cost.total_duration_ms // 0),
        (.cost.total_lines_added // 0),
        (.cost.total_lines_removed // 0)
    ] | @tsv'
)

# Git info
BRANCH=$(git -c core.useBuiltinFSMonitor=false branch --show-current 2>/dev/null || echo "")

# Latest released version (local tag, whatever repo cwd is in)
VERSION=$(git -c core.useBuiltinFSMonitor=false describe --tags --abbrev=0 2>/dev/null || echo "")
CI_ICON=""
[ -n "$VERSION" ] && CI_ICON="\033[38;2;${PINK}m🏷  $VERSION\033[0m"

# Build progress bar
FILLED=$((PCT * 10 / 100))
EMPTY=$((10 - FILLED))
BAR=""
for ((i=0; i<FILLED; i++)); do
  if [ $i -lt 3 ]; then BAR+="\033[38;2;${DATA1}m█"
  elif [ $i -lt 6 ]; then BAR+="\033[38;2;${DATA2}m█"
  else BAR+="\033[38;2;${PURPLE}m█"
  fi
done
for ((i=0; i<EMPTY; i++)); do BAR+="\033[38;2;${RULE}m⣀"; done

# Format duration
TOTAL_SEC=$((DURATION_MS / 1000))
H=$((TOTAL_SEC / 3600))
M=$(((TOTAL_SEC % 3600) / 60))
S=$((TOTAL_SEC % 60))
if [ "$H" -gt 0 ]; then TIME="${H}h ${M}m"
elif [ "$M" -gt 0 ]; then TIME="${M}m ${S}s"
else TIME="${S}s"
fi

# Threshold colors (mirrors dracula-nineties.css's .verdict-pass/-partial/-failed hues)
if [ "$PCT" -gt 80 ]; then CTX_CLR="\033[38;2;${RED}m"
elif [ "$PCT" -gt 50 ]; then CTX_CLR="\033[38;2;${ORANGE}m"
else CTX_CLR="\033[38;2;${GREEN}m"
fi

# Split display name into model + version (e.g. "Opus 4.6" → "Opus" + "4.6")
MODEL_BASE="${MODEL%% *}"
MODEL_VER="${MODEL#* }"
[ "$MODEL_VER" = "$MODEL_BASE" ] && MODEL_VER=""

MODEL_STR="\033[1;38;2;${PURPLE}m$MODEL_BASE\033[0m"
[ -n "$MODEL_VER" ] && MODEL_STR="$MODEL_STR \033[38;2;${MUTED}m$MODEL_VER\033[0m"

CLI_VER_STR=""
[ -n "$CLI_VERSION" ] && CLI_VER_STR="\033[38;2;${MUTED}mv$CLI_VERSION\033[0m\033[2;38;2;${RULE}m ║ \033[0m"

echo -e "\033[38;2;${PURPLE}m🏴‍☠️\033[0m ${CLI_VER_STR}$MODEL_STR\033[2;38;2;${RULE}m ║ \033[0m\033[38;2;${LABEL}m📁 $DIR\033[0m\033[2;38;2;${RULE}m ║ \033[0m$([ -n "$BRANCH" ] && printf '%b' "\033[38;2;${GREEN}m🌿 $BRANCH\033[0m")\033[2;38;2;${RULE}m ║ \033[0m$CI_ICON\033[0m\033[2;38;2;${RULE}m ║ \033[0m$BAR\033[0m ${CTX_CLR}$PCT%\033[0m\033[2;38;2;${RULE}m ║ \033[0m\033[38;2;${LINK}m$TIME\033[0m\033[2;38;2;${RULE}m ║ \033[0m\033[38;2;${GREEN}m+$ADDED\033[0m \033[38;2;${RED}m-$REMOVED\033[0m\033[0m"
