from Foundation import *
from AppKit import *

import objc

import os
import sys

import codec

class MSXAppController (NSObject):
	
	# --------------------
	# IBOutlets
	# --------------------
	
	window = objc.IBOutlet()
	
	world1Field = objc.IBOutlet()
	world2Field = objc.IBOutlet()
	world3Field = objc.IBOutlet()
	world4Field = objc.IBOutlet()
	world5Field = objc.IBOutlet()
	
	world1Button = objc.IBOutlet()
	world2Button = objc.IBOutlet()
	world3Button = objc.IBOutlet()
	world4Button = objc.IBOutlet()
	world5Button = objc.IBOutlet()
	
	otherWorldField = objc.IBOutlet()
	
	# --------------------
	# Cocoa Delegate Methods
	# --------------------
	
	def awakeFromNib(self):
		self.load_worlds()
		self.window.makeKeyAndOrderFront_(None)
	
	# --------------------
	# Loadng The Worlds
	# --------------------
	
	def load_worlds(self):
		self.worlds = {}
		
		try:
			self.mc_saves_folder
		except AttributeError:
			self.mc_saves_folder = NSString.stringWithString_("~/Library/Application Support/minecraft/saves").stringByStandardizingPath()
		try:
			self.world_vars
		except AttributeError:
			# This seems a horrific way to access the fields somewhat dynamically, but I haven't yet thought of a better way, so here it is.
			self.world_vars = {
				1: {'field': self.world1Field, 'button': self.world1Button},
				2: {'field': self.world2Field, 'button': self.world2Button},
				3: {'field': self.world3Field, 'button': self.world3Button},
				4: {'field': self.world4Field, 'button': self.world4Button},
				5: {'field': self.world5Field, 'button': self.world5Button}
			}
		
		for i in range(1, 6):
			mc_level_file = os.path.join(self.mc_saves_folder, ('World'+str(i)), 'level.dat')
			seed = ''
			exists = False
			
			if os.path.isfile(mc_level_file):
				tmpseed = self.get_seed(mc_level_file, ("The level.dat file for World " + str(i) + " is invalid."))
				if tmpseed:
					exists = True
					seed = tmpseed
			
			self.worlds[i] = {'exists': exists, 'seed': seed}
		
		for key in self.worlds.keys():
			field = self.world_vars[key]['field']
			field.setStringValue_("")
			if self.worlds[key]['exists']:
				field.setEditable_(False)
				field.setStringValue_(self.worlds[key]['seed'])
				self.world_vars[key]['button'].setTitle_('Copy')
			else:
				self.world_vars[key]['button'].setTitle_('Plant')
				field.setEditable_(True)
	
	# --------------------
	# Interface Actions
	# --------------------
	
	# Handles the Copy/Plant buttons as needed
	@objc.IBAction
	def handleCopyOrPlant_(self, sender):
		# The world ID is stored in the tag attribute of the button.
		tag = sender.tag()
		
		# If the tag is 6, it's the user loaded world button
		if tag == 6:
			self.copy_to_clipboard(self.otherWorldField.stringValue())
			return
		
		if self.worlds[tag]['exists']:
			self.copy_to_clipboard(self.worlds[tag]['seed'])
		else:
			seed = self.world_vars[tag]['field'].stringValue()
			model = codec.Seed()
			
			loaded = True
			
			try:
				model.load_string(seed)
			except:
				loaded = False
			
			if not loaded:
				self.show_invalid_seed_message()
				return
			
			model.decode()
			
			if not model.sanity_check():
				self.show_invalid_seed_message()
				return
			
			model.make_nbt()
			# Generate the paths...
			mc_level_folder = os.path.join(self.mc_saves_folder, ('World'+str(tag)))
			mc_level_file = os.path.join(mc_level_folder, 'level.dat')
			# ...create the necessary folders...
			os.makedirs(mc_level_folder)
			# ...and write the level.dat file.
			model.write_nbt(mc_level_file)
			# Then refresh the worlds so the newly generated one appears.
			self.load_worlds()
	
	# The "Load World..." button
	@objc.IBAction
	def loadWorld_(self, sender):
		panel = NSOpenPanel.openPanel()
		panel.setAllowsMultipleSelection_(False)
		panel.setCanChooseDirectories_(False)
		panel.setDelegate_(self)
		if panel.runModal() == NSOKButton:
			path = panel.URL().path()
			seed = self.get_seed(path, "The chosen level.dat file is invalid.")
			if seed:
				self.otherWorldField.setStringValue_(seed)
	
	# The "Refresh Worlds" button
	@objc.IBAction
	def refresh_(self, sender):
		self.load_worlds()

	# --------------------
	# Helpers
	# --------------------
	
	# Returns the seed of the level.dat file given in path when it's able to load it, and displays an invalid dat file using message as custom text and returns false when it can't 
	def get_seed(self, path, message):
		model = codec.Seed()
		try:
			model.load_tag(path)
			model.parse_nbt()
			model.encode()
		except:
			self.show_invalid_dat_message(message)
			return False
		return model.get_seed()
	
	def show_invalid_seed_message(self):
		alert = NSAlert.alertWithMessageText_defaultButton_alternateButton_otherButton_informativeTextWithFormat_("Invalid Seed", "Okay", None, None, "Make sure you entered the entire seed, including the brackets \"[ ]\"")
		alert.runModal()
	
	# Shows an invalid level.dat file message, with custom informative text 
	def show_invalid_dat_message(self, message):
		alert = NSAlert.alertWithMessageText_defaultButton_alternateButton_otherButton_informativeTextWithFormat_("Invalid level.dat File", "Okay", None, None, message)
		alert.runModal()
	
	# Copies a string to the clipboard
	def copy_to_clipboard(self, string):
		pb = NSPasteboard.generalPasteboard()
		pb.declareTypes_owner_([NSStringPboardType], self)
		pb.setString_forType_(string, NSStringPboardType)
	
	# --------------------
	# NSOpenPanel Delegate Methods
	# --------------------
	
	# Only allows .dat files, and folders to be selectable in the open dialog
	def panel_shouldShowFilename_(self, sender, filename):
		if os.path.splitext(filename)[1] == '.dat' or os.path.isdir(filename):
			return True
		return False