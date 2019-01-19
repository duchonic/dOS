#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  6 19:20:58 2019

dOS (duchoud Operating System)
manage weekly hours with lego technic bricks

@author: duchonic

"""

import sys
import time, datetime
import threading
import json
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLayout
from PyQt5.QtWidgets import QProgressBar, QGridLayout
class App(QWidget):

    buttonList = list()
    thTest = 0
    currentTime = 0
    mPlan = dict()

    class Button():

        day = 0
        hour = 0
        btn = 0
        form = 0
        layout = 0
        actualColor = 0

        COLORS = ("grey", "red", "yellow", "black")

        def __init__(self, day, hour, form, color):

            self.day = day
            self.hour = hour
            self.form = form
            self.btn = QPushButton( str(hour), form)
            self.actualColor = color
            self.btn.setStyleSheet("background-color: " + self.COLORS[self.actualColor])
            self.btn.setToolTip(str(day*24 + hour))
            self.btn.move(10+self.hour*40, 40+day*20)

            self.btn.setFixedWidth(30)
            self.btn.setFixedHeight(15)
            self.btn.clicked.connect( self.on_click )

        def on_click(self):
            self.actualColor += 1
            if self.actualColor >= len(self.COLORS):
                self.actualColor = 0
            self.btn.setStyleSheet("background-color: " + self.COLORS[self.actualColor])
            self.form.show()

        def getColor(self):
            return self.actualColor

    def __init__(self):
        super().__init__()
        self.title = 'dOS'
        self.left = 10
        self.top = 10
        self.width = 1000
        self.height = 300
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        mTopGrid = QGridLayout()
        self.setLayout(mTopGrid)

        #button to stop thUpdate
        btnQuit = QPushButton('quit', self)
        mTopGrid.addWidget(btnQuit, 0,0)
        btnQuit.clicked.connect(self.threadStop)

        #button to start thUpdate
        btnStart = QPushButton('start', self)
        mTopGrid.addWidget(btnStart, 0,1)
        btnStart.clicked.connect(self.threadUpdate)

        #button to save plan
        buttonSave = QPushButton('save', self)
        mTopGrid.addWidget(buttonSave, 0,2)
        buttonSave.clicked.connect(self.savePlan)

        buttonLoad = QPushButton('load', self)
        mTopGrid.addWidget(buttonLoad, 0,3)
        buttonLoad.clicked.connect(self.loadPlan)


        self.progress = QProgressBar(self)
        mTopGrid.addWidget(self.progress, 1,0)
        self.progress.setGeometry(10,250,300,50)
        self.progress.setMaximum(100)



        self.work = QLabel(self)
        self.work.setText('')
        self.work.setFixedSize(300,20)
        self.work.move(10,200)

        self.currentTime = QLabel(self)
        self.currentTime.setText('')
        self.currentTime.setFixedSize(300,20)
        self.currentTime.move(10,220)

        self.countdownTime = QLabel(self)
        self.countdownTime.setText('')
        self.countdownTime.setFixedSize(300,20)
        self.countdownTime.move(10,240)

        self.thTest = threading.Timer(1, self.threadUpdate)
        self.thTest.start()

        try:
            with open('data.json','r') as readData:
                self.mPlan = json.load(readData)
        except:
                self.mPlan = dict()
                for year in range(2019,2022):
                    self.mPlan[year] = dict()

        for day in range(7):
            for hour in range(24):
                try:
                    mTime = datetime.datetime.utcnow().isocalendar()
                    color = self.mPlan[str(mTime[0])][str(mTime[1])].get(str(day*24+hour))
                except:
                    color = 0
                self.buttonList.append( self.Button(day, hour, self, color) )
        self.show()

    def showTime(self):
        now = time.localtime( )
        actItem = now.tm_wday*24  + now.tm_hour
        workStr = str('act work: ') + str(self.buttonList[actItem].getColor())

        #check if more than one block is left
        showTimeBlock = 0
        showTimeActItem = actItem

        while self.buttonList[showTimeActItem+1].getColor() == self.buttonList[showTimeActItem].getColor():
            showTimeBlock += 1
            showTimeActItem += 1

        showTimeTotal = (showTimeBlock+1) * 60
        showTimeLeft  = ((showTimeBlock*60) + 59-now.tm_min)
        currentTimeStr = str(now.tm_hour) + ':' + str(now.tm_min) + ':' + str(now.tm_sec)
        countDownStr = str(showTimeLeft) + ':' + str(59-now.tm_sec)

        self.progress.setValue( 100 -  (showTimeLeft / showTimeTotal)*100 )

        self.currentTime.setText('current time: ' + currentTimeStr)
        self.countdownTime.setText('time left: ' + countDownStr)
        self.work.setText(workStr)
        self.show()

    def threadUpdate(self):
        self.thTest = threading.Timer(1, self.threadUpdate)
        self.thTest.start()
        self.showTime()

    def threadStop(self):
        print('kill update')
        self.thTest.cancel()
        self.savePlan()
        self.show()

    def getPlan(self):
        plan = dict()
        for day in range(7):
            for hour in range(24):
                mItem = day*24+hour
                plan.update({ mItem : self.buttonList[mItem].getColor() })
        return plan

    def savePlan(self):
        mTime = datetime.datetime.utcnow().isocalendar()
        self.mPlan[str(mTime[0])][str(mTime[1])] = self.getPlan()
        with open('data.json', 'w') as wrData:
            json.dump(self.mPlan, wrData, indent=2, ensure_ascii=False)

    def loadPlan(self):
        with open('data.json') as rdData:
            storedPlan = json.load(rdData)
        print(json.dumps(storedPlan, indent=2))
        print('load plan')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
