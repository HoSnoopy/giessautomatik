#!/usr/bin/python

import zmq

host="192.168.70.125"
thema="10001"

context = zmq.Context()

while True:
 port=10000
 sock = context.socket(zmq.SUB)
 sock.connect("tcp://{}:{}".format(host, port))
 sock.setsockopt(zmq.SUBSCRIBE, thema)

 string = sock.recv()
 string = string.strip().split(' ')[1]

 port = 10001
 sockf = context.socket(zmq.SUB)
 sockf.connect("tcp://{}:{}".format(host, port))
 sockf.setsockopt(zmq.SUBSCRIBE, thema)

 stringf = sockf.recv()
 stringf = stringf[7:]

 print (string + " " + stringf)
