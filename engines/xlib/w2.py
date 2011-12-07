from keysym_to_unicode import keysym_to_unicode
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
		('Control', 'Ctrl'),
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
	def __init__(self):
		#Connect to X
		disp = display.Display()
		
		#MODIFIERS
		
		#Find modifiers
		mapping = disp.get_modifier_mapping()
		#Add mask and keycodes to self.modifiers
		self.modifiers = [(1<<k,v[0],filter(lambda x: x!=0, list(mapping[k]), v[1])) for k, v in enumerate(self.modifiers)]
		#Format is now MASK, STRING, USE?, KEYCODES
		
		#KEYS
		
		self.keys = []
		#open up xmodmap
		for line in _xmodmap("-pk"):
			#match keycode -> keysym lines
			m = re.match("^\s*(\d+)\s+0x([0-9a-fA-F]+) \((\w*)\)\w*", line)
			if m:
				keycode= int(m.group(1))
				keysym = int(m.group(2), 16) #Decode hex
				string =     m.group(3)
				
				#Ignore undefined keys
				if keysym == 0:
					continue
				
				
				if string in keysym_to_unicode:
					string = unichr(keysym_to_unicode[string])	
				else:
					#Smarten it up
					for k, v in better_names:
						string = re.sub(k,v,string)
					#Special case: sort out CamelCase on XF86 keysyms
					if string.startswith("XF86"):
						string = string[4:]
						string = re.sub('([a-z]{1})([A-Z0-9]{1})', '\\1 \\2', string)
					string = string[0].upper()+string[1:]
		
				keys.append((keycode,keysym,string))

	def _xmodmap(self, flag):
		return subprocess.Popen(["xmodmap", flag], stdout=subprocess.PIPE).communicate()[0].split("\n")




def xmodmap(flag):
	return subprocess.Popen(["xmodmap", flag], stdout=subprocess.PIPE).communicate()[0].split("\n")


better_names = [
	('^(.*)_(L|R)$', '\\1'),
	('Control', 'Ctrl'),
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

###MODIFIERS
#Output format: mask, string, keycodes, use
mapping = disp.get_modifier_mapping()
modifiers = [
	[1<<0, 'Shift', True], 
	[1<<1, 'Caps Lock', False],
	[1<<2, 'Control', True],
	[1<<3, 'Alt', True],
	[1<<4, 'Num Lock', False],
	[1<<5, '', False],
	[1<<6, 'Super', True],
	[1<<7, 'Alt Gr', True]]
modifiers = [(1<<k,v[1],v[2],filter(lambda x: x!=0, list(mapping[k]))) for k, v in enumerate(modifiers)]

# in enumerate(disp.get_modifier_mapping())
#	mask = 1<<k
#	keycodes = tuple(m)
	
#modifiers = [(1<<k, modifiers[k], mod) for k, mod in enumerate(disp.get_modifier_mapping())]
print modifiers
#modifiers = xmodmap("-pm")[2:-2]
#for mod in modifiers:
	
sys.exit(1)



keys = []

for line in xmodmap("-pk"):
	m = re.match("^\s*(\d+)\s+0x([0-9a-fA-F]+) \((\w*)\)\w*", line)
	if m:
		keycode = int(m.group(1))
		keysym = int(m.group(2), 16)
		string = m.group(3)
		if keysym == 0:
			continue
		if string in keysym_to_unicode:
			string = unichr(keysym_to_unicode[string])	
		else:
			
			for k, v in better_names:
				string = re.sub(k,v,string)
			if string.startswith("XF86"):
				string = string[4:]
				#Get rid of camel case
				string = re.sub('([a-z]{1})([A-Z0-9]{1})', '\\1 \\2', string)
				#s = re.sub('
			string = string[0].upper()+string[1:]
		
		keys.append((keycode,keysym,string))



for i in keys:
	print i
	#print "%d\t%s" % (k, v)
