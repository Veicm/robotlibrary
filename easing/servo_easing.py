from machine import PWM, Pin

class Servo:
    def __init__(self, pin_number, min_us=500, max_us=2500, freq=50):
        self.pin = pin_number
        self.pwm = PWM(Pin(pin_number))
        self.pwm.freq(freq)
        self.min_us = min_us
        self.max_us = max_us
        self.freq = freq
        self._angle = 0  # interner Zustand

    def set_angle(self, angle):
        """ Setzt den Winkel des Servos """
        if angle < 0: angle = 0
        if angle > 180: angle = 180
        self._angle = angle
        us = self.min_us + (self.max_us - self.min_us) * angle / 180
        duty = int(us * 65535 * self.freq // 1000000)
        self.pwm.duty_u16(duty)

    def __angle(self, angle=None):
        """ Getter und Setter für Winkel über __angle() """
        if angle is None:
            return self._angle
        else:
            self.set_angle(angle)

    def calibrate(self, calibration=None):
        """ Optional: Kalibriert min/max Pulsbreiten """
        if calibration:
            self.min_us, self.max_us = calibration
        return (self.min_us, self.max_us)
