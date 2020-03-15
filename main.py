# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PPGUI.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!
import serial, serial.tools.list_ports
from numpy import mean
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal, QThread
from PyQt5.QtTest import QTest

## PyQt5 FrontEnd
class Ui_MainWindow(QtWidgets.QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.setupUi(self) #Setup UI Stuff

        self.BackEndArd = Arduino() #Init Backend
        self.BackEndArd._heartbeat.connect(self.dispval) #Connect Display
        self.BackEndArd.findport()
        self.BackEndArd.start()
    
    def dispval(self,data): #display PPG value
        if data == 1:
            self.HeartLab.show()
            QTest.qWait(500)
            self.HeartLab.hide()
        elif data == 0:
            self.BPMVal.setText("--")
        else:
            self.BPMVal.setText(str(data))

    def BGColour(self, MainWindow,text): #Change background colour
        MainWindow.setStyleSheet(text)

    def fontColour(self,text): #Change font colour
        self.BPMVal.setStyleSheet(text)
        self.HeartLab.setStyleSheet(text)

#Setup UI Stuff    
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(160, 120)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setStyleSheet("background-color: rgb(255, 255, 255);")

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.HeartLab = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.HeartLab.sizePolicy().hasHeightForWidth())
        self.HeartLab.setSizePolicy(sizePolicy)
        self.HeartLab.setMinimumSize(QtCore.QSize(50, 0))

        #Setup font
        font = QtGui.QFont()
        font.setPointSize(48)
        font.setWeight(50)

        #Setup HeartBeat Display
        self.HeartLab.setFont(font)
        self.HeartLab.setTextFormat(QtCore.Qt.RichText)
        self.HeartLab.setScaledContents(True)
        self.HeartLab.setAlignment(QtCore.Qt.AlignCenter)
        self.HeartLab.setObjectName("HeartLab")
        self.horizontalLayout.addWidget(self.HeartLab)
        self.HeartLab.hide()

        #Setup BPM Value Display
        self.BPMVal = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.BPMVal.sizePolicy().hasHeightForWidth())
        self.BPMVal.setSizePolicy(sizePolicy)
        self.BPMVal.setFont(font)
        self.BPMVal.setTextFormat(QtCore.Qt.RichText)
        self.BPMVal.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        self.BPMVal.setWordWrap(False)
        self.BPMVal.setObjectName("BPMVal")
        self.horizontalLayout.addWidget(self.BPMVal)

        MainWindow.setCentralWidget(self.centralwidget)

        #Setup Menu Bar
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 259, 21))
        self.menubar.setObjectName("menubar")
        self.menuBG_Colour = QtWidgets.QMenu(self.menubar)
        self.menuBG_Colour.setObjectName("menuBG_Colour")
        self.menuText_Colour = QtWidgets.QMenu(self.menubar)
        self.menuText_Colour.setObjectName("menuText_Colour")
        MainWindow.setMenuBar(self.menubar)

        #Setup Menu Bar Actions - B/G Colour
        self.actBGWhite = QtWidgets.QAction(MainWindow)
        self.actBGWhite.setObjectName("actBGWhite")
        self.actBGGreen = QtWidgets.QAction(MainWindow)
        self.actBGGreen.setObjectName("actBGGreen")
        self.actBGPink = QtWidgets.QAction(MainWindow)
        self.actBGPink.setObjectName("actBGPink")
        self.actBGBlack = QtWidgets.QAction(MainWindow)
        self.actBGBlack.setObjectName("actBGRed")
        self.menuBG_Colour.addAction(self.actBGWhite)
        self.menuBG_Colour.addAction(self.actBGGreen)
        self.menuBG_Colour.addAction(self.actBGPink)
        self.menuBG_Colour.addAction(self.actBGBlack)

        #Setup Menu Bar - Text Colour
        self.actTextBlack = QtWidgets.QAction(MainWindow)
        self.actTextBlack.setObjectName("actTextBlack")
        self.actTextWhite = QtWidgets.QAction(MainWindow)
        self.actTextWhite.setObjectName("actTextWhite")
        self.actTextRed = QtWidgets.QAction(MainWindow)
        self.actTextRed.setObjectName("self.actTextRed")
        self.menuText_Colour.addAction(self.actTextBlack)
        self.menuText_Colour.addAction(self.actTextWhite)
        self.menuText_Colour.addAction(self.actTextRed)

        self.menubar.addAction(self.menuText_Colour.menuAction())
        self.menubar.addAction(self.menuBG_Colour.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        #Setup Menu Bar connections
        self.actBGWhite.triggered.connect(lambda: self.BGColour(MainWindow,"background-color: rgb(255, 255, 255);"))
        self.actBGGreen.triggered.connect(lambda: self.BGColour(MainWindow,"background-color: rgb(0, 155, 0);"))
        self.actBGPink.triggered.connect(lambda: self.BGColour(MainWindow,"background-color: rgb(255, 100, 100);"))
        self.actBGBlack.triggered.connect(lambda: self.BGColour(MainWindow,"background-color: rgb(0, 0, 0);"))

        self.actTextBlack.triggered.connect(lambda: self.fontColour("color: rgb(0, 0, 0); "))
        self.actTextWhite.triggered.connect(lambda: self.fontColour("color: rgb(255, 255, 255); "))
        self.actTextRed.triggered.connect(lambda: self.fontColour("color: rgb(155, 0, 0); "))
    
# Set Default Text
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Heart Rate Viewer"))
        self.HeartLab.setText(_translate("MainWindow", "♥"))
        self.BPMVal.setText(_translate("MainWindow", "--"))
        self.menuBG_Colour.setTitle(_translate("MainWindow", "B/G Colour"))
        self.menuText_Colour.setTitle(_translate("MainWindow", "Text Colour"))
        self.actBGWhite.setText(_translate("MainWindow", "White"))
        self.actBGGreen.setText(_translate("MainWindow", "Green"))
        self.actBGPink.setText(_translate("MainWindow", "Pink"))
        self.actBGBlack.setText(_translate("MainWindow", "Black"))
        self.actTextBlack.setText(_translate("MainWindow", "Black"))
        self.actTextWhite.setText(_translate("MainWindow", "White"))
        self.actTextRed.setText(_translate("MainWindow", "Red"))
        self.fontColour("color: rgb(155, 0, 0); ")

## BackEnd
class Arduino(QtCore.QThread):
    _heartbeat = QtCore.pyqtSignal(int) # if emit 1, means heart beat, if emit between 30-200 means heart rate
    beatsArr=list() #for storing time between heart beat

    def findport(self):
        ports = list(serial.tools.list_ports.comports()) #find all coms
        for comnum, comname, comadd in ports:  #find comport of seeeduino nano
            if "Silicon Labs CP210x USB to UART Bridge" in comname:
                self.com = serial.Serial(port=comnum,baudrate=38400,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,rtscts=True)

    @property
    def acqhb(self): #acquire Heart beat from Seeeduino Nano
        self.com.flushInput()
        self.raw = self.com.readline()
        self.com.flushInput()
        return int(self.raw[:-2].decode())

    def acqhr(self,hb): #calculate and emit Heart Rate
        if hb == 0: #check if arduino emit value=0 representing idle
            self._heartbeat.emit(0)
        else:
            self.beatsArr.append(hb)
            if len(self.beatsArr) == 3: #use 5 beats average for heart rate
                try:
                    self._heartbeat.emit(int(60/(mean(self.beatsArr)/1000))) #emit heartrate, value 30-200
                except: 
                    print(int(60/(mean(self.beatsArr)/1000)))
                self.beatsArr.clear()
            else: pass

    def run(self): #QThread run
        while True:
            self.hb = self.acqhb
            if self.hb > 0:
                try:
                    self._heartbeat.emit(1) #emit heartbeat, value=1
                except: pass
            
            self.acqhr(self.hb)

if __name__ == "__main__":
    ## Run GUI + Backend ##
    import sys
    app = QtWidgets.QApplication(sys.argv)

    ui = Ui_MainWindow()
    ui.show()

    sys.exit(app.exec_())

    ## Run Backend only ##
    # ard = Arduino()
    # ard.findport()
    # ard.run()
