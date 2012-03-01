#!/usr/bin/python2

from sys import argv
from MarkyWindow import MarkyWindow
from gi.repository import Gtk

win = MarkyWindow()

if len(argv) == 2:
	win.set_file(argv[1])
	win.get_text()

win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
