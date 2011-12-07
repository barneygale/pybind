from Xlib import X, XK, display, keysymdef
import threading
from error import EngineError
from Queue import Queue
import string
from xkey import xkey
import time
import key
#import queue

class EngineXlib(threading.Thread):
	running = False
	queue = Queue()
	bound = {}
	mode = 'hotkey'
	def __init__ (self):
		threading.Thread.__init__(self)
		
		self.disp = display.Display()
		self.root = self.disp.screen().root
		
		#Init xkey
		self.xkey = xkey(self.disp)
		#print self.xkey.mask_permutations
		
		# we tell the X server we want to catch keyPress event
		# self.root.change_attributes(event_mask = X.KeyPressMask)
		self.daemon = True
		self.running = True
		self.start()
	def bindAll(self):
		pass
	def unbindAll(self):
		pass
	def run(self):
		while self.running:
			#Switch to polling mode if asked...
			if self.mode == 'hotkey' and not self.queue.empty():
				#print "Switching to polling mode..."
				bindkey, callback = self.queue.get()
				self.root.grab_keyboard(1, X.GrabModeAsync, X.GrabModeAsync, X.CurrentTime) 
				self.disp.flush()
				self.mode = 'poll'
			
			#Don't hammer the CPU
			if self.disp.pending_events() == 0:
				time.sleep(0.1)
				continue
			
			
			e = self.disp.next_event()
			if e.type == X.KeyPress:
				
				keycode = e.detail
				mods= self.xkey.getModStrings(e.state) # List of modifiers down
				key = dict(self.xkey.getKeyByKeycode(keycode)) # Key details
				
				if self.xkey.isMod(key["keycode"]):
					continue
				

				#Handle hotkey callbacks
				if self.mode == 'hotkey':
					for k, v in self.bound.items():
						if keycode == k.internal["keycode"] and e.state in k.internal["mask_permutations"]:
							v(k)
				
				#Otherwise process data and return
				elif self.mode == 'poll':
					#Get an english representation
					string = mods
					string.append(key["string"])
					string = " + ".join(string)
					
					key["ignore_mask"] = self.xkey.getIgnoreMask()
					key["mod_mask"] = e.state & key["ignore_mask"] 
					key["string"] = string
					key["mask_permutations"] = self.xkey.mask_permutations(key['mod_mask'], key['ignore_mask'])
					
					bindkey.internal = key
					bindkey.string = string	
					
					self.disp.ungrab_keyboard(X.CurrentTime)
					self.disp.flush()
					
					self.mode = 'hotkey'
					self.queue.task_done()
					
					if callback:
						callback(bindkey)				
	def poll(self, *args):
		bindkey = key.key()
		bindkey.engine = 'xlib'
		callback = None
		if args: callback = args[0]
		
		self.queue.put((bindkey, callback))
		if not callback:
			self.queue.join()
			return bindkey

	def stop(self):
		self.running = False
		self.disp.flush()
		self.disp.close()
	
	def add(self, key, callback):
		self.bound[key] = callback
		for mask in key.internal["mask_permutations"]:
			self.root.grab_key(key.internal["keycode"], mask, 1, X.GrabModeAsync, X.GrabModeAsync)
def getInstance():
	return EngineXlib()


