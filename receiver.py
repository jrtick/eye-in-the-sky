import bluetooth
import RPi.GPIO as GPIO


#globals
FREQ = 2500000
FRONT_LEFT_PIN = 0
FRONT_RIGHT_PIN = 0
BACK_LEFT_PIN = 0
BACK_RIGHT_PIN = 0


#setup pins
GPIO.setmode(GPIO.BOARD)
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


#get connection
socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
socket.bind(("",1))
socket.listen(1)
(client,client_addr) = socket.accept() #wait for connection
print("Connected")

try:
  while True:
    msg = client.recv(1024)
    if(msg.lower()=="stop"):
      break
    else:
      try:
        pwrs = eval(msg) #msg should be "ww xx yy zz"
      except:
        pwrs = [0,0,0,0]
      FL.changeDutyCycle(pwrs[0])
      FR.changeDutyCycle(pwrs[1])
      BL.changeDutyCycle(pwrs[2])
      BR.changeDutyCycle(pwrs[3])
except:
  print("an error occurred?")


#cleanup
client.close()
socket.close()

FL.stop()
FR.stop()
BL.stop()
BR.stop()

GPIO.cleanup()
