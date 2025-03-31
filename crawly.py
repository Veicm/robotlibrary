# peripherals
from robotlibrary.ultrasonic import Ultra
from robotlibrary.crawly_leg import Leg
import robotlibrary.config

########## Bluetooth
# This is not implemented yet.
import bluetooth
from robotlibrary.bluetooth.peripheral import BLEPeripheral
from robotlibrary.bluetooth.ble_services_definitions import ROBOT_UUID, MOTOR_RX_UUID, MOTOR_TX_UUID
from robotlibrary.bluetooth.parser import decode_motor, encode_motor

#import machine, sys, utime, random
from time import sleep
import utime


class Crawly:
    '''This is the central class which manages and uses all the other components of the robot. The parameters are defined in config.py'''
    def __init__(self,rc):
        self.legs = {
            "front_right" : Leg(6, True, True, "front right"),
            "rear_right" : Leg(4, True, False, "rear right"),
            "rear_left" : Leg(2, False, False, "rear left"),
            "front_left" : Leg(0, False, True, "front left")
            }
        if robotlibrary.config.US is not None:
            self.us = Ultra(robotlibrary.config.US)
        
############################Normal movement############################ 

    def move_forward(self, steps):
        '''This makes the crawler move forward in a coordinated way. Most of the funktionality lies in the other classes Joint and Leg.'''
        while steps > 0:
            walk = True
            # First half of one stepcycle.
            while walk:
                w1 = self.legs["front_right"].forward_move_forward()
                w2 = self.legs["rear_left"].forward_move_forward()
                w3 = self.legs["rear_right"].forward_move_backward()
                w4 = self.legs["front_left"].forward_move_backward()
                walk = w1 or w2 or w3 or w4
            
            walk = True
            # Second half of one stepcycle
            while walk:
                w1 = self.legs["front_right"].forward_move_backward()
                w2 = self.legs["rear_left"].forward_move_backward()
                w3 = self.legs["rear_right"].forward_move_forward()
                w4 = self.legs["front_left"].forward_move_forward()
                
                walk = w1 or w2 or w3 or w4
            steps = steps-1

    def move_backward(self, steps):
        '''This makes the crawler move backward in a coordinated way. Most of the funktionality lies in the other classes Joint and Leg.'''
        while steps > 0:
            walk = True
            # First half of one stepcycle.
            while walk:
                w1 = self.legs["front_right"].backward_move_backward()
                w2 = self.legs["rear_left"].backward_move_backward()
                w3 = self.legs["rear_right"].backward_move_forward()
                w4 = self.legs["front_left"].backward_move_forward()
                walk = w1 or w2 or w3 or w4
            
            walk = True
            # Second half of one stepcycle
            while walk:
                w1 = self.legs["front_right"].backward_move_forward()
                w2 = self.legs["rear_left"].backward_move_forward()
                w3 = self.legs["rear_right"].backward_move_backward()
                w4 = self.legs["front_left"].backward_move_backward()
                
                walk = w1 or w2 or w3 or w4
            steps = steps-1


    def turn_left(self, steps):
        '''This makes the crawler turn to the left in on place in a coordinated way. Most of the funktionality lies in the other classes Joint and Leg.'''
        while steps > 0:
            walk = True
            # First half of one stepcycle.
            while walk:
                w1 = self.legs["front_right"].forward_move_forward()
                w2 = self.legs["rear_left"].backward_move_backward()
                w3 = self.legs["rear_right"].forward_move_backward()
                w4 = self.legs["front_left"].backward_move_forward()
                walk = w1 or w2 or w3 or w4
            
            walk = True
            # Second half of one stepcycle
            while walk:
                w1 = self.legs["front_right"].forward_move_backward()
                w2 = self.legs["rear_left"].backward_move_forward()
                w3 = self.legs["rear_right"].forward_move_forward()
                w4 = self.legs["front_left"].backward_move_backward()
                
                walk = w1 or w2 or w3 or w4
            steps -= 1

    def turn_right(self, steps):
        '''This makes the crawler turn to the right in on place in a coordinated way. Most of the funktionality lies in the other classes Joint and Leg.'''
        while steps > 0:
            walk = True
            # First half of one stepcycle.
            while walk:
                w1 = self.legs["front_right"].backward_move_forward()
                w2 = self.legs["rear_left"].forward_move_backward()
                w3 = self.legs["rear_right"].backward_move_backward()
                w4 = self.legs["front_left"].forward_move_forward()
                walk = w1 or w2 or w3 or w4
            
            walk = True
            # Second half of one stepcycle
            while walk:
                w1 = self.legs["front_right"].backward_move_backward()
                w2 = self.legs["rear_left"].forward_move_forward()
                w3 = self.legs["rear_right"].backward_move_forward()
                w4 = self.legs["front_left"].forward_move_backward()
                
                walk = w1 or w2 or w3 or w4
            steps -= 1


    #############avoid objects#####################

    def _avoid_to_left(self, distance):
        '''This makes the crawler turn to the left while a objekt is detected.'''
        self.turn_left(1)
        while self.us.get_dist() < distance:
            self.turn_left(1)
        self.turn_left(2)
        self.calibrate

    def _avoid_to_right(self, distance):
        '''This makes the crawler turn to the right while a objekt is detected.'''
        self.turn_right(1)
        while self.us.get_dist() < distance:
            self.turn_right(1)
        self.turn_right(2)
        self.calibrate


    def avoid_objects(self, distance):
        '''This makes the crawler walk ahead as long as no objekt is detected'''
        trys = 0
        try:
            while True:
                while self.us.get_dist() > distance:
                    self.move_forward(1)
                
                if trys % 2 == 0:
                    self._avoid_to_right(distance)
                elif trys % 2 == 1:
                    self._avoid_to_left(distance)

                utime.sleep(0.3)
                trys += 1
        except KeyboardInterrupt:
            self.calibrate
            print("program terminated by user")


    #############avoid objects -end-#####################


