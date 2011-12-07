import win32con
for i in dir(win32con):
	if i.startswith("WH_KEYBOARD"):
		print i
