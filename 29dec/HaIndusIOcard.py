#!/usr/bin/env python
# File pportbits.py
# http://www.bristolwatch.com/pport/index.htm
# By Lewis Loflin - lewis@bvu.net
# Example code to turn ON-OFF individual bits on PC 
# printer port Db25 pins 2-9.
# Must use my version of pyparallel on website for self.p.getData().
# Bitwise AND is used to clear a bit while bitwise OR used to set bit.

import parallel
import time


class Parallel_ports:
	def __init__(self):
		self.p = parallel.Parallel()

	def clearPin(self,bit_val):
	    if bit_val == 1:
	        self.p.setDataStrobe(0) # set databit 0, Pin 1
	    if bit_val == 2:
	        self.p.setData(self.p.getData() & (255 - 1)) # set databit 0, Pin 2
	    if bit_val == 3:
	        self.p.setData(self.p.getData() & (255 - 2)) # set bit 1, Pin 3
	    if bit_val == 4:
	        self.p.setData(self.p.getData() & (255 - 4)) # set bit 3, Pin 4
	    if bit_val == 5:
	        self.p.setData(self.p.getData() & (255 - 8)) # set bit 4, Pin 5
	    if bit_val == 6:
	        self.p.setData(self.p.getData() & (255 - 16)) # set bit 5, Pin 6
	    if bit_val == 7:
	        self.p.setData(self.p.getData()& (255 - 32)) # set bit 6, Pin 7
	    if bit_val == 8:
	        self.p.setData(self.p.getData() & (255 - 64)) # set bit 7, Pin 8
	    if bit_val == 9:
	        self.p.setData(self.p.getData() & (255 - 128)) # set bit 8, Pin 9
	    if bit_val == 14:
	        self.p.setAutoFeed(0) # set , Pin 14
	    if bit_val == 16:
	        self.p.setInitOut(0) # set , Pin 16
	    if bit_val == 17:
	        self.p.setSelect(0) # set , Pin 17
		
	
	def setPin(self,bit_val):
	    if bit_val == 1:
	        self.p.setDataStrobe(1) # set databit 0, Pin 1
	    if bit_val == 2:
	        self.p.setData(self.p.getData() | 1) # set databit 0, Pin 2
	    if bit_val == 3:
	        self.p.setData(self.p.getData() | 2) # set bit 1, Pin 3
	    if bit_val == 4:
	        self.p.setData(self.p.getData() | 4) # set bit 2, Pin 4
	    if bit_val == 5:
	        self.p.setData(self.p.getData() | 8) # set bit 3, Pin 5
	    if bit_val == 6:
	        self.p.setData(self.p.getData() | 16) # set bit 4, Pin 6
	    if bit_val == 7:
	        self.p.setData(self.p.getData() | 32) # set bit 5, Pin 7
	    if bit_val == 8:
	        self.p.setData(self.p.getData() | 64) # set bit 6, Pin 8
	    if bit_val == 9:
	        self.p.setData(self.p.getData() | 128) # set bit 7, Pin 9
	    if bit_val == 14:
	        self.p.setAutoFeed(1) # set , Pin 14
	    if bit_val == 16:
	        self.p.setInitOut(1) # set , Pin 16
	    if bit_val == 17:
	        self.p.setSelect(1) # set , Pin 17
	
	
	def getPin(self,bit_val):
	    if bit_val == 15:
	        return self.p.getInError()   # Pin15
	    if bit_val == 13:
	        return self.p.getInSelected()   # Pin13
	    if bit_val == 12:
	        return self.p.getInPaperOut()   # Pin12
	    if bit_val == 10:
	        return self.p.getInAcknowledge()   # Pin10
	    if bit_val == 11:
        	return self.p.getInBusy()   # Pin11
        
	
'''
# convert a 8-bit number (integer) to a binary. 
# Returns string.
# unlike python bin() this doesn't drop leading zeros
def convBinary(value):
    binaryValue = 'b'
    for  x in range(0, 8):
        temp = value & 0x80
        if temp == 0x80:
           binaryValue = binaryValue + '1'
        else:
            binaryValue = binaryValue + '0'
        value = value << 1
    return binaryValue

# Set all data port bits to 0
self.p.setData(0) # LEDs off
print "Port data latches =", self.p.getData() 
# read port data latches - should be 0

# use differing combinations 

# set bits D0, D1, D2, D3 

#__________________________________MAIN_CODE___________________________
 
for x in range (0,10):
	print "Pin value =", getPin(12) 
	time.sleep(0.5)
	


# Read and print data port:
xp = self.p.getData()
print "Value of data port =", convBinary(xp), " ", hex(xp) 
xp = self.p.PPRSTATUS()
print "Value of control port =", convBinary(xp), " ", hex(xp)
# should be Value of control port = b10000011   0x83 
# LEDs connected to port will show 10000011  
'''