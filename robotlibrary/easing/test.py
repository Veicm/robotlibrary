import math
#from robotlibrary.servo import Servo
import time
def loop(start, stop, angle):
    increment = 2/angle
    i= start
    values = list()
    sum = 0
    while i < stop-increment:
        sum = sum+ ease_in_out_sine(i)
        #print(f"i: {i}, Ease: {ease_in_out_sine(i)}")
        i=i+increment
    #print(sum)
    i=start
    while i < stop-increment:
        #sum = sum+ ease_in_out_quad(i)
        #print(f"i: {i}, Ease: {ease_in_out_sine(i)}")
        values.append(ease_in_out_sine(i)*angle/sum)
        i=i+increment
    sumf = 0.00
    for v in values:
        #print(v)
        sumf = sumf+v
    
    
    #print(sumf)
    #print(sum(values))
    return values
    
class digital_servo():
    def __init__(self, _, a, b, c):
         pass

    def set_angle(self, angle):
        print(f"this is the curend angle {angle}.")

def ease_in_out_quad(t: float) -> float:
        t *= 2
        if t < 1:
            return 0.5 * t * t
        t -= 1
        return -0.5 * (t * (t - 2) - 1)
    
def ease_in_out_sine(t: float) -> float:
        return -0.5 * (math.cos(math.pi * t) - 1)


#print(loop(0,2,90))
#servo = digital_servo()
#servo2 = digital_servo()
angles = loop(0,2,90)

for _ in range (1): 
    for i in range(0,1): #ease loop!!!!!
        tmp=60
        for a in angles:
            tmp = tmp+a
            print(a)
            print(tmp)
            #servo.print_angle(tmp)
            #servo2.print_angle(tmp)
            time.sleep(0.002)
        for a in angles:
            tmp = tmp-a
            print(tmp)
            #servo.print_angle(tmp)
            #servo2.print_angle(tmp)
            time.sleep(0.002)
        
    #for i in range(0,1):
        #print("section------------------------")
        #tmp=60
        #for a in range(0,15):
            #tmp = tmp + a
            #servo.print_angle(tmp)
            #servo2.print_angle(tmp)
            #time.sleep(0.020)
        #for a in range(15,0,-1):
            #tmp = tmp-a
           #servo.print_angle(tmp)
            #servo2.print_angle(tmp)
            #time.sleep(0.020)