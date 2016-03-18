#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
from time import sleep

# for development of viscam, use git version
_path = os.path.abspath('./../libs')
sys.path.append(_path)

#from pydevicemanager.devicemanager import OSCServer
from pyvisca.PyVisca import Viscam

debug = True


if __name__ == '__main__':
	cams = Viscam()
	print('available ports :', cams.serial.listports())
	# open a connection on the serial object
	cams.reset('/dev/tty.usbserial-FTFNNBFM')
	# create OSC server for binding to v (instance of VISCA)
	v = cams.get_instances()[0]
	print v
	#osc = OSCServer(v, 22222, name='span')
	########################### main loop ##################################
	v.zoom_direct = 0
	sleep(2)
	v.zoom_tele(4)
	sleep(3)
	v.zoom_stop()