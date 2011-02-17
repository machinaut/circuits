#!/usr/bin/env python
# layerparser.py - parse layers from eagle file
import binascii

layers = {} # dict to hold all the layers
signals = {}

class Header:
    def __init__(self,s):
        # The header is interesting, there are a few bytes that keep changing
        # and as far as i can guess, they are some kind of parity or checksum
        # There are 3 bytes that are useful

class Layer:
    def __init__(self,s):
        self.s = s
        # first byte: edited or not
        if   s[1] == '\x00':
            self.edited = False
        elif s[1] == '\x80':
            self.edited = True
        else:
            self.edited = "Unknown"
        # second byte, some kind of print/not
        # TODO - not verified, but this is a guess
        #   top - prints on top side
        #   bot - prints on bottom side
        #   png - shows up in a print
        #   not - does not show up in a print
        if   s[2] == '\x0f':
            self.png = "top png"
        elif s[2] == '\x1f':
            self.png = "bot png"
        elif s[2] == '\x03':
            self.png = "top png"
        elif s[2] == '\x13':
            self.png = "bot png"
        else:
            self.png = "unknown"
        # Third Byte, it's layer number
        self.number = ord(s[3])
        # Fourth Byte - either the layer number
        #   of the opposing layer if it has an
        #   inverse (Top/Bottom, tSilk/bSilk)
        #   or just its number repeated otherwise
        # True - if it has an inverse (Top/Bottom)
        # False - if it does not (Pads, Vias, Holes)
        self.inverse = (s[3] == s[4])
        # Fifth Byte - Fill style (0-15)
        self.fillstyle = ord(s[5])
        # Sixth Byte - Color (0-63)
        self.color = ord(s[6])
        # Last bytes make up the name
        self.name = s[7:].strip()
        if self.edited != "Unknown":
            layers[self.number] = self
    def __str__(self):
        if self.edited != "Unknown":
            return str(self.number)+" : "+str(self.name)+" Edited: "+str(self.edited)\
                    +" Print: "+str(self.png)+" Inverse: "+str(self.inverse)\
                    +" Fillstyle: "+str(self.fillstyle)+" Color: "+str(self.color)
        else: # not actually a Layer
            # TODO - figure out why not every \x13 is a layer, or how to better filter
            return hexify(self.s)

class Signal:
    def __init__(self,s):
        self.s = s
        # first byte - no idea, could be extension of second byte
        # TODO - make a file w/ >256 wires of a single signal
        # Second Byte - Number of Wires
        self.qty = ord(s[2])
        # Last bytes make up the name
        self.name = s[12:].strip()
        self.wires = [] # list of wires on this signal
        signals[self.name] = self
    def __str__(self):
        return str(self.name)+" Wires("+str(self.qty)+"): "+str(self.wires)


class Wire:
    def __init__(self,s):
        self.s = s
        # first byte: edited or not
        if   s[1] == '\x00':
            self.edited = False
        elif s[1] == '\x80':
            self.edited = True
        else:
            self.edited = "Unknown"
        # Second Byte - no idea, so far always \x00
        # Third Byte - Layer
        self.layer = ord(s[3])
        # Bytes 4-11 make up the Y coordinate
        # Bytes 12-19 make up the X coordinate
        # TODO - no idea how they're packed in there
        self.y = s[4:12]
        self.x = s[12:19]
        # Last 4 bytes have to do with the thickness
        # TODO - figure that out out too
        self.thick = s[19:]

def hexify(s):
    return " ".join([binascii.hexlify(i) for i in s])

def parse_file(filename):
    """
    Attempt to read Eagle file data from their binary format
    """
    f = open(filename, "rb")
    buf = f.read()
    for i in range(0,len(buf),24):
        # NOTE: all of these have side effects of being added to a global storage
        while(buf[i] != '\x13'):
        if s[0] == '\x13':
            return Layer(s)
        if s[0] == '\x1c':
            return signalname(s)
        if s[0] == '\x22':
            return wire(s)
        else: # dont recognize it
            return hexify(s)

        print parsify(buf[i:i+24])
    print len(layers), hex(len(layers))
        


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print 'Usage: layerparser.py <eaglefile.brd>'
        exit()
    print 'Parsing file', sys.argv[1]
    parse_file(sys.argv[1])
