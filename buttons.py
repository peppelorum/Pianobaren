# import RPi.GPIO as GPIO
import rpyc
from time import sleep
# from gpiozero import Device, Servo, Button, AngularServo
from gpiozero import Button
# from gpiozero.pins.native import NativeFactory
# from gpiozero.pins.pigpio import PiGPIOFactory
# from gpiozero import Device, LED

# Device.pin_factory = PiGPIOFactory()
# my_factory = PiGPIOFactory()

from debounce import debounce



# Map of pinouts:
# 4 = 7, unload
# 5 = 29, pitch
# 6 = 31, play
# 12 = 32, stop
# 17 = 11, servo


# servo = AngularServo(5, min_angle=-90, max_angle=180)

unload_button = Button(4) #1
pitch_button = Button(17) #2
annan_button = Button(18) #3

eject_button = Button(16)

pause_button = Button(2)
play_button = Button(23)
stop_button = Button(24)
ff_button = Button(25)

# @debounce(0.2)
# def unload_cassette():
#     print("Unload was pushed!")

#     servo.angle = 180
#     sleep(2)
#     servo.angle = 0
#     sleep(2)
#     servo.detach()

#     conn = rpyc.connect("localhost", 12345)
#     unload = rpyc.async_(conn.root.unload)
#     unload()

@debounce(0.2)
def pitch():
    print("Pitch was pushed!")
    conn = rpyc.connect("localhost", 12345)
    f = rpyc.async_(conn.root.pitch)
    f()

@debounce(0.2)
def play():
    print("play was pushed!")
    conn = rpyc.connect("localhost", 12345)
    f = rpyc.async_(conn.root.play)
    f()

@debounce(0.2)
def stop():
    print("stop was activated!")
    conn = rpyc.connect("localhost", 12345)
    f = rpyc.async_(conn.root.stop)
    f()


@debounce(0.2)
def nest():
    print("next was activated!")
    conn = rpyc.connect("localhost", 12345)
    f = rpyc.async_(conn.root.nest)
    f()


ff_button.when_pressed = nest
unload_button.when_pressed = unload_cassette
pitch_button.when_pressed = pitch
play_button.when_pressed = play
stop_button.when_released = stop
# eject_button.when_pressed = unload_cassette
# eject_button.when_released = None



# servo.angle = 0
# servo.detach()

print('buttons up and running')


while True:
    sleep(10)
