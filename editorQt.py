#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  6 19:20:58 2019

dOS (duchoud Operating System)
manage weekly hours with lego technic bricks (prototype)

@author: duchonic

"""

import sys
import time, datetime
import threading
import json
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLayout
from PyQt5.QtWidgets import QProgressBar, QHBoxLayout, QVBoxLayout
class App(QWidget):

    buttonList = list()
    _thUpdate = 0
    currentTime = 0
    mPlan = dict()

    _WORKSTRINGS = ("nothing", "paid work", "learn", "sleep")

    class Button():

        day = 0
        hour = 0
        btn = 0
        form = 0
        layout = 0
        actualColor = 0

        COLORS = ("grey", "red", "yellow", "black")

        def __init__(self, day, hour, form, color, hboxTable):

            self.day = day
            self.hour = hour
            self.form = form
            self.btn = QPushButton( str(hour), form)
            if color < len(self.COLORS):
                self.actualColor = color
            else:
                self.actualColor = 0
            self.btn.setStyleSheet("color: pink; background-color: " + self.COLORS[self.actualColor])
            self.btn.setToolTip(str(day*24 + hour))
            hboxTable.addWidget(self.btn)
            self.btn.setFixedWidth(30)
            self.btn.clicked.connect( self.on_click )

        def on_click(self):
            self.actualColor += 1
            if self.actualColor >= len(self.COLORS):
                self.actualColor = 0
            self.btn.setStyleSheet("color: pink; background-color: " + self.COLORS[self.actualColor])
            self.form.show()

        def getColor(self):
            return self.actualColor

    def __init__(self):
        super().__init__()
        self.title = 'dOS'
        self.left = 10
        self.top = 10
        self.width = 1
        self.height = 1
        self.initUI()

    def initUI(self):

        try:
            with open('data.json','r') as readData:
                self.mPlan = json.load(readData)
                print('read the data')
        except:
                self.mPlan = dict()
                for year in range(2019,2022):
                    self.mPlan[year] = dict()

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # self.buttonQuit = QPushButton('quit', self)
        # self.buttonStart = QPushButton('start', self)
        # self.buttonSave = QPushButton('save', self)
        # self.buttonLoad = QPushButton('load', self)

        self.work = QLabel(self)
        self.work.setText('')
        self.work.setFixedSize(300,20)

        self.currentTime = QLabel(self)
        self.currentTime.setText('')

        self.countdownTime = QLabel(self)
        self.countdownTime.setText('')

        # self.buttonQuit.clicked.connect(self.threadStop)
        # self.buttonStart.clicked.connect(self.threadUpdate)
        # self.buttonSave.clicked.connect(self.savePlan)
        # self.buttonLoad.clicked.connect(self.loadPlan)

        self.progress = QProgressBar(self)
        self.progress.setGeometry(10,250,300,50)
        self.progress.setMaximum(100)


        _vbox = QVBoxLayout()
        # _hboxTop = QHBoxLayout()
        #
        # _hboxTop.addWidget(self.buttonQuit)
        # _hboxTop.addWidget(self.buttonStart)
        # _hboxTop.addWidget(self.buttonSave)
        # _hboxTop.addWidget(self.buttonLoad)
        # _vbox.addLayout(_hboxTop)

        for day in range(7):
            _hboxTable = QHBoxLayout()
            for hour in range(24):
                try:
                    mTime = datetime.datetime.utcnow().isocalendar()
                    color = self.mPlan[str(mTime[0])][str(mTime[1])].get(str(day*24+hour))
                except:
                    color = 0
                self.buttonList.append( self.Button(day, hour, self, color, _hboxTable) )
            _vbox.addLayout(_hboxTable)

        _vbox.addWidget(self.work)
        _vbox.addWidget(self.currentTime)
        _vbox.addWidget(self.countdownTime)
        _vbox.addWidget(self.progress)

        self.setLayout(_vbox)

        self._thUpdate = threading.Timer(1, self.threadUpdate)
        self._thUpdate.start()

        self.show()

    def closeEvent(self, event):
        print('closed with red cross')
        self._thUpdate.cancel()
        self.savePlan()

    def calcItemPos(self, _day, _hour):
        return (_day*24)+_hour

    def showTime(self):

        _now = time.localtime()
        _actItem = self.calcItemPos(_now.tm_wday, _now.tm_hour)
        _showTimeBlockLeft = 0
        _showTimeBlockPast = 0

        _showTimeActItem = _actItem
        try:
            while self.buttonList[_showTimeActItem-1].getColor() \
                    == self.buttonList[_showTimeActItem].getColor():
                _showTimeBlockPast += 1
                _showTimeActItem -= 1
        except:
            pass

        _showTimeActItem = _actItem
        try:
            while self.buttonList[_showTimeActItem+1].getColor() \
                    == self.buttonList[_showTimeActItem].getColor():
                _showTimeBlockLeft += 1
                _showTimeActItem += 1
        except:
            pass

        _showTimeTotal = (_showTimeBlockLeft+1 + _showTimeBlockPast)*60
        _showTimeLeft  = ((_showTimeBlockLeft*60) + 59-_now.tm_min)

        _workStr = str('dOS activity: ') + self._WORKSTRINGS[self.buttonList[_actItem].getColor()]
        _currentTimeStr = str(_now.tm_hour).zfill(2) + ':' \
                            + str(_now.tm_min).zfill(2) + ':' + str(_now.tm_sec).zfill(2)
        _countDownStr = str(_showTimeLeft).zfill(2) + ':' + str(59-_now.tm_sec).zfill(2)

        self.progress.setValue(100-(_showTimeLeft/_showTimeTotal)*100)
        self.work.setText(_workStr)
        self.currentTime.setText('current time: ' + _currentTimeStr)
        self.countdownTime.setText('time left: ' + _countDownStr)
        self.show()

    def threadUpdate(self):
        self._thUpdate = threading.Timer(1, self.threadUpdate)
        self._thUpdate.start()
        self.showTime()

    # def threadStop(self):
    #     print('kill update')
    #     self.thTest.cancel()
    #     self.savePlan()
    #     self.show()

    def getPlan(self):
        _plan = dict()
        for day in range(7):
            for hour in range(24):
                mItem = self.calcItemPos(day,hour)
                _plan.update({ mItem : self.buttonList[mItem].getColor() })
        return _plan

    def savePlan(self):
        _Time = datetime.datetime.utcnow().isocalendar()
        self.mPlan[str(_Time[0])][str(_Time[1])] = self.getPlan()
        with open('data.json', 'w') as wrData:
            print('saved plan')
            json.dump(self.mPlan, wrData, indent=2, ensure_ascii=False)
    #
    # def loadPlan(self):
    #     with open('data.json') as rdData:
    #         storedPlan = json.load(rdData)
    #     print(json.dumps(storedPlan, indent=2))
    #     print('load plan')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
