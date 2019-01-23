from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel, QProgressBar, QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QCheckBox, QGroupBox, QRadioButton
from myBlocks import Blocks
import threading, sys, time, datetime
from collections import Counter

import json

class App(QWidget):

    buttonList = list()
    _thUpdate = 0
    currentTime = 0
    _planLoad = dict()
    _planSave = Counter()
    _DAYOFWEEK = ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday")

    def __init__(self, parent):
        super(App, self).__init__(parent)
        self.initUI()

    def initUI(self):
        #open file with data for blocks
        try:
            with open('dataLoad.json','r') as readData:
                self._planLoad = json.load(readData)
                print('read the dataLoad')
        except:
            self._planLoad = dict()
            self._planLoad[ str(datetime.datetime.utcnow().isocalendar()[0]) ] = dict()

        #open file with saved data
        try:
            with open('dataSave.json','r') as readData:
                self._planSave = json.load(readData)
                print('read the dataSave')
        except:
            self._planSave = dict()
            self._planSave[ str(datetime.datetime.utcnow().isocalendar()[0]) ]  = dict()

        #open file with blockStrings
        try:
            with open('blockStrings.json', 'r') as readData:
                self._blockStrings = json.load(readData)
                print('read the blockStrings')
        except:
            self._blockStrings = dict()
            self._blockStrings.update({'0':'nothing', '1':'learn', '2':'read', '3':'work', '4':'sail', '5':'play'})

        print(self._planSave)

        self.work = QLabel(self)
        self.work.setText('')
        self.work.setFixedSize(300,20)
        self.currentTime = QLabel(self)
        self.currentTime.setText('')
        self.countdownTime = QLabel(self)
        self.dayofweek = [QLabel(self) for i in range(7)]
        self.countdownTime.setText('')
        self.progress = QProgressBar(self)
        self.progress.setGeometry(10,250,300,50)
        self.progress.setMaximum(100)

        self.groupBox = QGroupBox("Check")

        self.b1 = QRadioButton("CheckIn")
        self.b2 = QRadioButton("CheckOut")
        self.b1.setChecked(False)
        self.b2.setChecked(True)

        _vbox = QVBoxLayout()

        _vbox.addWidget(self.b1)
        _vbox.addWidget(self.b2)

        for day in range(7):
            _hboxTable = QHBoxLayout()
            for hour in range(24):
                try:
                    mTime = datetime.datetime.utcnow().isocalendar()
                    color = self._planLoad[str(mTime[0])][str(mTime[1])].get(str(day*24+hour))
                except:
                    color = 0
                self.buttonList.append( Blocks(day, hour, self, color, _hboxTable) )
            self.dayofweek[day].setText(self._DAYOFWEEK[day])
            _hboxTable.addWidget(self.dayofweek[day])

            _vbox.addLayout(_hboxTable)

        _vbox.addWidget(self.currentTime)
        _vbox.addWidget(self.work)
        _vbox.addWidget(self.countdownTime)
        _vbox.addWidget(self.progress)

        self.setLayout(_vbox)

        self._thUpdate = threading.Timer(1, self.threadUpdate)
        self._thUpdate.start()

    def btnstate(self, b):
        if b.text() == "CheckIn":
            if b.isChecked() == True:
                print(b.text() + "is selected")
        if b.text() == "CheckOut":
            if b.isChecked() == True:
                print(b.text() + "is selected")

    def calcItemPos(self, _day, _hour):
        return (_day*24)+_hour

    def showTime(self, full):
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
        _workStr = str('dOS activity: ') + self._blockStrings[ self.buttonList[_actItem].getColorStr() ]
        _currentTimeStr = str(_now.tm_hour).zfill(2) + ':' + str(_now.tm_min).zfill(2) + ':' + str(_now.tm_sec).zfill(2)
        _countDownStr = str(_showTimeLeft).zfill(2) + ':' + str(59-_now.tm_sec).zfill(2)

        if full:
            self.progress.setValue(100-(_showTimeLeft/_showTimeTotal)*100)
            self.work.setText(_workStr)
            self.currentTime.setText('current time: ' + _currentTimeStr)
            self.countdownTime.setText('time left: ' + _countDownStr)
        else:
            self.progress.setValue(0)
            self.work.setText("")
            self.currentTime.setText('current time: ' + _currentTimeStr)
            self.countdownTime.setText("")

    def calcSeconds(self):
        _now = time.localtime()
        _actItem = self.calcItemPos(_now.tm_wday, _now.tm_hour)
        _Time = datetime.datetime.utcnow().isocalendar()

        try:
            self._planSave[str(_Time[0])][ self._blockStrings[ self.buttonList[_actItem].getColorStr()] ] += 1
        except:
            self._planSave[str(_Time[0])][ self._blockStrings[ self.buttonList[_actItem].getColorStr()] ] = 0

    def getSeconds(self):
        _now = time.localtime()
        _actItem = self.calcItemPos(_now.tm_wday, _now.tm_hour)
        _Time = datetime.datetime.utcnow().isocalendar()

        try:
            return self._planSave[str(_Time[0])][ self._blockStrings[ self.buttonList[_actItem].getColorStr()] ]
        except:
            self._planSave[str(_Time[0])][ self._blockStrings[ self.buttonList[_actItem].getColorStr()] ] = 0
            return self._planSave[str(_Time[0])][ self._blockStrings[ self.buttonList[_actItem].getColorStr()] ]

    def threadUpdate(self):
        self._thUpdate = threading.Timer(1, self.threadUpdate)
        self._thUpdate.start()

        if self.b1.isChecked():
            self.calcSeconds()
            self.showTime(1)
        else:
            self.showTime(0)

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
        self._planLoad[str(_Time[0])][str(_Time[1])] = self.getPlan()
        with open('dataLoad.json', 'w') as wrData:
            print('saved dataLoad')
            json.dump(self._planLoad, wrData, indent=2, ensure_ascii=False)
        #self._planSave[str(_Time[0])] = self.getHours()
        with open('dataSave.json', 'w') as wrData:
            print('saved dataSave')
            json.dump(self._planSave, wrData, indent=2, ensure_ascii=False)
        with open('blockStrings.json', 'w') as wrData:
            print('saved blockStrings')
            json.dump(self._blockStrings, wrData, indent=2, ensure_ascii=False)
