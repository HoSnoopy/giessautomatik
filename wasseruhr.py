#!/usr/bin/env python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time, sys
import zmq
import os

#GPIO des Wasserhrsignals
FLOW_SENSOR = 22

#Datei, in der der Wert abgespeichert wurde
wdat="/opt/daten/wasseruhr.dat"

#GPIO für den Sensor konfigurieren
GPIO.setmode(GPIO.BCM)
GPIO.setup(FLOW_SENSOR, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)


global count
#Nachsehen, ob eine Datei der Wasseruhr existiert, wenn nicht, wird der Zähler auf "0" gesetzt
if os.path.isfile(wdat):
     print("benutze " + wdat)
     datei=open(wdat, 'r')
     for line in datei:
        count = int(line)
else:
     print("Keine Datei gefunden, setze Zaehler auf 0")
     count = 0 

#ZMQ-Einstellungen 
port = "10000"
host = "192.168.70.125"
thema = "10001"
context = zmq.Context()
sock = context.socket(zmq.PUB)
sock.bind("tcp://{}:{}".format(host, port))


#Zähle pro Impuls auf GPIO-Pin eins weiter
def countPulse(channel):
   global count
   count = count+1
   #print(count)

#Führe das Zählen auf, wenn ein Impuls auf GPIO ankommt
GPIO.add_event_detect(FLOW_SENSOR, GPIO.RISING, callback=countPulse)


while True:
    try:
        time.sleep(1)
        sock.send_string("{} {}".format(thema, str(count)))
    except KeyboardInterrupt:
        print '\ncaught keyboard interrupt!, bye'
        GPIO.cleanup()
        socket.close
        sys.exit()
