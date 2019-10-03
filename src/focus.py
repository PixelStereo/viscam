#! /usr/bin/python
# -*- coding: utf-8 -*-

from time import sleep
from PySide2.QtWidgets import QGroupBox, QCheckBox, QGridLayout, QPushButton, QSpinBox, \
                                QLabel, QSlider
from PySide2.QtCore import Qt


class Focus_UI(QGroupBox):
    """
    A QGroupbox widget with all properties of a Visca camera
    """
    def __init__(self, visca, v):
        super(Focus_UI, self).__init__()
        self.v = v
        self.visca = visca
        self.setTitle('Focus')
        focus_layout = QGridLayout()
        visca.focus_auto = QPushButton()
        visca.focus_auto.setCheckable(1)
        visca.focus_auto.setText('Auto')
        visca.focus_auto.toggled.connect(self.on_focus_auto_stateChanged)
        visca.focus_stop = QPushButton()
        visca.focus_stop.setText('Stop')
        visca.focus_stop.clicked.connect(self.on_focus_stop_pressed)
        visca.focus_near = QPushButton()
        visca.focus_near.setText('Near')
        visca.focus_near.clicked.connect(self.on_focus_near_pressed)
        visca.focus_far = QPushButton()
        visca.focus_far.setText('Far')
        visca.focus_far.clicked.connect(self.on_focus_far_pressed)
        visca.focus_far_speed = QSpinBox()
        visca.focus_far_speed.valueChanged.connect(self.on_focus_far_speed_valueChanged)
        visca.focus_far_speed_label = QLabel()
        visca.focus_far_speed_label.setText('Far Speed')
        visca.focus_near_speed = QSpinBox()
        visca.focus_near_speed.valueChanged.connect(self.on_focus_near_speed_valueChanged)
        visca.focus_near_speed_label = QLabel()
        visca.focus_near_speed_label.setText('Near Speed')
        visca.focus = QSlider()
        visca.focus.setOrientation(Qt.Horizontal)
        visca.focus.setMinimum(0)
        visca.focus.setMaximum(16384)
        visca.focus_direct_value = QSpinBox()
        visca.focus_direct_value.setKeyboardTracking(0)
        visca.focus_label = QLabel()
        visca.focus_label.setText('Focus Value')
        visca.focus.valueChanged.connect(visca.focus_direct_value.setValue)
        visca.focus_direct_value.setMinimum(0)
        visca.focus_direct_value.setMaximum(65536)
        visca.focus_direct_value.valueChanged.connect(self.on_focus_direct_valueChanged)
        visca.focus_nearlimit_label = QLabel()
        visca.focus_nearlimit_label.setText('Focus nearlimit')
        visca.focus_nearlimit_value = QSpinBox()
        visca.focus_nearlimit_value.setKeyboardTracking(0)
        visca.focus_nearlimit_value.setMinimum(0)
        visca.focus_nearlimit_value.setMaximum(65536)
        visca.focus_nearlimit_value.valueChanged.connect(self.on_focus_nearlimit_valueChanged)
        # create a groupbox for all manual settings
        self.focus_manual = QGridLayout()
        self.focus_manual.addWidget(visca.focus_near_speed, 2, 1, 1, 1)
        self.focus_manual.addWidget(visca.focus_far_speed, 2, 3, 1, 1)
        self.focus_manual.addWidget(visca.focus_label, 2, 4, 1, 1)
        self.focus_manual.addWidget(visca.focus_near_speed_label, 1, 1, 1, 1)
        self.focus_manual.addWidget(visca.focus_far_speed_label, 1, 3, 1, 1)
        #self.focus_manual.addWidget(self.focus, 4, 2, 3, 1)
        self.focus_manual.addWidget(visca.focus_near, 3, 1, 1, 1)
        self.focus_manual.addWidget(visca.focus_stop, 3, 2, 1, 1)
        self.focus_manual.addWidget(visca.focus_far, 3, 3, 1, 1)
        self.focus_manual.addWidget(visca.focus_direct_value, 3, 4, 1, 1)
        self.focus_manual.addWidget(visca.focus_nearlimit_label, 4, 1, 1, 1)
        self.focus_manual.addWidget(visca.focus_nearlimit_value, 4, 2, 1, 1)
        self.focus_manual_box = QGroupBox()
        self.focus_manual_box.setLayout(self.focus_manual)
        focus_layout.addWidget(visca.focus_auto, 1, 1, 1, 1)
        focus_layout.addWidget(self.focus_manual_box, 2, 1, 1, 1)
        self.setLayout(focus_layout)


    def on_focus_auto_stateChanged(self, state):
        if state:
            self.v.focus_auto = 1
            self.focus_manual_box.setEnabled(0)
        else:
            self.v.focus_auto = 0
            self.focus_manual_box.setEnabled(1)
        sleep(0.1)
        focus = self.v._query('focus')
        focus_auto___ = self.v._query('focus_auto')
        print('------autofocus is :', focus_auto___)
        self.visca.focus_direct_value.setValue(focus)
        sleep(0.1)
        nearlimit = self.v._query('focus_nearlimit')
        self.visca.focus_nearlimit_value.setValue(nearlimit)

    def on_focus_near_pressed(self):
        self.v.focus_near()

    def on_focus_far_pressed(self):
        self.v.focus_far()

    def focus_refresh(self):
        focus = self.v._query('focus')
        self.visca.focus_direct_value.setValue(focus)

    def on_focus_stop_pressed(self):
        self.v.focus_stop()
        self.focus_refresh()

    def on_focus_near_speed_valueChanged(self, speed):
        self.visca.focus_near_speed = speed

    def on_focus_far_speed_valueChanged(self, speed):
        self.visca.focus_far_speed = speed
    
    def on_focus_direct_valueChanged(self, value):
        self.v.focus = value
    
    def on_focus_nearlimit_valueChanged(self, nearlimit):
        self.v.focus_nearlimit = nearlimit



