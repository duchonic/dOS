#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  6 13:02:10 2019

@author: duchonic
"""

class Block:
    COLORS  = ((138,146,141), (250,200,10), (180,0,0), (0,0,0))
    col = 0
    size = 0


    def __init__(self, col, size):

        self.col = col
        self.size = size


    def colorOfBlock(self):
        return self.COLORS[self.col]

    def sizeOfBlock(self):
        return self.size
