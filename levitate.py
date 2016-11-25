import threading,time
import RPi.GPIO as GPIO
from i2c import Gyroscope

#globals
FREQ = 2500
FRONT_LEFT_PIN = 19
FRONT_RIGHT_PIN = 8
BACK_LEFT_PIN = 5
BACK_RIGHT_PIN = 24

#setup pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(FRONT_LEFT_PIN,GPIO.OUT)
GPIO.setup(FRONT_RIGHT_PIN,GPIO.OUT)
GPIO.setup(BACK_LEFT_PIN,GPIO.OUT)
GPIO.setup(BACK_RIGHT_PIN,GPIO.OUT)

FL = GPIO.PWM(FRONT_LEFT_PIN,FREQ)
FR = GPIO.PWM(FRONT_RIGHT_PIN,FREQ)
BL = GPIO.PWM(BACK_LEFT_PIN,FREQ)
BR = GPIO.PWM(BACK_RIGHT_PIN,FREQ)

FL.start(0)
FR.start(0)
BL.start(0)
BR.start(0)

#setup gyroscope
gyro = Gyroscope()
gyro.listen_background()

def fix(val,low,high):
  if(val<low):
    return low
  elif(val>high):
    return high
  else:
    return val

def PIDControl(error,pkfl=0.65,pkfr=0.4,pkbl=0.65,pkbr=0.4):
  (forward,sideways) = error
  front_left = (forward+sideways)*pkfl
  front_right = (forward-sideways)*pkfr
  back_left = (-forward+sideways)*pkbl
  back_right = (-forward-sideways)*pkbr
  return [fix(front_left,32,50),fix(front_right,15,50),fix(back_left,32,50),fix(back_right,15,50)]

while True:
  error = gyro.query()
  pwrs = PIDControl(error)
  print("error: (%2.2f,%2.2f)" % (error[0],error[1]))
  print("suggest: [%2.2f,%2.2f,%2.2f,%2.2f]" % (pwrs[0],pwrs[1],pwrs[2],pwrs[3]))
  FL.ChangeDutyCycle(pwrs[0])
  FR.ChangeDutyCycle(pwrs[1])
  BL.ChangeDutyCycle(pwrs[2])
  BR.ChangeDutyCycle(pwrs[3])
  time.sleep(0.1)

#cleanup
FL.stop()
FR.stop()
BL.stop()
BR.stop()

GPIO.cleanup()
