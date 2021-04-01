# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 13:03:24 2020

@author: Admin
"""
import numpy as np
import numerical_method as nm
#from scipy.integrate import quad
import AdaptiveIntegral as AI
import geom as g
import math as math

nam_re=0
nam_toch=0
nam_dn=[0,0]

def dataInput(arg1,arg2, arg3):
    global nam_re, nam_toch, nam_dn
    nam_re = arg1
    nam_toch  = arg2
    nam_dn=arg3



def namotka(a0,re,O0,toch,RR,ZZ,Rz,chec2,Z0,obr,s,chec1,f,f1):
    a1=a0*np.pi/180
    rp=re*np.sin(a1)

    def a(z):
       if rp/RR(z,f)>1:
           return 1
       return np.arcsin(rp/RR(z,f))
   
 
    def D(z1):
       return np.sqrt(Rz(z1,f)*Rz(z1,f)+1)*np.tan(a(z1))*obr/RR(z1,f)
   
    O=O0
    OZ=nm.Runge4(D,O,0,ZZ(rp,f),toch)
    
    a2=np.zeros((toch+1,1))
    for i in range(0,toch+1):
        a2[i]=a(OZ[i,0])
        if chec2==1:
            a2[toch]=np.pi/2
    OZ[toch,1]=AI.quadadapt(D, 0,ZZ(rp,f)-0.00000001)+O   
    #OZ[toch,1]=quad(D,0,ZZ(rp,f))[0]+O
    

    if chec1==1:
        OZ=np.flip(OZ,axis = 0)
        a2=np.flip(a2)

      
    XYZOaR=np.zeros((toch+1,10))
    

    
    for i in range(0,toch+1):
        XYZOaR[i,0]=RR(OZ[i,0],f)*np.cos(OZ[i,1])
        XYZOaR[i,1]=RR(OZ[i,0],f)*np.sin(OZ[i,1])
        XYZOaR[i,2]=Z0(f)+OZ[i,0]
        XYZOaR[i,3]=OZ[i,1]
        XYZOaR[i,4]=a2[i]
        XYZOaR[i,5]=np.sqrt(XYZOaR[i,0]**2+XYZOaR[i,1]**2)
        XYZOaR[i,6]=f
        XYZOaR[i,7]=f1        
        XYZOaR[i,8]=obr
        XYZOaR[i,9]=a2[i]*obr
    
    return XYZOaR

def W(R,Rz,Z0,Z,s,GG,razm):
    XYZ=np.zeros((razm,10))
    for i in range(0,razm):
        
        RR1=lambda z:R(z,GG[i,6])
        RR2=lambda z:R(z,GG[i,7])
        RR1z=lambda z:Rz(z,GG[i,6])
        RR2z=lambda z:Rz(z,GG[i,7])
        RR1zKV=lambda z:-2*RR1(z)*RR1z(z)
        RR2zKV=lambda z:-2*RR2(z)*RR2z(z)
        
        Zk=GG[i,2]-Z0(GG[i,6])
        Binorm1=nm.Binorm(Zk,GG[i,3],RR1z,GG[i,4],GG[i,8])
        Xa=GG[i,0]+s*Binorm1[0]
        Ya=GG[i,1]+s*Binorm1[1]
        Za=Zk+s*Binorm1[2]
        t=nm.Urav(Xa,Ya,Za,RR1,RR1z)
        if np.isnan(t):
            t=XYZ[i-1,3]
        XYZ[i,0]=Xa+2*Xa*t
        XYZ[i,1]=Ya+2*Ya*t
        XYZ[i,2]=Z0(GG[i,6])+Za+RR1zKV(Za)*t
        if np.isnan(RR1zKV(Za)):
            #??????? хз как лучше тут сделать 
            XYZ[i,2]=Z(np.sqrt(XYZ[i,0]**2+XYZ[i,1]**2),GG[i,6])+Z0(GG[i,6])
            #XYZ[i,2]=XYZ[i-1,2]
            
        XYZ[i,3]=t
        XYZ[i,4]=RR1zKV(Za)
        
        if ((XYZ[i,2])<Z0(GG[i,7]) and GG[i,7]!=GG[i,6]):
            if GG[i,8]>0:
                tt=(Za-Z0(GG[i,7]))/Binorm1[2]
            if GG[i,8]<0:
                tt=Za/Binorm1[2]
            Xa=GG[i,0]+(s-tt)*Binorm1[0]
            Ya=GG[i,1]+(s-tt)*Binorm1[1]
            Za=Zk+(s-tt)*Binorm1[2]
            t=nm.Urav(Xa,Ya,Za,RR1,RR1z)
            Binorm2=nm.Binorm(GG[i,2]-Z0(GG[i,7]),GG[i,3],RR2z,GG[i,4],GG[i,8])
            Xa=Xa+2*Xa*t+tt*Binorm2[0]
            Ya=Ya+2*Ya*t+tt*Binorm2[1]
            Za=Z0(GG[i,6])+Za+RR1zKV(Za)*t+tt*Binorm2[2]
            t1=nm.Urav(Xa,Ya,Za-Z0(GG[i,7]),RR2,RR2z)
            XYZ[i,0]=Xa+2*Xa*t1
            XYZ[i,1]=Ya+2*Ya*t1
            XYZ[i,2]=Za+RR2zKV(Za-Z0(GG[i,7]))*t1 
            XYZ[i,3]=t
            XYZ[i,4]=RR1zKV(Za)
             
    return XYZ

def otkl(R,Rz,Z0,GG,GG1,t0):
    t=t0
    XYZ=np.zeros((GG.shape[0],10))
    XYZ1=np.zeros((GG.shape[0],10))
    for i in range(0, GG.shape[0]-1):

        
        RR1=lambda z:R(z,GG[i,6])
        RR2=lambda z:R(z,GG1[i,3])
        RR1z=lambda z:Rz(z,GG[i,6])
        RR2z=lambda z:Rz(z,GG1[i,3])
        RR1zKV=lambda z:-2*RR1(z)*RR1z(z)
        RR2zKV=lambda z:-2*RR2(z)*RR2z(z)
        t1=nm.Urav(GG[i,0],GG[i,1],GG[i,2]-Z0(GG[i,6]),RR1,RR1z,t)
        t2=nm.Urav(GG1[i,0],GG1[i,1],GG1[i,2]-Z0(GG1[i,3]),RR2,RR2z,t)
        
        XYZ[i,0]=GG[i,0]+2*GG[i,0]*t1
        XYZ[i,1]=GG[i,1]+2*GG[i,1]*t1
        XYZ[i,2]=GG[i,2]+2*RR1zKV(GG[i,2]-Z0(GG[i,6]))*t1 
        
        XYZ1[i,0]=GG1[i,0]+2*GG1[i,0]*t2
        XYZ1[i,1]=GG1[i,1]+2*GG1[i,1]*t2
        XYZ1[i,2]=GG1[i,2]+2*RR2zKV(GG1[i,2]-Z0(GG1[i,3]))*t2 
        if GG[i,8]!=GG[i+1,8]:
            t=t+t0
        
    i=GG.shape[0]-1
    RR1=lambda z:R(z,GG[i,6])
    RR2=lambda z:R(z,GG1[i,3])
    RR1z=lambda z:Rz(z,GG[i,6])
    RR2z=lambda z:Rz(z,GG1[i,3])
    RR1zKV=lambda z:-2*RR1(z)*RR1z(z)
    RR2zKV=lambda z:-2*RR2(z)*RR2z(z)
    t1=nm.Urav(GG[i,0],GG[i,1],GG[i,2],RR1,RR1z,t)
    t2=nm.Urav(GG1[i,0],GG1[i,1],GG1[i,2],RR2,RR2z,t)
    
    XYZ[i,0]=GG[i,0]+2*GG[i,0]*t1
    XYZ[i,1]=GG[i,1]+2*GG[i,1]*t1
    XYZ[i,2]=GG[i,2]+2*RR1zKV(GG[i,2]-Z0(GG[i,6]))*t1 
        
    XYZ1[i,0]=GG1[i,0]+2*GG1[i,0]*t2
    XYZ1[i,1]=GG1[i,1]+2*GG1[i,1]*t2
    XYZ1[i,2]=GG1[i,2]+2*RR2zKV(GG1[i,2]-Z0(GG1[i,3]))*t2 
    return XYZ,XYZ1    
        

def masht(GG,GG1):
    XYZ=np.zeros((GG.shape[0],10))
    XYZ1=np.zeros((GG.shape[0],10))
    for i in range(0,GG.shape[0]):
        m=1.005
        XYZ[i,0]=GG[i,0]*m
        XYZ[i,1]=GG[i,1]*m
        XYZ[i,2]=GG[i,2]*m
        XYZ[i,3]=GG[i,3]
        XYZ1[i,0]=GG1[i,0]*m
        XYZ1[i,1]=GG1[i,1]*m
        XYZ1[i,2]=GG1[i,2]*m
        XYZ1[i,3]=GG1[i,3]
    return XYZ,XYZ1



def okr(z0,r,o0,O0,a0,toch,f,f1,obr,ugolreal):
    okr1=np.zeros((toch+1,10))
    for i in range(0,toch+1):
        okr1[i,0]=r*np.cos(-o0*i/toch+O0)
        okr1[i,1]=r*np.sin(-o0*i/toch+O0)
        okr1[i,2]=z0
        okr1[i,3]=-o0*i/toch+O0
        okr1[i,4]=a0
        okr1[i,5]=r
        okr1[i,6]=f
        okr1[i,7]=f1
        okr1[i,8]=obr
        okr1[i,9]=ugolreal
    return okr1



def cikl(n,a,O0,L,LL,nn,hh0):
    obr=1
    for i in range(1,n+1):
        if i>=nn+1:
            O0=O0-np.trunc((i-1)/nn)*LL/(nam_re*np.cos(a*np.pi/180))
        G1=namotka(a,nam_re,O0,nam_toch,g.R,g.Z,g.Rz,1,g.Z0,obr,L,1,nam_dn[0],2)
        G2=namotka(a,nam_re,G1[nam_toch,3],nam_toch,g.R,g.Z,g.Rz,0,g.Z0,obr,L,0,2,nam_dn[1])
        G3=namotka(a,nam_re,G2[nam_toch,3],nam_toch,g.R,g.Z,g.Rz,1,g.Z0,obr,L,0,nam_dn[1],nam_dn[1])
        okr1=okr(G3[nam_toch,2],G3[nam_toch,5],hh0,G3[nam_toch,3],G3[nam_toch,4],nam_toch,G3[nam_toch,6],G3[nam_toch,7],obr,G3[nam_toch,9])
        G4=namotka(a,nam_re,2*G3[nam_toch,3]-G2[nam_toch,3]-hh0,nam_toch,g.R,g.Z,g.Rz,1,g.Z0,-obr,L,1,nam_dn[1],nam_dn[1])
        G5=namotka(a,nam_re,G4[nam_toch,3],nam_toch,g.R,g.Z,g.Rz,0,g.Z0,-obr,L,0,4,nam_dn[1])
        G6=namotka(a,nam_re,G5[nam_toch,3],nam_toch,g.R,g.Z,g.Rz,1,g.Z0,-obr,L,0,nam_dn[0],2)
        
        if (i % nn)==0:
            okr2=okr(G6[nam_toch,2],G6[nam_toch,5],LL/(nam_re*np.cos(a*np.pi/180)),G6[nam_toch,3],G6[nam_toch,4],nam_toch,G6[nam_toch,6],G6[nam_toch,7],obr,G6[nam_toch,9])
            okr2=np.delete(okr2,(0), axis=0)
            G6=np.vstack((G6,okr2))
        
        O0=2*G6[nam_toch,3]-G5[nam_toch,3]

        G1=np.delete(G1,(nam_toch), axis=0)
        G2=np.delete(G2,(nam_toch), axis=0)
        G3=np.delete(G3,(nam_toch), axis=0)
        G4=np.delete(G4,(0), axis=0)
        G5=np.delete(G5,(0), axis=0)
        G6=np.delete(G6,(0), axis=0)
        
        if i>1:
            G1=np.delete(G1,(0), axis=0)
        if i>=nn+1:
            O0=O0+np.trunc((i-1)/nn)*LL/(nam_re*np.cos(a*np.pi/180))
        if i==1:
            cikl1=np.vstack((G1,G2,G3,okr1,G4,G5,G6))
        if i>1:
            cikl1=np.vstack((cikl1,G1,G2,G3,okr1,G4,G5,G6))

            
    return cikl1


def ciklV2(n,a,O0,L,LL,nn,hh0):
    obr=1
    for i in range(1,n+1):
        if i>=nn+1:
            O0=O0-np.trunc((i-1)/nn)*LL/(nam_re*np.cos(a*np.pi/180))
        G1=namotka(a,nam_re,O0,nam_toch,g.R,g.Z,g.Rz,1,g.Z0,obr,L,1,nam_dn[0],2)
        G2=namotka(a,nam_re,G1[nam_toch,3],nam_toch,g.R,g.Z,g.Rz,0,g.Z0,obr,L,0,2,nam_dn[1])
        G3=namotka(a,nam_re,G2[nam_toch,3],nam_toch,g.R,g.Z,g.Rz,1,g.Z0,obr,L,0,nam_dn[1],nam_dn[1])
        okr1=okr(G3[nam_toch,2],G3[nam_toch,5],hh0/2,G3[nam_toch,3],G3[nam_toch,4],nam_toch,G3[nam_toch,6],G3[nam_toch,7],obr,G3[nam_toch,9])
        G4=namotka(a,nam_re,2*G3[nam_toch,3]-G2[nam_toch,3]-hh0/2,nam_toch,g.R,g.Z,g.Rz,1,g.Z0,-obr,L,1,nam_dn[1],nam_dn[1])
        G5=namotka(a,nam_re,G4[nam_toch,3],nam_toch,g.R,g.Z,g.Rz,0,g.Z0,-obr,L,0,4,nam_dn[1])
        G6=namotka(a,nam_re,G5[nam_toch,3],nam_toch,g.R,g.Z,g.Rz,1,g.Z0,-obr,L,0,nam_dn[0],2)
        Okr2=okr(G6[nam_toch,2],G6[nam_toch,5],hh0/2,G6[nam_toch,3],G6[nam_toch,4],nam_toch,G6[nam_toch,6],G6[nam_toch,7],-obr,G6[nam_toch,9])
        
        if (i % nn)==0:
            okr3=okr(Okr2[nam_toch,2],Okr2[nam_toch,5],LL/(nam_re*np.cos(a*np.pi/180)),Okr2[nam_toch,3],Okr2[nam_toch,4],nam_toch,Okr2[nam_toch,6],Okr2[nam_toch,7],obr,Okr2[nam_toch,9])
            okr3=np.delete(okr3,(0), axis=0)
            Okr2=np.vstack((Okr2,okr3))
        
        O0=2*G6[nam_toch,3]-G5[nam_toch,3]-hh0/2
        

        G1=np.delete(G1,(nam_toch), axis=0)
        G2=np.delete(G2,(nam_toch), axis=0)
        G3=np.delete(G3,(nam_toch), axis=0)
        G4=np.delete(G4,(0), axis=0)
        G5=np.delete(G5,(0), axis=0)
        G6=np.delete(G6,(0), axis=0)
        Okr2=np.delete(Okr2,(0), axis=0)
        if i>1:
            G1=np.delete(G1,(0), axis=0)
        if i>=nn+1:
            O0=O0+np.trunc((i-1)/nn)*LL/(nam_re*np.cos(a*np.pi/180))
        if i==1:
            cikl1=np.vstack((G1,G2,G3,okr1,G4,G5,G6,Okr2))
        if i>1:
            cikl1=np.vstack((cikl1,G1,G2,G3,okr1,G4,G5,G6,Okr2))
 
            
    return cikl1


def ciklV2_dli_ugla(n,a,O0,L,LL,nn,hh0):
    obr=1
    for i in range(1,n+1):
        if i>=nn+1:
            O0=O0-np.trunc((i-1)/nn)*LL/(nam_re*np.cos(a*np.pi/180))
        G1=namotka(a,nam_re,O0,nam_toch,g.R,g.Z,g.Rz,1,g.Z0,obr,L,1,nam_dn[0],2)
        G2=namotka(a,nam_re,G1[nam_toch,3],nam_toch,g.R,g.Z,g.Rz,0,g.Z0,obr,L,0,2,nam_dn[1])
        G3=namotka(a,nam_re,G2[nam_toch,3],nam_toch,g.R,g.Z,g.Rz,1,g.Z0,obr,L,0,nam_dn[1],nam_dn[1])
        okr1=okr(G3[nam_toch,2],G3[nam_toch,5],hh0/2,G3[nam_toch,3],G3[nam_toch,4],nam_toch,G3[nam_toch,6],G3[nam_toch,7],obr,G3[nam_toch,9])
        G4=namotka(a,nam_re,2*G3[nam_toch,3]-G2[nam_toch,3]-hh0/2,nam_toch,g.R,g.Z,g.Rz,1,g.Z0,-obr,L,1,nam_dn[1],nam_dn[1])
        G5=namotka(a,nam_re,G4[nam_toch,3],nam_toch,g.R,g.Z,g.Rz,0,g.Z0,-obr,L,0,4,nam_dn[1])
        G6=namotka(a,nam_re,G5[nam_toch,3],nam_toch,g.R,g.Z,g.Rz,1,g.Z0,-obr,L,0,nam_dn[0],2)
        Okr2=okr(G6[nam_toch,2],G6[nam_toch,5],hh0/2,G6[nam_toch,3],G6[nam_toch,4],nam_toch,G6[nam_toch,6],G6[nam_toch,7],-obr,G6[nam_toch,9])
        O0=2*G6[nam_toch,3]-G5[nam_toch,3]-hh0/2
        
        if i>1:
            G1=np.delete(G1,(0), axis=0)
        if i>=nn+1:
            O0=O0+np.trunc((i-1)/nn)*LL/(nam_re*np.cos(a*np.pi/180))
        if i==1:
            cikl1=np.vstack((G1,G2,G3,okr1,G4,G5,G6,Okr2))
        if i>1:
            cikl1=np.vstack((cikl1,G1,G2,G3,okr1,G4,G5,G6,Okr2))
 
            
    return cikl1


def cikl_dli_ugla(n,a,O0,L,LL,nn,hh0):
    obr=1
    for i in range(1,n+1):
        if i>=nn+1:
            O0=O0-np.trunc((i-1)/nn)*LL/(nam_re*np.cos(a*np.pi/180))
        G1=namotka(a,nam_re,O0,nam_toch,g.R,g.Z,g.Rz,1,g.Z0,obr,L,1,nam_dn[0],2)
        G2=namotka(a,nam_re,G1[nam_toch,3],nam_toch,g.R,g.Z,g.Rz,0,g.Z0,obr,L,0,2,nam_dn[1])
        G3=namotka(a,nam_re,G2[nam_toch,3],nam_toch,g.R,g.Z,g.Rz,1,g.Z0,obr,L,0,nam_dn[1],nam_dn[1])
        okr1=okr(G3[nam_toch,2],G3[nam_toch,5],hh0,G3[nam_toch,3],G3[nam_toch,4],nam_toch,G3[nam_toch,6],G3[nam_toch,7],obr,G3[nam_toch,9])
        G4=namotka(a,nam_re,2*G3[nam_toch,3]-G2[nam_toch,3]-hh0,nam_toch,g.R,g.Z,g.Rz,1,g.Z0,-obr,L,1,nam_dn[1],nam_dn[1])
        G5=namotka(a,nam_re,G4[nam_toch,3],nam_toch,g.R,g.Z,g.Rz,0,g.Z0,-obr,L,0,4,nam_dn[1])
        G6=namotka(a,nam_re,G5[nam_toch,3],nam_toch,g.R,g.Z,g.Rz,1,g.Z0,-obr,L,0,nam_dn[0],2)
        O0=2*G6[nam_toch,3]-G5[nam_toch,3]
        
        if i>=nn+1:
            O0=O0+np.trunc((i-1)/nn)*LL/(nam_re*np.cos(a*np.pi/180))
        if i==1:
            cikl1=np.vstack((G1,G2,G3,okr1,G4,G5,G6))
        if i>1:
            cikl1=np.vstack((cikl1,G1,G2,G3,okr1,G4,G5,G6))
 
            
    return cikl1

def ugol(L,a0,re,nn):
    a1=a0*np.pi/180
    rp=re*np.sin(a1)
    yy=cikl_dli_ugla(1,a0,0,0,L,1,0)   
    Lhord=np.sqrt((yy[yy.shape[0]-1,0]-yy[0,0])**2+(yy[yy.shape[0]-1,1]-yy[0,1])**2)
    def ug():
        if yy[yy.shape[0]-1,0]-yy[0,0]<0:
            return 2*np.arcsin(Lhord/(2*rp))
        if yy[yy.shape[0]-1,0]-yy[0,0]>0:
            return 2*np.pi-2*np.arcsin(Lhord/(2*rp))
        
    ugol1=np.zeros((2,1))
    ugol1[0]=ug()+360*np.pi/(nn*180)
    ugol1[1]=ug()-360*np.pi/(nn*180)
    if nn==1:
        ugol1[0]=ug()
        ugol1[1]=ug()
        
    return ugol1

def ugolV2(L,a0,re,kol):
    i=1
    kol=20
    ugol=np.zeros((0,4))
    yy=cikl_dli_ugla(1,a0,0,0,L,2,0)
    cel=yy[yy.shape[0]-1,3]-math.trunc(yy[yy.shape[0]-1,3]/(2*np.pi))*2*np.pi
    ug0=2*np.pi+cel-yy[0,3]
    #ug0+2*np.pi/i>0 and
    while i<=kol:
        #ugol[i-1,0]=i
        if ug0+2*np.pi/i>0:
            ugol=np.append(ugol,[[i,ug0+2*np.pi/i, vitkovV2(L, a0, re, i)[0], vitkovV2(L, a0, re, i)[1]]],axis = 0)
            #ugol[i-1,1]=ug0+2*np.pi/i   
        if ug0-2*np.pi/i>0:
            ugol=np.append(ugol,[[i,ug0-2*np.pi/i, vitkovV2(L, a0, re, i)[0], vitkovV2(L, a0, re, i)[1]]],axis = 0)
            #ugol[i-1,2]=ug0-2*np.pi/i
        i+=1
    ugol = ugol[ugol[:,1].argsort()]
    '''
    i=1
    while i<=kol:
        ugol[i-1,2]=ug0-2*np.pi/i
        i+=1  
    '''
    return ugol

def vitkov(L,a0,re,nn):
    LL=L*180/(re*np.cos(a0*np.pi/180)*np.pi)
    return 360/LL

def vitkovV2(L,a0,re,nn):
    k=2*np.pi*re*np.cos(a0*np.pi/180)/(nn*L)
    kk=np.ceil(k)
    proc=100+(kk-k)*100/k
    return kk*nn, proc

def tolhinaVerh(z1,re,a0,L,t,Zr,R,f,Rline):
    R0=re*np.sin(a0*np.pi/180)
    r1=R(z1,f)
    Teq=2*t
    sR=lambda r:np.sqrt(1+(Zr(r,f))**2)
    B=L/R0
    Yeq=re/R0
    if r1>=R0 and r1<=Rline:
        h=lambda r:Teq*re*sR(r)*np.arccos(R0/r)*np.cos(a0*np.pi/180)/L
    elif r1>=Rline and r1<re:
        h=lambda r:Teq*re*sR(r)*(np.arcsin(R0*(1+B/sR(r))/r)-np.arcsin(R0/r))*np.cos(a0*np.pi/180)/L
    elif r1==re:
        h=lambda r:Teq
    return h(r1)

def tolhinaNiz(z1,re,a0,L,t,Zr,R,f,Rline):
    R0=Rline
    Rline=re*np.sin(a0*np.pi/180)
    a0=np.arcsin(R0/re)*180/np.pi
    r1=R(z1,f)
    Teq=2*t
    sR=lambda r:np.sqrt(1+(Zr(r,f))**2)
    B=L/R0
    Yeq=re/R0
    if r1>=R0 and r1<=Rline:
        h=lambda r:Teq*re*sR(r)*np.arccos(R0/r)*np.cos(a0*np.pi/180)/L
    elif r1>=Rline and r1<re:
        h=lambda r:Teq*re*sR(r)*(np.arcsin(R0*(1+B/sR(r))/r)-np.arcsin(R0/r))*np.cos(a0*np.pi/180)/L
    elif r1==re:
        h=lambda r:Teq
    return h(r1)