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

v = visca_app.v

try:
    # stylesheet
    import qdarkstyle
except:
    pass

debug = True
update_run = False


from properties import Properties_UI
from focus import Focus_UI
from zoom import Zoom_UI
from pan_tilt import Pan_Tilt_UI
from memory import Memory_UI
from exposure import Exposure_UI

class Viscam(QGroupBox):
    """
    A Visca Camera Control Panel
    """
    def __init__(self):
        super(Viscam, self).__init__()
        properties_UI = Properties_UI(self, v)
        focus_UI = Focus_UI(self, v)
        zoom_UI = Zoom_UI(self, v)
        pan_tilt_UI = Pan_Tilt_UI(self, v)
        memory_UI = Memory_UI(self, v)
        exposure_UI = Exposure_UI(self, v)
        mainLayout = QGridLayout()
        mainLayout.addWidget(properties_UI, 1, 1, 1, 1)
        mainLayout.addWidget(focus_UI, 2, 1, 1, 1)
        mainLayout.addWidget(zoom_UI, 3, 1, 1, 1)
        mainLayout.addWidget(pan_tilt_UI, 4, 1, 1, 1)
        mainLayout.addWidget(memory_UI, 5, 1, 1, 1)
        mainLayout.addWidget(exposure_UI, 6, 1, 1, 1)
        self.setTitle('VISCA')
        self.setLayout(mainLayout)
        self.initialise_values()

    def initialise_values(self):
        # query about params
        power = v._query('power') 
        self.power.setChecked(power)
        IR = v._query('IR') 
        self.IR.setChecked(IR)
        focus = v._query('focus')
        #self.focus_direct_value.setValue(focus)
        nearlimit = v._query('focus_nearlimit')
        #self.focus_nearlimit_value.setValue(nearlimit)
        pan,tilt = v._query('pan_tilt')
        self.tilt.setValue(tilt)
        self.pan.setValue(pan)
        v.IR_auto = False
        focus = v._query('focus')
        self.focus_far_speed = 3
        self.focus_near_speed = 3
        zoom = v._query('zoom')
        self.zoom_direct_value.setValue(zoom)
        self.focus_direct_value.setValue(focus)
        v.video = (1080, 25)
        VIDEO = v._query('video')
        v.chromasuppress = 0
