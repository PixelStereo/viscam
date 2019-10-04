#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
main script
"""

import os, sys

from pyviscam.broadcast import v_cams
from pydevicemanager.osc import OSCServer

from viscam import Viscam

from PySide2.QtCore import QFileInfo
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QApplication


try:
    # stylesheet
    import qdarkstyle
except Exception as error:
    print('failed ' + str(error))


# a camera is created in visca_app
# create a visca bus object
cams = v_cams()
# get a list of serial ports available and select the last one
ports = cams.serial.listports()
# open a connection on the serial object
cams.reset(ports[0])
cams = cams.get_instances()
v = cams[0]
# create OSC server for binding to v (instance of VISCA)
#osc = OSCServer(v, 22222, name='viscam')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    root = QFileInfo(__file__).absolutePath()
    path = root+'/icon/icon.png'
    app.setWindowIcon(QIcon(path))
    mainWin = Viscam()
    mainWin.show()
    sys.exit(app.exec_())



"""
if __name__ == "__main__" :
    # loop and dispatch messages every 100ms
    try:
        while 1:
            osc.server.recv(10)
    except KeyboardInterrupt:
        quit()
"""