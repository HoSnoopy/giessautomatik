#!/usr/bin/python
#coding: utf-8

import cgi, cgitb 
import time
import datetime
import zmq
import RPi.GPIO as GPIO
import spidev
import subprocess
import os

spi = spidev.SpiDev()
herz = 500000

status_html = '/var/www/html/giessen/stat_giess.html'

feuchte = []
log = ''

temp = subprocess.check_output('vcgencmd measure_temp', shell=True)
temp = temp[5:9]
temp = float(temp)
if temp > 70:
   t = (str(temp) + "&deg;C (zu hei&szlig;!!!)") 
if temp <= 70:
   t = (str(temp) + "&deg;C ") 

w = os.popen('iwconfig wlan0 |grep Quali |cut -c 24-25')
wlan = str(w.read())
wlan = wlan[:2]
wlan = (wlan + "&#37;")
b = os.popen('iwconfig wlan0 |grep Bit |cut -c 20-22')
bit = str(b.read())
bit = bit[:3]
bit = bit.replace(" ", "")
bit = (bit + "Mbit/s")

try:
  lese=open(status_html, 'r')
  for zeile in lese:
      log = log + zeile
  lese.close
except: 
  log = ''


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
       feuchte.append(str(u))
       time.sleep(0.1)
spi.close() 


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

def boden(volt):
      volt = float(volt)
      if volt < 0.1:
         boden = "Nicht angeschlossen"
      if volt >= 0.1:
         boden = ("Feucht (" + str(volt) + "V)")
      if volt > 1.9:
         boden = ("Trocken (" + str(volt) + "V)")
      return(boden)
def pin(pin):
  GPIO.setup(pin, GPIO.OUT)
  status= GPIO.input(pin)
  if status == 1:
     stat = "<b>offen</b>"
  elif status == 0:
     stat = "geschlossen"
  else: 
     stat = "<b>ERROR!!</b>"
  return(stat)

httpzeit = (time.strftime("%H:%M"))
datum = (time.strftime("%d.%m.%Y"))

context = zmq.Context()
socket = context.socket(zmq.SUB)
host="192.168.70.125"
thema="10001"
port=10000
sock = context.socket(zmq.SUB)
sock.connect("tcp://{}:{}".format(host, port))
sock.setsockopt(zmq.SUBSCRIBE, thema)
message = sock.recv()
message = message.strip().split(' ')[1]

os.system("/usr/bin/wget https://preachout.sytes.net/cgi-bin/bodenfeuchte.py -O /tmp/feuchte.html > /dev/null")

z = int(message)
z = z/420
z = round (z)
z = str(z)[:-2]

print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head>"
print "<title>Status Gie&szlig;anlage am " + datum + " um " + httpzeit +"Uhr  </title>"
print "</head>"
print "<body>"
print "<center>"
print "<h2>Status Gie&szlig;anlage am " + datum + " um " + httpzeit +"Uhr  </h2>"
print "<p><br><p>"
print ("Z&auml;hlerstand: " + message + " entspricht etwa " + z + "l")
print "<p><br><p>"
print ("Ventile:")
print ("<p>")
print ("Aquastop: " + pin(14))  
print ("<p>")
print ("Ventil 1: " + pin(17) + ", Ventil 2: " + pin(15))
print ("<p>")
print ("Ventil 3: " + pin(24) + ", Ventil 4: " + pin(27))

print "<p><br><p>"

print ("Feuchte:")
print ("<p>")
print ("Bereich 1: " + boden(str(feuchte[0])) + ", Bereich 2: " + boden(str(feuchte[1])))
print ("<p>")
print ("Bereich 3: " + boden(str(feuchte[2])) + ", Bereich 4: " + boden(str(feuchte[4])))

print "<p><br><p>"
print ("Zuletzt gegossen:")
print ("<p>")
print (log)

print "<p><br><p>"
print("Temperatur Raspberry Pi: " + t)

print ("<p>")
print("WLAN-Signal: " + wlan + " (" + bit + ")")


print ("<p>")
print ('<img src="https://preachout.sytes.net/bodentest/feuchte.png">')

print "</body>"
print "</html>"

