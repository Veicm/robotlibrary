from machine import Pin
from time import sleep
import utime

class Ultra:
    '''This class manages the ultrasonic sensor. It returns the distance to an obstacle in cm. '''
    def __init__(self, pinNo):
        self.trigger = Pin(pinNo, Pin.OUT) # to trigger a sound impulse
        self.echo = Pin(pinNo+1, Pin.IN) # records the echo of the trigger pulse      

    def get_dist(self):
        '''This returns the measured distance in cm. (float)'''
        time_passed = 0
        signal_on = 0
        signal_off = 0
        self.trigger.low()
        utime.sleep_us(2)
        self.trigger.high()
        utime.sleep_us(5)
        self.trigger.low()
        while self.echo.value() == 0:
            signal_off = utime.ticks_us()
        while self.echo.value() == 1:
            signal_on = utime.ticks_us()
        time_passed = signal_on - signal_off
        distance = round((time_passed * 0.0343) / 2, 2)
        # print("The distance from object is ", distance, "cm.") # for debugging purposes uncomment the line.
        utime.sleep_ms(10) # Wait necessary or program halts
        return distance
    
    def output(self):
        print(f"measured distance: {self.get_dist()} cm.")
        sleep(1)