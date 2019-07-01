#!/usr/bin/python

import zmq
import cgi, cgitb

status_html = '/var/www/html/giessen/stat_giess.html'

log = ''

try: 
  lese=open(status_html, 'r')
  for zeile in lese:
      log = log + zeile 
  lese.close
  
except:
  log = 'meeeh!'


host="192.168.70.125"
thema="10001"
port=10002

form = cgi.FieldStorage()
v = str(form.getvalue('v'))

if v=='None' or v=='':
    v=0
try:
   v = int(v)
except:
   v = 0



context = zmq.Context()

try:
  sock = context.socket(zmq.SUB)
  sock.connect("tcp://{}:{}".format(host, port))
  sock.setsockopt(zmq.SUBSCRIBE, thema)
  sock.setsockopt(zmq.RCVTIMEO, 2000)
  
  s=''
  string = sock.recv()
  string = string[6:]
  string = string+'%'

  refresh =  ('<meta http-equiv="refresh" content="1; URL=https://preachout.sytes.net/giess/giessen/giess/giess_status.py">')

except:
  v = v + 1
  string = 'Es wird gerade nicht gegossen.'
  if v < 5:
       refresh =  ('<meta http-equiv="refresh" content="1; URL=https://preachout.sytes.net/giess/giessen/giess/giess_status.py?v=' + str(v) + '">')
  else:
       refresh =  ('<meta http-equiv="refresh" content="1; URL=https://preachout.sytes.net/giess/cgi-bin/status.py">')
    



print "Content-type:text/html\r\n\r\n"

print "<html>"
print "<head>"
print refresh
print "</head><body><center>"
print "<h1>Gie&szlig-Status</h1>"

print  "<p>"

print log

print  "<br><p>"
print string