############################Normal movement -end-############################
       


############################Curled movement############################

    def curled_move_forward(self, steps):
        '''This makes the crawler move forward on tiptoes in a coordinated way. Most of the funktionality lies in the other classes Joint and Leg'''
        while steps > 0:
            walk = True
            # First half of one stepcycle.
            while walk:
                w1 = self.legs["front_right"].curled_forward_move_forward()
                w2 = self.legs["rear_left"].curled_forward_move_forward()
                w3 = self.legs["rear_right"].curled_forward_move_backward()
                w4 = self.legs["front_left"].curled_forward_move_backward()
                walk = w1 or w2 or w3 or w4
            
            walk = True
            # Second half of one stepcycle
            while walk:
                w1 = self.legs["front_right"].curled_forward_move_backward()
                w2 = self.legs["rear_left"].curled_forward_move_backward()
                w3 = self.legs["rear_right"].curled_forward_move_forward()
                w4 = self.legs["front_left"].curled_forward_move_forward()
                
                walk = w1 or w2 or w3 or w4
            steps = steps-1

        def curled_move_backward(self, steps):
            '''This makes the crawler move backward on tiptoes in a coordinated way. Most of the funktionality lies in the other classes Joint and Leg'''
        while steps > 0:
            walk = True
            # First half of one stepcycle.
            while walk:
                w1 = self.legs["front_right"].curled_backward_move_backward()
                w2 = self.legs["rear_left"].curled_backward_move_backward()
                w3 = self.legs["rear_right"].curled_backward_move_forward()
                w4 = self.legs["front_left"].curled_backward_move_forward()
                walk = w1 or w2 or w3 or w4
            
            walk = True
            # Second half of one stepcycle
            while walk:
                w1 = self.legs["front_right"].curled_backward_move_forward()
                w2 = self.legs["rear_left"].curled_backward_move_forward()
                w3 = self.legs["rear_right"].curled_backward_move_backward()
                w4 = self.legs["front_left"].curled_backward_move_backward()
                
                walk = w1 or w2 or w3 or w4
            steps = steps-1


    def curled_turn_left(self, steps):
        '''This makes the crawler turn to the left on tiptoes in on place in a coordinated way. Most of the funktionality lies in the other classes Joint and Leg'''
        while steps > 0:
            walk = True
            # First half of one stepcycle.
            while walk:
                w1 = self.legs["front_right"].curled_forward_move_forward()
                w2 = self.legs["rear_left"].curled_backward_move_backward()
                w3 = self.legs["rear_right"].curled_forward_move_backward()
                w4 = self.legs["front_left"].curled_backward_move_forward()
                walk = w1 or w2 or w3 or w4
            
            walk = True
            # Second half of one stepcycle
            while walk:
                w1 = self.legs["front_right"].curled_forward_move_backward()
                w2 = self.legs["rear_left"].curled_backward_move_forward()
                w3 = self.legs["rear_right"].curled_forward_move_forward()
                w4 = self.legs["front_left"].curled_backward_move_backward()
                
                walk = w1 or w2 or w3 or w4
            steps -= 1

    def curled_turn_right(self, steps):
        '''This makes the crawler turn to the right on tiptoes in on place in a coordinated way. Most of the funktionality lies in the other classes Joint and Leg'''
        while steps > 0:
            walk = True
            # First half of one stepcycle.
            while walk:
                w1 = self.legs["front_right"].curled_backward_move_forward()
                w2 = self.legs["rear_left"].curled_forward_move_backward()
                w3 = self.legs["rear_right"].curled_backward_move_backward()
                w4 = self.legs["front_left"].curled_forward_move_forward()
                walk = w1 or w2 or w3 or w4
            
            walk = True
            # Second half of one stepcycle
            while walk:
                w1 = self.legs["front_right"].curled_backward_move_backward()
                w2 = self.legs["rear_left"].curled_forward_move_forward()
                w3 = self.legs["rear_right"].curled_backward_move_forward()
                w4 = self.legs["front_left"].curled_forward_move_backward()
                
                walk = w1 or w2 or w3 or w4
            steps -= 1


    #############avoid objects#####################

    def _curled_avoid_to_left(self, distance):
        self.curled_turn_left(1)
        while self.us.get_dist() < distance:
            self.curled_turn_left(1)
        self.curled_turn_left(2)
        self.walking_curl()

    def _curled_avoid_to_right(self, distance):
        self.curled_turn_right(1)
        while self.us.get_dist() < distance:
            self.curled_turn_right(1)
        self.curled_turn_right(2)
        self.walking_curl()


    def curled_avoid_objects(self, distance):
        trys = 0
        try:
            while True:
                while self.us.get_dist() > distance:
                    self.curled_move_forward(1)
                
                if trys % 2 == 0:
                    self._curled_avoid_to_right(distance)
                elif trys % 2 == 1:
                    self._curled_avoid_to_left(distance)

                utime.sleep(0.3)
                trys += 1
        except KeyboardInterrupt:
            self.calibrate
            print("program terminated by user")


    #############avoid objects -end-#####################


