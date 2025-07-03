#!/bin/bash

# pad_audio_files.sh – Adds 200 ms of silence to the start and end of all .wav files in a folder
# Usage: "pad_audio_files.sh /path/to/folder"

# Exit immediately if any command fails
set -e

# Check that a path was given
if [ -z "$1" ]; then
    echo "Usage: $0 /path/to/folder"
    exit 1
fi

# Resolve the absolute path of the input directory
INPUT_DIR=$(realpath "$1")

# Verify that it’s a valid directory
if [ ! -d "$INPUT_DIR" ]; then
    echo "Error: '$INPUT_DIR' is not a directory."
    exit 1
fi

# Output directory for padded files
OUTPUT_DIR="$INPUT_DIR/padded"

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

echo "Processing .wav files in: $INPUT_DIR"
echo "Saving padded versions to: $OUTPUT_DIR"

# Loop through all .wav files in the input directory
for file in "$INPUT_DIR"/*.wav; do
    filename=$(basename "$file")
    echo "  → Padding: $filename"

    # Use sox to add 0.2 seconds of silence at the start and end
    sox "$file" "$OUTPUT_DIR/$filename" pad 0.2 0.2
done

echo "Done. All padded files are in: $OUTPUT_DIR"
