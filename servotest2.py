"""
Pi Servo module.
"""
import time

import RPi.GPIO as GPIO


OUT_PIN = 13
PULSE_FREQ = 50

GPIO.setmode(GPIO.BCM)
GPIO.setup(OUT_PIN, GPIO.OUT)

# def SetAngle(angle):
#     duty = angle / 18 + 2
#     GPIO.output(03, True)
#     pwm.ChangeDutyCycle(duty)
#     sleep(1)
#     GPIO.output(03, False)
#     pwm.ChangeDutyCycle(0)


def main():
    print("Starting")
    servo1 = GPIO.PWM(OUT_PIN, PULSE_FREQ)

    servo1.start(0)

    print("Spinning")

    # Test the full range of movement. Note only integers are allowed.
    # for x in range(2, 12):
    #     servo1.ChangeDutyCycle(x)
    #     time.sleep(0.5)

    angle = 90
    duty = angle / 18 + 2

    GPIO.output(OUT_PIN, True)
    servo1.ChangeDutyCycle(duty)
    time.sleep(1)
    GPIO.output(OUT_PIN, False)
    servo1.ChangeDutyCycle(0)

    print(f'{angle}, {duty}')

    # Start over and move in bigger, slower movements.
    # servo1.ChangeDutyCycle(7)
    # time.sleep(10)
    return

    time.sleep(1)
    servo1.ChangeDutyCycle(7)
    time.sleep(1)
    servo1.ChangeDutyCycle(12)
    time.sleep(4)

    # Jump between the opposite positions.
    servo1.ChangeDutyCycle(2)
    time.sleep(1)
    servo1.ChangeDutyCycle(12)
    time.sleep(1)
    servo1.ChangeDutyCycle(2)
    time.sleep(1)
    servo1.ChangeDutyCycle(12)
    time.sleep(4)

    # Test the fastest movement possible - no sleeping.
    servo1.ChangeDutyCycle(2)
    servo1.ChangeDutyCycle(12)
    servo1.ChangeDutyCycle(2)
    servo1.ChangeDutyCycle(12)
    servo1.ChangeDutyCycle(2)
    servo1.ChangeDutyCycle(12)
    servo1.ChangeDutyCycle(2)
    servo1.ChangeDutyCycle(12)

    servo1.stop()
    GPIO.cleanup()


if __name__ == "__main__":
    main()
