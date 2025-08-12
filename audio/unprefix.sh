#!/bin/bash

# Script to undo the prefixing of the prefix-script, that is, check if the first four characters are three digits
# followed by an underscore, and if yes, remove that.
#
# Usage: ./unprefix.sh /path/to/your/folder [--dry-run]

dir="$1"
dryrun="$2"

if [[ ! -d "$dir" ]]; then
  echo "Error: Directory not found."
  exit 1
fi

shopt -s nullglob
for file in "$dir"/*.wav; do
  base=$(basename "$file")
  if [[ "$base" =~ ^[0-9]{3}_ ]]; then
    newname="${base:4}"
    if [[ "$dryrun" == "--dry-run" ]]; then
      echo "[Dry run] Would rename: $base -> $newname"
    else
      mv -n "$file" "$dir/$newname"
      echo "Renamed: $base -> $newname"
    fi
  fi
done
