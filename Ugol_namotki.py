# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 13:07:03 2020

@author: PSPECE
"""


import sys
from PySide2 import QtCore, QtGui, QtWidgets
import UI.Ugol_namotki

class zavd_window(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
#        super().__init__()
        super(zavd_window, self).__init__(parent)                  # +++
        self.setWindowModality(QtCore.Qt.ApplicationModal) 
        self.parent = parent                                       # +++
 
        self.ui = UI.Ugol_namotki.Ui_MainWindow()
        self.ui.setupUi(self)       
