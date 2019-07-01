# giessautomatik

wasseruhr.py und feuchtestatus.py werden beim booten gestartet. 

wasseruhr: 
Gibt den aktuellen Zählerstand per ZMQ aus. Dzu muss der GPIO des Flowsensors angepasst werden. Der Zählerstand wird (je nach Bedarf) vom wspeichern.py per cronjob weggeschrieben. Wird der Raspi neu gestartet, wlädt wasseruhr.py diesen Wert ein und setzt den alten Zählerstand fort. Ohne wspeichern.py würde wasseruhr.py bei jedem Neustart bei 0 beginnen.

feuchtestatus:
Gibt die aktuellen Bodenfeuchtewerte (in Volt) per ZMQ raus. feuchtelog.py gibtden aktuellen wert aus und feuchtelog schreibt diesen Wert weg. 

zmq_listener.py:
Nur zum Testen, ob feuchtelog.py und wasseruhr.py laufen.

http-dir/indes.html
HMTL-Formblatt zum Giessen, ruft anschliessend 

http-dir/cgi-bin/startgiess.py auf:
giessen.py wird mit den entsprechenden Parametern vom HTML-Formblatt gstartet und in den Hintergrund geschoben. Sendet aktuellen Giess-status per ZMQ. 

http-dir/cgi-bin/giess_status-py:
Gibt aktuellen Giess-Status aus, der per ZMQ von giessen.py empfangen wird. Wird automatisch neu geladen, wird mehr als 4x ohne, dass gegossen wird, neu geladen, wird auf status.py umgeleitet.

http-dir/cgi-bin/status.py
Gibt alle Möglichen Werte (Feucte, GPIO/Relais-Status, Zählerstand der Wasseruhr, Raspi-Temperatur, -WLAN-Anbundung, etc.) aus. 

Ich habe status.py im normalen /usr/lib/cgi-bin liegen, die anderen cgi-bins liegen passwortgeschützt htpasswd) in einem extra Verzeichns. Man sollte über alle files drüberschauen, was man da anpassen muss (GPIOs, Verzeichnisse, Files,...)

Sicher gibt es bessere Möglichkeiten, nur bin ich kein guter Programmierer :}