############################Curled movement -end-############################
          


############################climbing############################
 
    def climb(self, steps):
        '''This makes the crawler climb forward over an object in a coordinated way. Most of the funktionality lies in the other classes Joint and Leg.'''
        while steps > 0:
            walk = True


            # First half of one stepcycle.
            while walk:
                walk = self.legs["front_right"].climb_move_forward()
            walk = True
            
            while walk:
                walk = self.legs["rear_left"].climb_move_forward()
            walk = True

            while walk:
                walk = self.legs["rear_right"].climb_move_backward()
            walk = True

            while walk:
                walk = self.legs["front_left"].climb_move_backward()
            walk = True


            # Second half of one stepcycle
            while walk:
                walk = self.legs["front_right"].climb_move_backward()
            walk = True
            
            while walk:
                walk = self.legs["rear_left"].climb_move_backward()
            walk = True

            while walk:
                walk = self.legs["rear_right"].climb_move_forward()
            walk = True

            while walk:
                walk = self.legs["front_left"].climb_move_forward()
            walk = True
            steps = steps-1
 

#############################climbing -end-############################          


############################offroad############################

    def _lookout(self, distance) -> bool:
        '''This makes he crawler stand on his tiptoes to see if he can climb over an object.'''
        self.curl()
        high_distance = self.us.get_dist()
        low_distance = distance + 5 #avoiding measurement errors by adding a 5cm tolerance
        if high_distance > low_distance:
            return True
        else:
            return False

    def offroad (self, distance):
        trys = 0
        try:
            while True:
                while self.us.get_dist() > distance:
                    self.move_forward(1)
                
                is_object = self._lookout(self.us.get_dist())

                if is_object:
                    self.climb(8)
                else:
                    if trys % 2 == 0:
                        self._avoid_to_right(distance)
                    elif trys % 2 == 1:
                        self._avoid_to_left(distance)

                utime.sleep(0.3)
                trys += 1
        except KeyboardInterrupt:
            self.calibrate
            print("program terminated by user")

    def curled_offroad (self, distance):
        trys = 0
        try:
            while True:
                while self.us.get_dist() > distance:
                    self.curled_move_forward(1)
                
                is_object = self._lookout(self.us.get_dist())

                if is_object:
                    self.climb(8)
                else:
                    if trys % 2 == 0:
                        self._curled_avoid_to_right(distance)
                    elif trys % 2 == 1:
                        self._curled_avoid_to_left(distance)

                utime.sleep(0.3)
                trys += 1
        except KeyboardInterrupt:
            self.calibrate
            print("program terminated by user")



############################offroad -end-############################



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
    
def main():
    '''Starting this file calibrates all servos and then terminates.'''
    try: 
        c = Crawly(True)
        c.offroad(20)
    except KeyboardInterrupt:
        c.park()
        sleep(1)
    
if __name__ == "__main__":
    # execute only if run as a script
    main()