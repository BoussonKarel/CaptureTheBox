# CaptureTheBox
A teambuilding game using Pi and Arduino

## Setting it up
Follow my Instructables on what you need and how to connect it
https://www.instructables.com/id/Capture-the-Box/

## Modify the code
There's a few things you'll need to change to get working code:

### RPI > Backend
**secrets.py**
Fill in your TTN credentials here, to connect via MQTT.

**config.py**
Fill in your database credentials here.

**ctb_service.service**
Copy this to /etc/systemd/system using the command
```sudo cp ctb_service.service /etc/systemd/system/ctb_service.service``
then enable it using
```sudo systemctl enable ctb_service.service```
The service will now run whenever the Pi is booted up. Use _disable_ to disable this.

You can also manually run the code or use _systemctl start/stop_

### Arduino > main.ino
Change your TTN credentials:
appeui, deveui, appkey

You also might want to change TX_INTERVAL, so you comply with the fair access policy.
(30ms airtime pe 24 hours etc...) [https://www.thethingsnetwork.org/docs/lorawan/duty-cycle.html#maximum-duty-cycle]
