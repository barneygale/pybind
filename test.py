#!/usr/bin/python

from binder import *
import time
import sys

def callback(key):
	print key
def call_escape(key):
	global escape
	escape = True
def call_assign(key):
	global assign
	assign = True


mybinder = Binder()

time.sleep(10)
sys.exit(1)

print mybinder.poll().internal["keycode"]
print "Select an an escape"
mybinder.add(mybinder.poll(), call_escape)
print "Select an assigner"
mybinder.add(mybinder.poll(), call_assign)
print "GO!"

escape = False
assign = False

while not escape:
	time.sleep(100)
	if assign:
		print "assign a key..."
		mybinder.add(mybinder.poll(), callback)
		assign = False



mybinder.stop()
