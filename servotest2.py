"""
Pi Servo module.
"""
import time

import RPi.GPIO as GPIO


OUT_PIN = 13
PULSE_FREQ = 50

GPIO.setmode(GPIO.BCM)
GPIO.setup(OUT_PIN, GPIO.OUT)

def main():
    print("Starting")
    servo1 = GPIO.PWM(OUT_PIN, PULSE_FREQ)

    servo1.start(0)

    print("Spinning")

    angle = 90
    duty = angle / 18 + 2

    print(f'{angle}, {duty}')

    GPIO.output(OUT_PIN, True)
    servo1.ChangeDutyCycle(duty)
    time.sleep(1)
    GPIO.output(OUT_PIN, False)
    servo1.ChangeDutyCycle(0)



    servo1.stop()
    GPIO.cleanup()


if __name__ == "__main__":
    main()
