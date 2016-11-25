import bluetooth,threading,time
import RPi.GPIO as GPIO


#globals
FREQ = 2500
FRONT_LEFT_PIN = 19
FRONT_RIGHT_PIN = 8
BACK_LEFT_PIN = 5
BACK_RIGHT_PIN = 24
msg = "[0,0,0,0]"
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

def update_command():
  global client,msg,stoplistening
  while True:
    if(stoplistening):
      break
    else:
      try:
        curmsg=client.recv(1024) #blocks until message found
      except:
        curmsg = "error"
      msg = curmsg #updates global message that pi sees


#get connection
print("listening for connection...")
socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
socket.bind(("",1))
socket.listen(1)
while True:
  (client,client_addr) = socket.accept() #wait for connection
  print("Connected")
  
  #bg thread will keep track of client's messages and keep pi updated
  stoplistening = False
  thread = threading.Thread(target=update_command)
  thread.daemon = True
  thread.start()

  try:
    while True:
      print(msg)
      if(msg.lower()=="stop"): #fall. fall hard.
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
  stoplistening=True #kill thread
  time.sleep(1)
  client.close()
  FL.ChangeDutyCycle(0)
  FR.ChangeDutyCycle(0)
  BL.ChangeDutyCycle(0)
  BR.ChangeDutyCycle(0)

#cleanup
stoplistening=True #kill thread
socket.close()

FL.stop()
FR.stop()
BL.stop()
BR.stop()

GPIO.cleanup()
