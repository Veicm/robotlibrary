import time, gc
from robotlibrary.easing.easer import Easer
from collections import deque
import micropython

class Calculator:

    def __init__(self):
        #micropython.mem_info()
        self.easer = Easer()
        gc.enable()

    def generate_angles(self, start, stop, d_angle):
        '''Calculates the necessary steps for the given angle d_angle to make a smooth movmeent'''
        #print(d_angle)
        gc.collect()
        increment = stop/d_angle #This is one way to determine the increment. Others are better.
        calc_steps = d_angle/increment
        #The bigger the angle, the smaller the increment is noch a good idea.
        # Another possibility: increment = d_angle/100
        i = start
        steps = list()
        sum_steps = 0
        while i < stop-increment:
            sum_steps = sum_steps + self.easer.ease_in_out_sine(i)
            #print(f"i: {i}, Ease: {ease_in_out_sine(i)}")
        
            i=i+increment
        #print(sum_steps)
        i = start
        while i < stop-increment:
            #sum_steps = sum_steps+ ease_in_out_sine(i)
            #print(f"i: {i}, Ease: {ease_in_out_sine(i)}")
            #print(self.easer.ease_in_out_sine(i)*d_angle/sum_steps)
            steps.append(self.easer.ease_in_out_sine(i)*d_angle/sum_steps)
            i=i+increment
        return deque(steps,len(steps))