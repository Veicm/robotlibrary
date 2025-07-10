# peripherals
from robotlibrary.servo import Servo
import robotlibrary.config.crawly_config as conf
from time import sleep, sleep_ms
from robotlibrary.easing.calculator import Calculator

class Joint:
    # FRONT_FORWARD_ANGLE = 130
    # FRONT_BACKWARD_ANGLE = 90
    # REAR_FORWARD_ANGLE = 90
    # REAR_BACKWARD_ANGLE = 50
    # UP_ANGLE = 75
    # DOWN_ANGLE = 90
    def __init__(self, j_type, name, left_side, inverted, pin):
        '''Initialize a joint in the Crawly robot. 
        Explanation of parameters: 
        j_type: Short for joint_type. Can be conf.SHOULDER_FRONT, conf.SHOULDER_REAR, 
            conf.KNEE
        name: The name of the joint. Use something useful like "front_right". 
        left_side: True or False. Servo motors on the left side need to be inverted in the code. 
        inverted: There are servo motors that turn in a different direction than other. In this case, set to True.
        pin: The pin number that controls the servo motor. 
        '''
        self.name = name
        self.j_type = j_type
        min_duty = conf.SERVO_MIN_DUTY
        max_duty = conf.SERVO_MAX_DUTY
        self.left_side = left_side
        if j_type == conf.SHOULDER_FRONT:
            self.__min_angle = conf.SHOULDER_FRONT_MIN_ANGLE
            self.__max_angle = conf.SHOULDER_FRONT_MAX_ANGLE
        elif j_type == conf.SHOULDER_REAR:
            self.__min_angle = conf.SHOULDER_REAR_MIN_ANGLE
            self.__max_angle = conf.SHOULDER_REAR_MAX_ANGLE
        elif j_type == conf.KNEE:
            self.__min_angle = conf.KNEE_MIN_ANGLE
            self.__max_angle = conf.KNEE_MAX_ANGLE
            min_duty = conf.SERVO_MIN_DUTY_TYPE2 # Comment out if the duty cycle is not different from the shoulder servo's duty cycle.
            max_duty = conf.SERVO_MAX_DUTY_TYPE2 # Comment out if the duty cycle is not different from the shoulder servo's duty cycle.
        self.servo = Servo(pin, inverted, min_duty, max_duty)
        self.calc = Calculator()
          
    @property
    def min_angle(self):
        return self.__min_angle

    @min_angle.setter
    def set_min_angle(self, a):
        self.__min_angle = a

    @property
    def max_angle(self):
        return self.__max_angle

    @max_angle.setter
    def set_max_angle(self, a):
        self.__max_angle = a

    def get_angles(self):
        '''This is called before each new leg movement cycle to refresh all values.'''
        self.normal_front_steps = self.calc.generate_angles(0, 2, conf.CRAWLY_FRONT_FORWARD_ANGLE - conf.CRAWLY_FRONT_BACKWARD_ANGLE)
        self.normal_rear_steps = self.calc.generate_angles(0, 2, conf.CRAWLY_REAR_FORWARD_ANGLE - conf.CRAWLY_REAR_BACKWARD_ANGLE)
        self.normal_knee_steps = self.calc.generate_angles(0, 2, conf.CRAWLY_DOWN_ANGLE - conf.CRAWLY_UP_ANGLE)

        self.side_front_steps = self.calc.generate_angles(0, 2, conf.CRAWLY_SIDE_WALKING_FRONT_ANGLE - conf.CRAWLY_SIDE_WALKING_CENTER_ANGLE)
        self.side_rear_steps = self.calc.generate_angles(0, 2, conf.CRAWLY_SIDE_WALKING_CENTER_ANGLE - conf.CRAWLY_SIDE_WALKING_REAR_ANGLE)
        self.side_knee_steps = self.calc.generate_angles(0, 2, conf.CRAWLY_SIDE_WALKING_DOWN_ANGLE - conf.CRAWLY_SIDE_WALKING_UP_ANGLE)
        

    def up(self) -> bool:
        '''If this object is a knee, it is moved up in one go. As the movement is then finished, it 
        returns False. 
        '''
        if self.j_type == conf.KNEE and self.servo.angle > conf.CRAWLY_UP_ANGLE and len(self.normal_knee_steps) > 0:
            self.servo.set_angle(self.servo.angle - self.normal_knee_steps.popleft())
            if self.servo.angle < conf.CRAWLY_DOWN_ANGLE - (conf.CRAWLY_DOWN_ANGLE - conf.CRAWLY_UP_ANGLE)/3:
                return False
            else:
                return True
        return False
    
    def down(self) -> bool:
        '''If this object is a knee, it is moved down in one go. As the movement is then finished, it 
        returns False. 
        '''
        if self.j_type == conf.KNEE and self.servo.angle < conf.CRAWLY_DOWN_ANGLE and len(self.normal_knee_steps) != 0:       
            self.servo.set_angle(self.servo.angle + self.normal_knee_steps.popleft())
            if self.servo.angle > conf.CRAWLY_UP_ANGLE + (conf.CRAWLY_DOWN_ANGLE - conf.CRAWLY_UP_ANGLE)/3:
                return False
            else:
                return True
        return False

