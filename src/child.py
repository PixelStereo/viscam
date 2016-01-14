#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from PyQt5.QtCore import Qt,QModelIndex,QFileInfo,QFile
from PyQt5.QtWidgets import QFileDialog,QListWidgetItem,QApplication,QMessageBox,QTableWidgetItem,QSpinBox,QComboBox
from PyQt5.QtWidgets import QGroupBox,QHBoxLayout,QLabel,QLineEdit,QListWidget,QAbstractItemView,QPushButton,QGridLayout

# for development of pyCamera, use git version
pyvisca_path = os.path.abspath('./../libs')
sys.path.append(pyvisca_path)

from pyvisca.PyVisca import _cmd_adress_set , _if_clear, Visca

class Document(object):
    """docstring for Document"""
    def __init__(self, arg):
        super(Document, self).__init__()
        self.arg = arg
        self.modified = True

    def contentsChanged(self):
        pass

    def isModified(self):
        return self.modified

    def setModified(self):
        pass


class Camera(QGroupBox,QModelIndex):
    """This is the Camera class"""
    sequenceNumber = 1

    def __init__(self,serial):
        super(Camera, self).__init__()

        self.serial = serial
        
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.isUntitled = True
        # I must change all 'document' class reference to 'camera' class… so I need to enhance camera with modify flags and signals
        self.document = Document('unknown')
        # Create a camera
        self.camera = Visca(serial)

        self.createPowerPanel()

        # Create the main layout
        mainLayout = QGridLayout()
        # Integrate the layout previously created
        mainLayout.addWidget(self.power_Groupbox)
        self.mainLayout = mainLayout
        # Integrate main layout to the main window
        self.setLayout(mainLayout)

    def power_pow_func(self):
        pass

    def createPowerPanel(self):
        power_pow_label = QLabel('power')
        power_pow = QPushButton()
        power_pow.setCheckable(True)
        power_pow.toggled.connect(self.power_pow_func)
        self.power_pow = power_pow

        power_layout = QHBoxLayout()
        power_layout.addWidget(power_pow_label)
        power_layout.addWidget(power_pow)
        power_layout.addStretch(1)

        self.power_Groupbox = QGroupBox()
        self.power_Groupbox.setLayout(power_layout)   

    def newFile(self):
        """create a new camera"""
        self.isUntitled = True
        self.curFile = "camera %d" % Camera.sequenceNumber
        Camera.sequenceNumber += 1
        self.setWindowTitle(self.curFile + '[*]')

        self.camera.name = self.curFile

    def userFriendlyCurrentFile(self):
        return self.strippedName(self.curFile)

    def currentFile(self):
        return self.curFile

    def closeEvent(self, event):
        if self.maybeSave():
            event.accept()
        else:
            event.ignore()

    def documentWasModified(self):
        self.setWindowModified(self.document().isModified())

    def maybeSave(self):
        if self.document.isModified():
            ret = QMessageBox.warning(self, "MDI",
                    "'%s' has been modified.\nDo you want to save your "
                    "changes?" % self.userFriendlyCurrentFile(),
                    QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)

            if ret == QMessageBox.Save:
                return self.save()

            if ret == QMessageBox.Cancel:
                return False

        return True

    def setCurrentFile(self, fileName):
        self.curFile = QFileInfo(fileName).canonicalFilePath()
        self.isUntitled = False
        #self.document().setModified(False)
        self.setWindowModified(False)
        self.setWindowTitle(self.userFriendlyCurrentFile() + "[*]")

    def strippedName(self, fullFileName):
        return QFileInfo(fullFileName).baseName()
  
