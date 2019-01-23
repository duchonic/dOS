#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  6 19:20:58 2019

dOS (duchoud Operating System)
manage weekly hours with lego technic bricks (prototype)

@author: duchonic

"""

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QAction
from PyQt5.QtWidgets import QMessageBox, QLineEdit
from PyQt5.QtGui import QIcon

from myApp import App
import sys

class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.app_widget = App(self)
        _widget = QWidget()
        _layout = QVBoxLayout(_widget)
        _layout.addWidget(self.app_widget)
        self.setCentralWidget(_widget)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('dOS')
        self.setGeometry(10,10, 1, 1)

        exitAct = QAction(QIcon('exit.png'), 'exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('exit application')
        exitAct.triggered.connect(self.close)

        statsAction = QAction('show', self)
        statsAction.setShortcut('Ctrl+S')
        statsAction.setStatusTip('show stats')
        statsAction.triggered.connect(self.showStats)

        blockAction = QAction('edit', self)
        blockAction.setShortcut('Ctrl+E')
        blockAction.setStatusTip('edit block strings')
        blockAction.triggered.connect(self.editBlocks)

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)

        statsMenu = menubar.addMenu('stats')
        blockMenu = menubar.addMenu('blocks')
        exitMenu = menubar.addMenu('exit')

        statsMenu.addAction(statsAction)
        blockMenu.addAction(blockAction)
        exitMenu.addAction(exitAct)

        self._statusbar = self.statusBar()
        self._statusbar.showMessage('running')

        #self.textbox = QLineEdit(self)
        #self.textbox.move(20, 20)
        #self.textbox.resize(280,40)

    def showStats(self):
        self._statusbar.showMessage('showStats ...')
        print(self.app_widget._planSave)

        _statString = str()

        for item in self.app_widget._planSave:
            _statString += str(item) + '\n'

            for entry in self.app_widget._planSave[item]:
                _statString += '-' + str(entry) + ':' + str(self.app_widget._planSave[item][entry]) + '\n'
        QMessageBox.about(self, "Stats",  _statString )

    def editBlocks(self):
        # textboxValue = self.textbox.text()
        # QMessageBox.question(self, 'Message - pythonspot.com', "You typed: " + textboxValue, QMessageBox.Ok, QMessageBox.Ok)
        # self.textbox.setText("")
        # QMessageBox.question(self, 'Message - pythonspot.com', "You typed: " + textboxValue, QMessageBox.Ok, QMessageBox.Ok)

        _editBlocks = str()
        self.app_widget._blockStrings[0] = "blub"
        for item in self.app_widget._blockStrings:
            _editBlocks += str(item) + '\n'
        QMessageBox.about(self, "Blocks",  _editBlocks )

    def closeEvent(self, event):
        print('closed with red cross')
        self.app_widget.exitWidget()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
