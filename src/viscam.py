#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
from time import sleep
from PySide2.QtGui import  QStandardItemModel, QStandardItem
from PySide2.QtCore import Slot, QDir, QAbstractListModel, Qt, QFile
from PySide2.QtWidgets import QWidget, QApplication, QHBoxLayout, QDialog, QListView, QListWidget, QPushButton, \
                            QTableWidget, QTableView, QFileDialog, QTableWidgetItem, QWidget, QTreeView, QMainWindow, \
                            QSpinBox, QGroupBox, QGridLayout, QCheckBox, QSlider, QLabel

# Create the visca application
import visca_app

cam = visca_app.v
debug = True
update_run = False


from properties import Properties_UI
from focus import Focus_UI
from zoom import Zoom_UI
from pan_tilt import Pan_Tilt_UI
from exposure import Exposure_UI
from white_balance import WhiteBalance_UI

class Viscam(QGroupBox):
    """
    A Visca Camera Control Panel
    """
    def __init__(self):
        super(Viscam, self).__init__()
        properties_UI = Properties_UI(self, cam)
        whiteBalance_UI = WhiteBalance_UI(self, cam)
        focus_UI = Focus_UI(self, cam)
        zoom_UI = Zoom_UI(self, cam)
        pan_tilt_UI = Pan_Tilt_UI(self, cam)
        exposure_UI = Exposure_UI(self, cam)
        mainLayout = QGridLayout()
        mainLayout.addWidget(properties_UI, 1, 1, 1, 1)
        mainLayout.addWidget(whiteBalance_UI, 1, 2, 1, 1)
        mainLayout.addWidget(zoom_UI, 2, 1, 1, 1)
        mainLayout.addWidget(focus_UI, 3, 2, 1, 1)
        mainLayout.addWidget(pan_tilt_UI, 3, 1, 1, 1)
        mainLayout.addWidget(exposure_UI, 2, 2, 1, 1)
        self.setTitle('VISCA')
        self.setLayout(mainLayout)
        self.initialise_values()
        self.move(40, 40)

    def initialise_values(self):
        # query about params
        power = cam._query('power') 
        self.power.setChecked(power)
        IR = cam._query('IR') 
        self.IR.setChecked(IR)
        slowshutter = cam._query('slowshutter') 
        self.slowshutter.setChecked(slowshutter)
        FX = cam._query('FX')
        self.FX.setCurrentIndex(self.FX.findText(FX))
        WB = cam._query('WB')
        self.WB.setCurrentIndex(self.WB.findText(WB))
        self.focus_far_speed = 3
        self.focus_near_speed = 3
        focus = cam._query('focus')
        self.focus_direct_value.setValue(focus)
        nearlimit = cam._query('focus_nearlimit')
        self.focus_nearlimit_value.setValue(nearlimit)
        pan,tilt = cam._query('pan_tilt')
        self.tilt.setValue(tilt)
        self.pan.setValue(pan)
        self.zoom_wide_speed = 3
        self.zoom_tele_speed = 3
        zoom = cam._query('zoom')
        self.zoom_direct_value.setValue(zoom)
        # -------------------------------------
        # TODO
        # these params needs to have UI 
        # -------------------------------------
        IR_auto = cam._query('IR_auto')
        cam.video = [1080, 25]
        VIDEO = cam._query('video')
        # Turn off digital zoom aka zoom_digital
        cam.zoom_digital = False
        # Turn off datascreen display
        cam.menu_off()
        cam.info_display = False