############################curled movement############################
    def curled_up(self) -> bool:
        '''If this object is a knee, it is moved up in one go. As the movement is then finished, it 
        returns False. It is needed for curled walking.
        '''
        if self.j_type == conf.KNEE and self.servo.angle > conf.CRAWLY_CURLED_UP_ANGLE and len(self.normal_knee_steps) != 0:
            self.servo.set_angle(self.servo.angle - self.normal_knee_steps.popleft())
            if self.servo.angle < conf.CRAWLY_CURLED_DOWN_ANGLE - (conf.CRAWLY_CURLED_DOWN_ANGLE - conf.CRAWLY_CURLED_UP_ANGLE)/3:
                return False
            else:
                return True
        return False
    
    def curled_down(self) -> bool:
        '''If this object is a knee, it is moved down in one go. As the movement is then finished, it 
        returns False. It is needed for curled walking.
        '''
        if self.j_type == conf.KNEE and self.servo.angle < conf.CRAWLY_CURLED_DOWN_ANGLE and len(self.normal_knee_steps) != 0:
            self.servo.set_angle(self.servo.angle + self.normal_knee_steps.popleft())
            if self.servo.angle > conf.CRAWLY_CURLED_UP_ANGLE + (conf.CRAWLY_CURLED_DOWN_ANGLE - conf.CRAWLY_CURLED_UP_ANGLE)/3:
                return False
            else:
                return True
        return False
    
############################curled movement -end-############################

    def forward(self) -> bool:
        '''See the documentation for crawly_leg.py for information.'''
        if not self.left_side:
            if self.j_type == conf.SHOULDER_FRONT and self.servo.angle > conf.CRAWLY_FRONT_BACKWARD_ANGLE and len(self.normal_front_steps) != 0:
                self.servo.set_angle(self.servo.angle - self.normal_front_steps.popleft())
                return True
            if self.j_type == conf.SHOULDER_REAR and self.servo.angle > conf.CRAWLY_REAR_BACKWARD_ANGLE and len(self.normal_rear_steps) != 0:
                self.servo.set_angle(self.servo.angle - self.normal_rear_steps.popleft())
                return True
            return False
        else:
            if self.j_type == conf.SHOULDER_FRONT and self.servo.angle < 180-conf.CRAWLY_FRONT_BACKWARD_ANGLE and len(self.normal_front_steps) != 0:
                self.servo.set_angle(self.servo.angle + self.normal_front_steps.popleft())
                return True
            if self.j_type == conf.SHOULDER_REAR and self.servo.angle < 180-conf.CRAWLY_REAR_BACKWARD_ANGLE and len(self.normal_rear_steps) != 0:
                self.servo.set_angle(self.servo.angle + self.normal_rear_steps.popleft())
                return True
            return False

    def backward(self) -> bool:
        '''See the documentation for crawly_leg.py for information.'''
        if not self.left_side:
            if self.j_type == conf.SHOULDER_FRONT and self.servo.angle < conf.CRAWLY_FRONT_FORWARD_ANGLE and len(self.normal_front_steps) != 0:
                self.servo.set_angle(self.servo.angle + self.normal_front_steps.popleft())
                return True
            if self.j_type == conf.SHOULDER_REAR and self.servo.angle < conf.CRAWLY_REAR_FORWARD_ANGLE and len(self.normal_rear_steps) != 0:
                self.servo.set_angle(self.servo.angle + self.normal_rear_steps.popleft())
                return True
            return False
        else:
            if self.j_type == conf.SHOULDER_FRONT and self.servo.angle > 180-conf.CRAWLY_FRONT_FORWARD_ANGLE and len(self.normal_front_steps) != 0:
                self.servo.set_angle(self.servo.angle - self.normal_front_steps.popleft())
                return True
            if self.j_type == conf.SHOULDER_REAR and self.servo.angle > 180-conf.CRAWLY_REAR_FORWARD_ANGLE and len(self.normal_rear_steps) != 0:
                self.servo.set_angle(self.servo.angle - self.normal_rear_steps.popleft())
                return True
            return False

    
