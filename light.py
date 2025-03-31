import utime
from machine import Pin

class Light:
    '''This class manages a one-color LED'''

    def __init__(self, pin):
        self.light = Pin(pin, Pin.OUT)


    def on(self):
        self.light.value(1)

    def off(self):
        self.light.value(0)

    def blink(self, speed, trys):
        while trys > 0:
            self.on()
            utime.sleep(1/speed)
            self.off()
            utime.sleep(1/speed)
            trys -= trys
            