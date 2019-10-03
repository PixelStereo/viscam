#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys

from pyviscam.broadcast import v_cams

# a camera is created in visca_app
# create a visca bus object
cams = v_cams()
# get a list of serial ports available and select the last one
ports = cams.serial.listports()

port = ports[0]

# open a connection on the serial object
cams.reset(port)
cams = cams.get_instances()
v = cams[0]

# create OSC server for binding to v (instance of VISCA)
libs_path = os.path.abspath('./../3rdparty')
sys.path.append(libs_path)
from pydevicemanager.osc import OSCServer
osc = OSCServer(v, 22222, name='viscam')

if __name__ == "__main__" :
	# loop and dispatch messages every 100ms
	try:
		while 1:
			osc.server.recv(10)
	except KeyboardInterrupt:
		quit()
