# peripherals
from robotlibrary.ultrasonic import Ultra
from robotlibrary.crawly_leg import Leg
from robotlibrary.button import Button
from robotlibrary.rainbow_light import Rainbow_Light
from robotlibrary.light import Light
from robotlibrary.buzzer import Buzzer
import robotlibrary.config.crawly_config

########## Bluetooth
# This is not implemented yet.
import bluetooth
from robotlibrary.bluetooth.peripheral import BLEPeripheral
from robotlibrary.bluetooth.ble_services_definitions import ROBOT_UUID, MOTOR_RX_UUID, MOTOR_TX_UUID
from robotlibrary.bluetooth.parser import decode_motor, encode_motor

#import machine, sys, utime, random
from time import sleep
import utime
import random


class Crawly:
    '''This is the central class which manages and uses all the other components of the robot. The parameters are defined in config.py'''
    def __init__(self, rc, button_mode=True):
        self.legs = {
            "front_right" : Leg(6, True, True, "front right"),
            "rear_right" : Leg(4, True, False, "rear right"),
            "rear_left" : Leg(2, False, False, "rear left"),
            "front_left" : Leg(0, False, True, "front left")
            }
        if robotlibrary.config.crawly_config.US is not None:
            self.us = Ultra(robotlibrary.config.crawly_config.US)

        self.button_mode = button_mode
        if button_mode:
            self.button_front = Button(robotlibrary.config.crawly_config.CRAWLY_BUTTON_FRONT, self.front_handler)
            self.button_rear = Button(robotlibrary.config.crawly_config.CRAWLY_BUTTON_REAR, self.rear_handler)

            self.curl_mode = False
            self.dance_mode = False
        
        if robotlibrary.config.crawly_config.INTERNAL_LED is not None:
            self.internal_led = Light(robotlibrary.config.crawly_config.INTERNAL_LED)
        else:
            self.internal_led = None
        
        if robotlibrary.config.crawly_config.CRAWLY_BUZZER is not None:
            self.buzzer = Buzzer(robotlibrary.config.crawly_config.CRAWLY_BUZZER)
        else:
            self.buzzer = None

        if robotlibrary.config.crawly_config.CRAWLY_RAINBOW_LIGHT is not None:
            self.rainbow_light = Rainbow_Light(robotlibrary.config.crawly_config.CRAWLY_RAINBOW_LIGHT, robotlibrary.config.crawly_config.CRAWLY_RAINBOW_LIGHT_NUMBER)
        else:
            self.rainbow_light = None


        
        
