#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
libs_path = os.path.abspath('./../3rdparty/pyvisca')
sys.path.append(libs_path)
from pyviscam.broadcast import Viscam

v = Viscam('/dev/tty.usbserial-FTFNNBFM').get_instances()[0]

# create OSC server for binding to v (instance of VISCA)
libs_path = os.path.abspath('./../3rdparty')
sys.path.append(libs_path)
from pydevicemanager.devicemanager import OSCServer
osc = OSCServer(v, 22222, name='span')


if __name__ == "__main__" :
	# loop and dispatch messages every 100ms
	try:
		while 1:
			osc.server.recv(100)
	except KeyboardInterrupt:
		quitclient_address