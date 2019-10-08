#! /usr/bin/python
# -*- coding: utf-8 -*-


from PySide2.QtWidgets import QGroupBox, QCheckBox, QGridLayout, QPushButton, QSpinBox, \
                                QLabel, QSlider
from PySide2.QtCore import Qt


class Pan_Tilt_UI(QGroupBox):
    """
    A QGroupbox widget with all properties of a Visca camera
    """
    def __init__(self, visca, v):
        super(Pan_Tilt_UI, self).__init__()
        self.v = v
        self.visca = visca
        self.setTitle('Pan & Tilt')
        pan_tilt_layout = QGridLayout()
        visca.pan_speed_label = QLabel()
        visca.pan_speed_label.setText('Pan Speed')
        visca.tilt_speed_label = QLabel()
        visca.tilt_speed_label.setText('Tilt Speed')
        visca.pan_label = QLabel()
        visca.pan_label.setText('Pan')
        visca.tilt_label = QLabel()
        visca.tilt_label.setText('Tilt')
        visca.pan = QSpinBox()
        visca.pan.valueChanged.connect(self.on_pan_valueChanged)
        visca.tilt = QSpinBox()
        visca.tilt.valueChanged.connect(self.on_tilt_valueChanged)
        visca.pan_speed = QSpinBox()
        visca.pan_speed.valueChanged.connect(self.on_pan_speed_valueChanged)
        visca.tilt_speed = QSpinBox()
        visca.tilt_speed.valueChanged.connect(self.on_tilt_speed_valueChanged)
        visca.home = QPushButton()
        visca.home.setText('Home')
        visca.home.clicked.connect(self.on_home_pressed)
        visca.reset = QPushButton()
        visca.reset.setText('reset')
        visca.reset.clicked.connect(self.on_reset_pressed)
        visca.upleft = QPushButton()
        visca.upleft.setText('upleft')
        visca.upleft.clicked.connect(self.on_upleft_pressed)
        visca.upright = QPushButton()
        visca.upright.setText('upright')
        visca.upright.clicked.connect(self.on_upright_pressed)
        visca.downleft = QPushButton()
        visca.downleft.setText('downleft')
        visca.downleft.clicked.connect(self.on_downleft_pressed)
        visca.downright = QPushButton()
        visca.downright.setText('downright')
        visca.downright.clicked.connect(self.on_downright_pressed)
        visca.left = QPushButton()
        visca.left.setText('left')
        visca.left.clicked.connect(self.on_left_pressed)
        visca.right = QPushButton()
        visca.right.setText('right')
        visca.right.clicked.connect(self.on_right_pressed)
        visca.up = QPushButton()
        visca.up.setText('up')
        visca.up.clicked.connect(self.on_up_pressed)
        visca.down = QPushButton()
        visca.down.setText('down')
        visca.down.clicked.connect(self.on_down_pressed)
        visca.stop = QPushButton()
        visca.stop.setText('stop')
        visca.stop.clicked.connect(self.on_stop_pressed)
        pan_tilt_layout.addWidget(visca.pan_speed_label, 1, 1, 1, 1)
        pan_tilt_layout.addWidget(visca.tilt_speed_label, 1, 3, 1, 1)
        pan_tilt_layout.addWidget(visca.tilt_speed, 2, 3, 1, 1)
        pan_tilt_layout.addWidget(visca.home, 2, 2, 1, 1)
        pan_tilt_layout.addWidget(visca.reset, 1, 2, 1, 1)
        pan_tilt_layout.addWidget(visca.pan, 2, 4, 1, 1)
        pan_tilt_layout.addWidget(visca.pan_label, 1, 4, 1, 1)
        pan_tilt_layout.addWidget(visca.pan_speed, 2, 1, 1, 1)
        pan_tilt_layout.addWidget(visca.tilt, 5, 4, 1, 1)
        pan_tilt_layout.addWidget(visca.tilt_label, 4, 4, 1, 1)
        pan_tilt_layout.addWidget(visca.upleft, 3, 1, 1, 1)
        pan_tilt_layout.addWidget(visca.up, 3, 2, 1, 1)
        pan_tilt_layout.addWidget(visca.upright, 3, 3, 1, 1)
        pan_tilt_layout.addWidget(visca.left, 4, 1, 1, 1)
        pan_tilt_layout.addWidget(visca.stop, 4, 2, 1, 1)
        pan_tilt_layout.addWidget(visca.right, 4, 3, 1, 1)
        pan_tilt_layout.addWidget(visca.downleft, 5, 1, 1, 1)
        pan_tilt_layout.addWidget(visca.down, 5, 2, 1, 1)
        pan_tilt_layout.addWidget(visca.downright, 5, 3, 1, 1)
        self.setLayout(pan_tilt_layout)

    def on_up_pressed(self):
        self.v.up()

    def on_left_pressed(self):
        self.v.left()

    def on_down_pressed(self):
        self.v.down()

    def on_right_pressed(self):
        self.v.right()

    def on_upleft_pressed(self):
        self.v.upleft()

    def on_downleft_pressed(self):
        self.v.downleft()

    def on_downright_pressed(self):
        self.v.downright()

    def on_upright_pressed(self):
        self.v.upright()
        
    def on_home_pressed(self):
        self.v.home()
        self.pan_tilt_refresh()
        
    def on_reset_pressed(self):
        self.v.reset()
        self.pan_tilt_refresh()

    def on_stop_pressed(self):
        self.v.stop()
        self.pan_tilt_refresh()

    def pan_tilt_refresh(self):
        pan, tilt = self.v._query('pan_tilt')
        self.visca.tilt.setValue(tilt)
        self.visca.pan.setValue(pan)

    def on_pan_speed_valueChanged(self, value):
        self.v.pan_speed = value

    def on_tilt_speed_valueChanged(self, value):
        self.v.tilt_speed = value

    def on_pan_valueChanged(self, value):
        value = int(value)
        self.v.pan = value

    def on_tilt_valueChanged(self, value):
        value = int(value)
        self.v.tilt = value
