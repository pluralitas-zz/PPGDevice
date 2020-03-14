import serial
import serial.tools.list_ports
from numpy import mean
from PyQt5.QtCore import pyqtSignal, QThread

class Arduino(QThread):
    _heartbeat = pyqtSignal(int)
    _heartrate = pyqtSignal(int)

    comports=list()
    comnames=list()
    beatsArr = list()

    def __init__(self):
        ports = serial.tools.list_ports.comports() #find all coms
        for p in ports: 
            self.comports.append(p[0])
            self.comnames.append(p[1])

        for i in range(len(self.comnames)):
            if "Silicon Labs CP210x USB to UART Bridge" in self.comnames[i]:
                self.comport = self.comports[i]
        
        if self.comport != []:
            self.com = serial.Serial(port=self.comport,baudrate=38400,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,rtscts=True)
        else:
            raise Exception("Please plug in the PPG device")

    @property
    def acqhb(self): #acquire Heartbeat from Seeeduino Nano
        self.com.flushInput()
        self.raw = self.com.readline()
        self.com.flushInput()
        self.heartbeat = int(self.raw[:-2].decode())
        return self.heartbeat

    def acqhr(self,hb):
        if hb > 0:
            self.beatsArr.append(hb)
        if len(self.beatsArr) == 5: #use 5 beats average for heart rate
            self.timemean = int(60/(mean(self.beatsArr)/1000))
            try:
                self._heartrate.emit(self.timemean) #emit heartrate
            except: 
                print(self.timemean)
            self.beatsArr.clear()
        else:
            return 

    def run(self):
        while True:
            self.hb = self.acqhb
            try:
                self._heartbeat.emit(1) #emit heartbeat
            except: pass
            self.heartrate = self.acqhr(self.hb)
                
if __name__ == "__main__":
    ard = Arduino()
    ard.run()