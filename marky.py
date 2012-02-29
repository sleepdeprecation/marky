#!/usr/bin/python2

from gi.repository import Gtk, Gdk
import markdown
from sys import argv

class MarkyWindow(Gtk.Window):
	
	def __init__(self):
		Gtk.Window.__init__(self, title="Marky")
		
		table = Gtk.Table(1, 2, True)
		self.add(table)	
		
		scrolled = Gtk.ScrolledWindow()
		scrolled.set_hexpand(True)
		scrolled.set_vexpand(True)
		
		self.text = Gtk.TextView()
		self.textbuff = self.text.get_buffer()
		self.textbuff.set_text("")
		self.text.set_wrap_mode(Gtk.WrapMode.WORD)
		scrolled.add(self.text)
		
		table.attach(scrolled, 0, 1, 0, 1)
		
		htmlscrolled = Gtk.ScrolledWindow()
		htmlscrolled.set_hexpand(True)
		htmlscrolled.set_vexpand(True)
		
		self.html = Gtk.TextView()
		self.html.set_wrap_mode(Gtk.WrapMode.WORD)
		self.html.set_editable(False)
		self.htmlbuff = self.html.get_buffer()
		self.htmlbuff.set_text(markdown.markdown(
			self.textbuff.get_text(
				self.textbuff.get_start_iter(),
				self.textbuff.get_end_iter(),
				include_hidden_chars=True
			)
		))
		htmlscrolled.add(self.html)
		
		table.attach(htmlscrolled, 1, 2, 0, 1)
		
		self.set_default_size(700, 350)
		self.connect('key_press_event', self.on_key)
		
		self.connect('key_release_event', self.update_markdown)

		self.filename = ""
		
	def on_key(self, widget, event):
		if event.state == Gdk.ModifierType.CONTROL_MASK:
			if Gdk.keyval_name(event.keyval) == "o":
				print "control + o?"
	
	def update_markdown(self, widget, event):
		self.htmlbuff.set_text(markdown.markdown(
			self.textbuff.get_text(
				self.textbuff.get_start_iter(),
				self.textbuff.get_end_iter(),
				include_hidden_chars=True
			)
		))

	def set_file(self, filename):
		self.filename = filename

	def get_text(self):
		if self.filename == "":
			return False

		file = open(self.filename)
		text = ""
		for line in file:
			text += line

		self.textbuff.insert(self.textbuff.get_end_iter(), text)

		self.htmlbuff.set_text(markdown.markdown(
			self.textbuff.get_text(
				self.textbuff.get_start_iter(),
				self.textbuff.get_end_iter(),
				include_hidden_chars=True
			)
		))

		
# let's go...


win = MarkyWindow()

if len(argv) == 2:
	win.set_file(argv[1])
	win.get_text()

win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
