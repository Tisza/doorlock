'''
Servo Library (basically).
'''
try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("ServoServer requires root access.")

import os
import atexit
import config

class Servo(object):
    '''
    Servo controller
    '''
    min_dc = 0
    range_dc = 0
    percent = 0.5
    def __init__(self):
        if (os.geteuid() != 0):
            print("ServoServer requires root access.")
            exit(1)
        GPIO.setmode(GPIO.BOARD)
        if (config.CONTROL < 1 or config.CONTROL > 40):
            print("config.py misconfigured. CONTROL must be a Raspberry Pi Board pinout number.")
            exit(1)
        GPIO.setup(config.CONTROL, GPIO.OUT)
        self.pwm = GPIO.PWM(config.CONTROL, config.FREQ)
        length = 1000 / config.FREQ
        self.min_dc = config.MIN / length * 100
        max_dc = config.MAX / length * 100
        self.range_dc = max_dc - self.min_dc
        self.pwm.start(self.min_dc + self.range_dc * self.percent)
        atexit.register(self.cleanup)
    
    def set_percent(self, percent):
        '''
        Sets the servo to a set percent of the range of motion
        '''
        if (percent < 0):
            percent = 0
        if (percent > 1):
            percent = 1
        self.percent = percent
        self.pwm.ChangeDutyCycle(self.min_dc + self.range_dc * self.percent)

    def get_percent(self):
        '''
        Gets the current set percent for the servo
        '''
        return self.percent

    def cleanup(self):
        '''
        Stops and cleans up the servo
        '''
        self.pwm.stop()
        GPIO.cleanup()
