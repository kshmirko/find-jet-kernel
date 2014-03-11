# -*- coding: utf-8 -*-
"""
Created on Tue Mar 11 17:13:46 2014

@author: kshmirko
"""

from numpy import shape, arange, sum, meshgrid

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