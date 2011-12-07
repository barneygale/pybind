from constants import vk_to_string
from ctypes import *
from ctypes import wintypes
import threading
import time
from Queue import Queue
import key

user32 = windll.user32
kernel32 = windll.kernel32

WH_KEYBOARD_LL = 0b1101 #TODO: check
WM_KEYDOWN     = 0x0100
WM_KEYUP       = 0x0101
WM_SYSKEYDOWN  = 0x0104

class EngineUser32(threading.Thread):
	queue = Queue()
	mode = None
	modifiers = [
		('Control', 1<<1, 0x11),
		('Win',     1<<3, 0x5b),
		('Alt',     1<<0, 0x12),
		('Shift',   1<<2, 0x10)]
		
		
	ignore = [
		0x10,
		0x11,
		0x12,
		0x5b,
		0x5c,
		0xa0,
		0xa1,
		0xa2,
		0xa3,
		0xa4,
		0xa5]
		
	"""vk_to_mod = {}
	mod_status = {}
	for mod in modifiers:
		vk_to_mod.update(dict([(i, mod[0]) for i in mod[2]]))
		mod_status[mod[0]] = False"""
	
	def __init__(self):
		threading.Thread.__init__(self)
		#self.callback_pointer = CFUNCTYPE(c_int, c_int, c_int, POINTER(c_void_p))(self.callback)
		self.start()
		#pass
		
	def run(self):
		print "running..."
		#Hook the keyboard
		
		#Enter the message loop
		#return
		while True:
			# 1. detect whether we need to poll
			if self.mode == 'poll':
				print "Going into polling mode"
				self.mode = None
				CMPFUNC = CFUNCTYPE(c_int, c_int, c_int, POINTER(c_void_p))
				pointer = CMPFUNC(self.callback)
				self.hook = user32.SetWindowsHookExW(
					WH_KEYBOARD_LL,
					pointer,
					kernel32.GetModuleHandleA(0),
					0 # this specifies that the hook is pertinent to all threads
				)
				if not self.hook:
					raise EngineError("Couldn't hook the keyboard")
			# 2. pump messages
			ret = True
			while ret:
				msg = wintypes.MSG ()
				#PeekMessage rather than GetMessage so it doesn't block!
				ret = user32.PeekMessageA (byref (msg), None, 0, 0, 1)
				if ret:
					print "something!"
					user32.TranslateMessage (byref (msg))
					user32.DispatchMessageA (byref (msg))
				else:
					#print "nothing"
					time.sleep(0.1)
					continue
		msg = True
		while msg and self.hook is not None:
			print "pumping message..."
			msg = self.pumpMessage()
		print "DONE?!"
	def pumpMessage(self):
		msg = wintypes.MSG ()
		print "getmessage"
		ret = user32.GetMessageA (byref (msg), None, 0, 0)
		if ret:
			print "translate"
			user32.TranslateMessage (byref (msg))
			print "dispatch"
			user32.DispatchMessageA (byref (msg))
			return msg
		return None
			
	def poll(self, *args):
		print "poll0"
		bindkey = key.key()
		bindkey.engine = 'user32'
		callback = None
		if args: callback = args[0]
		#Queue our request
		self.queue.put((bindkey, callback))
		self.mode = 'poll'
		if not callback:
			self.queue.join()
			return bindkey
		print "poll8: done"
	
	def callback(self, nCode, wParam, lParam):
		if wParam in (WM_KEYDOWN, WM_SYSKEYDOWN):
			vk, scancode = lParam[:2]
			if vk not in self.ignore:
				#string = eventToString(vk, scancode)
				#print string
				
				#Part 1: get modifiers
				
				user32.GetKeyState(0) #flush
				keyState = (c_uint8 * 256)() #Array of c_long
				user32.GetKeyboardState(byref(keyState))
				mods = []
				for mod in self.modifiers:
					if keyState[mod[2]] & 1<<7:
						mods.append(mod[0])
					keyState[mod[2]] = 0
				print mods
				
				#Part 2a: get key string via ToUnicodeEx
				
				string = None
				buf = create_string_buffer('')
				buflen = user32.ToUnicodeEx(vk, scancode, keyState, byref(buf), 1, 0, None)
				if buflen > 0:
					buf = buf.value[0]
					if ord(buf) > 32 and ord(buf) != 127:
						string = buf
				
				#Part 2b: get key string via constant lookup
				
				if not string and vk in vk_to_string:
					string = vk_to_string[vk]
				
				try:
					item = self.queue.get_nowait()
		return user32.CallNextHookEx(self.hook, nCode, wParam, lParam)


def getInstance():
	return EngineUser32()
