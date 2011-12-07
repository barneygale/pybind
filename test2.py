#!/usr/bin/python

from binder import *
import time
import sys

print "TEST: Starting binder..."
mybinder = Binder()
print "TEST: Polling..."
key = mybinder.poll()
print "TEST: Stopping..."
mybinder.stop()
