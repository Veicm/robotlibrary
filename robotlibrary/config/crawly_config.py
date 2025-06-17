from easing.calculator import Calculator
calc = Calculator()
########## Configuration for the Servos in the Crawly robot
# If you mix different servo types with different duty cycles, you can use the type2 constant for this.
SERVO_MIN_DUTY = 1350 # Change only if the servo doesn't move 180°.
SERVO_MAX_DUTY = 8100 # Change only if the servo doesn't move 180°.
SERVO_MIN_DUTY_TYPE2 = 1800 # In case you use different types of servos with different duty_cycles. You need to change the source code in crawly_joint.py
SERVO_MAX_DUTY_TYPE2 = 7600 # In case you use different types of servos with different duty_cycles. You need to change the source code in crawly_joint.py

########## Configuration for the Servos in the Crawly robot
SHOULDER_FRONT_MIN_ANGLE =  45 # backward motion
SHOULDER_FRONT_MAX_ANGLE = 180 # forward motion
SHOULDER_REAR_MIN_ANGLE =  20 # backward motion
SHOULDER_REAR_MAX_ANGLE = 140 # forward motion
KNEE_MIN_ANGLE = 65 # up motion
KNEE_MAX_ANGLE = 180 # down motion

### Configuration for the movements of Crawly
CRAWLY_FRONT_FORWARD_ANGLE = 130
CRAWLY_FRONT_BACKWARD_ANGLE = 90
CRAWLY_REAR_FORWARD_ANGLE = 90
CRAWLY_REAR_BACKWARD_ANGLE = 50
CRAWLY_UP_ANGLE = 75
CRAWLY_DOWN_ANGLE = 90
# Configuration for the curled walking
CRAWLY_CURLED_UP_ANGLE = 125
CRAWLY_CURLED_DOWN_ANGLE = 140

# Configurations for side walking
CRAWLY_SIDE_WALKING_FRONT_ANGLE = 150
CRAWLY_SIDE_WALKING_REAR_ANGLE = 30
CRAWLY_SIDE_WALKING_CENTER_ANGLE = 90

CRAWLY_SIDE_WALKING_UP_ANGLE = 140
CRAWLY_SIDE_WALKING_DOWN_ANGLE = 170

# Configuration for dancing
CRAWLY_DANCING_FRONT_ANGLE = 150
CRAWLY_DANCING_REAR_ANGLE = 30
CRAWLY_DANCING_CENTER_ANGLE = 90

CRAWLY_DANCING_UP_ANGLE = 120
CRAWLY_DANCING_DOWN_ANGLE = 170

# Buttons
CRAWLY_BUTTON_FRONT = 19
CRAWLY_BUTTON_REAR = 18

PRESSED = 0
UNPRESSED = 1

# Configuration for the Buzzer
CRAWLY_BUZZER = 9 # set None if you don't use it

# Configuration for the WS2812 rainbow lights
CRAWLY_RAINBOW_LIGHT = 22 # set None if you don't use it
CRAWLY_RAINBOW_LIGHT_NUMBER = 2 # defines how many LEDS are on the board

# Distance
CRAWLY_MIN_DISTANCE = 20



### Type definitions
SHOULDER_FRONT = 4
SHOULDER_REAR = 6
KNEE = 8
HIP = 10

# other
US=16
INTERNAL_LED=25

# Eased movement belongings (all variables are deque's)
## Normal/Curl movement
NORMAL_FRONT_STEPS = calc.generate_angles(0, 2, CRAWLY_FRONT_FORWARD_ANGLE - CRAWLY_FRONT_BACKWARD_ANGLE)
NORMAL_REAR_STEPS = calc.generate_angles(0, 2, CRAWLY_REAR_FORWARD_ANGLE - CRAWLY_REAR_BACKWARD_ANGLE)
NORMAL_KNEE_STEPS = calc.generate_angles(0, 2, CRAWLY_DOWN_ANGLE - CRAWLY_UP_ANGLE)

## Side walking movement
SIDE_FRONT_STEPS = calc.generate_angles(0, 2, CRAWLY_SIDE_WALKING_FRONT_ANGLE - CRAWLY_SIDE_WALKING_CENTER_ANGLE)
SIDE_REAR_STEPS = calc.generate_angles(0, 2, CRAWLY_SIDE_WALKING_CENTER_ANGLE - CRAWLY_SIDE_WALKING_REAR_ANGLE)
SIDE_KNEE_STEPS = calc.generate_angles(0, 2, CRAWLY_SIDE_WALKING_DOWN_ANGLE - CRAWLY_SIDE_WALKING_UP_ANGLE)