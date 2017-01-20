import threading,time
import RPi.GPIO as GPIO
import Gyroscope from i2c

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

def PIDControl(error,pkfl=10,pkfr=10,pkbl=10,pkbr=10):
  (forward,sideways) = error
  front_left = (forward+sideways)*pk
  front_right = (forward-sideways)*pk
  back_left = (-forward+sideways)*pk
  back_right = (forward-sideways)*pk
  return [front_left,front_right,back_left,back_right]

while True:
  pwrs = PIDControl(gyro.query())
  FL.ChangeDutyCycle(pwrs[0])
  FR.ChangeDutyCycle(pwrs[1])
  BL.ChangeDutyCycle(pwrs[2])
  BR.ChangeDutyCycle(pwrs[3])
  time.sleep(1)

#cleanup
FL.stop()
FR.stop()
BL.stop()
BR.stop()

GPIO.cleanup()
