import xkey
from Xlib import display



key = xkey.xkey(display.Display())
p = key.mask_permutations(0b10000001, 0b01111011)
for x in p:
	print "%s" % bin(x)
