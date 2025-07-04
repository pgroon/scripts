#!/bin/bash

# Usage: ./select.sh /path/to/folder

# Ensure a directory is passed
if [ -z "$1" ]; then
  echo "Usage: $0 /path/to/folder"
  exit 1
fi

DIR="$1"
KEEP_DIR="$DIR/keep"

# Create keep folder if it doesn't exist
mkdir -p "$KEEP_DIR"

# Only loop through .wav files (excluding subdirectories)
find "$DIR" -maxdepth 1 -type f -iname "*.wav" | sort | while read -r file; do
  filename=$(basename "$file")
  echo "Now playing: $filename"
  
  # Play the file
  aplay "$file"

  # Prompt user for action
  echo -n "[k]eep, [n/s]kip, [d]elete, [q]uit: "
  read -n 1 action
  echo

  case "$action" in
    k|K)
      mv "$file" "$KEEP_DIR/"
      echo "→ Moved to keep/"
      ;;
    d|D)
      rm "$file"
      echo "→ Deleted"
      ;;
    r|R)
      aplay "$file"
      echo "→ Replaying"
      ;;
    q|Q)
      echo "→ Quitting"
      exit 0
      ;;
    n|N|s|S)
      echo "→ Skipped"
      ;;
    *)
      echo "→ Invalid input, skipping"
      ;;
  esac

done
