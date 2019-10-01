#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
# for development of pyCamera, use git version
libs_path = os.path.abspath('./../3rdparty/pyvisca')
sys.path.append(libs_path)
libs_path = os.path.abspath('./../3rdparty/pydevicemanager')
sys.path.append(libs_path)

from pyviscam.broadcast import Viscam

# a camera is created in visca_app
# create a visca bus object
cams = Viscam()

# get a list of serial ports available and select the last one
ports = cams.serial.listports()

port = None
for item in ports:
    if 'usbserial' in item:
    	# this is for osx on my computer for testing
        port = item
if not port:
	try:
		port = ports[0]
	except IndexError:
		print('There is no available ports')
		quit()

print('serial port opening : ' + port)

# open a connection on the serial object
cams.reset(port)
cams = cams.get_instances()
v = cams[0]

# create OSC server for binding to v (instance of VISCA)
libs_path = os.path.abspath('./../3rdparty')
sys.path.append(libs_path)
from pydevicemanager.osc import OSCServer
osc = OSCServer(v, 22222, name='span')

if __name__ == "__main__" :
	# loop and dispatch messages every 100ms
	try:
		while 1:
			osc.server.recv(10)
	except KeyboardInterrupt:
		quit()
