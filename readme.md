# Marky

Marky is a very simple markdown editor written in python.

Marky has one main feature: you write markdown in the left pane, it gets generated into html so you can see what it'll look like in the right pane.

Like I said, simple.

## Keyboard Shortcuts

**Ctrl + S**

Save - if you haven't saved yet and it's a new file, you'll be prompted for where you want to save the file.

**Ctrl + O**

Open - Opens a `*.md` or `*.markdown` file on your local drive. Discards anything in the buffer (remember to save before opening a new file).

**Ctrl + W**

Close Window. I really like Ctrl+W as opposed to Alt+F4 (which works, but only because it's part of the operating system), so I implemented this.


## Requirements

- Python2 (duh?)
- PyGtk (Arch package: pygtk)
- python2-markdown (some distros might use python-markdown, making python3's python3-markdown)

## History

Marky was started at about 2200 on 28 Feb 2012. It is considered complete (there could be some optimizations) as of 0200 on 29 Feb 2012. Enjoy this four hour project. It does one task, and one task only.