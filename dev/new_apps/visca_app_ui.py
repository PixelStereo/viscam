#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
from time import sleep
from PyQt5.uic import loadUiType,loadUi
from PyQt5.QtGui import  QStandardItemModel , QStandardItem
from PyQt5.QtCore import pyqtSlot, QDir, QAbstractListModel, Qt
from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout, QDialog, QListView, QListWidget, \
                            QPushButton, QGridLayout, QCheckBox, QTableWidget, QTableView, QFileDialog, \
                            QTableWidgetItem, QWidget, QTreeView, QMainWindow, QGroupBox, QSlider, QLabel, QSpinBox

import visca_app

v = visca_app.v

debug = True

class ViscaUI(QMainWindow):
    """
    Create the UI
    """
    def __init__(self):
        super(ViscaUI, self).__init__()
        self.group = QGroupBox('Camera')
        self.grid = QGridLayout()
        self.group.setLayout(self.grid)
        self.setCentralWidget(self.group)
        # create and add power panel
        self.grid.addWidget(self.create_power())
        self.grid.addWidget(self.create_lens())

    def create_power(self):
        power_button = QCheckBox('Power')
        power_button.setTristate(False)
        power_button.setChecked = v._query('power')
        power_button.stateChanged.connect(self._power)
        return power_button

    def _power(self, state):
        v.power = state

    def create_lens(self):
        lens_group = QGroupBox('Lens Group')
        lens_layout = QGridLayout()
        lens_group.setLayout(lens_layout)

        # -----------------------------
        # ---------- ZOOM -------------
        # -----------------------------
        zoom_group = QGroupBox('Zoom Group')
        zoom_layout = QGridLayout()
        zoom_group.setLayout(zoom_layout)
        # zoom direct value
        zoom = QSlider()
        zoom.setOrientation(Qt.Horizontal)
        zoom_value = QSpinBox()
        zoom.valueChanged.connect(zoom_value.setValue)
        zoom.setRange(0,65535)
        zoom_value.setRange(0,65535)
        zoom_value.setMinimumWidth(80)
        zoom.setValue = v._query('zoom')
        zoom.sliderReleased.connect(self._zoom)
        self.zoom = zoom
        # Add Widgets to the Layout
        zoom_layout.addWidget(zoom, 0, 0)
        zoom_layout.addWidget(zoom_value, 0, 1)
        zoom_group.setMinimumHeight(200)
        # add zoom_group to lens_layout
        lens_layout.addWidget(zoom_group, 0, 0)

        # -----------------------------
        # ---------- FOCUS ------------
        # -----------------------------
        # for all manual focus parameters
        focus_manual_group = QGroupBox('Focus Manual Group')
        focus_manual_layout = QGridLayout()
        focus_manual_group.setLayout(focus_manual_layout)
        # Main Focus 
        focus_group = QGroupBox('Focus Auto')
        focus_group.setCheckable(True)
        # focus auto
        focus_group.toggled.connect(self._focus_auto)
        focus_group.toggled.connect(focus_manual_group.setVisible)
        focus_group.setChecked(v._query('focus_auto'))
        focus_layout = QGridLayout()
        focus_group.setLayout(focus_layout)
        focus_group.setFixedWidth(300)
        focus_group.setFixedHeight(300)

        # focus direct value
        focus = QSlider()
        focus.setOrientation(Qt.Horizontal)
        focus_value = QSpinBox()
        focus.valueChanged.connect(focus_value.setValue)
        focus.setRange(0,65535)
        focus_value.setRange(0,65535)
        focus_value.setMinimumWidth(80)
        focus.setValue = v._query('zoom')
        focus.sliderReleased.connect(self._focus)
        self.focus = focus
        focus_manual_layout.addWidget(focus, 1, 0)
        focus_manual_layout.addWidget(focus_value, 1, 1)
        
        # Add Widgets to the Layout
        focus_layout.addWidget(focus_manual_group, 0, 0)
        focus_group.setMinimumHeight(200)
        # add focus_group to lens_layout
        lens_layout.addWidget(focus_group, 0, 1)

        return lens_group

    def _zoom(self):
        v.zoom = self.zoom.value()

    def _focus_auto(self, state):
        v.focus_auto = state

    def _focus(self):
        v.focus = self.focus.value()

        """
        self.pan_value = 0
        self.tilt_value = 0
        self.tilt_speed = 17
        self.focus_near_speed = 4
        self.focus_near_speed = 4
        self.pan_speed = 18
        zoom = v._query('zoom')
        self.zoom_direct_value.setValue(zoom)
        self.zoom_tele_speed_label.setText(str(0))
        self.zoom_wide_speed_label.setText(str(0))
        focus = v._query('focus')
        self.focus_direct_value.setValue(focus)
        nearlimit = v._query('focus_nearlimit')
        self.focus_nearlimit_value.setValue(nearlimit)
        pan,tilt = v._query('pan_tilt')
        self.tilt.setValue(tilt)
        self.pan.setValue(pan)
        # exposition parameters
        IR = v._query('IR')
        self.IR.setChecked(IR)
        AE = v._query('AE')
        self.AE.setCurrentText(AE)
        v.video = (720, 50)
        VIDEO = v._query('video')
        if AE != 'auto':
            aperture = v._query('aperture')
            if aperture:
                self.aperture.setCurrentIndex(aperture)
            iris = v._query('iris')
            if iris:
                self.iris.setCurrentIndex(iris)
            shutter = v._query('shutter')
            if shutter:
                self.shutter.setCurrentIndex(shutter)
            gain = v._query('gain')
            if gain:
                self.gain.setCurrentIndex(gain)
        if self.AE.currentText() == 'auto':
            self.AE_manual.setVisible(False)"""

    
    def on_AE_currentIndexChanged(self,mode):
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
            if mode == 'shutter':
                self.AE_manual.setVisible(True)
                self.shutter.setVisible(True)
                self.shutter_label.setVisible(True)
                self.iris.setVisible(False)
                self.iris_label.setVisible(False)
                self.gain.setVisible(False)
                self.gain_label.setVisible(False)
            if mode == 'iris':
                self.AE_manual.setVisible(True)
                self.iris.setVisible(True)
                self.iris_label.setVisible(True)
                self.shutter.setVisible(False)
                self.shutter_label.setVisible(False)
                self.gain.setVisible(False)
                self.gain_label.setVisible(False)

    def on_shutter_currentIndexChanged(self, index):
        if type(index) == unicode:
            print 'shutter', index
        else:
            v.shutter = index

    def on_iris_currentIndexChanged(self, index):
        if type(index) == unicode:
            print 'iris', index
        else:
            v.iris = index

    def on_gain_currentIndexChanged(self, index):
        if type(index) == unicode:
            print 'gain', index
        else:
            v.gain = index

    def on_aperture_currentIndexChanged(self, index):
        if type(index) == unicode:
            print 'aperture', index
        else:
            v.aperture = index

    def on_slowshutter_currentIndexChanged(self,state):
        if type(state) == unicode:
            state = state.encode('utf-8')
        if state:
            v.slowshutter = 'auto'
        else:
            v.slowshutter = 'manual'
    
    def on_IR_toggled(self,state):
        v.IR = state

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

    def on_power_toggled(self, state):
        v.power = state
    
    def on_zoom_tele_pressed(self):
        v.zoom_tele()

    def on_zoom_wide_pressed(self):
        v.zoom_wide()

    def zoom_refresh(self):
        zoom = v._query('zoom')
        self.zoom_direct_value.setValue(zoom)

    def on_zoom_stop_pressed(self):
        v.zoom_stop()
        self.zoom_refresh()

    def on_zoom_tele_speed_valueChanged(self, speed):
        v.zoom_tele_speed(speed)

    def on_zoom_wide_speed_valueChanged(self, speed):
        v.zoom_wide_speed(speed)
    
    def on_zoom_direct_valueChanged(self, zoom):
        v.zoom = zoom

    def on_focus_mode_currentIndexChanged(self, mode):
        if type(mode) == unicode:
            mode = mode.encode('utf-8')
        v.focus_auto = mode
        sleep(0.1)
        focus = v._query('focus')
        focus_auto___ = v._query('focus_auto')
        print '------focus_mode-------', focus_auto___
        self.focus_direct_value.setValue(focus)
        sleep(0.1)
        nearlimit = v._query('focus_nearlimit')
        self.focus_nearlimit_value.setValue(nearlimit)

    def on_focus_near_pressed(self):
        v.focus_near()

    def on_focus_far_pressed(self):
        v.focus_far()

    def focus_refresh(self):
        focus = v._query('focus')
        self.focus_direct_value.setValue(focus)

    def on_focus_stop_pressed(self):
        v.focus_stop()
        self.focus_refresh()

    def on_focus_near_speed_valueChanged(self, speed):
        self.focus_near_speed = speed

    def on_focus_far_speed_valueChanged(self, speed):
        self.focus_far_speed = speed
    
    def on_focus_direct_valueChanged(self, value):
        v.focus = value
    
    def on_focus_nearlimit_valueChanged(self, nearlimit):
        v.focus_nearlimit = nearlimit

    def on_pan_speed_valueChanged(self,value):
        v.pan_speed = value

    def on_tilt_speed_valueChanged(self,value):
        v.tilt_speed = value

    def on_pan_valueChanged(self, value):
        value = int(value)
        v.pan = value

    def on_tilt_valueChanged(self, value):
        value = int(value)
        v.tilt = value

    def on_up_pressed(self):
        v.up()

    def on_left_pressed(self):
        v.left()

    def on_down_pressed(self):
        v.down()

    def on_right_pressed(self):
        v.right()

    def on_upleft_pressed(self):
        v.upleft()

    def on_downleft_pressed(self):
        v.downleft()

    def on_downright_pressed(self):
        v.downright()

    def on_upright_pressed(self):
        v.upright()
        
    def on_home_pressed(self):
        v.home()
        self.pan_tilt_refresh()
        
    def on_reset_pressed(self):
        v.reset()
        self.pan_tilt_refresh()

    def on_stop_pressed(self):
        v.stop()
        self.pan_tilt_refresh()

    def pan_tilt_refresh(self):
        pan, tilt = v._query('pan_tilt')
        self.tilt.setValue(tilt)
        self.pan.setValue(pan)

    def on_WB_currentTextChanged(self, text):
        if type(text) == unicode:
            text = text.encode('utf-8')
            v.WB = text
    def on_FX_currentTextChanged(self, text):
        if type(text) == unicode:
            text = text.encode('utf-8')
            v.FX = text


if __name__ == "__main__":
    app = QApplication(sys.argv)
    appWindow = ViscaUI()
    appWindow.move(5,12)
    appWindow.show()
    sys.exit(app.exec_())
    sdRef.close()