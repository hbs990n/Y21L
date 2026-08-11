#!/usr/bin/env python3
"""Convert the python2 print statements in scripts/gcc-wrapper.py to python3."""
p = 'scripts/gcc-wrapper.py'
src = open(p, encoding='utf-8').read()
src = src.replace('print "error, forbidden warning:", m.group(2)',
                  'print("error, forbidden warning:", m.group(2))')
src = src.replace('print line,', 'print(line, end=" ")')
src = src.replace("print args[0] + ':',e.strerror",
                  "print(args[0] + ':', e.strerror)")
src = src.replace("print 'Is your PATH set correctly?'",
                  "print('Is your PATH set correctly?')")
src = src.replace("print ' '.join(args), str(e)",
                  "print(' '.join(args), str(e))")
open(p, 'w', encoding='utf-8').write(src)
