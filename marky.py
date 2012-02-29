#!/usr/bin/python2

from gi.repository import Gtk, Gdk, WebKit
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
		
		self.html = WebKit.WebView()

		htmlscrolled.add(self.html)
		
		table.attach(htmlscrolled, 1, 2, 0, 1)
		
		self.set_default_size(700, 350)
		self.connect('key_press_event', self.on_key)
		
		self.connect('key_release_event', self.update_markdown)

		self.filename = ""

		self.style = """<style>
img {max-width:100%;}
li {padding-bottom:1em;}
body {font-family:"arimo", sans-serif; font-size:12px;}
		</style>"""
		
	def on_key(self, widget, event):
		if event.state == Gdk.ModifierType.CONTROL_MASK:
			if Gdk.keyval_name(event.keyval) == "o":
				self.open()
			elif Gdk.keyval_name(event.keyval) == "s":
				self.save()
			elif Gdk.keyval_name(event.keyval) == "w":
				print "ctrl w"
				Gtk.main_quit()
	
	def update_markdown(self, widget, event):
		self.html.load_html_string(self.style + markdown.markdown(
			self.textbuff.get_text(
				self.textbuff.get_start_iter(),
				self.textbuff.get_end_iter(),
				include_hidden_chars=True
			)), "file:///"
		)

	def set_file(self, filename):
		self.filename = filename

	def get_text(self):
		if self.filename == "":
			return False

		file = open(self.filename)
		text = ""
		for line in file:
			text += line

		self.textbuff.set_text(text)

		self.html.load_html_string(self.style + markdown.markdown(
			self.textbuff.get_text(
				self.textbuff.get_start_iter(),
				self.textbuff.get_end_iter(),
				include_hidden_chars=True
			)), "file:///"
		)

	def save(self):
		if self.filename == "":
			dialog = Gtk.FileChooserDialog(
				"Save Where?",
				self,
				Gtk.FileChooserAction.SAVE,
				(
					Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, 
					Gtk.STOCK_OPEN, Gtk.ResponseType.OK
				)
			)

			self.add_filters(dialog)
			response = dialog.run()
			
			if response == Gtk.ResponseType.OK:
				self.filename = dialog.get_filename()
			else:
				return False

			dialog.destroy()

		writer = open(self.filename, "w")
		writer.write(
			self.textbuff.get_text(
				self.textbuff.get_start_iter(),
				self.textbuff.get_end_iter(),
				include_hidden_chars=True
			)
		)

	def open(self):
		dialog = Gtk.FileChooserDialog(
			"What File?",
			self,
			Gtk.FileChooserAction.SAVE,
			(
				Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, 
				Gtk.STOCK_OPEN, Gtk.ResponseType.OK
			)
		)

		self.add_filters(dialog)
		response = dialog.run()
		
		if response == Gtk.ResponseType.OK:
			self.filename = dialog.get_filename()
		else:
			return False

		dialog.destroy()

		self.get_text()


	def add_filters(self, dialog):
		filter_text = Gtk.FileFilter()
		filter_text.set_name("Markdown files")
		filter_text.add_mime_type("text/x-markdown")
		dialog.add_filter(filter_text)

		
# let's go...


win = MarkyWindow()

if len(argv) == 2:
	win.set_file(argv[1])
	win.get_text()

win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
