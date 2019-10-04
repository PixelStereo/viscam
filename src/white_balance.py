#! /usr/bin/python
# -*- coding: utf-8 -*-

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QGroupBox, QCheckBox, QGridLayout, QComboBox, \
                                 QSlider, QLabel, QPushButton

class WhiteBalance_UI(QGroupBox):
    """
    A QGroupbox widget with all properties of a ui camera
    """
    def __init__(self, ui, cam):
        super(WhiteBalance_UI, self).__init__()
        self.cam = cam
        self.ui = ui
        self.setTitle('White Balance')
        WB_layout = QGridLayout()
        ui.WB = QComboBox()
        ui.WB.addItems(['auto', 'indoor', 'outdoor', 'trigger', 'manual'])
        ui.WB.currentTextChanged.connect(self.on_WB_currentTextChanged)
        WB_layout.addWidget(ui.WB, 1, 1, 1, 3)
        ui.WB_trigger_label = QLabel()
        ui.WB_trigger_label.setText('WB trigger')
        ui.WB_trigger = QPushButton()
        ui.WB_trigger.setText('WB trigger')
        ui.WB_trigger.clicked.connect(self.on_WB_trigger_clicked)
        WB_layout.addWidget(ui.WB_trigger, 1, 4, 1, 1)
        ui.RGain_label = QLabel()
        ui.RGain_label.setText('Red Gain')
        WB_layout.addWidget(ui.RGain_label, 2, 1, 1, 1)
        ui.BGain_label = QLabel()
        ui.BGain_label.setText('Blue Gain')
        WB_layout.addWidget(ui.BGain_label, 3, 1, 1, 1)
        ui.RGain = QSlider()
        ui.RGain.setOrientation(Qt.Horizontal)
        ui.RGain.setMaximum(255)
        ui.RGain.valueChanged.connect(self.on_RGain_valueChanged)
        WB_layout.addWidget(ui.RGain, 2, 2, 1, 3)
        ui.BGain = QSlider()
        ui.BGain.setOrientation(Qt.Horizontal)
        ui.BGain.setMaximum(255)
        ui.BGain.valueChanged.connect(self.on_BGain_valueChanged)
        WB_layout.addWidget(ui.BGain, 3, 2, 1, 3)
        self.setLayout(WB_layout)

    def on_WB_currentTextChanged(self, text):
        if type(text) == unicode:
            text = text.encode('utf-8')
            self.cam.WB = text
            if text == 'manual':
                self.ui.WB_trigger.setEnabled(False)
                self.ui.WB_trigger_label.setEnabled(False)
                self.ui.RGain.setEnabled(True)
                self.ui.BGain.setEnabled(True)
                self.ui.RGain_label.setEnabled(True)
                self.ui.BGain_label.setEnabled(True)
            elif text == 'trigger':
                self.ui.WB_trigger.setEnabled(True)
                self.ui.WB_trigger_label.setEnabled(True)
                self.ui.RGain.setEnabled(False)
                self.ui.BGain.setEnabled(False)
                self.ui.RGain_label.setEnabled(False)
                self.ui.BGain_label.setEnabled(False)
            else:
                self.ui.WB_trigger.setEnabled(False)
                self.ui.WB_trigger_label.setEnabled(False)
                self.ui.RGain.setEnabled(False)
                self.ui.BGain.setEnabled(False)
                self.ui.RGain_label.setEnabled(False)
                self.ui.BGain_label.setEnabled(False)

    def on_WB_trigger_clicked(self):
        self.cam.WB_trigger()

    def on_RGain_valueChanged(self, value):
        self.cam.RGain = value

    def on_BGain_valueChanged(self, value):
        self.cam.BGain = value
