#! /usr/bin/python
# -*- coding: utf-8 -*-

from pyviscam.constants import answers
from time import sleep
from PySide2.QtWidgets import QGroupBox, QCheckBox, QGridLayout, QPushButton, QSpinBox, \
                                QLabel, QSlider, QComboBox
from PySide2.QtCore import Qt


class Exposure_UI(QGroupBox):
    """
    A QGroupbox widget with all properties of a Visca camera
    """
    def __init__(self, visca, v):
        super(Exposure_UI, self).__init__()
        self.v = v
        self.visca = visca
        self.setTitle('Exposure')
        expo_layout = QGridLayout()
        visca.AE = QComboBox()
        visca.AE.addItems(['auto', 'manual', 'iris', 'shutter', 'bright'])
        visca.AE.currentTextChanged.connect(self.on_AE_currentTextChanged)
        visca.shutter_label = QLabel()
        visca.shutter_label.setText('Shutter')
        visca.shutter = QComboBox()
        visca.shutter.addItems([str(truc) for truc in answers['shutter'].values()])
        visca.shutter.currentTextChanged.connect(self.on_shutter_currentTextChanged)
        visca.iris_label = QLabel()
        visca.iris_label.setText('Iris')
        visca.iris = QComboBox()
        visca.iris.addItems([str(truc) for truc in answers['iris'].values()])
        visca.iris.currentTextChanged.connect(self.on_iris_currentTextChanged)
        visca.gain_label = QLabel()
        visca.gain_label.setText('Gain')
        visca.gain = QComboBox()
        visca.gain.addItems([str(truc) for truc in answers['gain'].values()])
        visca.gain.currentTextChanged.connect(self.on_gain_currentTextChanged)
        visca.gamma_label = QLabel()
        visca.gamma_label.setText('Gamma')
        visca.gamma = QSpinBox()
        visca.gamma.setMinimum(0)
        visca.gamma.setMaximum(4)
        visca.gamma.valueChanged.connect(self.on_gamma_valueChanged)
        visca.aperture_label = QLabel()
        visca.aperture_label.setText('Aperture')
        visca.aperture = QSpinBox()
        visca.aperture.setMinimum(0)
        visca.aperture.setMaximum(15)
        visca.aperture.valueChanged.connect(self.on_aperture_valueChanged)
        # create a groupbox for all manual settings
        self.expo_manual = QGridLayout()
        self.expo_manual.addWidget(visca.shutter_label, 1, 1, 1, 1)
        self.expo_manual.addWidget(visca.shutter, 2, 1, 1, 1)
        self.expo_manual.addWidget(visca.iris_label, 1, 2, 1, 1)
        self.expo_manual.addWidget(visca.iris, 2, 2, 1, 1)
        self.expo_manual.addWidget(visca.gain_label, 1, 3, 1, 1)
        self.expo_manual.addWidget(visca.gain, 2, 3, 1, 1)
        self.expo_manual.addWidget(visca.gamma_label, 1, 4, 1, 1)
        self.expo_manual.addWidget(visca.gamma, 2, 4, 1, 1)
        self.expo_manual.addWidget(visca.aperture_label, 1, 5, 1, 1)
        self.expo_manual.addWidget(visca.aperture, 2, 5, 1, 1)
        self.expo_manual_box = QGroupBox()
        self.expo_manual_box.setLayout(self.expo_manual)
        expo_layout.addWidget(visca.AE, 1, 1, 1, 1)
        expo_layout.addWidget(self.expo_manual_box, 2, 1, 1, 1)
        self.setLayout(expo_layout)

        AE = v._query('AE')
        visca.AE.setCurrentText(AE)
        if AE != 'auto':
            # if expo is manual, refresh values
            self.expo_refresh()
        if visca.AE.currentText() == 'auto':
            self.expo_manual_box.setEnabled(False)
        else:
            self.expo_manual_box.setEnabled(True)
    
    def expo_refresh(self):
        gamma = self.v._query('gamma')
        if gamma:
            self.visca.gamma.setValue(gamma)
        aperture = self.v._query('aperture')
        if aperture:
            self.visca.aperture.setValue(aperture)
        iris = self.v._query('iris')
        if iris:
            self.visca.iris.setCurrentText(str(iris))
        shutter = self.v._query('shutter')
        if shutter:
            self.visca.shutter.setCurrentText(str(shutter))
        gain = self.v._query('gain')
        if gain:
            self.visca.gain.setCurrentText(str(gain))

    def on_AE_currentTextChanged(self, mode):
        print(mode)
        if type(mode) == unicode:
            mode = mode.encode('utf-8')
            self.v.AE = mode
            if mode == 'auto':
                self.expo_manual_box.setEnabled(False)
            if mode == 'manual':
                self.expo_manual_box.setEnabled(True)
                self.visca.shutter.setEnabled(True)
                self.visca.shutter_label.setEnabled(True)
                self.visca.iris.setEnabled(True)
                self.visca.iris_label.setEnabled(True)
                self.visca.gain.setEnabled(True)
                self.visca.gain_label.setEnabled(True)
                self.expo_refresh()
            if mode == 'shutter':
                self.expo_manual_box.setEnabled(True)
                self.visca.shutter.setEnabled(True)
                self.visca.shutter_label.setEnabled(True)
                self.visca.iris.setEnabled(False)
                self.visca.iris_label.setEnabled(False)
                self.visca.gain.setEnabled(False)
                self.visca.gain_label.setEnabled(False)
                self.expo_refresh()
            if mode == 'iris':
                self.expo_manual_box.setEnabled(True)
                self.visca.iris.setEnabled(True)
                self.visca.iris_label.setEnabled(True)
                self.visca.shutter.setEnabled(False)
                self.visca.shutter_label.setEnabled(False)
                self.visca.gain.setEnabled(False)
                self.visca.gain_label.setEnabled(False)
                self.expo_refresh()

    def on_shutter_currentTextChanged(self, text):
        text = str(text)
        text = int(text)
        print('shutter', text, answers['shutter'].keys()[answers['shutter'].values().index(text)])
        self.v.shutter = answers['shutter'][text]

    def on_iris_currentTextChanged(self, text):
        text = str(text)
        text = int(text)
        print('iris', text, answers['iris'].keys()[answers['iris'].values().index(text)])
        self.v.iris = answers['iris'][index]

    def on_gain_currentTextChanged(self, text):
        text = str(text)
        text = int(text)
        print('gain', text, answers['gain'].keys()[answers['gain'].values().index(text)])
        self.v.gain = answers['gain'][text]

    def on_aperture_valueChanged(self, index):
        self.v.aperture = int(value)
        self.v._query('aperture')

    def on_gamma_valueChanged(self, value):
        print('gamma', value)
        self.v.gamma = value
        self.v._query('gamma')
