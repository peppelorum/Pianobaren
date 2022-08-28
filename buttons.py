# import RPi.GPIO as GPIO
import rpyc
from time import sleep
from gpiozero import Device, Servo, Button, AngularServo
# from gpiozero.pins.native import NativeFactory
# from gpiozero.pins.pigpio import PiGPIOFactory
# from gpiozero import Device, LED

# Device.pin_factory = PiGPIOFactory()
# my_factory = PiGPIOFactory()


import threading

from debounce import debounce

def hello():
    print('hello, world')
    sleep(2)



servo = AngularServo(12, min_angle=-90, max_angle=180)

unload_button = Button(4) #1
pitch_button = Button(5) #2
annan_button = Button(6) #3

eject_button = Button(13)

pause_button = Button(22)
play_button = Button(23)
stop_button = Button(24)
ff_button = Button(25)

@debounce(0.2)
def unload_cassette():
    print("Unload was pushed!")

    servo.angle = 180
    sleep(2)
    servo.angle = 0
    sleep(2)
    servo.detach()

    conn = rpyc.connect("localhost", 12345)
    unload = rpyc.async_(conn.root.unload)
    unload()

@debounce(0.2)
def pitch():
    print("Pitch was pushed!")
    conn = rpyc.connect("localhost", 12345)
    f = rpyc.async_(conn.root.pitch)
    f()

@debounce(0.2)
def play():
    t.cancel()
    print("play was pushed!")
    conn = rpyc.connect("localhost", 12345)
    f = rpyc.async_(conn.root.play)
    f()

@debounce(0.2)
def pause():
    t.cancel()
    print("pause was pushed!")
    conn = rpyc.connect("localhost", 12345)

    f = rpyc.async_(conn.root.stop)
    f()


@debounce(0.2)
def unpause():
    t.cancel()
    print("unpause!")
    conn = rpyc.connect("localhost", 12345)

    f = rpyc.async_(conn.root.play)
    f()

@debounce(0.2)
def stop_button_pretrigger():
    print("stop was activated!")
    newTimer()
    t.start()


def stop():
    print('stop was executed')
    conn = rpyc.connect("localhost", 12345)
    f = rpyc.async_(conn.root.stop)
    f()

t = threading.Timer(1.0, stop)

def newTimer():
    global t
    t = threading.Timer(3.0, stop)



@debounce(0.2)
def nest():
    t.cancel()
    print("next was activated!")
    print('stop was canceled')

    # (lambda x:(x % 2 and 'odd' or 'even'))(3)

    conn = rpyc.connect("localhost", 12345)
    f = rpyc.async_(conn.root.nest)
    f()

# var = 'something'
# if var == 'something':
#     t.cancel()


ff_button.when_pressed = nest
unload_button.when_pressed = unload_cassette
pitch_button.when_pressed = pitch

play_button.when_pressed = play
stop_button.when_released = stop_button_pretrigger
pause_button.when_pressed = pause
pause_button.when_released = unpause

# eject_button.when_pressed = unload_cassette
# eject_button.when_released = None



servo.angle = 0
servo.detach()

print('buttons up and running')


while True:
    sleep(10)
