from machine import Pin, PWM
import utime

# notes as frequency's:

A3  = 220
B3  = 247
C4  = 262
Cs4 = 277
D4  = 294
Ds4 = 311
E4  = 330
F4  = 349
Fs4 = 370
G4  = 392
Gs4 = 415
A4  = 440
As4 = 466
B4  = 494
C5  = 523
REST = 0


class Buzzer:
    '''This class manages an active buzzer, you can play a certain tone or a melody of you choice.'''
    def __init__(self, pin):
        self.buzzer = PWM(Pin(9))

        # melody:
        self.mario_melody = [
            (E4, 150), (E4, 150), (REST, 100), (E4, 150),
            (REST, 100), (C4, 150), (E4, 150), (REST, 100), (G4, 300),
            (REST, 300), (G3 := 196, 300), (REST, 300),
    
            (C4, 150), (REST, 100), (G3, 300),
            (REST, 300), (E3 := 165, 300), (REST, 300),

            (A3 := 220, 150), (REST, 100), (B3 := 247, 150), (REST, 100), (As3 := 233, 150), (A3, 150),
            (G3, 150), (E4, 150), (G4, 150), (A4, 300),
            (REST, 150), (F4, 150), (G4, 150),
            (REST, 150), (E4, 150), (C4, 150), (D4, 150), (B3, 300),

            (REST, 200), (C4, 150), (REST, 100), (G3, 300),
            (REST, 300), (E3, 300), (REST, 300),
    
            (A3, 150), (REST, 100), (B3, 150), (REST, 100), (As3, 150), (A3, 150),
            (G3, 150), (E4, 150), (G4, 150), (A4, 300),
    
            (REST, 150), (F4, 150), (G4, 150),
            (REST, 150), (E4, 150), (C4, 150), (D4, 150), (B3, 300)
        ]

        self.zelda_lullaby = [
            (G4, 300), (D4, 300), (E4, 300), (REST, 100),
            (G4, 300), (D4, 300), (E4, 300), (REST, 100),
            (G4, 300), (A4, 300), (B3, 600), (REST, 200),
            (G4, 300), (D4, 300), (E4, 300), (REST, 100),
            (G4, 300), (D4, 300), (E4, 300), (REST, 100),
            (G4, 300), (A4, 300), (B3, 600)
        ]


    def make_sound(self, frequency):
        self.buzzer.freq(frequency)# Hz
        self.buzzer.duty_u16(10000)

    def silence(self):
        '''This function will turn of the buzzer.'''
        self.buzzer.duty_u16(0)
        self.buzzer.deinit()


    def _play_tone(self, frequency, duration_ms):
        '''This function plays a tone in oder to play music.'''
        if frequency == REST:
            self.buzzer.duty_u16(0)
        else:
            self.buzzer.freq(frequency)
            self.buzzer.duty_u16(30000)
        utime.sleep_ms(duration_ms)
        self.buzzer.duty_u16(0)
        utime.sleep_ms(30)

    def play_melody(self, melody: str):
        '''This function is used to play a certain melody.
        You can select between "mario" and "zelda".'''
        if melody == "mario":
            theme = self.mario_melody
        elif melody == "zelda":
            theme = self.zelda_lullaby
        else:
            self.make_sound(100)
            utime.sleep(1)
            self.silence
        for note in theme:
            freq, dur = note
            self._play_tone(freq, dur)
        self.buzzer.deinit()