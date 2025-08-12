#!/bin/bash

# Usage: ./number_prefix.sh /path/to/folder

if [ -z "$1" ]; then
  echo "Usage: $0 /path/to/folder"
  exit 1
fi

TARGET_DIR="$1"

# Safety check: Make sure it's a directory
if [ ! -d "$TARGET_DIR" ]; then
  echo "Error: $TARGET_DIR is not a directory."
  exit 1
fi

cd "$TARGET_DIR" || exit 1

# Gather and sort all regular files (exclude dirs)
files=()
while IFS= read -r -d $'\0' file; do
  files+=("$file")
done < <(find . -maxdepth 1 -type f -printf "%f\0" | sort -z)

counter=1
for file in "${files[@]}"; do
  prefix=$(printf "%03d" "$counter")
  newname="${prefix}_$file"
  mv -n -- "$file" "$newname"
  ((counter++))
done

echo "Renamed ${#files[@]} files."
