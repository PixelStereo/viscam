#! /usr/bin/python
# -*- coding: utf-8 -*-

from pyviscam.constants import answers
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QGroupBox, QCheckBox, QGridLayout, QComboBox, \
                                 QSlider, QLabel, QPushButton

class Properties_UI(QGroupBox):
    """
    A QGroupbox widget with all properties of a ui camera
    """
    def __init__(self, ui, cam):
        super(Properties_UI, self).__init__()
        self.cam = cam
        self.ui = ui
        self.setTitle('Properties')
        properties_layout = QGridLayout()
        ui.power = QCheckBox()
        ui.power.setText('Power')
        ui.power.clicked.connect(self.on_power_toggled)
        properties_layout.addWidget(ui.power, 1, 1, 1, 1)
        ui.video = QComboBox()
        ui.video.addItems([str(truc) for truc in answers['video'].values()])
        ui.video.currentTextChanged.connect(self.on_video_currentTextChanged)
        properties_layout.addWidget(ui.video, 1, 2, 1, 1)
        ui.IR = QCheckBox()
        ui.IR.setText('IR')
        ui.IR.clicked.connect(self.on_IR_toggled)
        properties_layout.addWidget(ui.IR, 1, 3, 1, 1)
        ui.FX = QComboBox()
        ui.FX.addItems(['Normal', 'NegArt', 'B&W'])
        ui.FX.currentTextChanged.connect(self.on_FX_currentTextChanged)
        properties_layout.addWidget(ui.FX, 1, 4, 1, 1)
        mem_set_label = QLabel()
        mem_set_label.setText('Make Memory')
        properties_layout.addWidget(mem_set_label, 2, 1, 1, 1)
        ui.memory_set = QComboBox()
        mem_list = [str(i) for i in range(49)]
        ui.memory_set.addItems(mem_list)
        ui.memory_set.currentTextChanged.connect(self.on_memory_set_currentTextChanged)
        properties_layout.addWidget(ui.memory_set, 3, 1, 1, 1)
        mem_recall_label = QLabel()
        mem_recall_label.setText('Recall Memory')
        properties_layout.addWidget(mem_recall_label, 2, 2, 1, 1)
        ui.memory_recall = QComboBox()
        ui.memory_recall.addItems(mem_list)
        ui.memory_recall.currentTextChanged.connect(self.on_memory_recall_currentTextChanged)
        properties_layout.addWidget(ui.memory_recall, 3, 2, 1, 1)
        self.setLayout(properties_layout)

    def on_video_currentTextChanged(self, text):
        self.cam.video(text)

    def on_memory_set_currentTextChanged(self, text):
        text = int(text)
        self.cam.memory_set(text)

    def on_memory_recall_currentTextChanged(self, text):
        text = int(text)
        self.cam.memory_recall(text)

    def on_power_toggled(self, state):
        self.cam.power = state

    def on_IR_toggled(self, state):
        self.cam.IR = state

    def on_FX_currentTextChanged(self, text):
        if type(text) == unicode:
            text = text.encode('utf-8')
            self.cam.FX = text
