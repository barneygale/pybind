from Quartz import *

def MyFunction(p, t, e, c):
    print e

tap = CGEventTapCreate(kCGHIDEventTap, kCGHeadInsertEventTap, kCGEventTapOptionListenOnly, CGEventMaskBit(kCGEventLeftMouseDown), MyFunction, None)

runLoopSource = CFMachPortCreateRunLoopSource(None, tap, 0);
CFRunLoopAddSource(CFRunLoopGetCurrent(), runLoopSource, kCFRunLoopDefaultMode);
CGEventTapEnable(tap, True);

CFRunLoopRun();

