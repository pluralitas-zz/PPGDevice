# PPG Device using Arduino + PyQt5 GUI 

## Hardware
* Seeeduino Nano
http://wiki.seeedstudio.com/Seeeduino-Nano/
* Grove - Ear-clip Heart Rate Sensor http://wiki.seeedstudio.com/Grove-Ear-clip_Heart_Rate_Sensor/

## Software
* Arduino code outputs time between each heartbeat to COM serial at 38400 baud
* QThread pyserial backend to read and calculate Heart Rate
* PyQt5 used for GUI front-end using pyqtSignal slots