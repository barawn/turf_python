import os, sys, mmap

class XillybusDevice:
    def __init__(self, requestPath="/dev/xillybus_mmreq", responsePath="/dev/xillybus_mmresp"):
        try:
            self.reqf = os.open(requestPath, os.O_WRONLY | os.O_SYNC)
            self.rspf = os.open(responsePath, os.O_RDONLY)            
        except OSError as err:
            print("OS error: {0}".format(err))
        self.tag = 0
    
    def read(self, addr):
        tagaddr = ((self.tag & 0x7) << 4) | ((addr>>24) & 0xF)
        tagaddr |= 0x80
        b = bytearray([addr & 0xFF, (addr>>8) & 0xFF, (addr>>16) & 0xFF, tagaddr])
        buf = mmap.mmap(-1, 4)
        buf.write(b)
        print(b)
        os.write(self.reqf, buf)
        print(os.read(self.rspf, 4))
        print(os.read(self.rspf, 4))
        