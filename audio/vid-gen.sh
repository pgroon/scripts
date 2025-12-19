#!/usr/bin/env bash

# Usage:
#   ./vid-gen.sh background.png audio.wav [color]
#
# Examples:
#   ./vid-gen.sh bg.png story.wav
#   ./vid-gen.sh bg.png story.wav 81a1c1
#   ./vid-gen.sh bg.png story.wav '#ffb703'
#   ./vid-gen.sh bg.png story.wav 0x00e3c2

if [ "$#" -lt 2 ] || [ "$#" -gt 3 ]; then
    echo "Usage: $0 <background.png> <audio.wav> [color]"
    exit 1
fi

BG="$1"
AUDIO="$2"

# Default color if none given (Nord-ish highlight)
RAW_COLOR="${3:-81a1c1}"

# Normalize color: strip leading '#' or '0x' if present, then prepend '0x'
RAW_COLOR="${RAW_COLOR#\#}"
RAW_COLOR="${RAW_COLOR#0x}"
COLOR="0x${RAW_COLOR}"

# Derive output name from audio file: input.wav -> input.mp4
OUT="${AUDIO%.*}.mp4"

#showfreqs=s=32x480 generates 32 bars with an amplitude of 480px.The 32 bars are later scaled to 1440px.
#the whole thing below calls showfreqs, then performs --> crop --> transpose --> scale --> overlay, so that the result is a 90° rotated graph along the left edge of the video.
ffmpeg \
  -loop 1 -i "$BG" \
  -i "$AUDIO" \
  -filter_complex "[1:a]showfreqs=s=11x500:mode=bar:ascale=log:fscale=log:win_size=8192:overlap=1:colors=${COLOR},crop=10:500:0:0,transpose=1,scale=500:1440:flags=neighbor[spec];[0:v][spec]overlay=x=0:y=0:format=auto:shortest=1[v]" \
  -map "[v]" -map 1:a \
  -c:v libx264 -preset slow -crf 18 \
  -c:a aac -b:a 192k \
  -shortest \
  "$OUT"
