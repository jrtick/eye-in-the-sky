import bluetooth,time
from ps4controller import *

print("looking for ps4 controller")
controller = PS4Controller()
controller.listen_background()
print("PS4 controller found")

print("looking for devices")
nearby_devices = bluetooth.discover_devices()

print("searching nearby devices")
rpi_dev = None
for dev in nearby_devices:
  curname = bluetooth.lookup_name(dev)
  print(curname)
  if(curname is not None and "pi" in curname):
    rpi_dev = dev
    break

if(rpi_dev is not None):
  print("Found pi! Connecting...")
  socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
  socket.connect((rpi_dev,1))
  print("Connected!")

  try:
    while(True):
      lt=abs(int(100*controller.getValue("left-trigger")))
      rt=abs(int(100*controller.getValue("right-trigger")))
      lv=abs(int(100*controller.getValue("left-vertical")))
      rv=abs(int(100*controller.getValue("right-vertical")))
      socket.send("[%d,%d,%d,%d]" % (lt,rt,lv,rv))
  except:
    print("an error occurred.")
  finally:
    socket.send("stop")
    socket.close()
else:
  print("could not find rpi")
