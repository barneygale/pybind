#!/usr/bin/python
import keysym_to_unicode
import re, glob
lines = []
ask = raw_input("Keep orphaned syms [y]?")
if ask == "n":
	syms = {}
else:
	syms = keysym_to_unicode.keysym_to_unicode
for f in glob.glob("/usr/include/X11/*keysym*h"):
	f = open(f, 'r')
	lines.extend(f.readlines())
	f.close()

for l in lines:
	#Fuck YES!
	m = re.match("#define XK_\w+\s+0x([A-Fa-f0-9]+)\s*/\*\s*U\+([A-Fa-f0-9]+)", l)
	if m:
		sym = int(m.group(1),16)
		uni = int(m.group(2),16)
		#Exclude control characters and space (0x20)
		if	0x00 <= uni <= 0x20 or \
			        uni == 0x7F or \
			0x80 <= uni <= 0x9F:
			continue
		syms[sym] = uni

if len(syms):
	output = open('constants.py', 'w')
	output.write(
"""### This file has been automatically generated by gen_constants.py

keysym_to_unicode = {
""")
	for k, v in syms.items():
		output.write('\t0x%07x:\t0x%04x,\n' % (k,v))
		#print "%s\t%x" % (k,v)
	output.write("}")
	output.close()