############################Normal movement############################ 

    def move_forward(self, steps):
        '''This makes the crawler move forward in a coordinated way. Most of the functionality lies in the other classes Joint and Leg.'''
        for _ in range(steps):
            walk = True
            # First half of one step cycle.
            while walk:
                w1 = self.legs["front_right"].forward_move_forward()
                w2 = self.legs["rear_left"].forward_move_forward()
                w3 = self.legs["rear_right"].forward_move_backward()
                w4 = self.legs["front_left"].forward_move_backward()

                walk = w1 or w2 or w3 or w4
            
            walk = True
            # Second half of one step cycle
            while walk:
                w1 = self.legs["front_right"].forward_move_backward()
                w2 = self.legs["rear_left"].forward_move_backward()
                w3 = self.legs["rear_right"].forward_move_forward()
                w4 = self.legs["front_left"].forward_move_forward()
                
                walk = w1 or w2 or w3 or w4

    def move_backward(self, steps):
        '''This makes the crawler move backward in a coordinated way. Most of the functionality lies in the other classes Joint and Leg.'''
        for _ in range(steps):
            walk = True
            # First half of one step cycle.
            while walk:
                w1 = self.legs["front_right"].backward_move_backward()
                w2 = self.legs["rear_left"].backward_move_backward()
                w3 = self.legs["rear_right"].backward_move_forward()
                w4 = self.legs["front_left"].backward_move_forward()

                walk = w1 or w2 or w3 or w4
            
            walk = True
            # Second half of one step cycle
            while walk:
                w1 = self.legs["front_right"].backward_move_forward()
                w2 = self.legs["rear_left"].backward_move_forward()
                w3 = self.legs["rear_right"].backward_move_backward()
                w4 = self.legs["front_left"].backward_move_backward()
                
                walk = w1 or w2 or w3 or w4


    def turn_left(self, steps):
        '''This makes the crawler turn to the left in on place in a coordinated way. Most of the functionality lies in the other classes Joint and Leg.'''
        for _ in range(steps):
            walk = True
            # First half of one step cycle.
            while walk:
                w1 = self.legs["front_right"].forward_move_forward()
                w2 = self.legs["rear_left"].backward_move_backward()
                w3 = self.legs["rear_right"].forward_move_backward()
                w4 = self.legs["front_left"].backward_move_forward()

                walk = w1 or w2 or w3 or w4
            
            walk = True
            # Second half of one step cycle
            while walk:
                w1 = self.legs["front_right"].forward_move_backward()
                w2 = self.legs["rear_left"].backward_move_forward()
                w3 = self.legs["rear_right"].forward_move_forward()
                w4 = self.legs["front_left"].backward_move_backward()
                
                walk = w1 or w2 or w3 or w4
            steps -= 1

    def turn_right(self, steps):
        '''This makes the crawler turn to the right in on place in a coordinated way. Most of the functionality lies in the other classes Joint and Leg.'''
        for _ in range(steps):
            walk = True
            # First half of one step cycle.
            while walk:
                w1 = self.legs["front_right"].backward_move_forward()
                w2 = self.legs["rear_left"].forward_move_backward()
                w3 = self.legs["rear_right"].backward_move_backward()
                w4 = self.legs["front_left"].forward_move_forward()

                walk = w1 or w2 or w3 or w4
            
            walk = True
            # Second half of one step cycle
            while walk:
                w1 = self.legs["front_right"].backward_move_backward()
                w2 = self.legs["rear_left"].forward_move_forward()
                w3 = self.legs["rear_right"].backward_move_forward()
                w4 = self.legs["front_left"].forward_move_backward()
                
                walk = w1 or w2 or w3 or w4


    #############avoid objects#####################

    def _avoid_to_left(self, distance=robotlibrary.config.crawly_config.CRAWLY_MIN_DISTANCE):
        '''This makes the crawler turn to the left while a object is detected.'''
        self.turn_left(1)
        while self.us.get_dist() < distance:
            self.turn_left(1)
        self.turn_left(2)
        self.calibrate

    def _avoid_to_right(self, distance=robotlibrary.config.crawly_config.CRAWLY_MIN_DISTANCE):
        '''This makes the crawler turn to the right while a object is detected.'''
        self.turn_right(1)
        while self.us.get_dist() < distance:
            self.turn_right(1)
        self.turn_right(2)
        self.calibrate


    def avoid_objects(self, distance=robotlibrary.config.crawly_config.CRAWLY_MIN_DISTANCE):
        '''This makes the crawler walk ahead as long as no object is detected'''
        repeats = 0
        try:
            while True:
                while self.us.get_dist() > distance:
                    self.move_forward(1)
                
                if repeats % 2 == 0:
                    self._avoid_to_right(distance)
                elif repeats % 2 == 1:
                    self._avoid_to_left(distance)

                utime.sleep(0.3)
                repeats += 1
        except KeyboardInterrupt:
            self.calibrate
            print("program terminated by user")


    #############avoid objects -end-#####################


############################Normal movement -end-############################
       


