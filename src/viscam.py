#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
from time import sleep
from PySide2.QtUiTools import QUiLoader
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
        mainLayout = QGridLayout()
        mainLayout.addWidget(properties_UI, 1, 1, 1, 1)
        mainLayout.addWidget(focus_UI, 2, 1, 1, 1)
        mainLayout.addWidget(zoom_UI, 3, 1, 1, 1)
        mainLayout.addWidget(pan_tilt_UI, 4, 1, 1, 1)
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
        v.video = (720, 50)
        VIDEO = v._query('video')


"""


        AE = v._query('AE')
        self.AE.setCurrentText(AE)
        if AE != 'auto':
            # if expo is manual, refresh values
            self.expo_refresh()
        if self.AE.currentText() == 'auto':
            self.AE_manual.setVisible(False)
    
    def expo_refresh(self):
        aperture = v._query('aperture')
        if aperture:
            self.aperture.setCurrentText(str(aperture))
        iris = v._query('iris')
        if iris:
            self.iris.setCurrentText(str(iris))
        shutter = v._query('shutter')
        if shutter:
            self.shutter.setCurrentText(str(shutter))
        gain = v._query('gain')
        if gain:
            self.gain.setCurrentText(str(gain))

    def on_AE_currentIndexChanged(self, mode):
        print(mode)
        if type(mode) == unicode:
            mode = mode.encode('utf-8')
            v.AE = mode
            if mode == 'auto':
                self.AE_manual.setVisible(False)
            if mode == 'manual':
                self.AE_manual.setVisible(True)
                self.shutter.setVisible(True)
                self.shutter_label.setVisible(True)
                self.iris.setVisible(True)
                self.iris_label.setVisible(True)
                self.gain.setVisible(True)
                self.gain_label.setVisible(True)
                self.expo_refresh()
            if mode == 'shutter':
                self.AE_manual.setVisible(True)
                self.shutter.setVisible(True)
                self.shutter_label.setVisible(True)
                self.iris.setVisible(False)
                self.iris_label.setVisible(False)
                self.gain.setVisible(False)
                self.gain_label.setVisible(False)
                self.expo_refresh()
            if mode == 'iris':
                self.AE_manual.setVisible(True)
                self.iris.setVisible(True)
                self.iris_label.setVisible(True)
                self.shutter.setVisible(False)
                self.shutter_label.setVisible(False)
                self.gain.setVisible(False)
                self.gain_label.setVisible(False)
                self.expo_refresh()

    def on_shutter_currentIndexChanged(self, index):
        if type(index) == unicode:
            print('shutter', index)
        else:
            v.shutter = index

    def on_iris_currentIndexChanged(self, index):
        if type(index) == unicode:
            print('iris', index)
        else:
            v.iris = index

    def on_gain_currentIndexChanged(self, index):
        if type(index) == unicode:
            print('gain', index)
        else:
            v.gain = index

    def on_aperture_currentIndexChanged(self, index):
        if type(index) == unicode:
            print('aperture', index)
        else:
            v.aperture = index




    def on_gamma_valueChanged(self, value):
        v.gamma = int(value)
        v._query('gamma')






    def on_mem_recall_1_toggled(self,state):
        if state:
            v.memory_recall(0)

    def on_mem_recall_2_toggled(self,state):
        if state:
            v.memory_recall(1)
    def on_mem_recall_3_toggled(self,state):
        if state:
            v.memory_recall(2)
    def on_mem_recall_4_toggled(self,state):
        if state:
            v.memory_recall(3)

    def on_mem_recall_5_toggled(self,state):
        if state:
            v.memory_recall(4)

    def on_mem_set_1_toggled(self,state):
        if state:
            v.memory_set(0)
    def on_mem_set_2_toggled(self,state):
        if state:
            v.memory_set(1)

    def on_mem_set_3_toggled(self,state):
        if state:
            v.memory_set(2)

    def on_mem_set_4_toggled(self, state):
        if state:
            v.memory_set(3)
    def on_mem_set_5_toggled(self, state):
        if state:
            v.memory_set(4)


"""