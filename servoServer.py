try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("ServoServer requires root access.")

import config
import os
import atexit
import time

class Servo:
    minDC = 0
    rangeDC = 0
    percent = 0.5
    def __init__(self):
        if (os.geteuid() != 0):
            print("ServoServer requires root access.")
            exit(1)
        GPIO.setmode(GPIO.BOARD)
        if (config.control < 1 or config.control > 40):
            print("config.py misconfigured. CONTROL must be a Raspberry Pi Board pinout number.")
            exit(1)
        GPIO.setup(config.control, GPIO.OUT)
        self.pwm = GPIO.PWM(config.control, config.freq)
        length = 1000 / config.freq
        self.minDC = config.min / length * 100
        maxDC = config.max / length * 100
        self.rangeDC = maxDC - self.minDC
        self.pwm.start(self.minDC + self.rangeDC * self.percent)
        atexit.register(self.cleanup)
    
    def set_percent(self, percent):
        if (percent < 0):
            percent = 0
        if (percent > 1):
            percent = 1
        self.percent = percent
        self.pwm.ChangeDutyCycle(self.minDC + self.rangeDC * self.percent)

    def get_percent(self):
        return self.percent

    def cleanup(self):
        self.pwm.stop()
        GPIO.cleanup()
