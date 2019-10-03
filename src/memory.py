#! /usr/bin/python
# -*- coding: utf-8 -*-




from PySide2.QtWidgets import QGroupBox, QCheckBox, QGridLayout, QComboBox, QLabel

class Memory_UI(QGroupBox):
    """
    A QGroupbox widget with all properties of a Visca camera
    """
    def __init__(self, visca, v):
        super(Memory_UI, self).__init__()
        self.v = v
        self.visca = visca
        self.setTitle('Memory')
        memory_layout = QGridLayout()
        mem_set_label = QLabel()
        mem_set_label.setText('Make Memory')
        memory_layout.addWidget(mem_set_label, 1, 1, 1, 1)
        visca.memory_set = QComboBox()
        mem_list = [str(i) for i in range(16)]
        visca.memory_set.addItems(mem_list)
        visca.memory_set.currentTextChanged.connect(self.on_memory_set_currentTextChanged)
        memory_layout.addWidget(visca.memory_set, 2, 1, 1, 1)
        mem_recall_label = QLabel()
        mem_recall_label.setText('Recall Memory')
        memory_layout.addWidget(mem_recall_label, 1, 2, 1, 1)
        visca.memory_recall = QComboBox()
        visca.memory_recall.addItems(mem_list)
        visca.memory_recall.currentTextChanged.connect(self.on_memory_recall_currentTextChanged)
        memory_layout.addWidget(visca.memory_recall, 2, 2, 1, 1)
        self.setLayout(memory_layout)

    def on_memory_set_currentTextChanged(self, text):
        print(text)
        text = int(text)
        print(text)
        self.v.memory_set(text)

    def on_memory_recall_currentTextChanged(self, text):
        print(text)
        text = int(text)
        print(text)
        self.v.memory_recall(text)
