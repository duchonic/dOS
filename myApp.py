from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel, QProgressBar, QHBoxLayout, QVBoxLayout

from myBlocks import Blocks
import threading, sys, time, datetime

import json

class App(QWidget):

    buttonList = list()
    _thUpdate = 0
    currentTime = 0
    mPlan = dict()
    _blockStrings = ["nothing", "sail", "learn", "sleep", "read"]

    def __init__(self, parent):
        super(App, self).__init__(parent)
        self.initUI()

    def initUI(self):
        #open file with data for blocks
        try:
            with open('data.json','r') as readData:
                self.mPlan = json.load(readData)
                print('read the data')
        except:
                self.mPlan = dict()
                for year in range(2019,2022):
                    self.mPlan[year] = dict()

        self.work = QLabel(self)
        self.work.setText('')
        self.work.setFixedSize(300,20)
        self.currentTime = QLabel(self)
        self.currentTime.setText('')
        self.countdownTime = QLabel(self)
        self.countdownTime.setText('')
        self.progress = QProgressBar(self)
        self.progress.setGeometry(10,250,300,50)
        self.progress.setMaximum(100)

        _vbox = QVBoxLayout()

        for day in range(7):
            _hboxTable = QHBoxLayout()
            for hour in range(24):
                try:
                    mTime = datetime.datetime.utcnow().isocalendar()
                    color = self.mPlan[str(mTime[0])][str(mTime[1])].get(str(day*24+hour))
                except:
                    color = 0
                self.buttonList.append( Blocks(day, hour, self, color, _hboxTable) )
            _vbox.addLayout(_hboxTable)

        _vbox.addWidget(self.work)
        _vbox.addWidget(self.currentTime)
        _vbox.addWidget(self.countdownTime)
        _vbox.addWidget(self.progress)

        self.setLayout(_vbox)

        self._thUpdate = threading.Timer(1, self.threadUpdate)
        self._thUpdate.start()
        #self.show()

    def calcItemPos(self, _day, _hour):
        return (_day*24)+_hour

    def showTime(self):
        _now = time.localtime()
        _actItem = self.calcItemPos(_now.tm_wday, _now.tm_hour)
        _showTimeBlockLeft = 0
        _showTimeBlockPast = 0

        #check blocks in the future
        _showTimeActItem = _actItem
        try:
            while self.buttonList[_showTimeActItem-1].getColor() \
                    == self.buttonList[_showTimeActItem].getColor():
                _showTimeBlockPast += 1
                _showTimeActItem -= 1
        except:
            pass

        #check block in the past
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
        _workStr = str('dOS activity: ') + self._blockStrings[self.buttonList[_actItem].getColor()]
        _currentTimeStr = str(_now.tm_hour).zfill(2) + ':' + str(_now.tm_min).zfill(2) + ':' + str(_now.tm_sec).zfill(2)
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

    def getPlan(self):
        _plan = dict()
        for day in range(7):
            for hour in range(24):
                mItem = self.calcItemPos(day,hour)
                _plan.update({ mItem : self.buttonList[mItem].getColor() })
        return _plan

    def exitWidget(self):
        #kill thread
        self._thUpdate.cancel()
        #save stuff
        _Time = datetime.datetime.utcnow().isocalendar()
        self.mPlan[str(_Time[0])][str(_Time[1])] = self.getPlan()
        with open('data.json', 'w') as wrData:
            print('saved plan')
            json.dump(self.mPlan, wrData, indent=2, ensure_ascii=False)
