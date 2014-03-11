# -*- coding: utf-8 -*-
"""
Created on Tue Mar 11 16:30:07 2014

@author: kshmirko
"""

from numpy import log


def getAlt(P, P0):
    """
    Alt = getAlt(P, P0)

    Возвращает высоту для указанной изобарической поверхности.

    `P`  - уровни давления
    `P0` - давление на уровне земли
    """
    return 7988.28*log(P0/P)
