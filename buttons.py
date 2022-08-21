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
    GPIO.output(13, True)
    pwm.ChangeDutyCycle(duty)
    sleep(1)
    GPIO.output(13, False)
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
    # conn = rpyc.connect("localhost", 12345)
    print("stop was pushed!")
    # f = rpyc.async_(conn.root.pitch)
    # f()

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BCM) # Use physical pin numbering


GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(4,GPIO.RISING,callback=unload_cassette, bouncetime=1500)

GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(5,GPIO.RISING,callback=pitch, bouncetime=1500)

# PLAY
GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(6,GPIO.RISING,callback=play, bouncetime=1500)

# STOP
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(12,GPIO.RISING,callback=stop, bouncetime=1500)

GPIO.setup(13, GPIO.OUT)
pwm=GPIO.PWM(13, 50)

setAngle(90)


message = input("Press enter to quit\n\n") # Run until someone presses enter

print(message)

GPIO.cleanup() # Clean up