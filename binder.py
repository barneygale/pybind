import os, glob, imp, key
#import importlib
import sys
from error import *
import engines

class Binder:
	engines = ['xlib']
	def die(self, why):
		print why
		sys.exit()
	def __init__(self, *args):
		if args:
			self.engines = [args[0]]
		self.engine = None
		for e in engines.__all__:
			print " [ ENGINE %s ]" % e
			try:
				self.engine = __import__ ('engines.'+e)
				self.engine = sys.modules['engines.'+e]
				self.engine = self.engine.getInstance()
				self.engine_name = e
				print " ---> OK!"
				break
			except EngineError as e:
				print " ---> %s" % e
				e = None
			except ImportError as e:
				print " ---> %s" % e
				e = None
		if not self.engine:
			if args:
				self.die("Couldn't load engine %s" % args[0])
			else:
				self.die("Couldn't load any engines!")
		
	def poll(self, *args):
		return self.engine.poll(*args)
	def stop(self):
		self.engine.stop()
	def add(self, *args):
		return self.engine.add(*args)