############################Curled movement############################

    def curled_move_forward(self, steps):
        '''This makes the crawler move forward on tiptoes in a coordinated way. Most of the functionality lies in the other classes Joint and Leg'''
        for _ in range(steps):
            walk = True
            # First half of one step cycle.
            while walk:
                w1 = self.legs["front_right"].curled_forward_move_forward()
                w2 = self.legs["rear_left"].curled_forward_move_forward()
                w3 = self.legs["rear_right"].curled_forward_move_backward()
                w4 = self.legs["front_left"].curled_forward_move_backward()

                walk = w1 or w2 or w3 or w4
            
            walk = True
            # Second half of one step cycle
            while walk:
                w1 = self.legs["front_right"].curled_forward_move_backward()
                w2 = self.legs["rear_left"].curled_forward_move_backward()
                w3 = self.legs["rear_right"].curled_forward_move_forward()
                w4 = self.legs["front_left"].curled_forward_move_forward()
                
                walk = w1 or w2 or w3 or w4

    def curled_move_backward(self, steps):
        '''This makes the crawler move backward on tiptoes in a coordinated way. Most of the functionality lies in the other classes Joint and Leg'''
        for _ in range(steps):
            walk = True
            # First half of one step cycle.
            while walk:
                w1 = self.legs["front_right"].curled_backward_move_backward()
                w2 = self.legs["rear_left"].curled_backward_move_backward()
                w3 = self.legs["rear_right"].curled_backward_move_forward()
                w4 = self.legs["front_left"].curled_backward_move_forward()
                
                walk = w1 or w2 or w3 or w4
            
            walk = True
            # Second half of one step cycle
            while walk:
                w1 = self.legs["front_right"].curled_backward_move_forward()
                w2 = self.legs["rear_left"].curled_backward_move_forward()
                w3 = self.legs["rear_right"].curled_backward_move_backward()
                w4 = self.legs["front_left"].curled_backward_move_backward()
                
                walk = w1 or w2 or w3 or w4


    def curled_turn_left(self, steps):
        '''This makes the crawler turn to the left on tiptoes in on place in a coordinated way. Most of the functionality lies in the other classes Joint and Leg'''
        for _ in range(steps):
            walk = True
            # First half of one step cycle.
            while walk:
                w1 = self.legs["front_right"].curled_forward_move_forward()
                w2 = self.legs["rear_left"].curled_backward_move_backward()
                w3 = self.legs["rear_right"].curled_forward_move_backward()
                w4 = self.legs["front_left"].curled_backward_move_forward()
                
                walk = w1 or w2 or w3 or w4
            
            walk = True
            # Second half of one step cycle
            while walk:
                w1 = self.legs["front_right"].curled_forward_move_backward()
                w2 = self.legs["rear_left"].curled_backward_move_forward()
                w3 = self.legs["rear_right"].curled_forward_move_forward()
                w4 = self.legs["front_left"].curled_backward_move_backward()
                
                walk = w1 or w2 or w3 or w4

    def curled_turn_right(self, steps):
        '''This makes the crawler turn to the right on tiptoes in on place in a coordinated way. Most of the functionality lies in the other classes Joint and Leg'''
        for _ in range(steps):
            walk = True
            # First half of one step cycle.
            while walk:
                w1 = self.legs["front_right"].curled_backward_move_forward()
                w2 = self.legs["rear_left"].curled_forward_move_backward()
                w3 = self.legs["rear_right"].curled_backward_move_backward()
                w4 = self.legs["front_left"].curled_forward_move_forward()
                
                walk = w1 or w2 or w3 or w4
            
            walk = True
            # Second half of one step cycle
            while walk:
                w1 = self.legs["front_right"].curled_backward_move_backward()
                w2 = self.legs["rear_left"].curled_forward_move_forward()
                w3 = self.legs["rear_right"].curled_backward_move_forward()
                w4 = self.legs["front_left"].curled_forward_move_backward()
                
                walk = w1 or w2 or w3 or w4


    #############avoid objects#####################

    def _curled_avoid_to_left(self, distance=robotlibrary.config.crawly_config.CRAWLY_MIN_DISTANCE):
        self.curled_turn_left(1)
        while self.us.get_dist() < distance:
            self.curled_turn_left(1)
        self.curled_turn_left(2)
        self.walking_curl()

    def _curled_avoid_to_right(self, distance=robotlibrary.config.crawly_config.CRAWLY_MIN_DISTANCE):
        self.curled_turn_right(1)
        while self.us.get_dist() < distance:
            self.curled_turn_right(1)
        self.curled_turn_right(2)
        self.walking_curl()


    def curled_avoid_objects(self, distance=robotlibrary.config.crawly_config.CRAWLY_MIN_DISTANCE):
        repeats = 0
        try:
            while True:
                while self.us.get_dist() > distance:
                    self.curled_move_forward(1)
                
                if repeats % 2 == 0:
                    self._curled_avoid_to_right(distance)
                elif repeats % 2 == 1:
                    self._curled_avoid_to_left(distance)

                utime.sleep(0.3)
                repeats += 1
        except KeyboardInterrupt:
            self.calibrate
            print("program terminated by user")


    #############avoid objects -end-#####################


############################Curled movement -end-############################
          


