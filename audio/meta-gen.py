# Example usage:
# generate_metadata_csv("/your/path/to/wav_files")

import os
import csv
import wave

def generate_metadata_csv(directory_path):
    output_csv_path = os.path.join(directory_path, "metadata.csv")
    metadata_list = []

    for filename in sorted(os.listdir(directory_path)):
        if filename.lower().endswith(".wav"):
            file_path = os.path.join(directory_path, filename)
            try:
                with wave.open(file_path, 'rb') as wav_file:
                    frames = wav_file.getnframes()
                    rate = wav_file.getframerate()
                    duration = round(frames / float(rate), 3)
                    metadata_list.append({
                        "filename": filename,
                        "duration": f"{duration}s"
                    })
            except wave.Error:
                metadata_list.append({
                    "filename": filename,
                    "duration": "ERROR"
                })

    csv_headers = ["filename", "description", "tags", "duration", "category"]

    with open(output_csv_path, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_headers)
        writer.writeheader()
        for entry in metadata_list:
            entry.update({"description": "", "tags": "", "category": ""})
            writer.writerow(entry)

    print(f"Metadata written to {output_csv_path}")
