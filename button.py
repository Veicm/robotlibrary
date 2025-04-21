from machine import Pin
import robotlibrary.config
import utime


class Button:
    '''This class manage a simple binary button.'''

    def __init__(self, pin, callback=None):
        self.button = Pin(pin, Pin.IN, Pin.PULL_DOWN)
        if callback:
            self.button.irq(trigger=Pin.IRQ_FALLING, handler=callback)


    def output(self, raw):
        if raw:
            print(self.button.value())
        else:
            if self.button.value() == robotlibrary.config.PRESSED:
                print("Button pressed")
            else:
                print("Button unpressed")
        utime.sleep(0.5)

    def export(self) -> bool:
        '''returns False as long as the button is unpressed and True when the button is pressed.'''
        if self.button.value() == robotlibrary.config.PRESSED:
            return True
        else:
            return False
        utime.sleep(0.1)



def main():
    try:
        b = Button(18)
        while True:
            b.output
    except KeyboardInterrupt:
        print("Program terminated by user")

if __name__ == "__main__":
    main()

