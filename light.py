from machine import Pin
import utime

class Light:
    '''This class manages a one-color LED'''

    def __init__(self, pin):
        self.light = Pin(pin, Pin.OUT)


    def on(self):
        self.light.value(1)

    def off(self):
        self.light.value(0)

    def blink(self, speed, repeats):
        for i in range(0,repeats, 1):
            self.on()
            utime.sleep(1/speed)
            self.off()
            utime.sleep(1/speed)
            repeats -= 1
            