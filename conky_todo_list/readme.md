The goal of this project was to have an automated way for Conky to display my daily todos
on the desktop.

# How it works:

The Conky config file ".conkyrc" first defines a template, 
which you can read about in the conky docs:
https://conky.sourceforge.net/config_settings.html
https://conky.sourceforge.net/variables.html

Every time conky updates (as defined by "update_interval" in the config), it calls a python script.

The python script reads a simple text file ("todo.md"), prepends each paragraph 
with "{template0}", and writes it to stdout. Conky reads that and prints it to the screen,
edited according to the template.

# Usage

The way I personally use this is that "todo.md" is a file from my Obsidian vault, 
which I sync to all my devices via Syncthing. That means I can open Obsidian on any device, 
edit my todo.md, and have the todos show up as bullet points on all my PC desktops.
The process can be easily amended to work with different apps or synchronization options.
