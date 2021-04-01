# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 17:15:41 2020

@author: PSPECE
"""

from PySide2.QtCore import Qt,QLocale
from PySide2.QtGui  import QDoubleValidator, QKeySequence
from PySide2 import QtWidgets


import UI.Main
from Setup_Line import zavd_window as UI2
from GeometryV2 import zavd_window as UI3
from Tolhina import zavd_window as UI4
from Ugol_namotki import zavd_window as UI5
from ExitOkno import zavd_window as UI6

import sys
from glumpy import app, gl, glm, gloo, geometry
import numpy as np
import geom as g
import namotka as nam
import Point_Index as PI
import math as math
import pyqtgraph as pg

vertex = """
uniform mat4   model;         // Model matrix
uniform mat4   view;          // View matrix
uniform mat4   projection;    // Projection matrix

attribute vec3 position;      // Vertex position
attribute float off;
varying float z_off;

void main()
{
    gl_Position = projection * view * model * vec4(position,1.0);
    z_off = off;
 
  
}
"""

fragment = """
uniform vec4   color; 
varying float z_off;

void main()
{
    gl_FragColor =color;
    gl_FragDepth = gl_FragCoord.z*0.001-0.00002*z_off;


}
"""

vertex1 = """
uniform mat4   model;         // Model matrix
uniform mat4   view;          // View matrix
uniform mat4   projection;    // Projection matrix
attribute vec3 position;      // Vertex position

varying vec4 pos;

void main()
{
    gl_Position = projection * view * model * vec4(position,1.0);
    pos=projection * view * model * vec4(position,1.0);
}
"""

fragment1 = """
uniform vec4   color; 

varying vec4 pos;


