#! /usr/bin/python
# -*- coding: utf-8 -*-


from PySide2.QtWidgets import QGroupBox, QCheckBox, QGridLayout, QComboBox

class Properties_UI(QGroupBox):
    """
    A QGroupbox widget with all properties of a Visca camera
    """
    def __init__(self, visca, v):
        super(Properties_UI, self).__init__()
        self.v = v
        self.visca = visca
        self.setTitle('Properties')
        properties_layout = QGridLayout()
        visca.power = QCheckBox()
        visca.power.setText('Power')
        visca.power.clicked.connect(self.on_power_toggled)
        properties_layout.addWidget(visca.power, 1, 1, 1, 1)
        visca.IR = QCheckBox()
        visca.IR.setText('IR')
        visca.IR.clicked.connect(self.on_IR_toggled)
        properties_layout.addWidget(visca.IR, 1, 2, 1, 1)
        visca.FX = QComboBox()
        visca.FX.addItems(['Normal', 'NegArt', 'B&W'])
        visca.FX.currentTextChanged.connect(self.on_FX_currentTextChanged)
        properties_layout.addWidget(visca.FX, 2, 1, 1, 2)
        visca.slowshutter = QCheckBox()
        visca.slowshutter.setText('slowshutter')
        visca.slowshutter.clicked.connect(self.on_slowshutter_currentIndexChanged)
        properties_layout.addWidget(visca.slowshutter, 1, 3, 1, 1)
        visca.WB = QComboBox()
        visca.WB.addItems(['auto', 'indoor', 'outdoor', 'trigger', 'manual'])
        visca.WB.currentTextChanged.connect(self.on_WB_currentTextChanged)
        properties_layout.addWidget(visca.WB, 2, 3, 1, 2)
        self.setLayout(properties_layout)

    def on_power_toggled(self, state):
        self.v.power = state
        print('POWER', state)

    def on_IR_toggled(self, state):
        self.v.IR = state

    def on_FX_currentTextChanged(self, text):
        print(text)
        if type(text) == unicode:
            text = text.encode('utf-8')
            self.v.FX = text

    def on_slowshutter_currentIndexChanged(self, state):
        if type(state) == unicode:
            state = state.encode('utf-8')
        if state:
            self.v.slowshutter = 'auto'
        else:
            self.v.slowshutter = 'manual'

    def on_WB_currentTextChanged(self, text):
        if type(text) == unicode:
            text = text.encode('utf-8')
            self.v.WB = text
