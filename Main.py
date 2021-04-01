# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 16:32:55 2020

@author: PSPECE
"""


import sys
from PySide2 import QtUiTools
from PySide2 import QtCore, QtGui, QtWidgets
import UI.Main

class zavd_window(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
#        super().__init__()
        super(zavd_window, self).__init__(parent)                  # +++
        self.setWindowModality(QtCore.Qt.ApplicationModal) 
        self.parent = parent                                       # +++
 
        self.ui = UI.Main.Ui_MainWindow()
        self.ui.setupUi(self)