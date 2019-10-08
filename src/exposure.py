#! /usr/bin/python
# -*- coding: utf-8 -*-

from pyviscam.constants import answers
from time import sleep
from PySide2.QtWidgets import QGroupBox, QCheckBox, QGridLayout, QPushButton, QSpinBox, \
                                QLabel, QSlider, QComboBox
from PySide2.QtCore import Qt


def get_key_by_value(mydict, value):
    for key, val in mydict.items():
        if val == value:
            return key


class Exposure_UI(QGroupBox):
    """
    A QGroupbox widget with all properties of a Visca camera
    """
    def __init__(self, ui, cam):
        super(Exposure_UI, self).__init__()
        self.cam = cam
        self.ui = ui
        self.setTitle('Exposure')
        expo_layout = QGridLayout()
        ui.AE = QComboBox()
        ui.AE.addItems(['auto', 'manual', 'iris', 'shutter', 'bright'])
        ui.AE.currentTextChanged.connect(self.on_AE_currentTextChanged)
        ui.slowshutter = QCheckBox()
        ui.slowshutter.setText('auto slowshutter')
        ui.slowshutter.clicked.connect(self.on_slowshutter_currentIndexChanged)
        ui.backlight = QCheckBox()
        ui.backlight.setText('Backlight')
        ui.backlight.clicked.connect(self.on_backlight_toggled)
        ui.shutter_label = QLabel()
        ui.shutter_label.setText('Shutter')
        ui.shutter = QComboBox()
        ui.shutter.addItems([str(truc) for truc in answers['shutter'].values()])
        ui.shutter.currentTextChanged.connect(self.on_shutter_currentTextChanged)
        ui.iris_label = QLabel()
        ui.iris_label.setText('Iris')
        ui.iris = QComboBox()
        ui.iris.addItems([str(truc) for truc in answers['iris'].values()])
        ui.iris.currentTextChanged.connect(self.on_iris_currentTextChanged)
        ui.gain_label = QLabel()
        ui.gain_label.setText('Gain')
        ui.gain = QComboBox()
        ui.gain.addItems([str(truc) for truc in answers['gain'].values()])
        ui.gain.currentTextChanged.connect(self.on_gain_currentTextChanged)
        ui.gamma_label = QLabel()
        ui.gamma_label.setText('Gamma')
        ui.gamma = QSpinBox()
        ui.gamma.setMinimum(0)
        ui.gamma.setMaximum(4)
        ui.gamma.valueChanged.connect(self.on_gamma_valueChanged)
        ui.aperture_label = QLabel()
        ui.aperture_label.setText('Aperture')
        ui.aperture = QSpinBox()
        ui.aperture.setMinimum(0)
        ui.aperture.setMaximum(15)
        ui.aperture.valueChanged.connect(self.on_aperture_valueChanged)
        # create a groupbox for all manual settings
        self.expo_manual = QGridLayout()
        self.expo_manual.addWidget(ui.shutter_label, 1, 1, 1, 1)
        self.expo_manual.addWidget(ui.shutter, 2, 1, 1, 1)
        self.expo_manual.addWidget(ui.iris_label, 1, 2, 1, 1)
        self.expo_manual.addWidget(ui.iris, 2, 2, 1, 1)
        self.expo_manual.addWidget(ui.gain_label, 1, 3, 1, 1)
        self.expo_manual.addWidget(ui.gain, 2, 3, 1, 1)
        self.expo_manual.addWidget(ui.gamma_label, 1, 4, 1, 1)
        self.expo_manual.addWidget(ui.gamma, 2, 4, 1, 1)
        self.expo_manual.addWidget(ui.aperture_label, 1, 5, 1, 1)
        self.expo_manual.addWidget(ui.aperture, 2, 5, 1, 1)
        self.expo_manual_box = QGroupBox()
        self.expo_manual_box.setLayout(self.expo_manual)
        expo_layout.addWidget(ui.AE, 1, 1, 1, 1)
        expo_layout.addWidget(ui.slowshutter, 1, 2, 1, 1)
        expo_layout.addWidget(ui.backlight, 1, 3, 1, 1)
        expo_layout.addWidget(self.expo_manual_box, 2, 1, 1, 4)
        self.setLayout(expo_layout)

        AE = cam._query('AE')
        ui.AE.setCurrentText(AE)
        if AE != 'auto':
            # if expo is manual, refresh values
            self.expo_refresh()
        if ui.AE.currentText() == 'auto':
            self.expo_manual_box.setEnabled(False)
        else:
            self.expo_manual_box.setEnabled(True)

    def on_slowshutter_currentIndexChanged(self, state):
        if type(state) == unicode:
            state = state.encode('utf-8')
        if state:
            self.cam.slowshutter = 'auto'
        else:
            self.cam.slowshutter = 'manual'

    def on_backlight_toggled(self, state):
        self.cam.backlight = state

    def expo_refresh(self):
        gamma = self.cam._query('gamma')
        if gamma:
            self.ui.gamma.setValue(gamma)
        aperture = self.cam._query('aperture')
        if aperture:
            self.ui.aperture.setValue(aperture)
        iris = self.cam._query('iris')
        if iris:
            self.ui.iris.setCurrentText(str(iris))
        shutter = self.cam._query('shutter')
        if shutter:
            self.ui.shutter.setCurrentText(str(shutter))
        gain = self.cam._query('gain')
        if gain:
            self.ui.gain.setCurrentText(str(gain))

    def on_AE_currentTextChanged(self, mode):
        if type(mode) == unicode:
            mode = mode.encode('utf-8')
            self.cam.AE = mode
            if mode == 'auto':
                self.expo_manual_box.setEnabled(False)
                self.ui.backlight.setEnabled(True)
                self.ui.slowshutter.setEnabled(True)
            if mode == 'manual':
                self.ui.backlight.setEnabled(False)
                self.ui.slowshutter.setEnabled(False)
                self.expo_manual_box.setEnabled(True)
                self.ui.shutter.setEnabled(True)
                self.ui.shutter_label.setEnabled(True)
                self.ui.iris.setEnabled(True)
                self.ui.iris_label.setEnabled(True)
                self.ui.gain.setEnabled(True)
                self.ui.gain_label.setEnabled(True)
                self.expo_refresh()
            if mode == 'shutter':
                self.ui.backlight.setEnabled(False)
                self.ui.slowshutter.setEnabled(False)
                self.expo_manual_box.setEnabled(True)
                self.ui.shutter.setEnabled(True)
                self.ui.shutter_label.setEnabled(True)
                self.ui.iris.setEnabled(False)
                self.ui.iris_label.setEnabled(False)
                self.ui.gain.setEnabled(False)
                self.ui.gain_label.setEnabled(False)
                self.expo_refresh()
            if mode == 'iris':
                self.ui.backlight.setEnabled(False)
                self.ui.slowshutter.setEnabled(False)
                self.expo_manual_box.setEnabled(True)
                self.ui.iris.setEnabled(True)
                self.ui.iris_label.setEnabled(True)
                self.ui.shutter.setEnabled(False)
                self.ui.shutter_label.setEnabled(False)
                self.ui.gain.setEnabled(False)
                self.ui.gain_label.setEnabled(False)
                self.expo_refresh()

    def on_shutter_currentTextChanged(self, text):
        index = get_key_by_value(answers['shutter'], text)
        self.cam.shutter = index

    def on_iris_currentTextChanged(self, text):
        index = get_key_by_value(answers['iris'], text)
        self.cam.iris = index

    def on_gain_currentTextChanged(self, text):
        index = get_key_by_value(answers['gain'], text)
        self.cam.gain = index

    def on_aperture_valueChanged(self, index):
        self.cam.aperture = int(index)
        self.cam._query('aperture')

    def on_gamma_valueChanged(self, index):
        self.cam.gamma = index
        self.cam._query('gamma')
