from machine import Pin
import neopixel
import utime

class Rainbow_Light:
    '''This class manages rgb lights, as long as they are controlled with WS2812.'''
    def __init__(self, pin, num_leds):
        self.rainbow_light = neopixel.NeoPixel(Pin(pin), num_leds)
        self.num_leds = num_leds

        self.colors_vault = [(0, 0, 0) for _ in range(num_leds)]

    def set_all_color(self, red, green, blue):
        '''This function will set all LEDS to the same color.
        You have to use the basic rgb color code(0-255).'''
        for i in range(self.num_leds):
            self.rainbow_light[i] = (red, green, blue)
            self.colors_vault[i] = (red, green, blue)
        self.rainbow_light.write()

    def set_one_color(self, index, red, green, blue):
        self.rainbow_light[index] = (red, green, blue)
        self.colors_vault[index] = (red, green, blue)
        self.rainbow_light.write()


    def all_fade(self, to_red, to_green, to_blue, mirror_index=0, from_red=False, from_green=False, from_blue=False, steps=30, delay_ms=20):

        if isinstance(from_red, int) and isinstance(from_green, int) and isinstance(from_blue, int):
            r1 = from_red
            g1 = from_green
            b1 = from_blue
        else:
            if isinstance(mirror_index, int):
                r1, g1, b1 = self.colors_vault[mirror_index]
            else:
                print("Error arguments are not correct.")
        r2 = to_red
        g2 = to_green
        b2 = to_blue

        for step in range(steps + 1):
            r = int(r1 + (r2 - r1) * step / steps)
            g = int(g1 + (g2 - g1) * step / steps)
            b = int(b1 + (b2 - b1) * step / steps)
            for index in range (self.num_leds):
                self.rainbow_light[index] = (r, g, b)
                self.colors_vault[index] = (r, g, b)
            self.rainbow_light.write()
            utime.sleep_ms(delay_ms)

    def one_fade(self, index, to_red, to_green, to_blue, from_red=False, from_green=False, from_blue=False, steps=30, delay_ms=20):
        if isinstance(from_red, int) and isinstance(from_green, int) and isinstance(from_blue, int):
            r1 = from_red
            g1 = from_green
            b1 = from_blue
        else:
            r1, g1, b1 = self.colors_vault[index]
        r2 = to_red
        g2 = to_green
        b2 = to_blue

        for step in range(steps + 1):
            r = int(r1 + (r2 - r1) * step / steps)
            g = int(g1 + (g2 - g1) * step / steps)
            b = int(b1 + (b2 - b1) * step / steps)
            self.rainbow_light[index] = (r, g, b)
            self.colors_vault[index] = (r, g, b)
            self.rainbow_light.write()
            utime.sleep_ms(delay_ms)


    def all_off(self):
        for i in range(self.num_leds):
            self.rainbow_light[i] = (0, 0, 0)
            self.colors_vault[i] = (0, 0, 0)
        self.rainbow_light.write()
    
    def one_off(self, index):
        self.rainbow_light[index] = (0, 0, 0)
        self.colors_vault[index] = (0, 0, 0)
        self.rainbow_light.write()