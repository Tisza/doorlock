try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("ServoServer requires root access.")

import config
import os
import atexit
import time

minDC = 0
rangeDC = 0

def main():
    pwm = init()
    set(pwm, 0)
    time.sleep(1)
    set(pwm, 1)
    time.sleep(1)
    set(pwm, 0.5)
    time.sleep(1)

def init():
    global minDC
    global rangeDC
    if (os.geteuid() != 0):
        print("ServoServer requires root access.")
        exit(1)
    GPIO.setmode(GPIO.BOARD)
    if (config.control < 1 or config.control > 40):
        print("config.py misconfigured. CONTROL must be a Raspberry Pi Board pinout number.")
        exit(1)
    GPIO.setup(config.control, GPIO.OUT)
    pwm = GPIO.PWM(config.control, config.freq)
    length = 1000 / config.freq
    minDC = config.min / length * 100
    maxDC = config.max / length * 100
    rangeDC = maxDC - minDC
    pwm.start(minDC + rangeDC * 0.5)
    atexit.register(cleanup, pwm)
    return pwm

def set(pwm, percent):
    global minDC
    global rangeDC
    if (percent < 0):
        percent = 0
    if (percent > 1):
        percent = 1
    pwm.ChangeDutyCycle(minDC + rangeDC * percent)

def cleanup(pwm):
    pwm.stop()
    GPIO.cleanup()


if __name__ == "__main__":
    main()
