# import RPi.GPIO as GPIO
import rpyc
from time import sleep
from gpiozero import Servo, Button, AngularServo



# Map of pinouts:
# 4 = 7, unload
# 5 = 29, pitch
# 6 = 31, play
# 12 = 32, stop
# 17 = 11, servo


servo = AngularServo(17, min_angle=-90, max_angle=90)

unload_button = Button(4, bounce_time=1)
pitch_button = Button(27, bounce_time=1)
annan_button = Button(22, bounce_time=1)

play_button = Button(23, bounce_time=1)
stop_button = Button(24, bounce_time=1)


def setAngle():
    servo.angle = -90
    sleep(2)
    servo.angle = -45
    sleep(2)
    servo.angle = 0
    sleep(2)
    servo.angle = 45
    sleep(2)
    servo.angle = 90
    sleep(2)

    # pass
    # servo = Servo(22)
    # servo.value = 0.5
    # duty = angle / 18 + 2
    # GPIO.output(13, True)
    # pwm.ChangeDutyCycle(duty)
    # sleep(1)
    # GPIO.output(13, False)
    # pwm.ChangeDutyCycle(0)

def unload_cassette(channel):
    # conn = rpyc.connect("localhost", 12345)
    print("Unload was pushed!")

    # setAngle(90)
    # unload = rpyc.async_(conn.root.unload)
    # unload()

def pitch(channel):
    # conn = rpyc.connect("localhost", 12345)
    print("Pitch was pushed!")
    # f = rpyc.async_(conn.root.pitch)
    # f()

def play(channel):
    # conn = rpyc.connect("localhost", 12345)
    print("play was pushed!")
    # f = rpyc.async_(conn.root.play)
    # f()

def stop(channel):
    # conn = rpyc.connect("localhost", 12345)
    print("stop was activated!")
    # f = rpyc.async_(conn.root.pitch)
    # f()



unload_button.when_pressed = unload_cassette
pitch_button.when_pressed = pitch
play_button.when_pressed = play
stop_button.when_released = stop




# setAngle(90)

servo.angle = 0


message = input("Press enter to quit\n\n") # Run until someone presses enter

print(message)

# GPIO.cleanup() # Clean up