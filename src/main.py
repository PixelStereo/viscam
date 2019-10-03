#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
main script
"""

import sys
from viscam import Viscam
from PySide2.QtCore import QFileInfo
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QApplication


try:
    # stylesheet
    import qdarkstyle
except Exception as error:
    print('failed ' + str(error))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    try:
        #app.setStyleSheet(qdarkstyle.load_stylesheet_PySide2())
        pass
    except Exception as error:
        print('failed ' + str(error))
    root = QFileInfo(__file__).absolutePath()
    path = root+'/icon/icon.png'
    app.setWindowIcon(QIcon(path))
    mainWin = Viscam()
    mainWin.show()
    sys.exit(app.exec_())
