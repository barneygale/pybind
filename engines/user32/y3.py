#!/usr/bin/env python
from ctypes import *
from ctypes import wintypes
#import win32con, win32api, win32gui

class KeyboardHook:
	"""
	Written by: TwhK / Kheldar
	What do? Installs a global keyboard hook
	 
	To install the hook, call the (gasp!) installHook() function.
	installHook() takes a pointer to the function that will be called
	after a keyboard event.	installHook() returns True if everything
	was successful, and False if it failed
	Note:	I've also provided a function to return a valid function pointer
	 
	To make sure the hook is actually doing what you want, call the
	keepAlive() function
	Note:	keepAlive() doesn't return until kbHook is None, so it should
	be called from a separate thread
	 
	To uninstall the hook, call uninstallHook()	 

	Note:	relies on modules provided by pywin32.
	http://sourceforge.net/projects/pywin32/
	"""
	def __init__(self):
		self.user32	 = windll.user32
		self.kbHook	 = None
	 
	def installHook(self, pointer):
		self.kbHook = self.user32.SetWindowsHookExW(
			13, #win32con.WH_KEYBOARD_LL,
			pointer,
			windll.kernel32.GetModuleHandleA(0),
			0 # this specifies that the hook is pertinent to all threads
		)
		if not self.kbHook:
			return False
		return True
	"""
	def keepAlive(self):
		if self.kbHook is None:
			return
		msg = win32gui.GetMessage(None, 0, 0)
		while msg and self.kbHook is not None:
			win32gui.TranslateMessage(byref(msg))
			win32gui.DispatchMessage(byref(msg))
			msg = win32gui.GetMessage(None, 0, 0)
	"""
	def keepAlive(self):
		
		ret = True
		while ret and self.kbHook is not None:
			msg = wintypes.MSG ()
			ret = self.user32.GetMessageA (byref (msg), None, 0, 0)
			if ret:
				user32.TranslateMessage (byref (msg))
				user32.DispatchMessageA (byref (msg))

	def uninstallHook(self):
		if self.kbHook is None:
			return
		self.user32.UnhookWindowsHookEx(self.kbHook)
		self.kbHook = None

from ctypes import *

##################################################
# returns a function pointer to the fn paramater #
# assumes the function takes three params:		 #
# c_int, c_int, and POINTER(c_void_p)			#
##################################################
def getFunctionPointer(fn):
	CMPFUNC = CFUNCTYPE(c_int, c_int, c_int, POINTER(c_void_p))
	return CMPFUNC(fn)

#!/usr/bin/env python
from ctypes import *
#from misc import *
#from KeyboardHook import KeyboardHook
user32 = windll.user32

#############################################
# Sample function to handle keyboard events #
#############################################
def kbEvent(nCode, wParam, lParam):
	if wParam is not 256: #win32con.WM_KEYDOWN: # It just occured to me that I should aso be checking for WM_SYSKEYDOWN as well
		return user32.CallNextHookEx(keyboardHook.kbHook, nCode, wParam, lParam)
	#print bin(lParam[2])	
	
	
	
	
	print "VK: %d %s" % (lParam[0], chr(lParam[0]))
	print "scanCode: %d" % lParam[1]
	keyStateType = c_long * 256
	keyState = keyStateType()
	user32.GetKeyboardState(byref(keyState))
	

	buf = create_string_buffer('')
	buflen = user32.ToUnicodeEx(lParam[0], lParam[1], keyState, byref(buf), 10, 0, None)
	buf = buf.value[0]
	print buf
	
	print "ok did that"
	return user32.CallNextHookEx(keyboardHook.kbHook, nCode, wParam, lParam)
	 
keyboardHook = KeyboardHook()
pointer = getFunctionPointer(kbEvent)
if keyboardHook.installHook(pointer):
	print "installed hook"
#keyboardHook.uninstallHook()
#print "removed hook"
keyboardHook.keepAlive()

raw_input()


