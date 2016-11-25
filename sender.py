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
      if(controller.getValue("power"):
        socket.send("stop")
        break
      else:
        lt=abs(int(15+35*controller.getValue("left-trigger")))
        rt=abs(int(15+35*controller.getValue("right-trigger")))
        lv=abs(int(15+35*controller.getValue("left-vertical")))
        rv=abs(int(15+35*controller.getValue("right-vertical")))
        msg = "[%d,%d,%d,%d]" % (lt,rt,lv,rv)
        socket.send(msg)
      time.sleep(0.1)
  except:
    print("an error occurred.")
  finally:
    socket.send("stop")
    socket.close()
else:
  print("could not find rpi")
