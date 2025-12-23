#!/usr/bin/env bash

# Usage:
#   ./vid-gen.sh background.png audio.wav [color]
#
# Examples:
#   ./vid-gen.sh bg.png story.wav
#   ./vid-gen.sh bg.png story.wav 81a1c1
#   ./vid-gen.sh bg.png story.wav '#ffb703'
#   ./vid-gen.sh bg.png story.wav 0x00e3c2

if [ "$#" -lt 2 ]; then
    echo "Usage: $0 <background.png> <audio.wav> [color]"
    exit 1
fi

BG="$1"
AUDIO="$2"

# Default color if none given (Nord-ish highlight)
RAW_COLOR="d79921"
# Default mode is horizontal video
VERT=0

# Parse remaining args after BG + AUDIO
shift 2
while [ "$#" -gt 0 ]; do
  case "$1" in
    --vert) VERT=1 ;;
    --color)
      shift
      RAW_COLOR="${1:-81a1c1}"
      ;;
    *)
      # Allow color without --color, but only if it looks like a hex color
      if [[ "$1" =~ ^#?[0-9A-Fa-f]{6}$ ]] || [[ "$1" =~ ^0x[0-9A-Fa-f]{6}$ ]]; then
        RAW_COLOR="$1"
      else
        echo "Unknown argument: $1"
        exit 1
      fi
      ;;
  esac
  shift
done

# Normalize color to 0xRRGGBB
RAW_COLOR="${RAW_COLOR#\#}"
RAW_COLOR="${RAW_COLOR#0x}"
COLOR="0x${RAW_COLOR}"

# Derive output name from audio file: input.wav -> input.mp4
BASE="${AUDIO%.*}"
OUT="${BASE}.mp4"
if [ "$VERT" -eq 1 ]; then
  OUT="${BASE}_vert.mp4"
fi

# Target canvas sizes
if [ "$VERT" -eq 1 ]; then
  OUT_W=1080
  OUT_H=1920
  # Keep strip proportional-ish: 500/2560 ≈ 0.195 -> ~210 on 1080
  STRIP_W=250
else
  OUT_W=2560
  OUT_H=1440
  STRIP_W=500
fi

# 10 bars stacked over the full height -> period is height/10
BARS=40
GAP=4
PERIOD=$(( OUT_H / BARS ))   # currently 144 for 1440p, 192 for 1920p
KEEP=$(( PERIOD - GAP ))   # keep region per bar "slot"

#showfreqs=s=11x500 generates 11 bars with an amplitude of 500px. The 11 bars are trimmed to 10 because the last one is always empty, and then scaled to 1440px.
#the whole thing below calls showfreqs, then performs --> crop --> transpose --> scale --> overlay, so that the result is a 90° rotated graph along the left edge of the video.

# Build video
ffmpeg \
  -loop 1 -i "$BG" \
  -i "$AUDIO" \
  -filter_complex "\
[0:v]scale=${OUT_W}:${OUT_H},setsar=1,format=rgba[bg];\
[1:a]showfreqs=s=$((BARS+1))x${STRIP_W}:mode=bar:ascale=log:fscale=log:win_size=8192:overlap=1:colors=${COLOR},\
crop=${BARS}:${STRIP_W}:0:0,\
transpose=1,\
scale=${STRIP_W}:${OUT_H}:flags=neighbor,\
format=rgba,\
geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='if(lt(mod(Y,${PERIOD}),${KEEP}),alpha(X,Y),0)'[spec];\
[bg][spec]overlay=x=0:y=0:format=auto:shortest=1[v]" \
  -map "[v]" -map 1:a \
  -c:v libx264 -preset slow -crf 18 \
  -c:a aac -b:a 192k \
  -shortest \
  "$OUT"
  
  # for debugging:
echo "--------------------------------------------------------"
echo "VERT=$VERT  OUT_W=$OUT_W OUT_H=$OUT_H STRIP_W=$STRIP_W" "Color=${COLOR}"
echo "--------------------------------------------------------"