void main()
{
    

    gl_FragColor =color;


}
"""

config = app.configuration.Configuration()
config.double_buffer
config.samples=8
#config.depth_size=64

app.use('pyside2')
window = app.Window(width=640, height=640,color=(1, 1, 1, 1),config=config)
k=0
j=0

Z0=-5000
X0=0
Y0=0
frame=0
cube=0
V=0
dno=[1,6]
countEx=0
keyset=0

phi, theta,animate = 80, 30, 0
model = np.eye(4, dtype=np.float32)
glm.rotate(model, phi, 0, 1, 0)
glm.rotate(model, theta, 1, 0, 0)
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self)
        
        self.originalPalette = QtWidgets.QApplication.palette()
        self.setLine = UI2(self)
        self.Geometry = UI3(self)
        self.Tolhina = UI4(self)
        self.Ugol_namotki = UI5(self)
        self.Exit_Okno = UI6(self)
        
        
        self.ui = UI.Main.Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.ui.menu.setEnabled(False)

        '''
        self.setWindowFlags(
        Qt.Window |
        Qt.CustomizeWindowHint |
        Qt.WindowTitleHint |
        Qt.WindowMaximizeButtonHint |
        Qt.WindowMinimizeButtonHint 
        )
        '''
        self.Exit_Okno.setWindowFlags(
        Qt.Window |
        Qt.CustomizeWindowHint |
        Qt.WindowTitleHint 
        )
        
        
        pDoubleValidator = QDoubleValidator(self)
        pDoubleValidator.setNotation(QDoubleValidator.StandardNotation)
        pDoubleValidator.setLocale(QLocale(QLocale.C))

        #Настройки модуля геометрии
        self.Geometry.ui.lineEdit.setValidator(pDoubleValidator)
        self.Geometry.ui.lineEdit_2.setValidator(pDoubleValidator)
        self.Geometry.ui.lineEdit_3.setValidator(pDoubleValidator)
        self.Geometry.ui.lineEdit_4.setValidator(pDoubleValidator)
        self.Geometry.ui.lineEdit_5.setValidator(pDoubleValidator)
        self.Geometry.ui.lineEdit_6.setValidator(pDoubleValidator)
   
        #Настройки модуля ленты
        self.setLine.ui.lineEdit.setValidator(pDoubleValidator)
        self.setLine.ui.lineEdit_2.setValidator(pDoubleValidator)

        #Триггеры основной формы
        self.ui.action_6.triggered.connect(self.open_zavdannia)
        self.ui.action_2.triggered.connect(self.open_Geom)
        self.ui.action_3.triggered.connect(self.open_Tolhina)
        self.ui.action_4.triggered.connect(self.open_Ugol_namotki)
        self.ui.action_5.triggered.connect(self.Close)
        self.ui.pushButton.pressed.connect(self.anim1)
        self.ui.pushButton.clicked.connect(self.vpered)
        self.ui.pushButton_5.clicked.connect(self.stop)
        self.ui.pushButton_6.pressed.connect(self.anim2)
        self.ui.pushButton_6.clicked.connect(self.nazad)
        self.ui.pushButton_7.clicked.connect(self.anim1)
        self.ui.pushButton_8.clicked.connect(self.anim2)
        self.ui.pushButton_9.clicked.connect(self.vievAll)
        
       
        self.ui.vbox = QtWidgets.QVBoxLayout()
        self.ui.groupBox.setLayout(self.ui.vbox)

        self.ui.vbox.addWidget(window._native_window)
       
        #Триггеры геометрии ленты формы
        self.setLine.ui.pushButton.clicked.connect(self.Create_Line)
        self.setLine.ui.pushButton_2.clicked.connect(self.CloseLent)
        self.setLine.ui.pushButton_4.clicked.connect(self.pattern)
        self.setLine.ui.tableWidget.itemClicked.connect(self.setppattern)


        #Триггеры геометрии бака формы
        self.Geometry.ui.comboBox.currentIndexChanged.connect(self.setParam_1)
        self.Geometry.ui.comboBox_2.currentIndexChanged.connect(self.setParam_2)

        self.Geometry.ui.groupBox_3.setVisible(False)
        self.Geometry.ui.groupBox_4.setVisible(False)
        
        self.Geometry.ui.lineEdit.textChanged.connect(self.ChangedRE)
        self.Geometry.ui.lineEdit_2.textChanged.connect(self.ChangedRE)
        self.Geometry.ui.lineEdit_3.textChanged.connect(self.ChangedRE)
        self.Geometry.ui.lineEdit_4.textChanged.connect(self.ChangedRE)
        self.Geometry.ui.lineEdit_5.textChanged.connect(self.ChangedRE)
        self.Geometry.ui.lineEdit_6.textChanged.connect(self.ChangedRE)
        self.Geometry.ui.pushButton.clicked.connect(self.Create_Geom)
        
        
        
        #Тригеры для выходного окна
        self.Exit_Okno.ui.pushButton.clicked.connect(self.exitALL)

        #График построения толщины
        self.Graf_Tolhina = QtWidgets.QVBoxLayout()
        self.Tolhina.ui.groupBox.setLayout(self.Graf_Tolhina)
        
        self.pw_Tolhina = pg.PlotWidget(name='Plot1')
        self.pw_Tolhina.setMenuEnabled(False)
        self.Graf_Tolhina.addWidget(self.pw_Tolhina)
        
        #График построения угла намотки
        self.Graf_Ugol = QtWidgets.QVBoxLayout()
        self.Ugol_namotki.ui.groupBox.setLayout(self.Graf_Ugol)
        
        self.pw_Ugol = pg.PlotWidget(name='Plot1')
        self.pw_Ugol.setMenuEnabled(False)
        self.Graf_Ugol.addWidget(self.pw_Ugol)        

        #График построения контура бака
        self.Graf_Kontur = QtWidgets.QVBoxLayout()
        self.Geometry.ui.groupBox_5.setLayout(self.Graf_Kontur)
        
        self.pw_Kontur = pg.PlotWidget(name='Plot1')
        self.pw_Kontur.setMenuEnabled(False)
        self.Graf_Kontur.addWidget(self.pw_Kontur) 


    def vievAll(self):
        global frame,cube,V
        frame=0
        window.clear()
        #window._native_window.setFocus()
        
 
    def exitALL(self):
        global cube,V
        self.Exit_Okno.hide()
        del cube
        del V
        self.close()
       
    def ChangedRE(self):
        self.pw_Kontur.clear()
        try: 
            re=float(self.Geometry.ui.lineEdit.text())
            Hcil=float(self.Geometry.ui.lineEdit_2.text())
            Hkonus1=float(self.Geometry.ui.lineEdit_5.text())
            Hkonus2=float(self.Geometry.ui.lineEdit_6.text())
            Hsf1=(re**2-float(self.Geometry.ui.lineEdit_3.text())**2)/(2*float(self.Geometry.ui.lineEdit_3.text()))
            Hsf2=(re**2-float(self.Geometry.ui.lineEdit_4.text())**2)/(2*float(self.Geometry.ui.lineEdit_4.text()))
        except ValueError:
            okk1=1
        else:
            g.dataInput(re, Hcil,Hkonus1,Hkonus2,Hsf1,Hsf2)
            z1=np.linspace(0, g.Z(0,dno[0]), 100)
            z3=np.linspace(g.Z(0,dno[1]), 0, 100)
            #print(g.Z(0,dno[0]))
            r1=g.R(z1,dno[0])
            r3=g.R(z3,dno[1])
            self.pw_Kontur.setYRange(0, 2*np.amax([r1,r3]))
            self.pw_Kontur.plot(z1-g.Z(0,dno[1])+Hcil,r1,pen='r')
            self.pw_Kontur.plot(z3-g.Z(0,dno[1]),r3,pen='r')
            self.pw_Kontur.plot(np.array([-g.Z(0,dno[1]),Hcil-g.Z(0,dno[1])]),np.array([re,re]),pen='r')

    def open_Ugol_namotki(self):
        global r,hh
        re=float(self.Geometry.ui.lineEdit.text())
        L=float(self.setLine.ui.lineEdit.text())
        Hcil=float(self.Geometry.ui.lineEdit_2.text())
        toch=20
        ug=float(self.setLine.ui.lineEdit_2.text())
        nn=int(r)+1
        n=1
        nam.dataInput(re, toch, dno)

        Hkonus1=float(self.Geometry.ui.lineEdit_5.text())
        Hkonus2=float(self.Geometry.ui.lineEdit_6.text())
        Hsf1=(re**2-float(self.Geometry.ui.lineEdit_3.text())**2)/(2*float(self.Geometry.ui.lineEdit_3.text()))
        Hsf2=(re**2-float(self.Geometry.ui.lineEdit_4.text())**2)/(2*float(self.Geometry.ui.lineEdit_4.text()))
        g.dataInput(re, Hcil,Hkonus1,Hkonus2,Hsf1,Hsf2)

        #hh=float(self.setLine.ui.tableWidget.item(r,s).text())
        hh1=hh[r,s+1]
        if self.setLine.ui.radioButton.isChecked():
            gg=nam.cikl_dli_ugla(n,ug,0,0,L,nn,hh1)
        elif self.setLine.ui.radioButton_2.isChecked(): 
            gg=nam.ciklV2_dli_ugla(n,ug,0,0,L,nn,hh1)
        
        
        z1=gg[:,2]
        t1=gg[:,4]*180/np.pi
        self.pw_Ugol.clear()
        self.pw_Ugol.plot(z1+Hcil-g.Z(0,dno[1]),t1)
        self.Ugol_namotki.show()
       
    def open_Tolhina(self):
        global dno,gg1
        re=float(self.Geometry.ui.lineEdit.text())
        ug=float(self.setLine.ui.lineEdit_2.text())
        L=float(self.setLine.ui.lineEdit.text())
        Hcil=float(self.Geometry.ui.lineEdit_2.text())
        
        Hkonus1=float(self.Geometry.ui.lineEdit_5.text())
        Hkonus2=float(self.Geometry.ui.lineEdit_6.text())
        Hsf1=(re**2-float(self.Geometry.ui.lineEdit_3.text())**2)/(2*float(self.Geometry.ui.lineEdit_3.text()))
        Hsf2=(re**2-float(self.Geometry.ui.lineEdit_4.text())**2)/(2*float(self.Geometry.ui.lineEdit_4.text()))
        g.dataInput(re, Hcil,Hkonus1,Hkonus2,Hsf1,Hsf2)
        
        toch=20
        toch1=toch*3+1
        Rline1=np.sqrt(gg1[0,0]**2+gg1[0,1]**2)
        Rline2=np.sqrt(gg1[toch1,0]**2+gg1[toch1,1]**2)
        t=0.1
        zmax1=g.Z(re*np.sin(ug*np.pi/180),dno[0])-1
        zmax2=g.Z(Rline2,dno[1])+1
        

        z1=np.linspace(0, zmax1, 1000)
        t1=np.zeros(1000)
        for i in range(1000):
            t1[i]=nam.tolhinaVerh(z1[i],re,ug,L,t,g.Zr,g.R,dno[0],Rline1)
        
        z2=np.linspace(zmax2, 0, 1000)
        t2=np.zeros(1000)
        for i in range(1000):
            t2[i]=nam.tolhinaNiz(z2[i],re,ug,L,t,g.Zr,g.R,dno[1],Rline2)  
        self.pw_Tolhina.clear()
        self.pw_Tolhina.plot(z1-g.Z(0,dno[1])+Hcil,t1)
        self.pw_Tolhina.plot(np.array([-g.Z(0,dno[1]),Hcil-g.Z(0,dno[1])]),np.array([2*t,2*t]))
        self.pw_Tolhina.plot(z2-g.Z(0,dno[1]),t2)
        self.Tolhina.show()

    def setParam_1(self,i):
        if i==0:
            self.Geometry.ui.groupBox_3.hide()
            self.Geometry.ui.groupBox.show()
            dno[0]=1
            self.pw_Kontur.clear()
            re=float(self.Geometry.ui.lineEdit.text())
            Hcil=float(self.Geometry.ui.lineEdit_2.text())
            Hkonus1=float(self.Geometry.ui.lineEdit_5.text())
            Hkonus2=float(self.Geometry.ui.lineEdit_6.text())
            Hsf1=(re**2-float(self.Geometry.ui.lineEdit_3.text())**2)/(2*float(self.Geometry.ui.lineEdit_3.text()))
            Hsf2=(re**2-float(self.Geometry.ui.lineEdit_4.text())**2)/(2*float(self.Geometry.ui.lineEdit_4.text()))
            g.dataInput(re, Hcil,Hkonus1,Hkonus2,Hsf1,Hsf2)
            z1=np.linspace(0, g.Z(0,dno[0]), 100)
            z3=np.linspace(g.Z(0,dno[1]), 0, 100)
            #print(g.Z(0,dno[0]))
            r1=g.R(z1,dno[0])
            r3=g.R(z3,dno[1])
            self.pw_Kontur.setYRange(0, 2*re)
            self.pw_Kontur.plot(z1-g.Z(0,dno[1])+Hcil,r1,pen='r')
            self.pw_Kontur.plot(z3-g.Z(0,dno[1]),r3,pen='r')
            self.pw_Kontur.plot(np.array([-g.Z(0,dno[1]),Hcil-g.Z(0,dno[1])]),np.array([re,re]),pen='r')
            
        if i==1:
            self.Geometry.ui.groupBox.hide()
            self.Geometry.ui.groupBox_3.show()
            dno[0]=5
            self.pw_Kontur.clear()
            re=float(self.Geometry.ui.lineEdit.text())
            Hcil=float(self.Geometry.ui.lineEdit_2.text())
            Hkonus1=float(self.Geometry.ui.lineEdit_5.text())
            Hkonus2=float(self.Geometry.ui.lineEdit_6.text())
            Hsf1=(re**2-float(self.Geometry.ui.lineEdit_3.text())**2)/(2*float(self.Geometry.ui.lineEdit_3.text()))
            Hsf2=(re**2-float(self.Geometry.ui.lineEdit_4.text())**2)/(2*float(self.Geometry.ui.lineEdit_4.text()))
            g.dataInput(re, Hcil,Hkonus1,Hkonus2,Hsf1,Hsf2)
            z1=np.linspace(0, g.Z(0,dno[0]), 100)
            z3=np.linspace(g.Z(0,dno[1]), 0, 100)
            #print(g.Z(0,dno[0]))
            r1=g.R(z1,dno[0])
            r3=g.R(z3,dno[1])
            self.pw_Kontur.setYRange(0, 2*re)
            self.pw_Kontur.plot(z1-g.Z(0,dno[1])+Hcil,r1,pen='r')
            self.pw_Kontur.plot(z3-g.Z(0,dno[1]),r3,pen='r')
            self.pw_Kontur.plot(np.array([-g.Z(0,dno[1]),Hcil-g.Z(0,dno[1])]),np.array([re,re]),pen='r')
            
            
    def setParam_2(self,i):
        if i==0:
            self.Geometry.ui.groupBox_4.hide()
            self.Geometry.ui.groupBox_2.show()
            dno[1]=6
            self.pw_Kontur.clear()
            re=float(self.Geometry.ui.lineEdit.text())
            Hcil=float(self.Geometry.ui.lineEdit_2.text())
            Hkonus1=float(self.Geometry.ui.lineEdit_5.text())
            Hkonus2=float(self.Geometry.ui.lineEdit_6.text())
            Hsf1=(re**2-float(self.Geometry.ui.lineEdit_3.text())**2)/(2*float(self.Geometry.ui.lineEdit_3.text()))
            Hsf2=(re**2-float(self.Geometry.ui.lineEdit_4.text())**2)/(2*float(self.Geometry.ui.lineEdit_4.text()))
            g.dataInput(re, Hcil,Hkonus1,Hkonus2,Hsf1,Hsf2)
            z1=np.linspace(0, g.Z(0,dno[0]), 100)
            z3=np.linspace(g.Z(0,dno[1]), 0, 100)
            #print(g.Z(0,dno[0]))
            r1=g.R(z1,dno[0])
            r3=g.R(z3,dno[1])
            self.pw_Kontur.setYRange(0, 2*re)
            self.pw_Kontur.plot(z1-g.Z(0,dno[1])+Hcil,r1,pen='r')
            self.pw_Kontur.plot(z3-g.Z(0,dno[1]),r3,pen='r')
            self.pw_Kontur.plot(np.array([-g.Z(0,dno[1]),Hcil-g.Z(0,dno[1])]),np.array([re,re]),pen='r')
            
        if i==1:
            self.Geometry.ui.groupBox_2.hide()
            self.Geometry.ui.groupBox_4.show()
            dno[1]=3
            self.pw_Kontur.clear()
            re=float(self.Geometry.ui.lineEdit.text())
            Hcil=float(self.Geometry.ui.lineEdit_2.text())
            Hkonus1=float(self.Geometry.ui.lineEdit_5.text())
            Hkonus2=float(self.Geometry.ui.lineEdit_6.text())
            Hsf1=(re**2-float(self.Geometry.ui.lineEdit_3.text())**2)/(2*float(self.Geometry.ui.lineEdit_3.text()))
            Hsf2=(re**2-float(self.Geometry.ui.lineEdit_4.text())**2)/(2*float(self.Geometry.ui.lineEdit_4.text()))
            g.dataInput(re, Hcil,Hkonus1,Hkonus2,Hsf1,Hsf2)
            z1=np.linspace(0, g.Z(0,dno[0]), 100)
            z3=np.linspace(g.Z(0,dno[1]), 0, 100)
            #print(g.Z(0,dno[0]))
            r1=g.R(z1,dno[0])
            r3=g.R(z3,dno[1])
            self.pw_Kontur.setYRange(0, 2*re)
            self.pw_Kontur.plot(z1-g.Z(0,dno[1])+Hcil,r1,pen='r')
            self.pw_Kontur.plot(z3-g.Z(0,dno[1]),r3,pen='r')
            self.pw_Kontur.plot(np.array([-g.Z(0,dno[1]),Hcil-g.Z(0,dno[1])]),np.array([re,re]),pen='r')
            

    def open_Geom(self):
        re=float(self.Geometry.ui.lineEdit.text())
        Hcil=float(self.Geometry.ui.lineEdit_2.text())
        Hkonus1=float(self.Geometry.ui.lineEdit_5.text())
        Hkonus2=float(self.Geometry.ui.lineEdit_6.text())
        Hsf1=(re**2-float(self.Geometry.ui.lineEdit_3.text())**2)/(2*float(self.Geometry.ui.lineEdit_3.text()))
        Hsf2=(re**2-float(self.Geometry.ui.lineEdit_4.text())**2)/(2*float(self.Geometry.ui.lineEdit_4.text()))
        g.dataInput(re, Hcil,Hkonus1,Hkonus2,Hsf1,Hsf2)
        
        z1=np.linspace(0, g.Z(0,dno[0]), 100)
        z3=np.linspace(g.Z(0,dno[1]), 0, 100)
        r1=g.R(z1,dno[0])
        r3=g.R(z3,dno[1])

        self.pw_Kontur.clear()
        self.pw_Kontur.setYRange(0, 2*np.amax([r1,r3]))
        
        self.pw_Kontur.plot(z1-np.amin(z3)+Hcil,r1,pen='r')
        self.pw_Kontur.plot(z3-np.amin(z3),r3,pen='r')
        self.pw_Kontur.plot(np.array([-np.amin(z3),Hcil-np.amin(z3)]),np.array([re,re]),pen='r')

        self.Geometry.show()


    def setppattern(self):
        global r, s
        r = self.setLine.ui.tableWidget.currentRow()
        s = 1



    def pattern(self):
        global hh
        re=float(self.Geometry.ui.lineEdit.text())
        kol=20
        toch=20
        L=float(self.setLine.ui.lineEdit.text())
        ug=float(self.setLine.ui.lineEdit_2.text())
        nam.dataInput(re, toch, dno)
        hh=nam.ugolV2(L,ug,re,kol)
        kol=hh.shape[0]-1
        self.setLine.ui.tableWidget.setRowCount(kol) 
        for i in range(kol):
            self.setLine.ui.tableWidget.setItem(i,0,QtWidgets.QTableWidgetItem(str(hh[i,0])))
            self.setLine.ui.tableWidget.setItem(i,1,QtWidgets.QTableWidgetItem(str(round(hh[i,1]*180/np.pi,3))))
            self.setLine.ui.tableWidget.setItem(i,2,QtWidgets.QTableWidgetItem(str(round(hh[i,3],1))))
            self.setLine.ui.tableWidget.setItem(i,3,QtWidgets.QTableWidgetItem(str(hh[i,2])))



    def stop(self):
        window.clear()
        self.ui.pushButton_6.setDown(False)
        self.ui.pushButton.setDown(False)
        #window._native_window.setFocus()
        
    def vpered(self):
        window.clear()
        self.ui.pushButton.setDown(True)
        #window._native_window.setFocus()

    def nazad(self):
        window.clear()
        self.ui.pushButton_6.setDown(True)
        #window._native_window.setFocus()

    def anim1(self):
        global cube,V,frame,animate,gg, model
        window.clear()
        #cube.bind(V[:frame])
        if frame<V.shape[0] and frame>=6:
            frame+=6
            #animate=2*gg[0,3]*180/np.pi-(gg[int(frame/2-3),3]*180/np.pi)
            if frame/2<V.shape[0]/2:
                animate=gg[int(frame/2-3),3]-gg[int(frame/2),3]
            else:
                animate=0
            glm.rotate(model, -animate*180/np.pi, -model[2,0], -model[2,1], -model[2,2])
        elif frame==0:
            model = np.eye(4, dtype=np.float32)
            glm.rotate(model, phi, 0, 1, 0)
            glm.rotate(model, theta, 1, 0, 0)
            glm.rotate(model, -gg[0,3]*180/np.pi, -model[2,0], -model[2,1], -model[2,2])
            frame=6

            
    def anim2(self):
        global cube,V,frame,animate,gg
        window.clear()
        #cube.bind(V[:frame])
        if frame>6:
            
            #animate=2*gg[0,3]*180/np.pi-(gg[int(frame/2-3),3]*180/np.pi)
            if frame/2<V.shape[0]/2:
                animate=gg[int(frame/2-3),3]-gg[int(frame/2),3]
            else:
                animate=0
            glm.rotate(model, animate*180/np.pi, -model[2,0], -model[2,1], -model[2,2])
            frame-=6
        
        

    def open_zavdannia(self):
        self.setLine.show()

      
    
    def CloseLent(self):
        self.setLine.close()

    
    def Close(self):
        global countEx
        countEx=1
        self.ui.pushButton_6.setDown(False)
        self.ui.pushButton.setDown(False)
        window.clear()
        window._native_window.close()  
        self.Exit_Okno.show()
        #ex.close()

      
    def closeEvent(self, event):
        global countEx
        if countEx==0:
            event.ignore()
            window.clear()
            window._native_window.close()
            countEx=1
            self.Exit_Okno.show()
        else:
            event.accept()
    

#Создание геометрии
    @window.event
    def on_draw(dt):
        
        global phi, theta, duration,k,cube,cube1,j,animate,frame,Igeom
        window.clear()
        gl.glClear(gl.GL_DEPTH_BUFFER_BIT)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        
            
        if k==1:
            #model = np.eye(4, dtype=np.float32)
            #phi =phi
            #theta =theta
            #animate=animate
            
            #glm.rotate(model, animate, 0, 0, 1)
            #glm.rotate(model, phi, 0, 1, 0)
            #glm.rotate(model, theta, 1, 0, 0)
            
            
            cube['model'] = model
            
            
            gl.glEnable(gl.GL_CULL_FACE)
            gl.glCullFace(gl.GL_FRONT)

            gl.glPolygonMode(gl.GL_BACK, gl.GL_FILL)
            gl.glEnable(gl.GL_POLYGON_OFFSET_FILL)
            cube['color'] = 0, 1, 0, 1
            gl.glPolygonOffset( -10, -10)
            cube.draw(gl.GL_TRIANGLE_STRIP,frame=frame)
            #???? может тут убрать I
            #gl.glDepthMask(gl.GL_FALSE)
            gl.glPolygonMode(gl.GL_BACK, gl.GL_LINE)
            gl.glEnable(gl.GL_POLYGON_OFFSET_LINE)
            cube['color'] = 0, 0, 0, 1
            gl.glLineWidth( 2)
            gl.glPolygonOffset( 0, 0)
            cube.draw(gl.GL_TRIANGLE_STRIP,frame=frame)
            #gl.glDepthMask(gl.GL_TRUE)
  
            gl.glDisable(gl.GL_POLYGON_OFFSET_FILL)
            gl.glDisable(gl.GL_CULL_FACE)

 
          
        if j==1:
            
            #phi =phi
            #theta =theta
            #animate=animate
            #model = np.eye(4, dtype=np.float32)
            #glm.rotate(model, animate, 0, 0, 1)
            #glm.rotate(model, phi, 0, 1, 0)
            #glm.rotate(model, theta, 1, 0, 0)

            cube1['model'] = model
            gl.glEnable(gl.GL_CULL_FACE)
            gl.glCullFace(gl.GL_FRONT)
            
            gl.glEnable(gl.GL_LINE_SMOOTH)
            gl.glEnable(gl.GL_POLYGON_OFFSET_LINE)
        
            gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_FILL)
            gl.glPolygonOffset( -10, -10)
            cube1['color'] = 1, 1, 0, 1
            cube1.draw(gl.GL_TRIANGLES, Igeom)
    
            gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE)
            gl.glLineWidth( 1)
            cube1['color'] = 0, 0, 0, 1
            cube1.draw(gl.GL_TRIANGLES, Igeom)

            gl.glDisable(gl.GL_LINE_SMOOTH)
            gl.glDisable(gl.GL_POLYGON_OFFSET_LINE)

            gl.glDisable(gl.GL_POLYGON_OFFSET_FILL)
            gl.glDisable(gl.GL_CULL_FACE)
      
    @window.event
    def on_resize(width, height):
        
        global cube,cube1,k,width1,height1,j
        height1=height
        width1=width
        if k==1:
            cube['projection'] = glm.perspective(45, width / float(height), 1, 10000.0)
        if j==1:
            cube1['projection'] = glm.perspective(45, width / float(height), 1, 10000.0)
    
    
    @window.event
    def on_init():
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glEnable(gl.GL_BLEND) 
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA) 
        #gl.glEnable(gl.GL_FRAMEBUFFER_SRGB)
        gl.glHint(gl.GL_LINE_SMOOTH_HINT, gl.GL_NICEST)
        gl.glEnable(gl.GL_MULTISAMPLE)
    
#Смещение по нажатию стрелок 
    '''       
    @window.event
    def on_key_press(key, modifiers):
        #print(modifiers)
        global keyset
        if modifiers == 2:
            keyset=1
    
    @window.event        
    def on_key_release(key, modifiers):
        global keyset
        keyset=0
    '''           
        
    
    def keyPressEvent(self, e):
        global keyset
        val = e.key()
        if val==Qt.Key_Control:
            keyset=1
          
    def keyReleaseEvent(self, e):
        global keyset
        keyset=0

#Отдаление/приблежение колесиком мыши     
    @window.event
    def on_mouse_scroll(x, y, dx, dy):
        global Z0,cube,cube1,X0,Y0,Z0,k,j
        Z0=Z0+dy*20
        if k==1:
            cube['view'] = glm.translation(X0, Y0, Z0)
        if j==1:
            cube1['view'] = glm.translation(X0, Y0, Z0)

#Вращение по нажатие мыши       
    @window.event
    def on_mouse_drag(x, y, dx, dy, button):
        global phi,theta,X0,Y0,Z0,keyset,k,j
        #window._native_window.setFocus()
        #phi+=dx/10
        #theta+=dy/10
        if phi>360:
            phi=0
        if phi<0:
            phi=360
        if theta>360:
            theta=0
        if theta<0:
            theta=360
        if keyset==0:
            glm.rotate(model, dx/2, 0, 1, 0)
            glm.rotate(model, dy/2, 1, 0, 0)
        elif keyset==1:
            X0+=dx*5
            Y0-=dy*5
            if k==1:
                cube['view']=glm.translation(X0, Y0, Z0)
            if j==1:
                cube1['view']=glm.translation(X0, Y0, Z0)

        #print('Угол (phi=%.1f, theta=%.1f, dx=%.1f, dy=%.1f, button=%d)' % (phi,theta,dx,dy,button))
        #print('Mouse drag (x=%.1f, y=%.1f, dx=%.1f, dy=%.1f, button=%d)' % (x,y,dx,dy,button))

        
    def Create_Geom(self):
        window.clear()
        global cube,cube1,k,phi,theta,X0,Y0,Z0,width1,height1,j,Igeom
        k=0
        #window._native_window.setFocus()
        j=1
        re=float(self.Geometry.ui.lineEdit.text())
        Hcil=float(self.Geometry.ui.lineEdit_2.text())
        Hkonus1=float(self.Geometry.ui.lineEdit_5.text())
        Hkonus2=float(self.Geometry.ui.lineEdit_6.text())
        Hsf1=(re**2-float(self.Geometry.ui.lineEdit_3.text())**2)/(2*float(self.Geometry.ui.lineEdit_3.text()))
        Hsf2=(re**2-float(self.Geometry.ui.lineEdit_4.text())**2)/(2*float(self.Geometry.ui.lineEdit_4.text()))
        
        g.dataInput(re, Hcil,Hkonus1,Hkonus2,Hsf1,Hsf2)


        V1,I1,VV1,II1=PI.surface(g.FF,umin=0, umax=2*np.pi, ucount=20,
                  vmin=0, vmax=g.Z(0,dno[0]), vcount=20,f=dno[0])

        V2,I2,VV2,II2=PI.surface(g.FF,umin=0, umax=-2*np.pi, ucount=20,
                  vmin=0, vmax=g.Z(0,2), vcount=20,f=2)

        V3,I3,VV3,II3=PI.surface(g.FF,umin=0, umax=-2*np.pi, ucount=20,
                  vmin=0, vmax=g.Z(0,dno[1]), vcount=20,f=dno[1])
        
        #print(geometry.normals(VV1["position"], II1))
        #np.savetxt('ggg.txt',V1["position"][:,2])
        #print(V1["position"][:,1])
        Vgeom = np.zeros(np.max(I3)+np.max(I1)+np.max(I2)+3, [('position', np.float32, 3)])
        Vgeom["position"]=np.row_stack((V1["position"],V2["position"],V3["position"]))
        Igeom=np.hstack((I1,I2+1+np.max(I1),I3+np.max(I1)+np.max(I2)+2))
        Igeom=Igeom.view(gloo.IndexBuffer)
        cube1 = gloo.Program(vertex1, fragment1)
 
        cube1.bind(Vgeom.view(gloo.VertexBuffer))



        cube1['model'] = np.eye(4, dtype=np.float32)
        cube1['view'] = glm.translation(X0, Y0, Z0)


        
        #phi, theta = 90, 0
        window.dispatch_event('on_resize',  width1, height1)
        self.Geometry.hide()
        self.ui.menu.setEnabled(True)
        
    def Create_Line(self):
        #window.clear()
        global cube,cube1,k,I,I1,I2,I3,phi,theta,X0,Y0,Z0,width1,height1,V,frame,gg,animate,r,s,gg1,hh
        #window._native_window.setFocus()
        k=1
        frame=0
        re=float(self.Geometry.ui.lineEdit.text())
        L=float(self.setLine.ui.lineEdit.text())
        toch=20
        ug=float(self.setLine.ui.lineEdit_2.text())
        nn=int(hh[r,0])
        n=int(hh[r,2])
        nam.dataInput(re, toch, dno)

        #hh=float(self.setLine.ui.tableWidget.item(r,s).text())
        hh1=hh[r,s]
        #hh=nam.ugolV2(L,ug,re,nn)
        if self.setLine.ui.radioButton.isChecked():
            gg=nam.cikl(n,ug,0,0,L,nn,hh1)
        elif self.setLine.ui.radioButton_2.isChecked(): 
            gg=nam.ciklV2(n,ug,0,0,L,nn,hh1)
        gg1=nam.W(g.R,g.Rz,g.Z0,g.Z,L,gg,gg.shape[0])

        #gg,gg1=nam.masht(gg,gg1)
        points3=PI.point(gg,gg1)  
        #np.savetxt('ff.txt',gg1)
    
        V = np.zeros(points3[0].shape[0], [('position', np.float32, 3)])
        V['position']=points3[0]

        V = V.view(gloo.VertexBuffer)
        I=points3[1]
        I=I.view(gloo.IndexBuffer)
        cube = gloo.Program(vertex, fragment)
        cube.bind(V)
        phi, theta, animate = phi, theta, animate

        cube['model'] = np.eye(4, dtype=np.float32)
        cube['view'] = glm.translation(X0, Y0, Z0)
        cube['off'] = points3[3]
        
        window.dispatch_event('on_resize',  width1, height1)
        


if __name__ == '__main__':
    app1 = QtWidgets.QApplication.instance()
    if app1 is None: 
        app1 = QtWidgets.QApplication(sys.argv)
    form = MainWindow()
    form.show()
    app.run()
    sys.exit(app1.exec_())