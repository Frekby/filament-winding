# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 11:20:29 2020

@author: Admin
"""
import numpy as np
from glumpy import gloo

def point(gg,gg1):
    p=np.row_stack((gg[0],gg1[0]))
    f=np.array([0,1,2],dtype=np.uint32)
    l=np.array([0,2],dtype=np.uint32)
    off=np.array([0,0],dtype=np.uint32)
    for i in range(1,gg.shape[0]):
        p=np.row_stack((p,gg[i],gg1[i]))
        off=np.hstack((off,[i/(gg.shape[0]*1-1),i/(gg.shape[0]*1-1)]))
    for i in range(1,2*gg.shape[0]-2):
        f1=np.array([i,i+1,i+2],dtype=np.uint32)
        l1=np.array([i,i+2],dtype=np.uint32)
        f=np.hstack((f,f1))
        l=np.hstack((l,l1))
    p=np.column_stack((p[:,0], p[:,1], p[:,2]))
    return p,f,l,off

def pointV2(gg,gg1):
    p=np.row_stack((gg[0],gg1[0]))
    f=np.array([0,2,1],dtype=np.uint32)
    l=np.array([0,2],dtype=np.uint32)
    off=np.array([0,0],dtype=np.uint32)
    ris=np.array([0,0],dtype=np.uint32)
    for i in range(1,gg.shape[0]):
        p=np.row_stack((p,gg[i],gg1[i]))
        off=np.hstack((off,[i/(gg.shape[0]*1-1),i/(gg.shape[0]*1-1)]))
        ris=np.hstack((ris,[0,0]))
    for i in range(1,2*gg.shape[0]-2):
        if i % 2:
            f1=np.array([i,i+1,i+2],dtype=np.uint32)
        else:
            f1=np.array([i,i+2,i+1],dtype=np.uint32)
        l1=np.array([i,i+2],dtype=np.uint32)
        f=np.hstack((f,f1))
        l=np.hstack((l,l1))
    p=np.column_stack((p[:,0], p[:,1], p[:,2]))
    return p,f,l,off,ris

def surface(func, umin=0, umax=np.pi, ucount=128,
                  vmin=0, vmax=np.pi, vcount=128,f=1):
    vtype = [('position', np.float32, 3)]
    itype = np.uint32
    vcount += 1
    ucount += 1
    n = vcount*ucount
    Un = np.repeat(np.linspace(0, 1, ucount, endpoint=True), vcount)
    Vn = np.tile  (np.linspace(0, 1, vcount, endpoint=True), ucount)
    U = umin+Un*(umax-umin)
    V = vmin+Vn*(vmax-vmin)
    vertices = np.zeros(n, dtype=vtype)
    for i,(u,v) in enumerate(zip(U,V)):
        x,y,z = func(u,v,f)
        vertices["position"][i] = x,y,z
    indices = []
    for i in range(ucount-1):
        for j in range(vcount-1):
            indices.append(i*(vcount) + j        )
            indices.append(i*(vcount) + j+1      )
            indices.append(i*(vcount) + j+vcount+1)
            indices.append(i*(vcount) + j+vcount+1  )
            indices.append(i*(vcount) + j+vcount+0)
            indices.append(i*(vcount) + j        )
    indices = np.array(indices, dtype=itype)
    return vertices.view(gloo.VertexBuffer), indices.view(gloo.IndexBuffer), vertices, indices