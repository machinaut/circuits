#!/usr/bin/env python
# script to auto-indent this random file i made
fn ="/home/ajray/eagle-5.11.0/projects/examples/hexapod/board.json"
f = open(fn)
indent = -1 # indentation level
for line in f.readlines():
  print "  "*indent + line.strip()
  indent += line.count('{')
  indent -= line.count('}')

