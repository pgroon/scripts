#!/usr/bin/env bash

#---------------------------------------------------------------
# Simple bash script to read a video URL from the clipboard and 
# download its soundtrack as an mp3.
#---------------------------------------------------------------

set -Eeuo pipefail

link="$(xclip -o -selection clipboard || true)"
if [[ -z "${link:-}" || ! "$link" =~ ^https?:// ]]; then
  zenity --error --text="Clipboard does not contain a URL."
  exit 1
fi

outdir="$HOME/Downloads/Music"
mkdir -p "$outdir"

zenity --notification --text="Download started: ($link)"

# ffmpeg is required for mp3 extraction
yt-dlp -x --audio-format mp3 --no-playlist \
  -o "$outdir/%(title).200B.%(ext)s" \
  "$link" && \
zenity --notification --text="Download finished!" || \
zenity --error --text="Download failed (exit $?)"
