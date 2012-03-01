#!/usr/bin/python2

from gi.repository import Gtk, Gdk, Pango, WebKit
import markdown, yaml
from sys import argv

class MarkyWindow(Gtk.Window):
	
	def __init__(self):
		Gtk.Window.__init__(self, title="Marky")

		self.state = "both"
		
		'''
			Basic table, used for the both view
		'''
		self.table = Gtk.Table(1, 2, True)
		self.table.set_col_spacing(0, 5)
		self.add(self.table)

		font = Pango.FontDescription("monospace normal 10")
		font.set_family("Cousine,Droid Sans Mono,Anonymous Pro,Anonymous,Andale Mono,monospace")
		
		'''
			scrolled area for the main text view
		'''
		self.scrolled = Gtk.ScrolledWindow()
		self.scrolled.set_hexpand(True)
		self.scrolled.set_vexpand(True)
		
		'''
			The afformentioned text view
		'''
		self.text = Gtk.TextView()
		self.textbuff = self.text.get_buffer()
		self.textbuff.set_text("")
		self.text.set_wrap_mode(Gtk.WrapMode.WORD)
		self.text.modify_font(font)
		self.text.set_right_margin(5)
		self.text.set_left_margin(5)
		
		'''
			Display that scrolled area
		'''
		self.scrolled.add(self.text)
		self.table.attach(self.scrolled, 0, 1, 0, 1)

		'''
			The html viewer for the both view
		'''
		self.htmlscrolled = Gtk.ScrolledWindow()
		self.htmlscrolled.set_hexpand(True)
		self.htmlscrolled.set_vexpand(True)
		
		self.html = WebKit.WebView()

		self.htmlscrolled.add(self.html)
		self.table.attach(self.htmlscrolled, 1, 2, 0, 1)
		
		'''
			Extra stuff...
		'''
		self.set_default_size(700, 350)
		self.connect('key_press_event', self.on_key)
		
		self.connect('key_release_event', self.update_markdown)

		self.filename = ""

		self.style = "";
		self.update_style()
		
		self.full = "unfull"
		
	def on_key(self, widget, event):
		if event.state == Gdk.ModifierType.CONTROL_MASK:
			if Gdk.keyval_name(event.keyval) == "o":
				self.open()
			elif Gdk.keyval_name(event.keyval) == "s":
				self.save()
			elif Gdk.keyval_name(event.keyval) == "f":
				self.fullscreenize()
			elif Gdk.keyval_name(event.keyval) == "w":
				print "ctrl w"
				Gtk.main_quit()
		elif event.state == Gdk.ModifierType.MOD1_MASK:
			if Gdk.keyval_name(event.keyval) == "Right":
				if self.state == "both":
					self.state = "right"
				elif self.state == "right" or self.state == "left":
					self.state = "both"
				self.mod_state()
			elif Gdk.keyval_name(event.keyval) == "Left":
				if self.state == "both":
					self.state = "left"
				elif self.state == "left" or self.state == "right":
					self.state = "both"
				self.mod_state()
			elif Gdk.keyval_name(event.keyval) == "s":
				self.set_file("css/marky.css")
				self.get_text()
				self.state = "left"
				self.mod_state()
		elif Gdk.keyval_name(event.keyval) == "F11":
			self.fullscreenize()

	def mod_state(self):
		if self.state == "both":
			self.scrolled.show()
			self.htmlscrolled.show()
			self.table.remove(self.scrolled)
			self.table.attach(self.scrolled, 0, 1, 0 , 1)
			self.table.remove(self.htmlscrolled)
			self.table.attach(self.htmlscrolled, 1, 2, 0, 1)
		elif self.state == "left":
			self.htmlscrolled.hide()
			self.table.remove(self.scrolled)
			self.table.attach(self.scrolled, 0, 2, 0, 1)
		elif self.state == "right":
			self.scrolled.hide()
			self.table.remove(self.htmlscrolled)
			self.table.attach(self.htmlscrolled, 0, 2, 0, 1)

	def fullscreenize(self):
		if self.full == "unfull":
			self.fullscreen()
			self.full = "full"
		elif self.full == "full":
			self.unfullscreen()
			self.full = "unfull"

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
		self.set_title(self.filename)

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
		
		self.set_title(self.filename)

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
			self.set_file(dialog.get_filename())
		else:
			return False

		dialog.destroy()

		self.get_text()
		self.state = "both"
		self.mod_state()
		self.update_style()


	def add_filters(self, dialog):
		filter_text = Gtk.FileFilter()
		filter_text.set_name("Markdown files")
		filter_text.add_mime_type("text/x-markdown")
		dialog.add_filter(filter_text)

	def update_style(self):
		cssfile = "css/marky.css"
		cssopen = open(cssfile)
		self.style = "<style>";
		for line in cssopen:
			self.style += line
		self.style += "</style>"
		
# let's go...


win = MarkyWindow()

if len(argv) == 2:
	win.set_file(argv[1])
	win.get_text()

win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
