import bluetooth
import RPi.GPIO as GPIO


#globals
FREQ = 2500
FRONT_LEFT_PIN = 2
FRONT_RIGHT_PIN = 3
BACK_LEFT_PIN = 4
BACK_RIGHT_PIN = 17


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


#get connection
print("listening for connection...")
socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
socket.bind(("",1))
socket.listen(1)
(client,client_addr) = socket.accept() #wait for connection
print("Connected")

try:
  while True:
    msg = client.recv(1024)
    print("heard",msg)
    if(msg.lower()=="stop"):
      FL.ChangeDutyCycle(0)
      FR.ChangeDutyCycle(0)
      BL.ChangeDutyCycle(0)
      BR.ChangeDutyCycle(0)
      break
    else:
      try:
        pwrs = eval(msg) #[msg should be "ww xx yy zz]"
      except:
        pwrs = [0,0,0,0]
      for i in range(4):
        if(pwrs[i]>40):
          pwrs[i]=40
        if(pwrs[i]<0):
          pwrs[i]=0
      print(pwrs)
      FL.ChangeDutyCycle(pwrs[0])
      FR.ChangeDutyCycle(pwrs[1])
      BL.ChangeDutyCycle(pwrs[2])
      BR.ChangeDutyCycle(pwrs[3])
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