############################side walking############################

    def side_walking_up(self) -> bool:
        '''If this object is a knee, it is moved slowly. As the movement is then finished, it 
        returns False. 
        '''
        if self.j_type == conf.KNEE and self.servo.angle > conf.CRAWLY_SIDE_WALKING_UP_ANGLE:
            self.servo.set_angle(conf.CRAWLY_SIDE_WALKING_UP_ANGLE)
            if self.servo.angle < conf.CRAWLY_SIDE_WALKING_DOWN_ANGLE - (conf.CRAWLY_SIDE_WALKING_DOWN_ANGLE - conf.CRAWLY_SIDE_WALKING_UP_ANGLE)/3:
                return False
            else:
                return True
        return False
    
    def side_walking_down(self) -> bool:
        '''If this object is a knee, it is moved down slowly. As the movement is then finished, it 
        returns False. 
        '''
        if self.j_type == conf.KNEE and self.servo.angle < conf.CRAWLY_SIDE_WALKING_DOWN_ANGLE:
            self.servo.set_angle(conf.CRAWLY_SIDE_WALKING_DOWN_ANGLE)
            if self.servo.angle < conf.CRAWLY_SIDE_WALKING_UP_ANGLE - (conf.CRAWLY_SIDE_WALKING_DOWN_ANGLE - conf.CRAWLY_SIDE_WALKING_UP_ANGLE)/3:
                return False
            else:
                return True
        return False


    def ahead(self) -> bool:
        '''See the documentation for crawly_leg.py for information.'''
        if not self.left_side:
            if self.j_type == conf.SHOULDER_FRONT and self.servo.angle < conf.CRAWLY_SIDE_WALKING_FRONT_ANGLE:
                self.servo.set_angle(self.servo.angle + 2)
                return True
            if self.j_type == conf.SHOULDER_REAR and self.servo.angle > conf.CRAWLY_SIDE_WALKING_REAR_ANGLE:
                self.servo.set_angle(self.servo.angle - 2)
                return True
            return False
        else:
            if self.j_type == conf.SHOULDER_FRONT and self.servo.angle > 180-conf.CRAWLY_SIDE_WALKING_FRONT_ANGLE:
                self.servo.set_angle(self.servo.angle - 2)
                return True
            if self.j_type == conf.SHOULDER_REAR and self.servo.angle < 180-conf.CRAWLY_SIDE_WALKING_REAR_ANGLE:
                self.servo.set_angle(self.servo.angle + 2)
                return True
            return False

    def center(self) -> bool:
        '''See the documentation for crawly_leg.py for information.'''
        if not self.left_side:
            if self.j_type == conf.SHOULDER_FRONT and self.servo.angle > conf.CRAWLY_SIDE_WALKING_CENTER_ANGLE:
                self.servo.set_angle(self.servo.angle - 2)
                return True
            if self.j_type == conf.SHOULDER_REAR and self.servo.angle < conf.CRAWLY_SIDE_WALKING_CENTER_ANGLE:
                self.servo.set_angle(self.servo.angle + 2)
                return True
            return False
        else:
            if self.j_type == conf.SHOULDER_FRONT and self.servo.angle < 180-conf.CRAWLY_SIDE_WALKING_CENTER_ANGLE:
                self.servo.set_angle(self.servo.angle + 2)
                return True
            if self.j_type == conf.SHOULDER_REAR and self.servo.angle > 180-conf.CRAWLY_SIDE_WALKING_CENTER_ANGLE:
                self.servo.set_angle(self.servo.angle - 2)
                return True
            return False


