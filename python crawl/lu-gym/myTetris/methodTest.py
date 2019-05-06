# -*- coding: utf-8 -*-
"""

@Author: lushaoxiao
@Date: 2019/5/6
@IDE: PyCharm
"""
import json

class Method(object):
    def __init__(self):
        self._startx = 0
        self._starty = 9

    def getPos(self):
        data = {
            "x":self._startx,
            "y":self._starty
        }
        return json.dumps(data)
