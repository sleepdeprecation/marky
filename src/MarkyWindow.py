#!/usr/bin/python2

from gi.repository import Gtk, Gdk, Pango, WebKit
import markdown, yaml, os

# Public:	The basic Gtk Window for running Marky, plus all of 
#			Marky's useful internal classes
class MarkyWindow(Gtk.Window):
	
	# Internal:	Inialize the MarkyWindow. Really, you'll never call it...
	def __init__(self):

		# to get started, let's call this window 'Marky'.
		# why you ask, because eventually it'll get overwritten.
		self.title = "Marky"
		Gtk.Window.__init__(self, title=self.title)

		# some useful internal variables that'll show up later

		# settings_file:	The settings file...
		self.settings_file = os.path.join(os.path.dirname(__file__), 'settings/marky.yml')

		# css_file:			The css file...
		self.css_file = os.path.join(os.path.dirname(__file__), 'settings/marky.css')

		# state:	The starting state for the MarkyWindow.
		#			Options: both | left | right
		self.state = "both"

		# size:		An array containing the width and height
		#			for the window.
		self.size = [700, 500]
		
		# filename:	The name of the currently open file.
		#			If there isn't an open file, it's just ""
		self.filename = ""

		# style:	Will eventually contain the CSS used to make 
		#			Marky's rendered pane all pretty-like
		self.style = ""

		# full:		Is Marky running in full screen?
		#			Options: True | False
		self.full = False

		# Grab the settings from marky.yml
		self.settings = self.load_yaml()

		# adjust the settings to the newly loaded settings...
		self.state = self.settings['start-state']
		self.size = self.settings['start-size']

		# alright, let's build the GUI
		self.build_gui() 
		self.update_style()

		self.set_default_size(self.size[0], self.size[1])
		
		self.connect('key_press_event', self.on_key)
		self.connect('key_release_event', self.update_markdown)
		self.connect('delete-event', self.quit)

	# Internal: load the settings from settings/marky.yml
	def load_yaml(self):
		cont = ""
		file = open(self.settings_file)
		for line in file:
			cont += line
		return yaml.load(cont)

	# Internal: save the settings to settings/marky.yml
	def save_yaml(self):
		self.settings['start-size'] = list(self.get_size())
		self.settings['start-state'] = self.state

		writer = open(self.settings_file, "w")
		writer.write(yaml.dump(self.settings))

	# Internal: Create the basic GUI structure
	def build_gui(self):
		# table used for EVERYTHING
		self.table = Gtk.Table(1, 2, True)
		self.table.set_col_spacing(0, 5)
		self.add(self.table)

		# setup the left - the markdown area

		# markdown scroll area
		self.scrolled = Gtk.ScrolledWindow()
		self.scrolled.set_hexpand(True)
		self.scrolled.set_vexpand(True)

		# markdown textview		
		self.text = Gtk.TextView()
		self.text.set_right_margin(5)
		self.text.set_left_margin(5)
		self.text.set_wrap_mode(Gtk.WrapMode.WORD)
		
		# markdown textview font stuff
		font = Pango.FontDescription("monospace normal" + str(self.settings['font-size']))
		font.set_family(self.settings['font-family'])
		self.text.modify_font(font)

		# markdown textbuffer
		self.textbuff = self.text.get_buffer()
		self.textbuff.set_text("")
		
		# put the markdown textview inside of the markdown scroll area
		self.scrolled.add(self.text)

		# html scroll area
		self.htmlscrolled = Gtk.ScrolledWindow()
		self.htmlscrolled.set_hexpand(True)
		self.htmlscrolled.set_vexpand(True)
		
		# html area
		self.html = WebKit.WebView()

		# put the html area in the html scroll area
		self.htmlscrolled.add(self.html)

		# put the GUI together...
		self.mod_state()

	# Internal: modify the windows view based on self.state
	def mod_state(self):
		# dual pane mode:
		if self.state == "both":
			self.scrolled.show()
			self.htmlscrolled.show()
			self.table.remove(self.scrolled)
			self.table.attach(self.scrolled, 0, 1, 0 , 1)
			self.table.remove(self.htmlscrolled)
			self.table.attach(self.htmlscrolled, 1, 2, 0, 1)

		# markdown only mode:
		elif self.state == "left":
			self.htmlscrolled.hide()
			self.table.remove(self.scrolled)
			self.table.attach(self.scrolled, 0, 2, 0, 1)

		# html only mode
		elif self.state == "right":
			self.scrolled.hide()
			self.table.remove(self.htmlscrolled)
			self.table.attach(self.htmlscrolled, 0, 2, 0, 1)

	# Internal: Update self.style
	def update_style(self):
		cssopen = open(self.css_file)
		self.style = "<style>";
		for line in cssopen:
			self.style += line
		self.style += "</style>"

	# Internal: when a key is pressed, not released.
	def on_key(self, widget, event):
		# if it's modified with a CTRL key
		if event.state == Gdk.ModifierType.CONTROL_MASK:
			# ctrl + e
			'''if Gdk.keyval_name(event.keyval) == "e":
				self.change_font()
			'''
			# ctrl + f
			if Gdk.keyval_name(event.keyval) == "f":
				self.fullscreenize()
			
			# ctrl + o
			elif Gdk.keyval_name(event.keyval) == "o":
				self.open()

			# ctrl + s
			elif Gdk.keyval_name(event.keyval) == "s":
				self.save()

			# ctrl + shift + S
			elif Gdk.keyval_name(event.keyval) == "S":
				self.pick_file()
				self.save()

			# ctrl + w
			elif Gdk.keyval_name(event.keyval) == "w":
				self.quit(widget, event)


		# if it's modified with an ALT key
		elif event.state == Gdk.ModifierType.MOD1_MASK:
			# alt + ->
			if Gdk.keyval_name(event.keyval) == "Right":
				if self.state == "both":
					self.state = "right"
				elif self.state == "right" or self.state == "left":
					self.state = "both"
				self.mod_state()

			# alt + <-
			elif Gdk.keyval_name(event.keyval) == "Left":
				if self.state == "both":
					self.state = "left"
				elif self.state == "left" or self.state == "right":
					self.state = "both"
				self.mod_state()

			# alt + s
			elif Gdk.keyval_name(event.keyval) == "s":
				self.set_file(self.settings_file)
				self.get_text()
				self.state = "left"
				self.mod_state()

			# alt + c
			elif Gdk.keyval_name(event.keyval) == "c":
				self.set_file(self.css_file)
				self.get_text()
				self.state = "left"
				self.mod_state()

		# F11?
		elif Gdk.keyval_name(event.keyval) == "F11":
			self.fullscreenize()

	# Public: Open a file, utilizing a file-picker.
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

		dialog.destroy()

		self.get_text()
		self.state = self.settings['start-state']
		self.mod_state()
		self.update_style()

	# Internal: set filters for open/save
	def add_filters(self, dialog):
		filter_text = Gtk.FileFilter()
		filter_text.set_name("Markdown files")
		filter_text.add_mime_type("text/x-markdown")
		dialog.add_filter(filter_text)

	# Public: Set what file is being used in Marky
	def set_file(self, filename):
		self.filename = filename
		self.title = self.filename
		self.set_title(self.title)	

	# Public: if Marky's editing a file, save it, otherwise, select where to save the file.	
	def save(self):
		if self.filename == "":
			self.pick_file()

		self.title = self.filename;
		self.set_title(self.title + " - Saved")

		writer = open(self.filename, "w")
		writer.write(
			self.textbuff.get_text(
				self.textbuff.get_start_iter(),
				self.textbuff.get_end_iter(),
				include_hidden_chars=True
			)
		)

	# Internal: select what file's being used...
	def pick_file(self):
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
			return True
		else:
			return False

		dialog.destroy()

	# Public: make Marky fullscreen. or if it's already full, unfull it.
	def fullscreenize(self):
		if self.full:
			self.unfullscreen();
			self.full = False
		elif not self.unfull:
			self.fullscreen()
			self.full = True

	# Public: Update the html section
	def update_markdown(self, widget, event):
		self.html.load_html_string(self.style + markdown.markdown(
			self.textbuff.get_text(
				self.textbuff.get_start_iter(),
				self.textbuff.get_end_iter(),
				include_hidden_chars=True
			)), "file:///"
		)
		if (
			event.state != Gdk.ModifierType.CONTROL_MASK and 
			event.state != Gdk.ModifierType.MOD1_MASK
		):
			self.set_title(self.title);

	# Public: set the markdown area's text
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

	# Internal: Quit the application
	def quit(self, widget, event):
		try:
			self.save_yaml()
		except IOError as io:
			print "error saving file"
			print io

		Gtk.main_quit()

	# Internal: Change the editor's font
	'''def change_font(self):
		fontsel = Gtk.FontSelectionDialog("Editor Font")

		fontsel.set_font_name(
			self.settings['font-family'] +
			" " + 
			str(self.settings['font-size'])
		)
		
		fontsel.show()
		fontsel.ok_button

		if fontsel.ok_button:
			print fontsel.get_font_name()'''
