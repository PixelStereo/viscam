#! /usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep
import threading

import os, sys
# for development of pyCamera, use git version
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
if debug : print '-----pyvisca module initialisation-----'
cams = _cmd_adress_set(serial)
if debug : print 'is there a camera somewhere? aka address_set :',cams
clear = _if_clear(serial)
if debug : print 'clear all the camera buffers aka _if_clear :',clear
if debug : print 'Turn off digital zoom aka zoom_digital(False)'
if debug : print v.zoom_digital(False).encode('hex')
if debug : print 'trig from APP :','datascreen off'
if debug : print v.noOSD().encode('hex')

# create OSC server
osc = OSCServer(22222,name='span')
osc = osc.serverThread.oscServer
# it will be nice to do next lines in devicemanager
# create multi-thread server
#st = threading.Thread(target=osc.serve_forever)
#st.daemon = True
#st.start()
#if debug :print  "Server loop running in thread:", st.name
if debug :print  '----------- VISCA APP LOADED AND RUNNING----------------'

print '---------registering osc callback-----------------'
parameters =  dir(Visca)
for parameter in parameters:
	if not parameter.startswith('_'):
		old = parameter.split('_')
		new = ''
		for item in old:
			new = new+'/'+item
			handler = parameter+'_handler'
		# some commands doesn't need arguments, but it's more simple to send all and ignore these after
		function = 'def '+handler+'(addr, tags, args, source):v.'+parameter+'(args)'
		exec(function)
		osc.addMsgHandler(parameter,eval(handler))
		print new , '->' , parameter
print '---------end of registering osc callback----------'

#sleep(30)