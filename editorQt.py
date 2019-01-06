#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  6 19:20:58 2019

dOS (duchoud Operating System)
manage weekly hours with lego technic bricks

@author: duchonic
"""

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
 
class App(QWidget):
 
    buttonList = list()
    
    class Button():
    
        day = 0
        hour = 0
        btn = 0
        form = 0
        layout = 0
        actualColor = 0
        
        color = ("grey","red","yellow","black")
        
        def __init__(self, day, hour, form):
            
            self.day = day
            self.hour = hour
            self.form = form
            self.btn = QPushButton( str(hour), form) 
            
            # default settings ...
            if hour < 6 or hour > 22: #sleep
                self.actualColor = 3
            if day < 5 and hour >= 8 and hour < 12:  #work morning
                self.actualColor = 1
            if day < 5 and hour >= 13 and hour < 17: #work evening
                self.actualColor = 1
                
            self.btn.setStyleSheet("background-color: " + self.color[self.actualColor])
            self.btn.setToolTip('blubi')
            self.btn.move(10+self.hour*40, 10+day*20)
            self.btn.setFixedWidth(30)
            self.btn.setFixedHeight(15)
            self.btn.clicked.connect( self.on_click )
              
        def on_click(self):
            self.actualColor += 1
            self.btn.setStyleSheet("background-color: " + self.color[self.actualColor%4])
            self.form.show()
    
    def __init__(self):
        super().__init__()
        self.title = 'dOS'
        self.left = 10
        self.top = 10
        self.width = 1000
        self.height = 200
        self.initUI()
             
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)                  
        for day in range(7):
            for hour in range(24):
                self.buttonList.append( self.Button(day, hour, self) )            
        self.show()    
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
