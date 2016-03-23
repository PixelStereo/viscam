#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
# for development of pyCamera, use git version
libs_path = os.path.abspath('./../3rdparty/pyvisca')
sys.path.append(libs_path)

from pyvisca.PyVisca import Viscam

# a camera is created in visca_app
# create a visca bus object
cams = Viscam()

# get a list of serial ports available and select the last one
ports = cams.serial.listports()

port = None
for item in ports:
    if 'usbserial' in item:
        port = item
if not port:
    port = ports[0]
print('serial port opening : ' + port)

# open a connection on the serial object
cams.reset(port)
cams = cams.get_instances()
v = cams[0]

# create OSC server for binding to v (instance of VISCA)
libs_path = os.path.abspath('./../3rdparty')
sys.path.append(libs_path)
from pydevicemanager.devicemanager import OSCServer
osc = OSCServer(v, 22222, name='span')
