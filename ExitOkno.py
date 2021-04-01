# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 19:41:19 2020

@author: PSPECE
"""
import sys
from PySide2 import QtCore, QtGui, QtWidgets
import UI.ExitOkno

class zavd_window(QtWidgets.QDialog):
    def __init__(self, parent=None):
#        super().__init__()
        super(zavd_window, self).__init__(parent)                  # +++
        self.setWindowModality(QtCore.Qt.ApplicationModal) 
        self.parent = parent                                       # +++
 
        self.ui = UI.ExitOkno.Ui_Dialog()
        self.ui.setupUi(self)

