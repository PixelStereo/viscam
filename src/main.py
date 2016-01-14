#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from time import sleep
# I need to import these modules here because of pyinstaller
import json, socket, OSC, pjlink
from PyQt5.QtGui import QIcon,QKeySequence
from PyQt5.QtCore import QModelIndex,Qt,QSignalMapper,QSettings,QPoint,QSize,QSettings,QPoint,QFileInfo,QFile
from PyQt5.QtWidgets import QMainWindow,QGroupBox,QApplication,QMdiArea,QWidget,QAction,QListWidget,QPushButton,QMessageBox,QFileDialog,QDialog,QMenu,QToolBar
from PyQt5.QtWidgets import QVBoxLayout,QLabel,QLineEdit,QGridLayout,QHBoxLayout,QSpinBox,QStyleFactory,QListWidgetItem,QAbstractItemView,QComboBox,QTableWidget

# for development of pyCamera, use git version
pyvisca_path = os.path.abspath('./../pyvisca')
sys.path.append(pyvisca_path)

from child import Camera
import PyVisca
from PyVisca.PyVisca import _cmd_adress_set , _if_clear
from PyVisca.PyVisca import Serial as serial


serial = serial()

class MainWindow(QMainWindow):
    """This create the main window of the application"""
    def __init__(self):
        super(MainWindow, self).__init__()    

        self.ports = serial.listports()
        self.port = None

        # remove close & maximize window buttons
        #self.setWindowFlags(Qt.CustomizeWindowHint|Qt.WindowMinimizeButtonHint)
        self.setMinimumSize(850,450)

        self.mdiArea = QMdiArea()
        self.mdiArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdiArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setCentralWidget(self.mdiArea)

        self.mdiArea.subWindowActivated.connect(self.updateMenus)
        self.mdiArea.setViewMode(QMdiArea.TabbedView)

        self.windowMapper = QSignalMapper(self)
        self.windowMapper.mapped[QWidget].connect(self.setActiveSubWindow)

        
        self.child = None

        self.createActions()
        self.createMenus()
        self.createStatusBar()
        self.updateMenus()
        self.readSettings()
        self.setWindowTitle("VISCAM")

        mytoolbar = QToolBar() 
        ports_menu = QComboBox()
        ports_menu.addItem('Output Port')
        ports_menu.insertSeparator(1)
        for port in self.ports:
            ports_menu.addItem(port)
        self.ports_menu = ports_menu
        ports_menu.currentTextChanged.connect(self.setActivePort)
        mytoolbar.addWidget(ports_menu)
        mytoolbar.addSeparator()
        mytoolbar.setMovable(False)
        mytoolbar.setFixedHeight(60)
        self.addToolBar( Qt.TopToolBarArea , mytoolbar )

    def closeEvent(self, scenario):
        self.mdiArea.closeAllSubWindows()
        if self.mdiArea.currentSubWindow():
            scenario.ignore()
        else:
            self.writeSettings()
            scenario.accept()

    def about(self):
        QMessageBox.about(self, "About Viscam",
                "<b>Viscam</b> controls and manage your video camera through VISCA protocol."
                "This release is an alpha version. Don't use it in production !!")

    def updateMenus(self):
        hasCamera = (self.activeCamera() is not None)
        self.nextAct.setEnabled(hasCamera)
        self.previousAct.setEnabled(hasCamera)
        self.separatorAct.setVisible(hasCamera)

    def updatePortMenu(self):
        self.PortMenu.clear()
        for i, port in enumerate(self.ports):

            text = "%d %s" % (i + 1, port)
            if i < 9:
                text = '&' + text

            action = self.PortMenu.addAction(text)
            action.setCheckable(True)
            if port == self.port:
                action.setChecked(True)
            action.triggered.connect(self.setActivePort)

    def updateWindowMenu(self):
        self.windowMenu.clear()
        self.windowMenu.addAction(self.nextAct)
        self.windowMenu.addAction(self.previousAct)
        self.windowMenu.addAction(self.separatorAct)

        windows = self.mdiArea.subWindowList()
        self.separatorAct.setVisible(len(windows) != 0)

        for i, window in enumerate(windows):
            child = window.widget()

            text = "%d %s" % (i + 1, child.userFriendlyCurrentFile())
            if i < 9:
                text = '&' + text

            action = self.windowMenu.addAction(text)
            action.setCheckable(True)
            action.setChecked(child is self.activeCamera())
            action.triggered.connect(self.windowMapper.map)
            self.windowMapper.setMapping(action, window)

    def createCamera(self):
        child = Camera(serial)
        self.mdiArea.addSubWindow(child)
        child.newFile()
        self.child = child
        return child

    def createActions(self):
        self.exitAct = QAction("E&xit", self, shortcut=QKeySequence.Quit,
                statusTip="Exit the application",
                triggered=QApplication.instance().closeAllWindows)

        self.closeAct = QAction("Cl&ose", self,
                statusTip="Close the active window",
                triggered=self.mdiArea.closeActiveSubWindow)

        self.closeAllAct = QAction("Close &All", self,
                statusTip="Close all the windows",
                triggered=self.mdiArea.closeAllSubWindows)

        self.nextAct = QAction("Ne&xt", self, shortcut=QKeySequence.NextChild,
                statusTip="Move the focus to the next window",
                triggered=self.mdiArea.activateNextSubWindow)

        self.previousAct = QAction("Pre&vious", self,
                shortcut=QKeySequence.PreviousChild,
                statusTip="Move the focus to the previous window",
                triggered=self.mdiArea.activatePreviousSubWindow)

        self.separatorAct = QAction(self)
        self.separatorAct.setSeparator(True)

        self.aboutAct = QAction("&About", self,
                statusTip="Show the application's About box",
                triggered=self.about)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.exitAct)

        self.PortMenu = self.menuBar().addMenu("&Ports")
        self.updatePortMenu()
        self.PortMenu.aboutToShow.connect(self.updatePortMenu)

        self.windowMenu = self.menuBar().addMenu("&Window")
        self.updateWindowMenu()
        self.windowMenu.aboutToShow.connect(self.updateWindowMenu)

        self.menuBar().addSeparator()

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAct)

    def createStatusBar(self):
        self.statusBar().showMessage("Ready")

    def readSettings(self):
        settings = QSettings('Pixel Stereo', 'viscam')
        port = settings.value('port')
        pos = settings.value('pos', QPoint(200, 200))
        size = settings.value('size', QSize(1000, 650))
        self.move(pos)
        self.resize(size)

    def writeSettings(self):
        settings = QSettings('Pixel Stereo', 'viscam')
        settings.setValue('port', self.port)
        settings.setValue('pos', self.pos())
        settings.setValue('size', self.size())

    def activeCamera(self):
        activeSubWindow = self.mdiArea.activeSubWindow()
        if activeSubWindow:
            return activeSubWindow.widget()
        else:
            return None

    def findCamera(self, fileName):
        canonicalFilePath = QFileInfo(fileName).canonicalFilePath()

        for window in self.mdiArea.subWindowList():
            if window.widget().currentFile() == canonicalFilePath:
                return window
        return None

    def setActiveSubWindow(self, window):
        if window:
            self.mdiArea.setActiveSubWindow(window)

    def setActivePort(self):
        self.port = self.ports_menu.currentText().encode('utf-8')
        self.updatePortMenu()
        serial.open(portname=self.port)
        viscams = _cmd_adress_set(serial)
        _if_clear(serial)
        for v in viscams:
            v = self.createCamera()




if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())