import time
import threading

import json
import threading

from serial import Serial, PARITY_NONE

class ArduinoSerial:
    def __init__(self, rx_return, port="/dev/ttyS0", baudrate=9600):
        self._Serial = Serial(port, baudrate, bytesize=8, parity=PARITY_NONE, stopbits=1)
        self._rx_return = rx_return

        threading.Thread(target=self.rx_thread).start()

    @property
    def Serial(self):
        """The Serial property."""
        return self._Serial

    @property
    def rx_return(self):
        """The rx_return property."""
        return self._rx_return

    def tx(self, msg):
        self.Serial.write(f"{msg}".encode(encoding="utf-8"))
        print(f"[TX] {msg}")

    def rx(self):
        msg = self.Serial.readline()
        msg = str(msg, encoding="utf-8")
        print(f"[RX] {msg}")
        self.rx_return(msg)

    def rx_thread(self):
        while True:
            if (self.Serial.in_waiting > 0):
                self.rx()
            time.sleep(.1)