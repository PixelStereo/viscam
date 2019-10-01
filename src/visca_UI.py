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
                            QSpinBox, QGroupBox, QGridLayout, QCheckBox, QSlider

import sys
print(sys.version)


import sys
print(sys.version)

import visca_app
v = visca_app.v

try:
    # stylesheet
    import qdarkstyle
except:
    pass

debug = True
update_run = False


class ViscaUI(QMainWindow):
    """create span view and controller (MVC)"""
    def __init__(self):
        super(ViscaUI, self).__init__()

        mainLayout = QGridLayout()

        # query about params
        self.power = QCheckBox()
        self.power.setText('Power')
        self.power.clicked.connect(self.on_power_toggled)
        power = v._query('power') 
        self.power.setChecked(power)
        self.IR = QCheckBox()
        self.IR.setText('IR')
        self.IR.clicked.connect(self.on_IR_toggled)
        IR = v._query('IR') 
        self.IR.setChecked(IR)


        properties_groupbox = QGroupBox()
        properties_groupbox.setTitle('Properties')
        properties_layout = QGridLayout()
        properties_layout.addWidget(self.power, 1, 1, 1, 1)
        properties_layout.addWidget(self.IR, 1, 2, 1, 1)
        properties_groupbox.setLayout(properties_layout)





        pan_tilt_groupbox = QGroupBox()
        pan_tilt_groupbox.setTitle('Pan & Tilt')
        pan_tilt_layout = QGridLayout()
        self.pan = QSpinBox()
        self.pan.valueChanged.connect(self.on_pan_valueChanged)
        self.tilt = QSpinBox()
        self.tilt.valueChanged.connect(self.on_tilt_valueChanged)
        self.pan_speed = QSpinBox()
        self.pan_speed.valueChanged.connect(self.on_pan_speed_valueChanged)
        self.tilt_speed = QSpinBox()
        self.tilt_speed.valueChanged.connect(self.on_tilt_speed_valueChanged)
        self.home = QPushButton()
        self.home.setText('Home')
        self.home.clicked.connect(self.on_home_pressed)
        self.reset = QPushButton()
        self.reset.setText('reset')
        self.reset.clicked.connect(self.on_reset_pressed)
        self.upleft = QPushButton()
        self.upleft.setText('upleft')
        self.upleft.clicked.connect(self.on_upleft_pressed)
        self.upright = QPushButton()
        self.upright.setText('upright')
        self.upright.clicked.connect(self.on_upright_pressed)
        self.downleft = QPushButton()
        self.downleft.setText('downleft')
        self.downleft.clicked.connect(self.on_downleft_pressed)
        self.downright = QPushButton()
        self.downright.setText('downright')
        self.downright.clicked.connect(self.on_downright_pressed)
        self.left = QPushButton()
        self.left.setText('left')
        self.left.clicked.connect(self.on_left_pressed)
        self.right = QPushButton()
        self.right.setText('right')
        self.right.clicked.connect(self.on_right_pressed)
        self.up = QPushButton()
        self.up.setText('up')
        self.up.clicked.connect(self.on_up_pressed)
        self.down = QPushButton()
        self.down.setText('down')
        self.down.clicked.connect(self.on_down_pressed)
        self.stop = QPushButton()
        self.stop.setText('stop')
        self.stop.clicked.connect(self.on_stop_pressed)
        pan_tilt_layout.addWidget(self.tilt_speed, 1, 2, 1, 1)
        pan_tilt_layout.addWidget(self.home, 1, 5, 1, 1)
        pan_tilt_layout.addWidget(self.reset, 2, 5, 1, 1)
        pan_tilt_layout.addWidget(self.pan, 3, 5, 1, 1)
        pan_tilt_layout.addWidget(self.pan_speed, 1, 1, 1, 1)
        pan_tilt_layout.addWidget(self.tilt, 4, 5, 1, 1)
        pan_tilt_layout.addWidget(self.upleft, 2, 1, 1, 1)
        pan_tilt_layout.addWidget(self.up, 2, 2, 1, 1)
        pan_tilt_layout.addWidget(self.upright, 2, 3, 1, 1)
        pan_tilt_layout.addWidget(self.left, 3, 1, 1, 1)
        pan_tilt_layout.addWidget(self.stop, 3, 2, 1, 1)
        pan_tilt_layout.addWidget(self.right, 3, 3, 1, 1)
        pan_tilt_layout.addWidget(self.downleft, 4, 1, 1, 1)
        pan_tilt_layout.addWidget(self.down, 4, 2, 1, 1)
        pan_tilt_layout.addWidget(self.downright, 4, 3, 1, 1)
        pan_tilt_groupbox.setLayout(pan_tilt_layout)
        # initialize speeds
        #self.pan_speed = 5
        #self.tilt_speed = 5
        self.pan_speed.setValue(5)
        self.tilt_speed.setValue(5)
        

        focus_groupbox = QGroupBox()
        focus_groupbox.setTitle('Focus')
        focus_layout = QGridLayout()
        self.focus_near_speed = QSpinBox()
        self.focus_far_speed = QSpinBox()
        focus_layout.addWidget(self.focus_near_speed, 1, 1, 1, 1)
        focus_layout.addWidget(self.focus_far_speed, 1, 2, 1, 1)
        focus_groupbox.setLayout(focus_layout)
        self.focus_near_speed = 4
        self.focus_far_speed = 4


        zoom_groupbox = QGroupBox()
        zoom_groupbox.setTitle('Zoom')
        zoom_layout = QGridLayout()
        self.zoom_tele_speed = QSpinBox()
        self.zoom_wide_speed = QSpinBox()
        self.zoom = QSlider()
        self.zoom.setOrientation(Qt.Horizontal)
        self.zoom.setMinimum(0)
        self.zoom.setMaximum(16384)
        self.zoom_direct_value = QSpinBox()

        self.zoom.valueChanged.connect(self.zoom_direct_value.setValue)
        self.zoom_direct_value.setMinimum(0)
        self.zoom_direct_value.setMaximum(65536)
        zoom = v._query('zoom')
        self.zoom_direct_value.valueChanged.connect(self.on_zoom_direct_valueChanged)
        self.zoom_direct_value.setValue(zoom)


        zoom_layout.addWidget(self.zoom_tele_speed, 1, 1, 1, 1)
        zoom_layout.addWidget(self.zoom_wide_speed, 1, 2, 1, 1)
        #zoom_layout.addWidget(self.zoom, 1, 3, 3, 1, Qt.Alignment)
        zoom_layout.addWidget(self.zoom_direct_value, 1, 4, 1, 1)
        zoom_groupbox.setLayout(zoom_layout)
        self.zoom_tele_speed = 3
        self.zoom_wide_speed = 3

        

        mainLayout.addWidget(properties_groupbox, 1, 1, 1, 1)
        mainLayout.addWidget(focus_groupbox, 2, 1, 1, 1)
        mainLayout.addWidget(zoom_groupbox, 3, 1, 1, 1)
        mainLayout.addWidget(pan_tilt_groupbox, 4, 1, 1, 1)
        self.setLayout(mainLayout)
        visca_widget = QGroupBox()
        visca_widget.setTitle('VISCA')
        visca_widget.setLayout(mainLayout)
        self.setCentralWidget(visca_widget)
        self.setFixedSize(612, 512)



    def on_power_toggled(self, state):
        v.power = state
        print('POWER', state)
    
    def on_IR_toggled(self,state):
        v.IR = state

    def on_zoom_direct_valueChanged(self, zoom):
        v.zoom = zoom
        self.zoom = zoom

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


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    MainWindow = ViscaUI()
    MainWindow.show()
    sys.exit(app.exec_())
