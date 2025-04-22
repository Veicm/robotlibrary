from machine import Pin
import neopixel
import utime

class Rainbow_Light:
    '''This class manages rgb lights, as long as they are controlled with WS2812.'''
    def __init__(self, pin_num, num_leds):
        self.rainbow_light = neopixel.NeoPixel(Pin(pin_num), num_leds)
        self.num_leds = num_leds

    def set_all_color(self, red, green, blue):
        '''This function will set all LEDS to the same color.
        You have to use the basic rgb color code(0-255).'''
        for i in range(self.num_leds):
            self.rainbow_light[i] = (red, green, blue)
            self.rainbow_light.write()

    def all_off(self):
        for i in range(self.num_leds):
            self.rainbow_light[i] = (0, 0, 0)
        self.rainbow_light.write()