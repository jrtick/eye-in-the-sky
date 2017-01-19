import bluetooth,threading
import RPi.GPIO as GPIO


#globals
FREQ = 2500
FRONT_LEFT_PIN = 2
FRONT_RIGHT_PIN = 3
BACK_LEFT_PIN = 4
BACK_RIGHT_PIN = 17
msg = ""
stoplistening = False
client = None

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

def update_command():
  global client,msg,stoplistening
  while True:
    if(not stoplistening):
      curmsg=client.recv(1024) #blocks until message found
      msg = curmsg #updates global message that pi sees

#bg thread will keep track of client's messages and keep pi updated
thread = threading.Thread(target=update_command)
thread.daemon = True
thread.start()

try:
  while True:
    if(msg.lower()=="stop"): #fall. fall hard.
      FL.ChangeDutyCycle(0)
      FR.ChangeDutyCycle(0)
      BL.ChangeDutyCycle(0)
      BR.ChangeDutyCycle(0)
      break
    else:
      try:
        pwrs = eval(msg) #msg should be "[ww xx yy zz]"
      except:
        print("couldn't evalute message")
        pwrs = [0,0,0,0]
      FL.ChangeDutyCycle(pwrs[0])
      FR.ChangeDutyCycle(pwrs[1])
      BL.ChangeDutyCycle(pwrs[2])
      BR.ChangeDutyCycle(pwrs[3])
except: #also will fall hard.
  print("an error occurred?")


#cleanup
stoplistening=True #kill thread
client.close()
socket.close()

FL.stop()
FR.stop()
BL.stop()
BR.stop()

GPIO.cleanup()
