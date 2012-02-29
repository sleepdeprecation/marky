#!/usr/bin/python2

from gi.repository import Gtk, Gdk, Pango, WebKit
import markdown
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

		self.style = """<style>
h1, h2, h3, h4, h5, h6 {
  border: 0 !important;
}

h1 {
  font-size: 170% !important;
  border-top: 4px solid #aaa !important;
  padding-top: .5em !important;
  margin-top: 1.5em !important;
}

  h1:first-child {
    margin-top: 0 !important;
    padding-top: .25em !important;
    border-top: none !important;
  }

h2 {
  font-size: 150% !important;
  margin-top: 1.5em !important;
  border-top: 4px solid #e0e0e0 !important;
  padding-top: .5em !important;
}

h3 {
  margin-top: 1em !important;
}

p {
  margin: 1em 0 !important;
  line-height: 1.5em !important;
}

ul {
  margin: 1em 0 1em 2em !important;
}

  ul {
    margin-top: 0 !important;
    margin-bottom: 0 !important;
  }

ol {
  margin: 1em 0 1em 2em !important;
}

  ol ol {
    margin-top: 0 !important;
    margin-bottom: 0 !important;
  }

ul ul,
ul ol,
ol ol,
ol ul {
  margin-top: 0 !important;
  margin-bottom: 0 !important;
}

blockquote {
  margin: 1em 0 !important;
  border-left: 5px solid #ddd !important;
  padding-left: .6em !important;
  color: #555 !important;
}

dt {
  font-weight: bold !important;
  margin-left: 1em !important;
}

dd {
  margin-left: 2em !important;
  margin-bottom: 1em !important;
}

table {
  margin: 1em 0 !important;
}

  table th {
    border-bottom: 1px solid #bbb !important;
    padding: .2em 1em !important;
  }

  table td {
    border-bottom: 1px solid #ddd !important;
    padding: .2em 1em !important;
  }

pre {
  margin: 1em 0 !important;
  font-size: 90% !important;
  background-color: #f8f8ff !important;
  border: 1px solid #dedede !important;
  padding: .5em !important;
  line-height: 1.5em !important;
  color: #444 !important;
  overflow: auto !important;
}

  pre code {
    padding: 0 !important;
    font-size: 100% !important;
    background-color: #f8f8ff !important;
    border: none !important;
  }

code {
  font-size: 90% !important;
  background-color: #f8f8ff !important;
  color: #444 !important;
  padding: 0 .2em !important;
  border: 1px solid #dedede !important;
}

img,embed {max-width:100%;}
li {padding-bottom:1em;}
body {font-family: "Droid Sans",sans-serif; font-size:14px;}
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
		if event.state == Gdk.ModifierType.MOD1_MASK:
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