############################side walking############################
 
    def move_left(self, steps):
        '''This makes the crawler move to the left in a coordinated way. Most of the functionality lies in the other classes Joint and Leg.'''
        for _ in range(steps):
            walk = True
            # First half of one step cycle.
            while walk:
                w1 = self.legs["front_right"].left_move_ahead()
                w2 = self.legs["rear_left"].left_move_center()
                w3 = self.legs["rear_right"].left_move_center()
                w4 = self.legs["front_left"].left_move_ahead()

                walk = w1 or w2 or w3 or w4
            
            walk = True
            # Second half of one step cycle
            while walk:
                w1 = self.legs["front_right"].left_move_center()
                w2 = self.legs["rear_left"].left_move_ahead()
                w3 = self.legs["rear_right"].left_move_ahead()
                w4 = self.legs["front_left"].left_move_center()
                
                walk = w1 or w2 or w3 or w4

    def move_right(self, steps):
        '''This makes the crawler move to the right in a coordinated way. Most of the functionality lies in the other classes Joint and Leg.'''
        for _ in range(steps):
            walk = True
            # First half of one step cycle.
            while walk:
                w1 = self.legs["front_right"].right_move_ahead()# down
                w2 = self.legs["rear_left"].right_move_center()# down
                w3 = self.legs["rear_right"].right_move_center()# up
                w4 = self.legs["front_left"].right_move_ahead()# up
                
                walk = w1 or w2 or w3 or w4
            
            walk = True
            # Second half of one step cycle
            while walk:
                w1 = self.legs["front_right"].right_move_center()# up
                w2 = self.legs["rear_left"].right_move_ahead()# up
                w3 = self.legs["rear_right"].right_move_ahead()# down
                w4 = self.legs["front_left"].right_move_center()# down
                
                walk = w1 or w2 or w3 or w4
 

#############################side walking -end-############################          


############################walk around############################

    def go_to_left(self, distance=robotlibrary.config.crawly_config.CRAWLY_MIN_DISTANCE):
        '''This makes the robot moves to the left, while an object is closer than the given distance.'''
        self.move_left(1)
        while self.us.get_dist() < distance:
            self.move_left(1)
        self.move_left(2)

    def go_to_right(self, distance=robotlibrary.config.crawly_config.CRAWLY_MIN_DISTANCE):
        '''This makes the robot moves to the right, while an object is closer than the given distance.'''
        self.move_right(1)
        while self.us.get_dist() < distance:
            self.move_right(1)
        self.move_right(2)


############################walk around -end-############################


############################auto pilot############################

    def _lookout(self, distance) -> bool:
        '''This makes he crawler stand on his tiptoes to see if he can walk around an object.'''
        self.curl()
        utime.sleep(2)
        high_distance = self.us.get_dist()
        low_distance = distance + 5 #avoiding measurement errors by adding a 5cm tolerance
        if high_distance > low_distance:
            return True
        else:
            return False

    def auto_pilot (self, distance=robotlibrary.config.crawly_config.CRAWLY_MIN_DISTANCE):
        '''This function makes the robot run on auto pilot by combining many other functions.'''
        repeats = 0
        try:
            while True:
                if self.rainbow_light:
                    self.rainbow_light.all_off()
                while self.us.get_dist() > distance:
                    if self.button_mode:
                        self._check_if_normal()
                    self.move_forward(1)
                    if self.internal_led:
                        self.internal_led.on()

                if self.internal_led:
                    self.internal_led.off()
                if self.rainbow_light:
                    self.rainbow_light.set_all_color(255, 255, 0)
                if self.buzzer:
                    self.buzzer.make_sound(50)
                    utime.sleep(0.8)
                    self.buzzer.silence()
                is_object = self._lookout(self.us.get_dist())

                if is_object:
                    if self.rainbow_light:
                        self.rainbow_light.set_all_color(0, 222, 131)
                    if repeats % 2 == 0:
                        self.go_to_right(distance)
                    elif repeats % 2 == 1:
                        self.go_to_left(distance)
                else:
                    if self.rainbow_light:
                        self.rainbow_light.set_all_color(0, 255,255)
                    if repeats % 2 == 0:
                        self._avoid_to_right(distance)
                    elif repeats % 2 == 1:
                        self._avoid_to_left(distance)

                utime.sleep(0.3)
                repeats += 1
        except KeyboardInterrupt:
            if self.rainbow_light:
                self.rainbow_light.all_off()
            if self.internal_led:
                self.internal_led.off()
            if self.buzzer:
                self.buzzer.silence()
            self.calibrate
            print("program terminated by user")

    def curled_auto_pilot (self, distance=robotlibrary.config.crawly_config.CRAWLY_MIN_DISTANCE):
        '''This function makes the robot run on auto pilot an walk on his tiptoes by combining many other functions.'''
        repeats = 0
        try:
            while True:
                if self.rainbow_light:
                    self.rainbow_light.all_off()
                while self.us.get_dist() > distance:
                    if self.button_mode:
                        self._check_if_curled()
                    else:
                        pass
                    self.curled_move_forward(1)
                    if self.internal_led:
                        self.internal_led.on()

                if self.internal_led:
                    self.internal_led.off()
                if self.rainbow_light:
                    self.rainbow_light.set_all_color(255, 255, 0)
                if self.buzzer:
                    self.buzzer.make_sound(50)
                    utime.sleep(0.8)
                    self.buzzer.silence()
                is_object = self._lookout(self.us.get_dist())

                if is_object:
                    if self.rainbow_light:
                        self.rainbow_light.set_all_color(0, 222, 131)
                    if repeats % 2 == 0:
                        self.go_to_right(distance)
                    elif repeats % 2 == 1:
                        self.go_to_left(distance)
                else:
                    if self.rainbow_light:
                        self.rainbow_light.set_all_color(0, 255,255)
                    if repeats % 2 == 0:
                        self._curled_avoid_to_right(distance)
                    elif repeats % 2 == 1:
                        self._curled_avoid_to_left(distance)

                utime.sleep(0.3)
                repeats += 1
        except KeyboardInterrupt:
            if self.rainbow_light:
                self.rainbow_light.all_off()
            if self.internal_led:
                self.internal_led.off()
            if self.buzzer:
                self.buzzer.silence()
            self.calibrate
            print("program terminated by user")


