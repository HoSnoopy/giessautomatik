#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import cgi, cgitb


#URL
refresh =  ('<meta http-equiv="refresh" content="0; URL=https://preachout.sytes.net/giess/giessen/giess/giess_status.py">')

giesspfad = "/var/www/html/giessen/giess/giessen.py"


def main():
#Instanz FieldStorage

    form = cgi.FieldStorage()

#Hole Daten vom skript

    v1 = str(form.getvalue('v1'))
    v2 = str(form.getvalue('v2'))
    v3 = str(form.getvalue('v3'))
    v4 = str(form.getvalue('v4'))

    parameter = ('"v1=' + v1 + '&v2=' + v2 + '&v3=' + v3 + '&v4=' + v4 + '"')
    
    shell = "/usr/bin/nohup " + giesspfad + " " + parameter + " > /dev/null &"

    os.system(shell)

    
    print "Content-type:text/html\r\n\r\n"

    print "<html>"
    print "<head>"
    print refresh
    print "</head>"
    print "</html>"

if __name__ == "__main__":
   main()

