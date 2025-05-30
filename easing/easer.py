import math

class Easer:

    def __init__(self) -> None:
        pass


    def ease_in_out_quad(self, t: float) -> float:
        t *= 2
        if t < 1:
            return 0.5 * t * t
        t -= 1
        return -0.5 * (t * (t - 2) - 1)
    
    def ease_in_out_sine(self, t: float) -> float:
        return -0.5 * (math.cos(math.pi * t) - 1)