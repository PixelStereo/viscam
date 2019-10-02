#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
from time import sleep
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import  QStandardItemModel, QStandardItem
from PySide2.QtCore import Slot, QDir, QAbstractListModel, Qt, QFile
from PySide2.QtWidgets import QWidget, QApplication, QHBoxLayout, QDialog, QListView, QListWidget, QPushButton, \
                            QTableWidget, QTableView, QFileDialog, QTableWidgetItem, QWidget, QTreeView, QMainWindow, \
                            QSpinBox, QGroupBox, QGridLayout, QCheckBox, QSlider, QLabel

# Create the visca application
import visca_app

v = visca_app.v

try:
    # stylesheet
    import qdarkstyle
except:
    pass

debug = True
update_run = False


from panels import *


    
class ViscaUI(QMainWindow):
    """create viscam view and controller (MVC)"""
    def __init__(self):
        super(ViscaUI, self).__init__()

        main_panel = self.create_panels()

        # query about params
        power = v._query('power') 
        self.power.setChecked(power)
        IR = v._query('IR') 
        self.IR.setChecked(IR)
        focus = v._query('focus')
        #self.focus_direct_value.setValue(focus)
        nearlimit = v._query('focus_nearlimit')
        #self.focus_nearlimit_value.setValue(nearlimit)
        pan,tilt = v._query('pan_tilt')
        self.tilt.setValue(tilt)
        self.pan.setValue(pan)
        v.IR_auto = False
        focus = v._query('focus')
        self.focus_far_speed = 3
        self.focus_near_speed = 3
        zoom = v._query('zoom')
        self.zoom_direct_value.setValue(zoom)
        self.focus_direct_value.setValue(focus)
        v.video = (720, 50)
        VIDEO = v._query('video')

    def create_panels(self):
        """
        create differents UI panels
        """
        properties_groupbox = create_properties_panel(self)
        focus_groupbox = create_focus_panel(self)
        zoom_groupbox = create_zoom_panel(self)
        pan_tilt_groupbox = create_pan_tilt_panel(self)

        mainLayout = QGridLayout()
        mainLayout.addWidget(properties_groupbox, 1, 1, 1, 1)
        mainLayout.addWidget(focus_groupbox, 2, 1, 1, 1)
        mainLayout.addWidget(zoom_groupbox, 3, 1, 1, 1)
        mainLayout.addWidget(pan_tilt_groupbox, 4, 1, 1, 1)
        #self.setLayout(mainLayout)

        visca_widget = QGroupBox()
        visca_widget.setTitle('VISCA')
        visca_widget.setLayout(mainLayout)
        self.setCentralWidget(visca_widget)
        #self.setFixedSize(640, 512)


    def on_power_toggled(self, state):
        v.power = state
        print('POWER', state)
    
    def on_IR_toggled(self,state):
        v.IR = state






    def on_focus_auto_stateChanged(self, state):
        if state:
            v.focus_auto = 1
            self.focus_manual_box.setEnabled(0)
        else:
            v.focus_auto = 0
            self.focus_manual_box.setEnabled(1)
        sleep(0.1)
        focus = v._query('focus')
        focus_auto___ = v._query('focus_auto')
        print('------autofocus is :', focus_auto___)
        self.focus_direct_value.setValue(focus)
        sleep(0.1)
        nearlimit = v._query('focus_nearlimit')
        self.focus_nearlimit_value.setValue(nearlimit)

    def on_focus_near_pressed(self):
        v.focus_near()

    def on_focus_far_pressed(self):
        v.focus_far()

    def focus_refresh(self):
        focus = v._query('focus')
        self.focus_direct_value.setValue(focus)

    def on_focus_stop_pressed(self):
        v.focus_stop()
        self.focus_refresh()

    def on_focus_near_speed_valueChanged(self, speed):
        self.focus_near_speed = speed

    def on_focus_far_speed_valueChanged(self, speed):
        self.focus_far_speed = speed
    
    def on_focus_direct_valueChanged(self, value):
        v.focus = value
    
    def on_focus_nearlimit_valueChanged(self, nearlimit):
        v.focus_nearlimit = nearlimit








    def on_zoom_direct_valueChanged(self, zoom):
        v.zoom = zoom
        self.zoom = zoom
    
    def on_zoom_tele_pressed(self):
        v.zoom_tele(self.zoom_tele_speed)

    def on_zoom_wide_pressed(self):
        v.zoom_wide(self.zoom_wide_speed)

    def zoom_refresh(self):
        zoom = v._query('zoom')
        self.zoom_direct_value.setValue(zoom)

    def on_zoom_stop_pressed(self):
        v.zoom_stop()
        self.zoom_refresh()

    def on_zoom_tele_speed_valueChanged(self, speed):
        self.zoom_tele_speed = speed

    def on_zoom_wide_speed_valueChanged(self, speed):
        self.zoom_wide_speed = speed







    def on_up_pressed(self):
        v.up()

    def on_left_pressed(self):
        v.left()

    def on_down_pressed(self):
        v.down()

    def on_right_pressed(self):
        v.right()

    def on_upleft_pressed(self):
        v.upleft()

    def on_downleft_pressed(self):
        v.downleft()

    def on_downright_pressed(self):
        v.downright()

    def on_upright_pressed(self):
        v.upright()
        
    def on_home_pressed(self):
        v.home()
        self.pan_tilt_refresh()
        
    def on_reset_pressed(self):
        v.reset()
        self.pan_tilt_refresh()

    def on_stop_pressed(self):
        v.stop()
        self.pan_tilt_refresh()

    def pan_tilt_refresh(self):
        pan, tilt = v._query('pan_tilt')
        self.tilt.setValue(tilt)
        self.pan.setValue(pan)

    def on_pan_speed_valueChanged(self,value):
        v.pan_speed = value

    def on_tilt_speed_valueChanged(self,value):
        v.tilt_speed = value

    def on_pan_valueChanged(self, value):
        value = int(value)
        v.pan = value

    def on_tilt_valueChanged(self, value):
        value = int(value)
        v.tilt = value


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    MainWindow = ViscaUI()
    MainWindow.show()
    sys.exit(app.exec_())



