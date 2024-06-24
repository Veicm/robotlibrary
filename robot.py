# peripherals
from robotlibrary.motor import Motor
from robotlibrary.ultrasonic import Ultra
from robotlibrary.infrared import IR
from robotlibrary.servo import Servo
import robotlibrary.config

########## Bluetooth
import bluetooth
from robotlibrary.bluetooth.peripheral import BLEPeripheral
from robotlibrary.bluetooth.ble_services_definitions import ROBOT_UUID, MOTOR_RX_UUID, MOTOR_TX_UUID
from robotlibrary.bluetooth.parser import decode_motor, encode_motor
#from robotlibrary.bluetooth.pin_map import MOTOR_LEFT_FORWARD, MOTOR_LEFT_BACKWARD, MOTOR_RIGHT_FORWARD, MOTOR_RIGHT_BACKWARD

from time import sleep


# Version 1.1
import utime, random
class Robot:
    
    def __init__(self,rc):
        '''Initialize the class. The parameters are defined in config.py
        Motors and ultrasonic sensor must use consecutive pins.'''
        if robotlibrary.config.ML is not None: 
            self.ml = Motor(robotlibrary.config.ML)
        if robotlibrary.config.MR is not None:
            self.mr = Motor(robotlibrary.config.MR)
        if robotlibrary.config.US is not None:
            self.us = Ultra(robotlibrary.config.US)
        if robotlibrary.config.IR is not None:
            self.ir = IR(robotlibrary.config.IR,self)
        if robotlibrary.config.SERVO is not None:
            self.servo = Servo(robotlibrary.config.SERVO)
        self.speed = 0
        self.new_speed = 0
        self.last_turn_right = random.randint(0,1) == 0
        if rc:
            self.controller = BLEPeripheral(add_robot_stuff=True)
            self.controller.register_read_callback(MOTOR_RX_UUID, self.read)
            self.controller.advertise()
        
    def read(buffer: memoryview):
        print("read")
        speed, turn, forward = decode_motor(bytes(buffer))
        print(f"Speed: {speed}, Turn: {turn}, forward: {forward}")
        self.set_speed(speed)
        if turn == 0:
            forward()
        elif turn < 0:
            turn_left()
        elif turn > 0:
            turn_right()
        if forward:
            forward()
        else:
            backward()
        to_send = encode_motor(self.speed, 0, True) # Brauche ich das?
        self.controller.send(ROBOT_UUID, MOTOR_TX_UUID, to_send) # Brauche ich das?
        
    def drive(self, dir_l, dir_r):
        '''This abstracted driving function is only called locally by the other functions with better names. '''
        self.ml.set_forward(dir_l)
        self.mr.set_forward(dir_r)
        if self.new_speed < self.speed:
            steps = -1
        else:
            steps = 1
        for i in range(self.speed,self.new_speed,steps):
            self.ml.set_speed(i)
            self.mr.set_speed(i)
            utime.sleep_ms(10+int(i/2))
        self.speed = self.new_speed
        
    def drive_instantly(self,dir_l,dir_r):
        self.ml.set_forward(dir_l)
        self.mr.set_forward(dir_r)
        self.ml.set_speed(self.new_speed)
        self.mr.set_speed(self.new_speed)
        self.speed = self.new_speed
        
    def set_speed(self,s):
        '''Sets the new speed. Doesn't change the driving mode of the robot. '''
        self.ml.set_speed(self.new_speed)
        self.mr.set_speed(self.new_speed)
        self.new_speed = s
        
    def forward(self):
        '''Drive forward. Speed has to be set before with set_speed()'''
        self.drive(True, True)
        
    def backward(self):
        '''Drive forward. Speed has to be set before with set_speed()'''
        self.drive(False, False)

    def spin_right(self, d):
        '''Turn right for the given duration. We cannot determine the angle the robot turns without a compass or gyroscope.'''
        self.drive_instantly(True,False)
        utime.sleep_ms(d)
        self.emergency_stop()
        
    def turn_right(self):
        '''This turns the robot to the right without it spinning on the spot. Each call makes the curve steeper.'''
        new_speed = self.mr.speed -10
        self.ml.set_speed(self.ml.speed + 5)
        self.mr.set_speed(self.ml.speed -5)
    
    def turn_left(self):
        '''This turns the robot to the right without it spinning on the spot. Each call makes the curve steeper.'''
        new_speed = self.ml.speed -10
        self.mr.set_speed(self.mr.speed + 5)
        self.ml.set_speed(self.ml.speed -5)
          
    def spin_before_obstacle(self, distance):
        '''This spins until the distance is greater than distance'''
        self.drive(True,False)
        while self.get_dist() < distance:
            pass
        self.emergency_stop()
            
    def spin_left(self, d):
        '''Turn right for the given duration. We cannot determine the angle the robot turns without a compass or gyroscope.'''
        self.drive_instantly(False,True)
        utime.sleep_ms(d)
        self.emergency_stop()
        
    def toggle_spin(self, d):
        '''Toggle turn for the given duration. We cannot determine the angle the robot turns without a compass or gyroscope.'''
        if self.last_turn_right:
            self.turn_left(d)
        else:
            self.turn_right(d)
        self.last_turn_right = not self.last_turn_right
    
    
    def random_spin(self,d):
        '''Randomly turn for the given duration. We cannot determine the angle the robot turns without a compass or gyroscope.'''
        if random.randint(0,1) == 0:
            self.turn_left(d)
        else:
            self.turn_right(d)
                
    def stop(self):
        '''Stop the robot slowly by deceleration. '''
        self.set_speed(0)
        self.drive(self.ml.forward, self.mr.forward)
        
    def emergency_stop(self):
        '''Stop the robot immediately.'''
        self.ml.set_speed(0)
        self.mr.set_speed(0)
        # self.set_speed(0)
        self.speed = 0
    
    def ir_detected(self, pin, pin_num):
        '''This method is called when the IR-sensor has detected a change. Fill in your code accordingly'''
        if pin.value() == 0:
            print("obstacle detected on pin", pin_num)
        else:
            print("There is no obstacle anymore on pin ", pin_num)
        # self.emergency_stop()
        
    def get_dist(self):
        '''Get the distance from the ultrasonic sensor.'''
        return self.us.get_dist()

    def set_angle(self,a):
        '''If implemented, turn the servo motor with the ultrasonic sensor to the given angle.'''
        self.servo.set_angle(a)
    
    def get_smallest_distance(self):
        '''This returns the angle of the ultrasonic sensor where it measured the smallest distance'''
        self.set_angle(0)
        utime.sleep_ms(500)
        dist_map = {}
        smallest_index=0
        smallest_dist=2000.0
        for i in range(0,180):
            self.set_angle(i)
            dist_map.update({i : self.get_dist()})
        for i,dist in dist_map.items():
            if dist<smallest_dist:
                smallest_index=i
                smallest_dist=dist
        return smallest_index+1

    def get_longest_distance(self):
        '''This returns the angle of the ultrasonic sensor where it measured the longest distance'''
        self.set_angle(0)
        utime.sleep_ms(500)
        dist_map = {}
        longest_index=0
        longest_dist=0.0
        for i in range(0,180):
            self.set_angle(i)
            dist_map.update({i : self.get_dist()})
        for i,dist in dist_map.items():
            if dist>longest_dist:
                longest_index=i
                longest_dist=dist
        return longest_index+1
        
        
