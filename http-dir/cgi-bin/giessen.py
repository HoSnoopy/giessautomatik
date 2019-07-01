#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Import modules for CGI handling 
import RPi.GPIO as GPIO
import cgi, cgitb 
import time, datetime
import zmq
import os

status_html = '/var/www/html/giessen/stat_giess.html'

def wasserlesen():
    #Hostname für ZMQ editieren!
    host="192.168.70.125"
    thema="10001"
    port = 10000
#    try:
    context = zmq.Context()
    sock = context.socket(zmq.SUB)
    sock.connect("tcp://{}:{}".format(host, port))
    sock.setsockopt(zmq.SUBSCRIBE, thema)
    string = sock.recv()
    message = string.strip().split(' ')[1]
 
#    except: 
#      message = 0
#      os.system('/usr/local/sbin/wstop.py')
#      GPIO.cleanup()
    sock.close
    return(int(message))

def astop_stop():
    time.sleep(2) 
    #GPIO für Aquastop anpassen!
    astop = 14
    GPIO.setwarnings(False) 
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(astop, GPIO.OUT)
    GPIO.output(astop, GPIO.LOW)
    return('Aquastop geschlossen')

def stop(ventil):
    time.sleep(2) 
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False) 
    ventil = int(ventil)
    #GPIO der Ventile anpassen!
    ventile = [14, 25, 17, 27, 24] 
    vent = int(ventile[ventil])
    GPIO.setup(vent, GPIO.OUT)
    GPIO.output(vent, GPIO.LOW)
    return("Ventil " + str(ventil) + " (GPIO" + str(vent) + ") gestoppt.") 

def start(ventil):
    time.sleep(2)
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False) 
    #GPIO der Ventile anpassen!
    ventil = int(ventil)
    ventile = [14, 25, 17, 27, 24] 
    vent = int(ventile[ventil])
    GPIO.setup(vent, GPIO.OUT)
    GPIO.output(vent, GPIO.HIGH)
    return("Ventil " + str(ventil) + " (GPIO" + str(vent) + ") gestartet.") 

def astop_start():
    time.sleep(2) 
    GPIO.setwarnings(False) 
    #GPIO für Aquastop anpassen!
    astop = 14
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(astop, GPIO.OUT)
    GPIO.output(astop, GPIO.HIGH)
    meldung = ('Aquastop (GPIO'+str(astop)+') geöffnet')
    return(meldung)


def main(): 
#Instanz FieldStorage

    schreib = open(status_html, 'w')
    schreib.close


    form = cgi.FieldStorage() 

#Hole Daten vom skript

    v1 = str(form.getvalue('v1'))

    if v1=='None' or v1=='':
        v1=0

    try: 
        v1 = int(v1)
    except:
        v1 = 0


    v2 = str(form.getvalue('v2'))

    if v2 == 'None' or v2 == '':
        v2=0

    try: 
         v2 = int(v2)
    except:
         v2 = 0

    v3 = str(form.getvalue('v3'))

    if v3 == 'None' or v3 == '':
         v3=0
    try: 
         v3 = int(v3)
    except:
         v3 = 0

    v4 = str(form.getvalue('v4'))

    if v4 == 'None' or v4 == '':
         v4=0

    try: 
         v4 = int(v4)
    except:
         v4 = 0

    ventile = []
    ventile.append(v1)
    ventile.append(v2)
    ventile.append(v3)
    ventile.append(v4)

    
    thema = "10000"
    v = 0
    for m in ventile: 
        schreib = open(status_html, 'a')
        oldcount = wasserlesen()
        v=v+1
        zeit = (time.strftime("%H:%M"))
        datum = (time.strftime("%d.%m.%Y"))
        if m == 0:
           print('Bereich '+ str(v) + ' wird nicht gegossen.')
           schreib.write('Bereich ' + str(v) + ' wurde am ' + datum + ' um ' + zeit + 'Uhr laut Befehl nicht gegossen.<p>') 
        else:
           global venti
           venti = str(v) 
           menge = m*420
           print('Bereich '+ str(v) + ': ' + str(m) + 'l, entspricht ' + str(menge) + ' Einheiten.\n')
           print(astop_start())
           print(start(venti))
           newcount = wasserlesen()
           differenz = newcount - oldcount

           port = "10002"
           host = "192.168.70.125"
           thema = "10001"
           context = zmq.Context()
           socket = context.socket(zmq.PUB)
           socket.bind("tcp://{}:{}".format(host, port)) 


           while differenz < menge:
                 newcount = wasserlesen()
                 differenz = newcount - oldcount
                 proz = int(differenz*100/menge)
                 if proz > 100:
                    proz = 100 
                 sendung = ('Gie&szlig;e Bereich ' + str(v) + ' (' + str(m) + 'l), ' + str(proz)) 
                 socket.send_string("{} {}".format(thema, sendung))
           #      print(proz)
           
           print(astop_stop())
           print(stop(venti))
  
           schreib.write('Bereich ' + str(v) + ' wurde am ' + datum + ' um ' + zeit + 'Uhr mit ' + str(m) + 'l gegossen.<p>') 



           schreib.close

if __name__ == "__main__":
   main()
