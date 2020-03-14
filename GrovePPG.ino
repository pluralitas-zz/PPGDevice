//Seeeduino Nano + Grove Ear-clip heart rate sensor

#define LEDpin 13
#define intpin 2 //Interrupt pin; PIN2

//define global value(s)
unsigned long HRarr[20];

//define constants
const int HR_max = 300; //200 bpm
const int HR_min = 2000; //30 bpm

void setup() {
  pinMode(LEDpin,OUTPUT);
  Serial.begin(38400);
  attachInterrupt(digitalPinToInterrupt(intpin), intfunc, RISING);
}

void intfunc() {
  static int lasttime = millis();
  int currenttime = millis();
  int timediff = currenttime - lasttime;

  if ((timediff < HR_min) && (timediff > HR_max)){
    Serial.println(timediff,DEC);
    Serial.flush();
  }
  
  lasttime = millis(); 
}

void loop(){}
