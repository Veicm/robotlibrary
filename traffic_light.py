from robotlibrary.light import Light

class Traffic_Light:
    '''This class handel a breadboard traffic light and provide basic functions for it.'''
    def __init__(self, yellow_pin):
        self.yellow = Light(yellow_pin)
        self.red = Light(yellow_pin + 1)
        self.green = Light(yellow_pin + 2)


    def red_on(self, on):
        if on:
            self.red.on()
        else:
            self.red.off()

    def yellow_on(self, on):
        if on:
            self.yellow.on()
        else:
            self.yellow.off()

    def green_on(self, on):
        if on:
            self.green.on()
        else:
            self.green.off()

    
    def all_on(self, on):
        if on:
            self.red_on(True)
            self.yellow_on(True)
            self.green_on(True)
        else:
            self.red_on(False)
            self.yellow_on(False)
            self.green_on(False)


    def red_only(self):
        self.all_on(False)
        self.red_on
    
    def yellow_only(self):
        self.all_on(False)
        self.yellow_on

    def green_only(self):
        self.all_on(False)
        self.green_on


    def red_blink(self, speed, repeats):
        self.red.blink(speed, repeats)
    
    def yellow_blink(self, speed, repeats):
        self.yellow.blink(speed, repeats)
    
    def green_blink(self, speed, repeats):
        self.green.blink(speed, repeats)