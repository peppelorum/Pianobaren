# import RPi.GPIO as GPIO
from unittest import case
import rpyc

conn = rpyc.connect("localhost", 12345)

def unload_cassette():
    print("Button was pushed!")

    unload = rpyc.async_(conn.root.unload)
    unload()

def play():
    print("Button was pushed!")

    play = rpyc.async_(conn.root.play)
    play()

def cmd():
    print("Button was pushed!")

    ff = rpyc.async_(conn.root.ff)
    ff()

def pitch():
    print("Pitch was pushed!")

    pitch = rpyc.async_(conn.root.pitch)
    pitch()

# GPIO.setwarnings(False) # Ignore warning for now
# GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
# GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)

# GPIO.add_event_detect(10,GPIO.RISING,callback=unload_cassette) # Setup event on pin 10 rising edge

message = input("Press enter to quit\n\n") # Run until someone presses enter


if message == 'pause':
    unload_cassette()
elif message == 'play':
    play()
elif message == 'ff':
    cmd()
elif message == 'pitch':
    pitch()


print(message)

# GPIO.cleanup() # Clean up