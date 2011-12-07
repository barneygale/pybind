import objc
from Foundation import *
from PyObjCTools import AppHelper
from Quartz import *
from AppKit import *
import threading
from error import EngineError
from ctypes import *
from constants import keycode_to_string
import sys
import math


class EngineQuartz(threading.Thread):
	flags = 0
	def __init__ (self, key):
		self.modifiers = {
			'mods_considered_mods': [
				('Shift', kCGEventFlagMaskShift),
				('Control', kCGEventFlagMaskControl),
				(unichr(0x2318), kCGEventFlagMaskAlternate),
				(unichr(0x2318), kCGEventFlagMaskCommand),
				('Help', kCGEventFlagMaskHelp),
				('Secondary Function', kCGEventFlagMaskSecondaryFn),
				('Num Pad', kCGEventFlagMaskNumericPad),
				('NonCoalesced', kCGEventFlagMaskNonCoalesced)],
			'mods_considered_keys': [
				('Caps Lock', kCGEventFlagMaskAlphaShift),
			]}
		#self.keys_c_mods_state = dict([(v[1]
		#self.modifier_flag_to_name = dict((v[1], v[0]) for v in self.modifiers)
		self.ignore_mask = 0
		for name, mask in self.modifiers['mods_considered_mods']:
			self.ignore_mask |= mask
		#print bin(self.ignore_mask)
		threading.Thread.__init__(self)
		self.keyFactory = key
		self.start()
	def poll(self, *args):
		bindkey = self.keyFactory.key()
		bindkey.engine = 'quartz'
		if args: callback = args[0]
		else:    callback = None
		self.queue.put((bindkey, callback))
		if not callback:
			self.queue.join()
			return bindkey
	def run(self):
		tap = CGEventTapCreate(
			kCGHIDEventTap, 
			kCGHeadInsertEventTap,
			kCGEventTapOptionListenOnly, 
			CGEventMaskBit(kCGEventFlagsChanged)|CGEventMaskBit(kCGEventKeyDown)|CGEventMaskBit(kCGEventKeyDown),
			self.testcallback,
			None)
		runLoopSource = CFMachPortCreateRunLoopSource(
			None, 
			tap, 
			0);
		CFRunLoopAddSource(
			CFRunLoopGetCurrent(), 
			runLoopSource, 
			kCFRunLoopDefaultMode)
		CGEventTapEnable(tap, True)
		print "starting event loop"
		CFRunLoopRun()
		print "running..."

	def testcallback(self, p, t, e, c):
		#keycode = CGEventGetIntegerValueField(e, kCGKeyboardEventKeycode)
		#if index, data in enumerate(self.modifiers['keys_considered_mods']):
		#	self.modifiers['keys_considered_mods'][index] = 
		
		flags = int(CGEventGetFlags(e))
		if t == kCGEventFlagsChanged:
			for string, mask in self.modifiers['mods_considered_keys']:
				if mask & flags:
					code = ('m', mask)
					
			
		#	if index, data in enumerate(self.modifiers['keys_considered_mods']):
		
		
		
		
		print bin(flags)
		for name, mod in self.modifiers['mods_considered_mods']:
			if mod & flags:
				print name
		return
		mods = []
		#for mod in self.modifiers:
		#	if mod | flags:
				
		
		
		
		
		#if t == kCGEventFlagsChanged:
		#	self.flags = CGEventGetFlags(e)
		#	return
		
		
		
		
		
		
		#print "callback!"
		#print dir(p)
		#print t
		#print dir(e)
		#print c
		#print t
		#print "FLAGS", bin(CGEventGetFlags(e))
		string = self.event_to_string(e)
		print "GOT:", string
		if string == "Escape":
			sys.exit(1)
		#if string in [e[0] for e in self.modifiers]:
		#	print "GOT A MOD!"
		#print "KEYCODE", CGEventGetIntegerValueField(e, kCGKeyboardEventKeycode)
		#if t == kCGEventFlagsChanged:
		#print "FLAGS", CGEventGetFlags(e)
	def event_to_string(self, e):
		keycode = CGEventGetIntegerValueField(e, kCGKeyboardEventKeycode)
		maxStringLength = 10
		char = CGEventKeyboardGetUnicodeString(e, maxStringLength, None, None);
		if char[0]: 
			char = char[1][0]
			if char > 32 and char != 127:
				return unichr(char)
		if keycode in keycode_to_string:
			return keycode_to_string[keycode]
		return "NOT FOUND!"
def getInstance(key):
	return EngineQuartz(key)
