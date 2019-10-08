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


from properties import Properties_UI
from focus import Focus_UI
from zoom import Zoom_UI
from pan_tilt import Pan_Tilt_UI
from exposure import Exposure_UI
from white_balance import WhiteBalance_UI

class Visca_UI(QGroupBox):
    """
    A Visca Camera Control Panel
    """
    def __init__(self, cam):
        super(Visca_UI, self).__init__()
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
        self.cam = cam
        self.initialise_values()
        self.move(40, 40)
        self.refresh()

    def initialise_values(self):
        # -------------------------------------
        # TODO
        # these params needs to have UI 
        # -------------------------------------
        IR_auto = self.cam._query('IR_auto')
        self.cam.video = [1080, 25]
        VIDEO = self.cam._query('video')
        # Turn off digital zoom aka zoom_digital
        self.cam.zoom_digital = False
        # Turn off datascreen display
        self.cam.menu_off()
        self.cam.info_display = False

    def refresh(self):
        """
        ask the camera the actual values and refresh UI
        """
        # PROPERTIES
        power = self.cam._query('power') 
        self.power.setChecked(power)
        IR = self.cam._query('IR') 
        self.IR.setChecked(IR)
        FX = self.cam._query('FX')
        self.FX.setCurrentIndex(self.FX.findText(FX))
        # WHITE BALANCE
        WB = self.cam._query('WB')
        self.WB.setCurrentIndex(self.WB.findText(WB))
        RGain = self.cam._query('RGain')
        self.RGain.setValue(RGain)
        BGain = self.cam._query('BGain')
        self.BGain.setValue(BGain)
        # ZOOM
        self.zoom_wide_speed.setValue(3)
        self.zoom_tele_speed.setValue(3)
        zoom = self.cam._query('zoom')
        self.zoom_direct_value.setValue(zoom)
        # EXPOSURE
        slowshutter = self.cam._query('slowshutter') 
        self.slowshutter.setChecked(slowshutter)
        # PAN TILT
        self.pan_speed.setValue(3)
        self.tilt_speed.setValue(3)
        pan,tilt = self.cam._query('pan_tilt')
        self.tilt.setValue(tilt)
        self.pan.setValue(pan)
        # FOCUS
        self.focus_far_speed.setValue(3)
        self.focus_near_speed.setValue(3)
        focus = self.cam._query('focus')
        self.focus_direct_value.setValue(focus)
        nearlimit = self.cam._query('focus_nearlimit')
        self.focus_nearlimit_value.setValue(nearlimit)
