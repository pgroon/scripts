#!/usr/bin/env python3
"""
Rename WAV files exported from Tenacity based on a CSV list.

Usage:
    python3 list_to_filename.py path/to/wav-folder /path/to/list.csv

CSV format:
    category,number,phrase
    Confirmations,1,Confirmed
    Confirmations,2,Affirmative
    ...

The script:
  - Reads the CSV and matches the "number" column to exported WAV files.
  - Renames the files to "category_number_phrase.wav".
  - Sanitizes the names (removes punctuation, replaces spaces with underscores).
  - Handles 1.wav, 01.wav, 001.wav (case-insensitive).
  - Appends -a, -b, ... if a name collision occurs.
"""

import csv
import os
import re
import sys
import unicodedata
from pathlib import Path

# ----------------------
# Helper functions
# ----------------------

def usage():
    """Print usage and exit."""
    print("Usage: python3 list_to_filename.py <wav_folder> <list.csv>")
    sys.exit(1)

def slugify(s: str) -> str:
    """
    Convert a string into a filesystem-safe format:
      - Remove accents and non-ASCII characters
      - Replace spaces with underscores
      - Remove punctuation except underscore and hyphen
      - Collapse multiple underscores
      - Limit to 80 characters
    """
    # Normalize Unicode (e.g., é -> e)
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    # Replace ampersand with 'and'
    s = s.replace("&", "and")
    # Remove all non-word characters except underscores, spaces, and hyphens
    s = re.sub(r"[^\w\s-]", "", s)
    # Replace spaces with underscores
    s = re.sub(r"\s+", "_", s.strip())
    # Collapse multiple underscores into one
    s = re.sub(r"_+", "_", s)
    # Return shortened or fallback to 'clip' if empty
    return s[:80] or "clip"

def find_export(wav_dir: Path, n: int) -> Path | None:
    """
    Try to find a Tenacity-exported WAV file matching the given number.
    Handles:
      - 1.wav, 01.wav, 001.wav
      - Case-insensitive (.wav or .WAV)
    Returns the Path if found, or None if no match.
    """
    stems = [f"{n}", f"{n:02d}", f"{n:03d}"]
    for stem in stems:
        for ext in (".wav", ".WAV"):
            p = wav_dir / f"{stem}{ext}"
            if p.exists():
                return p
    return None

def unique_path(dst: Path) -> Path:
    """
    Ensure the destination path is unique.
    If a file already exists with the same name, append:
      - -a, -b, ... for first 26 collisions
      - -2, -3, ... after that
    """
    if not dst.exists():
        return dst
    stem, suf = dst.stem, dst.suffix
    # Try letters
    for i in range(97, 123):  # ASCII a..z
        cand = dst.with_name(f"{stem}-{chr(i)}{suf}")
        if not cand.exists():
            return cand
    # Fallback to numbers
    k = 2
    while True:
        cand = dst.with_name(f"{stem}-{k}{suf}")
        if not cand.exists():
            return cand
        k += 1

# ----------------------
# Main script
# ----------------------

def main():
    # Require exactly two arguments: wav folder and CSV file
    if len(sys.argv) != 3:
        usage()

    wav_dir = Path(sys.argv[1]).expanduser().resolve()
    csv_path = Path(sys.argv[2]).expanduser().resolve()

    # Check input paths
    if not wav_dir.is_dir():
        print(f"Error: wav folder not found: {wav_dir}")
        sys.exit(2)
    if not csv_path.is_file():
        print(f"Error: CSV not found: {csv_path}")
        sys.exit(3)

    renamed = 0
    missing = 0

    # Open and parse the CSV
    with csv_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        required = {"category", "number", "phrase"}
        # Validate header (case-insensitive match)
        if set(h.strip().lower() for h in reader.fieldnames or []) != required:
            print('Error: CSV must have header exactly: "category,number,phrase"')
            sys.exit(4)

        for row in reader:
            try:
                n = int(row["number"].strip())
            except Exception:
                continue  # skip bad rows

            # Find matching exported WAV
            src = find_export(wav_dir, n)
            if not src:
                print(f"[MISS] {n:03d} -> no matching source file in {wav_dir}")
                missing += 1
                continue

            # Sanitize parts for filename
            category = slugify(row["category"])
            phrase   = slugify(row["phrase"])
            dst = wav_dir / f"{n:03d}_{category}_{phrase}.wav"
            dst = unique_path(dst)

            # Rename the file
            os.rename(src, dst)
            print(f"[OK] {src.name} -> {dst.name}")
            renamed += 1

    # Summary
    print(f"\nDone. Renamed: {renamed}, Missing: {missing}")

if __name__ == "__main__":
    main()
