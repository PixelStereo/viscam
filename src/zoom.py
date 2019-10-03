#! /usr/bin/python
# -*- coding: utf-8 -*-


from PySide2.QtWidgets import QGroupBox, QCheckBox, QGridLayout, QPushButton, QSpinBox, \
                                QLabel, QSlider
from PySide2.QtCore import Qt


class Zoom_UI(QGroupBox):
    """
    A QGroupbox widget with all properties of a Visca camera
    """
    def __init__(self, visca, v):
        super(Zoom_UI, self).__init__()
        self.setTitle('Zoom')
        self.v = v
        self.visca = visca
        zoom_layout = QGridLayout()
        visca.zoom_stop = QPushButton()
        visca.zoom_stop.setText('Stop')
        visca.zoom_stop.clicked.connect(self.on_zoom_stop_pressed)
        visca.zoom_wide = QPushButton()
        visca.zoom_wide.setText('Wide')
        visca.zoom_wide.clicked.connect(self.on_zoom_wide_pressed)
        visca.zoom_tele = QPushButton()
        visca.zoom_tele.setText('Tele')
        visca.zoom_tele.clicked.connect(self.on_zoom_tele_pressed)
        visca.zoom_tele_speed = QSpinBox()
        visca.zoom_tele_speed.valueChanged.connect(self.on_zoom_tele_speed_valueChanged)
        visca.zoom_tele_speed_label = QLabel()
        visca.zoom_tele_speed_label.setText('Tele Speed')
        visca.zoom_wide_speed = QSpinBox()
        visca.zoom_wide_speed.valueChanged.connect(self.on_zoom_wide_speed_valueChanged)
        visca.zoom_wide_speed_label = QLabel()
        visca.zoom_wide_speed_label.setText('Wide Speed')
        visca.zoom = QSlider()
        visca.zoom.setOrientation(Qt.Horizontal)
        visca.zoom.setMinimum(0)
        visca.zoom.setMaximum(16384)
        visca.zoom_direct_value = QSpinBox()
        visca.zoom_direct_value.setKeyboardTracking(0)
        visca.zoom_label = QLabel()
        visca.zoom_label.setText('Zooom Value')
        visca.zoom.valueChanged.connect(visca.zoom_direct_value.setValue)
        visca.zoom_direct_value.setMinimum(0)
        visca.zoom_direct_value.setMaximum(65536)

        visca.zoom_direct_value.valueChanged.connect(self.on_zoom_direct_valueChanged)
        
        zoom_layout.addWidget(visca.zoom_wide_speed, 2, 1, 1, 1)
        zoom_layout.addWidget(visca.zoom_tele_speed, 2, 3, 1, 1)
        zoom_layout.addWidget(visca.zoom_label, 2, 4, 1, 1)
        zoom_layout.addWidget(visca.zoom_wide_speed_label, 1, 1, 1, 1)
        zoom_layout.addWidget(visca.zoom_tele_speed_label, 1, 3, 1, 1)
        #zoom_layout.addWidget(self.zoom, 4, 2, 3, 1)
        zoom_layout.addWidget(visca.zoom_wide, 3, 1, 1, 1)
        zoom_layout.addWidget(visca.zoom_stop, 3, 2, 1, 1)
        zoom_layout.addWidget(visca.zoom_tele, 3, 3, 1, 1)
        zoom_layout.addWidget(visca.zoom_direct_value, 3, 4, 1, 1)
        self.setLayout(zoom_layout)
        visca.zoom_tele_speed = 3
        visca.zoom_wide_speed = 3

    def on_zoom_direct_valueChanged(self, zoom):
        self.v.zoom = zoom
        self.visca.zoom = zoom
    
    def on_zoom_tele_pressed(self):
        self.v.zoom_tele(self.visca.zoom_tele_speed)

    def on_zoom_wide_pressed(self):
        self.v.zoom_wide(self.visca.zoom_wide_speed)

    def zoom_refresh(self):
        zoom = self.v._query('zoom')
        self.visca.zoom_direct_value.setValue(zoom)

    def on_zoom_stop_pressed(self):
        self.v.zoom_stop()
        self.zoom_refresh()

    def on_zoom_tele_speed_valueChanged(self, speed):
        self.visca.zoom_tele_speed = speed

    def on_zoom_wide_speed_valueChanged(self, speed):
        self.visca.zoom_wide_speed = speed
