#!/bin/bash

#---------------------------------------------------------------
# Simple bash script to read a video URL from the clipboard and 
# download its soundtrack as an mp3.
#---------------------------------------------------------------

link=$(xclip -o)
zenity --notification --text "Download started: ($link)"

youtube-dl -x --audio-format mp3 -o '~/Downloads/Music/%(title)s.%(ext)s' "$link" &
zenity --notification --text "Download finished!"
