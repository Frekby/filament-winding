# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 12:06:09 2020

@author: Admin
"""
import numpy as np
import math as math

g_re=0
g_Hcil=0
g_Konus1=0
g_Konus2=0
g_Hsf1=0
g_Hsf2=0

def dataInput(arg1,arg2,arg3, arg4, arg5,arg6):
    global g_re, g_Hcil, g_Konus1, g_Konus2,g_Hsf1,g_Hsf2
    g_re = arg1
    g_Hcil = arg2
    g_Konus1=arg3
    g_Konus2=arg4
    g_Hsf1=arg5
    g_Hsf2=arg6

def R(z,f):
    if f==1:
        return np.sqrt(abs(g_re**2+g_Hsf1**2-(z+g_Hsf1)**2))
    if f==2:
        return g_re
    if f==3:
        return (g_Konus2+z)*g_re/g_Konus2
    if f==4:
        return g_re
    if f==5:
        return (g_Konus1-z)*g_re/g_Konus1
    if f==6:
        return np.sqrt(abs(g_re**2+g_Hsf2**2-(z-g_Hsf2)**2))

def Rz(z,f):
    if f==1:
        return -(z+g_Hsf1)/np.sqrt(g_re**2+g_Hsf1**2-(z+g_Hsf1)**2)
    if f==2:
        return 0
    if f==3:
        return g_re/g_Konus2 
    if f==4:
        return 0
    if f==5:
        return -g_re/g_Konus1
    if f==6:
        return -(z-g_Hsf2)/np.sqrt(g_re**2+g_Hsf2**2-(z-g_Hsf2)**2) 

        

def Z(r,f):
    if f==1:
        return np.sqrt(g_re**2+g_Hsf1**2-r**2)-g_Hsf1
    if f==2:
        return -g_Hcil
    if f==3:
        return (r-g_re)*g_Konus2/g_re
    if f==4:
        return g_Hcil
    if f==5:
        return (g_re-r)*g_Konus1/g_re
    if f==6:
        return -np.sqrt(g_re**2+g_Hsf2**2-r**2)+g_Hsf2
    
    
def Zr(r,f):
    if f==1:
        return -r/np.sqrt(g_re**2+g_Hsf1**2-r**2)
    if f==2:
        return 0
    if f==3:
        return g_Konus2/g_re
    if f==4:
        return 0
    if f==5:
        return -g_Konus2/g_re
    if f==6:
        return r/np.sqrt(g_re**2+g_Hsf2**2-r**2) 

def g(z,f):
    if f==1:
        return z
    if f==2:
        return z
    if f==3:
        return z-g_Hcil
    if f==4:
        return z
    if f==5:
        return z
    if f==6:
        return z-g_Hcil

def Z0(f):
    if f==1:
        return 0
    if f==2:
        return 0
    if f==3:
        return -g_Hcil
    if f==4:
        return -g_Hcil
    if f==5:
        return 0   
    if f==6:
        return -g_Hcil
    
def FF(u,v,i):

    x1 = abs(R(v,i))*np.cos(u)
    y1 = abs(R(v,i))*np.sin(u)
    z1 = g(v,i)
    
    return x1, y1, z1
