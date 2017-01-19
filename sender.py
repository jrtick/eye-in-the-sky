import bluetooth,time

target_name = "pi"

print("looking for devices")
nearby_devices = bluetooth.discover_devices()

print("searching nearby devices")
rpi_dev = None
for dev in nearby_devices:
  curname = bluetooth.lookup_name(dev)
  print(curname)
  if(curname is not None and target_name in curname):
    rpi_dev = dev
    break

if(rpi_dev is not None):
  print("Found pi! Connecting...")
  socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
  socket.connect((rpi_dev,1))
  print("Connected!")
  socket.send("[10,10,10,10]")
  time.sleep(10)
  socket.send("[40,40,40,40]")
  time.sleep(5)
  socket.send("[30,30,30,30]")
  time.sleep(5)
  socket.send("stop")
  socket.close()
else:
  print("could not find rpi")
