from machine import Pin
import utime

def is_wifi() -> bool:
    '''This function is used to check if the program run on a normal pico or a pico-w.'''
    try:
        import network
        return True
    except Exception:
        return False

class Light:
    '''This class manages a one-color LED'''

    def __init__(self, pin):
        if pin == 25 and is_wifi():
            self.light = Pin("LED", Pin.OUT)
        else:
            self.light = Pin(pin, Pin.OUT)


    def on(self):
        self.light.value(1)

    def off(self):
        self.light.value(0)

    def blink(self, speed, repeats):
        for i in range(0, repeats, 1):
            self.on()
            utime.sleep(1/speed)
            self.off()
            utime.sleep(1/speed)
            repeats -= 1
            