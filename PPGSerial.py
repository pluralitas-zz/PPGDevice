import serial
import serial.tools.list_ports
from numpy import mean
from PyQt5.QtCore import pyqtSignal, QThread

class Arduino(QThread):
    _heartbeat = pyqtSignal(int) # if emit 1, means heart beat, if emit between 30-200 means heart rate
    beatsArr=list() #for storing time between heart beat

    def __init__(self):
        ports = list(serial.tools.list_ports.comports()) #find all coms
        for comnum, comname, comadd in ports:  #find comport of seeeduino nano
            if "Silicon Labs CP210x USB to UART Bridge" in comname:
                self.com = serial.Serial(port=comnum,baudrate=38400,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,rtscts=True)
        try: #see if serial is connected and open
            self.com.name
        except:
            raise Exception("Please plug in the PPG device.")

    @property
    def acqhb(self): #acquire Heart beat from Seeeduino Nano
        self.com.flushInput()
        self.raw = self.com.readline()
        self.com.flushInput()
        return int(self.raw[:-2].decode())

    def acqhr(self,hb): #calculate and emit Heart Rate
        if hb > 0:
            self.beatsArr.append(hb)
        if len(self.beatsArr) == 5: #use 5 beats average for heart rate
            try:
                self._heartbeat.emit(int(60/(mean(self.beatsArr)/1000))) #emit heartrate, value 30-200
            except: 
                print(int(60/(mean(self.beatsArr)/1000)))
            self.beatsArr.clear()

    def run(self): #QThread run
        while True:
            self.hb = self.acqhb
            try:
                self._heartbeat.emit(1) #emit heartbeat, value=1
            except: pass
            self.acqhr(self.hb)
                
if __name__ == "__main__":
    ard = Arduino()
    ard.run()