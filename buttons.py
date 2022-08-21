import RPi.GPIO as GPIO
import rpyc
from time import sleep
from gpiozero import Servo



# Map of pinouts:
# 4 = 7, unload
# 5 = 29, pitch
# 6 = 31, play
# 12 = 32, stop
# 17 = 11, servo


def setAngle(angle):
    # servo = Servo(22)
    # servo.value = 0.5
    duty = angle / 18 + 2
    GPIO.output(33, True)
    pwm.ChangeDutyCycle(duty)
    sleep(1)
    GPIO.output(33, False)
    pwm.ChangeDutyCycle(0)

def unload_cassette(channel):
    # conn = rpyc.connect("localhost", 12345)
    print("Unload was pushed!")

    setAngle(90)
    # unload = rpyc.async_(conn.root.unload)
    # unload()

def pitch(channel):
    conn = rpyc.connect("localhost", 12345)
    print("Pitch was pushed!")
    f = rpyc.async_(conn.root.pitch)
    f()

def play(channel):
    conn = rpyc.connect("localhost", 12345)
    print("play was pushed!")
    f = rpyc.async_(conn.root.play)
    f()

def stop(channel):
    conn = rpyc.connect("localhost", 12345)
    print("stop was pushed!")
    f = rpyc.async_(conn.root.pitch)
    f()

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering


GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(7,GPIO.RISING,callback=unload_cassette, bouncetime=1500)

GPIO.setup(29, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(29,GPIO.RISING,callback=pitch, bouncetime=1500)

GPIO.setup(31, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(31,GPIO.RISING,callback=play, bouncetime=1500)

GPIO.setup(33, GPIO.OUT)
pwm=GPIO.PWM(33, 50)

setAngle(90)


message = input("Press enter to quit\n\n") # Run until someone presses enter

print(message)

GPIO.cleanup() # Clean up