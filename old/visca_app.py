#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
# for development of viscam, use git version
_path = os.path.abspath('./../libs')
sys.path.append(_path)

from pydevicemanager.devicemanager import OSCServer
from pyvisca.PyVisca import Visca, _cmd_adress_set, _if_clear,Serial

debug = True

# create a serial object
serial = Serial()
# open a connection on the serial object
serial.open(portname='/dev/tty.usbserial-FTFNNBFM')
v = Visca(serial)

if debug:
	print '-----pyvisca module initialisation-----'
cams = _cmd_adress_set(serial)
if debug:
	print 'is there a camera somewhere? aka address_set :',cams
clear = _if_clear(serial)
if debug:
	print 'clear all the camera buffers aka _if_clear :',clear
if debug:
	print 'Turn off digital zoom aka zoom_digital(False)'
if debug:
	print v.zoom_digital(False).encode('hex')
if debug:
	print 'trig from APP :','datascreen off'
if debug:
	print v.noOSD().encode('hex')

# create OSC server for binding to v (instance of VISCA)
osc = OSCServer(v, 22222, name='span')


if debug:
	print('----------- VISCA APP LOADED AND RUNNING----------------')


if __name__ == '__main__':
	print qq.q
	while not qq.q.empty():
		print qq.q.get()