############################auto pilot -end-############################

    def dance(self, repeats):
        '''This function makes the robot dance. (It's awesome)'''
        if self.internal_led:
            self.internal_led.off()
        for _ in range(repeats):
            if self.button_mode:
                self._check_if_dancing()
            dance = True
            # First half of the dance move.
            while dance:
                d1 = self.legs["front_right"].dance_move_ahead()
                d2 = self.legs["rear_left"].dance_move_ahead()
                d3 = self.legs["rear_right"].dance_move_center()
                d4 = self.legs["front_left"].dance_move_center()
                dance = d1 or d2 or d3 or d4
                if self.rainbow_light:
                    self.rainbow_light.set_all_color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            
            dance = True
            # Second half of the dance move.
            while dance:
                d1 = self.legs["front_right"].dance_move_center()
                d2 = self.legs["rear_left"].dance_move_center()
                d3 = self.legs["rear_right"].dance_move_ahead()
                d4 = self.legs["front_left"].dance_move_ahead()
                dance = d1 or d2 or d3 or d4
                if self.rainbow_light:
                    self.rainbow_light.set_all_color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        if self.rainbow_light:
            self.rainbow_light.all_off()

############################Positions############################

    def park(self):
        '''This stretches legs the legs lengthwise, so the robot lies on its underside.'''
        for l in self.legs.values():
            l.park()
        
    def curl(self):
        '''This movement bends the legs, so the robot stands on tiptoes.'''
        for l in self.legs.values():
            l.curl()
            
    def walking_curl(self):
        '''This movement bends the legs, so the robot stands on low tiptoes.'''
        for l in self.legs.values():
            l.walking_curl()
    
    def calibrate(self):
        '''This sets all servos to 90° so the legs can be assembled with the correct angles.'''
        for l in self.legs.values():
            l.calibrate
        
    def tap(self):
        '''This taps all the legs. Looks and sounds scary and can also identify the legs.'''
        for l in self.legs.values():
            l.tap()
            sleep(0.1)


############################Positions -end-############################



############################Button dependencies############################

    def front_handler(self, _):
        '''This function gets called when the front button is pressed.
        It is used to switch between curled walking and normal walking.
        '''
        if self.curl_mode:
            self.curl_mode = False
        else:
            self.curl_mode = True

    def rear_handler(self, _):
        '''This function gets called when the rear button is pressed.
        It is used to switch between dancing and walking.
        '''
        if self.dance_mode:
            self.dance_mode = False
        else:
            self.dance_mode = True


    def _check_if_normal(self):
        '''This function is used in the auto_pilot function.'''
        if self.dance_mode:
            self.dance(1000)
        else:
            if self.curl_mode:
                self.curled_auto_pilot()
            else:
                pass

    def _check_if_curled(self):
        '''This function is used in the curled_auto_pilot function.'''
        if self.dance_mode:
            self.dance(1000)
        else:
            if self.curl_mode:
                pass
            else:
                self.auto_pilot()

    def _check_if_dancing(self):
        '''This function is used in the dance function.'''
        if self.dance_mode:
            pass
        else:
            if self.rainbow_light:
                self.rainbow_light.all_off()
            if not self.curl_mode:
                self.auto_pilot()
            else:
                self.curled_auto_pilot()


############################Button dependencies -end-############################

    
def main():
    '''Starting this file makes the robot work on auto pilot.'''
    try: 
        c = Crawly(True)
        c.auto_pilot()
    except KeyboardInterrupt:
        c.park()
        sleep(1)
    
if __name__ == "__main__":
    # execute only if run as a script
    main()