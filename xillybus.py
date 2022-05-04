import os, sys, mmap, struct

class XillybusDevice:
    def __init__(self, requestPath="/dev/xillybus_mmreq", responsePath="/dev/xillybus_mmresp"):
        try:
            self.reqf = os.open(requestPath, os.O_WRONLY | os.O_SYNC)
            self.rspf = os.open(responsePath, os.O_RDONLY)            
        except OSError as err:
            print("OS error: {0}".format(err))
        self.tag = 0
    
    def _buildtagaddr(self, addr, read=False):
        tagaddr = ((self.tag & 0x7) << 4) | ((addr>>24) & 0xF)
        if read:
            tagaddr |= 0x80
        b = bytearray([addr & 0xFF, (addr>>8) & 0xFF, (addr>>16) & 0xFF, tagaddr])
        return b
        
    def read(self, addr):
        b = self._buildtagaddr(addr, True)
        buf = mmap.mmap(-1, 4)
        buf.write(b)
        os.write(self.reqf, buf)
        rb = os.read(self.rspf, 4)
        if rb != b:
            # should raise an error here or something, I dunno
            print("tagaddr readback incorrect: sent", b, "got", rb)
            return None
        self.tag = self.tag + 1
        return struct.unpack('I', os.read(self.rspf, 4))[0]

    def write(self, addr, value):
        b = self._buildtagaddr(addr, False)
        buf = mmap.mmap(-1, 8)
        buf.write(b)
        buf.write(struct.pack('I', value))
        os.write(self.reqf, buf)
        rb = os.read(self.rspf, 4)
        if rb != b:
            print("tagaddr readback incorrect: sent", b, "got", rb)
            return
        self.tag = self.tag + 1
        
    
        