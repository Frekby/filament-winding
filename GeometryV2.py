# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 17:17:40 2020

@author: PSPECE
"""

import sys
from PySide2 import QtCore, QtGui, QtWidgets
import UI.Geometry

class zavd_window(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
#        super().__init__()
        super(zavd_window, self).__init__(parent)   
        self.setWindowModality(QtCore.Qt.ApplicationModal)               # +++

        self.parent = parent                                       # +++
 
        self.ui = UI.Geometry.Ui_MainWindow()
        self.ui.setupUi(self)
        

