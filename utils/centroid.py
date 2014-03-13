# -*- coding: utf-8 -*-
"""
Created on Tue Mar 11 17:13:46 2014

@author: kshmirko
"""

from numpy import sum, meshgrid, where, floor, round
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

    for ilat in range(len(alat)):
        x = fmin(f, (3,ilat), args=(data,))
        la = round(x[1])
        le = round(x[0])
        mins.append((la,le))
    print mins
    return 0, 1