############################side walking -end-############################

    
###########################Dancing############################
        
    def dancing_up(self):
        '''If this object is a knee, it is moved slowly. As the movement is then finished, it 
        returns False. 
        '''
        if self.j_type == conf.KNEE:
            self.servo.set_angle(conf.CRAWLY_DANCING_UP_ANGLE)
        return False
    
    def dancing_down(self):
        '''If this object is a knee, it is moved down slowly. As the movement is then finished, it 
        returns False. 
        '''
        if self.j_type == conf.KNEE:
            self.servo.set_angle(conf.CRAWLY_DANCING_DOWN_ANGLE)
        return False


    def dancing_ahead(self) -> bool:
        '''See the documentation for crawly_leg.py for information.'''
        if not self.left_side:
            if self.j_type == conf.SHOULDER_FRONT and self.servo.angle < conf.CRAWLY_DANCING_FRONT_ANGLE:
                self.servo.set_angle(self.servo.angle + 2)
                return True
            if self.j_type == conf.SHOULDER_REAR and self.servo.angle > conf.CRAWLY_DANCING_REAR_ANGLE:
                self.servo.set_angle(self.servo.angle - 2)
                return True
            return False
        else:
            if self.j_type == conf.SHOULDER_FRONT and self.servo.angle > 180-conf.CRAWLY_DANCING_FRONT_ANGLE:
                self.servo.set_angle(self.servo.angle - 2)
                return True
            if self.j_type == conf.SHOULDER_REAR and self.servo.angle < 180-conf.CRAWLY_DANCING_REAR_ANGLE:
                self.servo.set_angle(self.servo.angle + 2)
                return True
            return False

    def dancing_center(self) -> bool:
        '''See the documentation for crawly_leg.py for information.'''
        if not self.left_side:
            if self.j_type == conf.SHOULDER_FRONT and self.servo.angle > conf.CRAWLY_DANCING_CENTER_ANGLE:
                self.servo.set_angle(self.servo.angle - 2)
                return True
            if self.j_type == conf.SHOULDER_REAR and self.servo.angle < conf.CRAWLY_DANCING_CENTER_ANGLE:
                self.servo.set_angle(self.servo.angle + 2)
                return True
            return False
        else:
            if self.j_type == conf.SHOULDER_FRONT and self.servo.angle < 180-conf.CRAWLY_DANCING_CENTER_ANGLE:
                self.servo.set_angle(self.servo.angle + 2)
                return True
            if self.j_type == conf.SHOULDER_REAR and self.servo.angle > 180-conf.CRAWLY_DANCING_CENTER_ANGLE:
                self.servo.set_angle(self.servo.angle - 2)
                return True
            return False
        
        
###########################Dancing -end-############################



    def park(self):
        if self.j_type == conf.KNEE:
            self.servo.set_angle(self.min_angle)
        elif self.j_type == conf.SHOULDER_FRONT:
            if not self.left_side: 
                self.servo.set_angle(self.max_angle)
            else:
                self.servo.set_angle(180-self.max_angle)
        else:
            if not self.left_side: 
                self.servo.set_angle(self.min_angle)
            else:
                self.servo.set_angle(180-self.min_angle)
    
    def curl(self):
        if self.j_type == conf.KNEE:
            self.servo.set_angle(self.max_angle)
        elif self.j_type == conf.SHOULDER_FRONT or self.j_type == conf.SHOULDER_REAR:
            self.servo.set_angle(90)
              
    def walking_curl(self):
        if self.j_type == conf.KNEE:
            self.servo.set_angle(conf.CRAWLY_CURLED_DOWN_ANGLE)
        elif self.j_type == conf.SHOULDER_FRONT or self.j_type == conf.SHOULDER_REAR:
            self.servo.set_angle(90)
                
    def tap(self):
        '''If this joint is a knee, it is tapped three times.'''
        if self.j_type == conf.KNEE:
            for i in range(3):
                self.servo.set_angle(85)
                sleep_ms(50)
                self.servo.set_angle(70)
                sleep_ms(50)
            
    def calibrate(self):
        self.servo.set_angle(0)
        sleep_ms(500)
        self.servo.set_angle(90)
        
    def __set_angle(self,a):
        if not self.left_side:
            self.servo.set_angle(a)
            #print(f"Angle right: {a}") # Uncomment for debug messages.
        else:
            self.servo.set_angle(180-a)
            #print(f"Angle left: {a}") # Uncomment for debug messages.
        
def main():    
    '''Executed, this sets all servos to 90°.'''
    j = Joint(conf.KNEE, "rear left", True, True, 7)
    j.__set_angle(0)
    
if __name__ == "__main__":
    # execute only if run as a script
    main()