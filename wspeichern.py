#!/usr/bin/python

import zmq
import os
import socket as socke

wdat="/opt/daten/wasseruhr.dat"

global count

if os.path.isfile(wdat):
     print("benutze " + wdat)
     datei=open(wdat, 'r')
     for line in datei:
        count = int(line)
     datei.close 
else:
     print("Keine Datei gefunden, setze Zaehler auf 0")
     count = 0


context = zmq.Context()
socket = context.socket(zmq.SUB)
host="192.168.70.125"
thema="10001"

context = zmq.Context()

port=10000
sock = context.socket(zmq.SUB)
sock.connect("tcp://{}:{}".format(host, port))
sock.setsockopt(zmq.SUBSCRIBE, thema)

message = sock.recv()
message = message.strip().split(' ')[1]
newcount = int(message)
if newcount > count:
    datei = open(wdat, "w+") 
    datei.write(str(newcount))
    print ("Schreibe neuen Wert ("+ str(newcount)+") in Zaehlerdatei (" + wdat + ")")
    datei.close
else:
    print("Wert("+str(message)+") hat sich nicht geaendert => schreibe nicht")


