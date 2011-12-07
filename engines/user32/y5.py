from ctypes import *
from ctypes import wintypes
import threading
user32 = windll.user32
kernel32 = windll.kernel32

class foo(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		CMPFUNC = CFUNCTYPE(c_int, c_int, c_int, POINTER(c_void_p))
		pointer = CMPFUNC(self.callback)
		hook = user32.SetWindowsHookExW(
			13, #win32con.WH_KEYBOARD_LL,
			pointer,
			kernel32.GetModuleHandleA(0),
			0 # this specifies that the hook is pertinent to all threads
		)
		ret = True
		while ret and hook is not None:
			msg = wintypes.MSG ()
			ret = user32.GetMessageA (byref (msg), None, 0, 0)
			if ret:
				user32.TranslateMessage (byref (msg))
				user32.DispatchMessageA (byref (msg))
	def callback(self, a, b, c):
		print "CALLBACK"			

print "k"
bar = foo()
