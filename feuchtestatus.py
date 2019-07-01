#!/usr/bin/env python
# -*- coding: utf-8 -*-

import zmq
import spidev
import time

herz = 1000

spi = spidev.SpiDev()

#ZMQ-Einstellungen 
port = "10001"
host = "192.168.70.125"
thema = "10001"
context = zmq.Context()
sock = context.socket(zmq.PUB)
sock.bind("tcp://{}:{}".format(host, port))

#Lese Spannungswerte aller 8 Eingänge am MCP3208 ein
def spannung():
   feuchte = ""
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
       u = val * (3.3/4095)  #12-bit => 0...4095                 
       u = round (u,3)
       feuchte = feuchte + " " + str(u)
       time.sleep(0.1)
   spi.close() 
   return (feuchte)
    

while True:
    try:
        time.sleep(1)
        feuchte = spannung()
        #print(feuchte)
        sock.send_string("{} {}".format(thema, feuchte))
    except KeyboardInterrupt:
        print '\ncaught keyboard interrupt!, bye'
        GPIO.cleanup()
        socket.close
        sys.exit()