"""


        AE = v._query('AE')
        self.AE.setCurrentText(AE)
        if AE != 'auto':
            # if expo is manual, refresh values
            self.expo_refresh()
        if self.AE.currentText() == 'auto':
            self.AE_manual.setVisible(False)
    
    def expo_refresh(self):
        aperture = v._query('aperture')
        if aperture:
            self.aperture.setCurrentText(str(aperture))
        iris = v._query('iris')
        if iris:
            self.iris.setCurrentText(str(iris))
        shutter = v._query('shutter')
        if shutter:
            self.shutter.setCurrentText(str(shutter))
        gain = v._query('gain')
        if gain:
            self.gain.setCurrentText(str(gain))

    def on_AE_currentIndexChanged(self, mode):
        print(mode)
        if type(mode) == unicode:
            mode = mode.encode('utf-8')
            v.AE = mode
            if mode == 'auto':
                self.AE_manual.setVisible(False)
            if mode == 'manual':
                self.AE_manual.setVisible(True)
                self.shutter.setVisible(True)
                self.shutter_label.setVisible(True)
                self.iris.setVisible(True)
                self.iris_label.setVisible(True)
                self.gain.setVisible(True)
                self.gain_label.setVisible(True)
                self.expo_refresh()
            if mode == 'shutter':
                self.AE_manual.setVisible(True)
                self.shutter.setVisible(True)
                self.shutter_label.setVisible(True)
                self.iris.setVisible(False)
                self.iris_label.setVisible(False)
                self.gain.setVisible(False)
                self.gain_label.setVisible(False)
                self.expo_refresh()
            if mode == 'iris':
                self.AE_manual.setVisible(True)
                self.iris.setVisible(True)
                self.iris_label.setVisible(True)
                self.shutter.setVisible(False)
                self.shutter_label.setVisible(False)
                self.gain.setVisible(False)
                self.gain_label.setVisible(False)
                self.expo_refresh()

    def on_shutter_currentIndexChanged(self, index):
        if type(index) == unicode:
            print('shutter', index)
        else:
            v.shutter = index

    def on_iris_currentIndexChanged(self, index):
        if type(index) == unicode:
            print('iris', index)
        else:
            v.iris = index

    def on_gain_currentIndexChanged(self, index):
        if type(index) == unicode:
            print('gain', index)
        else:
            v.gain = index

    def on_aperture_currentIndexChanged(self, index):
        if type(index) == unicode:
            print('aperture', index)
        else:
            v.aperture = index

    def on_slowshutter_currentIndexChanged(self,state):
        if type(state) == unicode:
            state = state.encode('utf-8')
        if state:
            v.slowshutter = 'auto'
        else:
            v.slowshutter = 'manual'


    def on_gamma_valueChanged(self, value):
        v.gamma = int(value)
        v._query('gamma')


    def on_WB_currentTextChanged(self, text):
        if type(text) == unicode:
            text = text.encode('utf-8')
            v.WB = text
    def on_FX_currentTextChanged(self, text):
        if type(text) == unicode:
            text = text.encode('utf-8')
            v.FX = text




    def on_mem_recall_1_toggled(self,state):
        if state:
            v.memory_recall(0)

    def on_mem_recall_2_toggled(self,state):
        if state:
            v.memory_recall(1)
    def on_mem_recall_3_toggled(self,state):
        if state:
            v.memory_recall(2)
    def on_mem_recall_4_toggled(self,state):
        if state:
            v.memory_recall(3)

    def on_mem_recall_5_toggled(self,state):
        if state:
            v.memory_recall(4)

    def on_mem_set_1_toggled(self,state):
        if state:
            v.memory_set(0)
    def on_mem_set_2_toggled(self,state):
        if state:
            v.memory_set(1)

    def on_mem_set_3_toggled(self,state):
        if state:
            v.memory_set(2)

    def on_mem_set_4_toggled(self, state):
        if state:
            v.memory_set(3)
    def on_mem_set_5_toggled(self, state):
        if state:
            v.memory_set(4)


"""