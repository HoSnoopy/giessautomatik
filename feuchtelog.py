#!/usr/bin/python


import spidev
import time
import math

spi = spidev.SpiDev()

proz=2.8/100

herz = 500000



def eformat(f, prec, exp_digits):
    s = "%.*e"%(prec, f)
    mantissa, exp = s.split('e')
    # add 1 to digits as 1 is taken by sign +/-
    return "%se%+0*d"%(mantissa, exp_digits+1, int(exp))

out = ''

spi.open(0,1)  
spi.max_speed_hz=(herz)
for c in range (8):
       if c < 4:
          com1 = 0x06
          com2 = c * 0x40
       else: 
          com1 = 0x07
          com2 = (c-4) * 0x40
    
       antwort = spi.xfer([com1, com2, 0])


       val = ((antwort[1] << 8) + antwort[2])  # Interpretieren der Antwort
       val = int(val)
       u = val * (3.3/4095)                   
       u = round (u,3)
       out = out + (str(u) + ' ')
       time.sleep(0.1)
spi.close() 
print (out)
out = ''
