#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 31 11:57:42 2018

@author: duchonic
"""

import sys
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5 import QtCore
import random

class Example(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
        self.CIRCLES = 20
        self.GAP     = 10
                       #grey           yellow         red        black
        self.COLORS  = ((138,146,141), (250,200,10), (180,0,0), (0,0,0))
        
        self.TAGS    = ( 'sport', 'learn', 'work', 'sleep' )
        
    def initUI(self):      
        
        self.text = "helloworld"

        self.setGeometry(480, 800, 800, 800)
        self.setWindowTitle('Drawing text')
        self.show()
        
        self.Xstart=10
        self.Ystart=50
        
    def paintEvent(self, event):

        qp = QPainter()
        qp.begin(self)
        qp.setPen(QColor( 0,0,0 ))
        
        for day in range(7):
            for hrs in range(24):
                color = random.choice(self.COLORS)
                
                if hrs < 6:
                    color = self.COLORS[3]
                elif hrs > 23:
                    color = slef.COLORS[3]
                #qp.setPen(QColor( color[0],color[1], color[2]  ))
                qp.setBrush( QColor( color[0],color[1], color[2] )  )
                qp.drawEllipse(self.Xstart + hrs*(self.CIRCLES+self.GAP), self.Ystart + day*(self.CIRCLES+self.GAP),self.CIRCLES,self.CIRCLES)
                
        self.drawTags(qp)
        
        

            
            
        qp.end()
        
        
    def drawTags(self, qp):
        y = 300
        for tags in self.TAGS:    
            
            color = self.COLORS[ self.TAGS.index(tags) ]
            qp.setBrush( QColor( color[0],color[1], color[2] )  )
            qp.drawEllipse(10,y ,self.CIRCLES,self.CIRCLES)
            
            qp.setPen(QColor( color[0],color[1], color[2] ))
            qp.drawText(20,y, tags)
            y += 20
                
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())