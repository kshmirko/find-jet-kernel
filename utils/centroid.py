# -*- coding: utf-8 -*-
"""
Created on Tue Mar 11 17:13:46 2014

@author: kshmirko
"""

from numpy import sum, meshgrid, where, floor, round, linspace, arange, array
from scipy.cluster.vq import kmeans2, whiten

from scipy.optimize import fmin

def centroid(alat, alev, data):
    """
    cx, cy = centroud(alat, alev, data)

    возвращает цетр масс выделенного объекта

    `cx` - х координата
    `cy` - y координата
    """

    X,Y = meshgrid(alat,alev)

    cx = sum(X*data)/sum(data)
    cy = sum(Y*data)/sum(data)

    return cx,cy

def centroidmax(alat, alev, data):
    """
    cx, cy = centroidmax(alat, alev, data)

    возвращает положение глобального максимума объекта

    `cx` - х координата
    `cy` - y координата
    """
    row, col = where(data==data.max())
    cx = alat[col]
    cy = alev[row]

    return cx, cy

def centroidmin(alat, alev, data):
    """
    """

    def f(x,data):
        r, c = x
        r = round(r)
        c = round(c)
        return -data[r,c]

    mins=[]

    for ilat in range(len(alat[2:-2])):
        x = fmin(f, (3,ilat), args=(data,))
        la = round(x[1])
        le = round(x[0])
        mins.append((la,le))
    print mins
    return 0, 1

def findmax(alat, alev, fuwnd):

    X = []
    V = []
    N=30
    alat = linspace(30,60,N)
    LAT, LEV, V = arange(N), arange(N), arange(N)
    for ilat in range(N):

        x,v,a1,a2,a3 = fmin(lambda x: 20-fuwnd(x[0],x[1]), (alat[ilat], 10000.0),
                        args=(), disp=0, full_output=1)
        LAT[ilat] = x[0]
        LEV[ilat] = x[1]
        V[ilat] = 20-v

    idx = (LAT>30) & (LAT<60)
    LAT=LAT[idx]
    LEV = LEV[idx]
    V = V[idx]
    data = whiten(zip(LAT,LEV))
    a,b = kmeans2(data, 2)
    b=b.astype('bool')
    print a

    lat = [LAT[b].mean(),LAT[~b].mean()]
    lev = [LEV[b].mean(),LEV[~b].mean()]
    v = [V[b].mean(),V[~b].mean()]
    return lat, lev, v

