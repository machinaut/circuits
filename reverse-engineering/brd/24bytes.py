#!/usr/bin/env python
# 24bytes.py - display binary in 24 byte rows
import binascii

def hexify(s):
    return " ".join([binascii.hexlify(i) for i in s])


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print 'Usage: layerparser.py <eaglefile.brd>'
        exit()
    f = open(sys.argv[1],"rb")
    buf = f.read()
    for i in range(0,len(buf),24):
        print hexify(buf[i:i+24])
