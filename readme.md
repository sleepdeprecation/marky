# Marky

Marky is a simple markdown editor that utilizes the GTK and is written in python.

Right now, Marky doesn't do anything other than render any markdown you place in the left pane to html in the right. Eventually I'll add in a webkit (or maybe gecko) based rendering engine to display the html, but for now, that's all it does.

If you specify a file as an argument in calling marky (`./marky.py readme.md`), it will open up that file, and display the generated html.

Marky can now open and save files using Ctrl+O and Ctrl+S respectively. That is all.

Also, Ctrl+W closes it too.

## Requirements

- Python2 (duh?)
- PyGtk (Arch package: pygtk)
- python2-markdown (some distros might use python-markdown, making python3's python3-markdown)

## Future

Eventually it'll have two keybindings - Ctrl+O and Ctrl+S to open and save. Nothing else. It does support OS based clipboards, so Ctrl+C/Ctrl+V words. It looks like Ctrl+A also works.