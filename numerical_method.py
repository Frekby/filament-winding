# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 11:38:25 2020

@author: Admin
"""
import numpy as np
import math as math

def Chord_root(tol,x1,x2,f):
    while math.fabs(x2-x1)>=tol:
        xroot=x2-(f(x2)*(x2-x1)/(f(x2)-f(x1)))
        x1=x2
        x2=xroot
    return xroot


def Urav(Xa1,Ya1,Za1,RR1,RRz1):
    F=lambda t1:(Xa1+2*Xa1*t1)**2+(Ya1+2*Ya1*t1)**2-(RR1(Za1-2*RR1(Za1)*RRz1(Za1)*t1))**2
    return Chord_root(0.00001,-0.00001,0.00001,F)


def Runge4(f,y0,a,b,n):
    x=np.zeros((n+1,1))
    y=np.zeros((n+1,1))
    x[0]=a
    y[0]=y0
    h=(b-a)/n
    for i in range(0,n):
        x[i+1]=x[i]+h
        k1=f(x[i])
        k2=f(x[i]+h/2)
        k3=f(x[i]+h/2)
        k4=f(x[i]+h)
        y[i+1]=y[i]+h*((k1+2*k2+2*k3+k4)/6)
    return np.column_stack((x,y))

def Binorm(z,O,RRz,a,obr):
    Binorm=np.zeros(3)
    Binorm[0]=-obr*np.sin(O)*np.cos(a)*(RRz(z)**2+1)/np.sqrt(RRz(z)**2+1)-RRz(z)*np.cos(O)*np.sin(a)
    Binorm[1]=obr*np.cos(O)*np.cos(a)*(RRz(z)**2+1)/np.sqrt(RRz(z)**2+1)-RRz(z)*np.sin(O)*np.sin(a)
    Binorm[2]=-np.sin(a)
    Binorm=Binorm/np.sqrt(RRz(z)**2+1)
    return Binorm

def Normal(z,O,RRz,a,obr):
    Normal=np.zeros(3)
    Normal[0]=np.cos(O)
    Normal[1]=np.sin(O)
    Normal[2]=-RRz(z)
    Normal=-obr*Normal/np.sqrt(RRz(z)**2+1)
    return Binorm