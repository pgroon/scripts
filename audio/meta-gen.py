#!/usr/bin/env python3

# Generates a .csv with metadata for all .wav files in a folder and its subfolders.
# Only includes the base filename (no full path) and subfolder columns.
#
# Example usage:
#   meta-gen.py /your/path/to/wav_files

import os
import csv
import sys
import wave

def generate_metadata_csv(directory_path):
    print(f"Scanning: {directory_path}")
    output_csv_path = os.path.join(directory_path, "metadata.csv")
    metadata_list = []

    for root, dirs, files in os.walk(directory_path):
        for filename in sorted(files):
            if filename.lower().endswith(".wav"):
                file_path = os.path.join(root, filename)
                subfolder = os.path.relpath(root, directory_path)
                if subfolder == ".":
                    subfolder = ""  # Root-level files

                try:
                    with wave.open(file_path, 'rb') as wav_file:
                        frames = wav_file.getnframes()
                        rate = wav_file.getframerate()
                        duration = round(frames / float(rate), 3)
                        duration_str = f"{duration}s"
                except wave.Error:
                    duration_str = "ERROR"
                except Exception as e:
                    duration_str = f"ERROR:{type(e).__name__}"

                metadata_list.append({
                    "filename": filename,
                    "subfolder": subfolder.replace(os.sep, '/'),
                    "description": "",
                    "tags": "",
                    "duration": duration_str,
                    "category": ""
                })

    csv_headers = ["filename", "subfolder", "description", "tags", "duration", "category"]

    with open(output_csv_path, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_headers)
        writer.writeheader()
        writer.writerows(metadata_list)

    print(f"Metadata written to {output_csv_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: meta-gen.py /path/to/wav-folder")
        sys.exit(1)

    wav_folder = sys.argv[1]

    if not os.path.isdir(wav_folder):
        print(f"Error: '{wav_folder}' is not a valid directory.")
        sys.exit(1)

    generate_metadata_csv(wav_folder)
