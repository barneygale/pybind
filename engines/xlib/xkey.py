from constants import keysym_to_unicode
from Xlib import display
import subprocess
import re



class xkey:
	modifiers = [
		['Shift', True], 
		['Caps Lock', False],
		['Control', True],
		['Alt', True],
		['Num Lock', False],
		['', False],
		['Super', True],
		['Alt Gr', True]]
	better_names = [
		('^(.*)_(L|R)$', '\\1'),
		('Control', 'Control'),
		('ISO_Level3_Shift', 'Alt_Gr'),
		('KP_End', 	'KP_1'),
		('KP_Down', 	'KP_2'),
		('KP_Next',	'KP_3'),
		('KP_Left', 	'KP_4'),
		('KP_Begin', 	'KP_5'),
		('KP_Right', 	'KP_6'),
		('KP_Home', 	'KP_7'),
		('KP_Up', 	'KP_8'),
		('KP_Prior', 	'KP_9'),
		('KP_Insert', 	'KP_0'),
		('KP_Divide',	'KP_/'),
		('KP_Multiply',	'KP_*'),
		('KP_Subtract',	'KP_-'),
		('KP_Add',	'KP_+'),
		('KP', 'NumPad'),
		('BackSpace', 'Backspace'),
		('^Prior$', 'Page Up'),
		('^Next$', 'Page Down'),
		('_', ' ')]
	def __init__(self, disp):
		#Connect to X
		#disp = display.Display()
		
		#MODIFIERS
		
		#Find modifiers
		mapping = disp.get_modifier_mapping()
		#Add mask and keycodes to self.modifiers
		self.modifiers = [(
			1<<k,
			v[0],
			filter(lambda x: x!=0, list(mapping[k])), 
			v[1]
		) for k, v in enumerate(self.modifiers)]
		#Format is now MASK, STRING, KEYCODES, USE?
		
		#KEYS
		
		self.keys = []
		for line in self._xmodmap("-pk"):
			#match keycode -> keysym lines
			m = re.match("^\s*(\d+)\s+0x([0-9a-fA-F]+) \((\w*)\)\w*", line)
			if not m: continue
			keycode= int(m.group(1))
			keysym = int(m.group(2), 16) #Decode hex
			string =     m.group(3)
			
			#Ignore undefined keys
			if keysym == 0: continue
			
			if keysym in keysym_to_unicode:
				string = unichr(keysym_to_unicode[keysym])	
			else:
				#Smarten it up
				for k, v in self.better_names:
					string = re.sub(k,v,string)
				#Special case: sort out CamelCase on XF86 keysyms
				if string.startswith("XF86"):
					string = string[4:]
					string = re.sub('([a-z]{1})([A-Z0-9]{1})', '\\1 \\2', string)
				string = string[0].upper()+string[1:]
			self.keys.append({'keycode':keycode,'keysym': keysym, 'string': string})
		
		#Convenient arrays!
		self.keyByKeycode = dict([(v['keycode'], v) for v in self.keys])
		self.modifier_keycodes = []
		for mod in self.modifiers:
			if mod[3]:
				self.modifier_keycodes.extend(mod[2])
	
	def _xmodmap(self, flag):
		return subprocess.Popen(["xmodmap", flag], stdout=subprocess.PIPE).communicate()[0].split("\n")
	def getKeyByKeycode(self, keycode):
		return dict(self.keyByKeycode[keycode])
	def getModStrings(self, mask):
		return [i[1] for i in self.modifiers if (i[3] and mask & i[0])]
	def getIgnoreMask(self):
		mask = 0
		for i in self.modifiers:
			if i[3]:
				mask |= i[0]
		return mask
	def mask_permutations(self, mask, ignore_mask):
		#PERM & (~IGNO | modm)
		#Get all permutations of replacing some "0"s with "1"s in ignore_mask
		i = ignore_mask
		out = []
		while i < 256:
			i |= ignore_mask
			out.append(i & (~ignore_mask | mask))
			i+=1
		return out	
	def isMod(self,keycode):
		return keycode in self.modifier_keycodes
