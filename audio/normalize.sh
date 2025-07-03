#!/bin/bash

# Exit on error
set -e

# Check argument
if [[ $# -ne 1 || ! -d "$1" ]]; then
    echo "Usage: $0 /path/to/wav_folder"
    exit 1
fi

INPUT_DIR="$(realpath "$1")"
OUTPUT_DIR="$INPUT_DIR/normalized"
TARGET_LUFS="-14"

mkdir -p "$OUTPUT_DIR"

for file in "$INPUT_DIR"/*.wav; do
    [[ -e "$file" ]] || continue
    base="$(basename "$file")"
    out="$OUTPUT_DIR/${base%.*}_norm.wav"

    echo "Normalizing $base → $(basename "$out")"
    ffmpeg -i "$file" -af loudnorm=I=$TARGET_LUFS:TP=-1.5:LRA=11 -ar 44100 -acodec pcm_s16le "$out"
done

echo "All done. Normalized files in: $OUTPUT_DIR"
