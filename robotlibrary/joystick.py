from machine import Pin,ADC,Timer
from robotlibrary.config.general_config import JS_MIN_DUTY, JS_MAX_DUTY, JS_X_MEDIAN, JS_Y_MEDIAN, DEBOUNCE_WAIT
import utime
from robotlibrary.motor import Motor

class Joystick:
    def __init__(self, x,y,b):
        self.x = ADC(x)
        self.y = ADC(y)
        self.b = Pin(b,Pin.IN, Pin.PULL_UP)
        self.b.irq(trigger=Pin.IRQ_FALLING, handler=self.button_handler)
        self.pressed = False
        self.last_pressed = 0
        self.timer = Timer()
        
    def reset(self,t):
        self.pressed = False
    
    def button_handler(self,pin):
        while utime.ticks_diff(utime.ticks_ms(), self.last_pressed) < DEBOUNCE_WAIT: 
            pass
        self.last_pressed = utime.ticks_ms()
        if not self.pressed:
            while utime.ticks_diff(utime.ticks_ms(), self.last_pressed) < DEBOUNCE_WAIT:
                pass
            if pin.value() == 1:
                self.pressed=True 
                print(pin.value(), "Button pressed")
                self.last_pressed = utime.ticks_ms()
                self.timer.init(mode=Timer.ONE_SHOT, period=300, callback=self.reset)
    
    def get_speed(self,s):
        speed = 0
        if s < JS_Y_MEDIAN-300:
            speed = abs(JS_MAX_DUTY-s*2)
        elif s > JS_Y_MEDIAN+300:
            speed = -abs(JS_MAX_DUTY-s*2)    
        else:
            speed = 0
        if speed > -4000 and speed < 4000:
                speed = 0
        return int(100/JS_MAX_DUTY*speed)
    
    def get_direction(self,d):
        direction = 0
        if d < JS_X_MEDIAN-200:
            direction = -abs(90-(90/JS_X_MEDIAN*d))
        elif d > JS_X_MEDIAN+200:
            direction = abs(90/65535*d)
        else:
            direction = 0
        return int(direction)

joystick = Joystick(26,27,0)

while True:
#     y_values = list()
#     x_values = list()
#     for i in range(0,100):
#         x_values.append(joystick.x.read_u16())
#         y_values.append(joystick.y.read_u16())
#     sum = 0
#     print(y_values)
#     for y in y_values:
#         sum += y
    #print(f"Y-values median: {sum/100}")
    #print(f"X-value: {joystick.x.read_u16()}")
    #print(f"Y-value: {joystick.y.read_u16()}")

    print(f"X-value: {joystick.get_direction(joystick.x.read_u16())}")
    print(f"Y-value: {joystick.get_speed(joystick.y.read_u16())}")
    utime.sleep_ms(1000)