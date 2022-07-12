import RPi.GPIO as GPIO
import rpyc

conn = rpyc.connect("localhost", 12345)

# class Pin():          # leave this empty
#     def __init__(self):   # constructor function using self
#         self.physicalPin = None  # variable using self.
#         self.pin = None  # variable using self


# Map of pinouts:
# 4 = 7, unload
# 5 = 29, pitch
# 6 = 31, play
# 12 = 32, stop


def unload_cassette(channel):
    print("Unload was pushed!")
    unload = rpyc.async_(conn.root.unload)
    unload()

def pitch(channel):
    print("Pitch was pushed!")
    f = rpyc.async_(conn.root.pitch)
    f()

def play(channel):
    print("Pitch was pushed!")
    f = rpyc.async_(conn.root.play)
    f()

def stop(channel):
    print("Pitch was pushed!")
    f = rpyc.async_(conn.root.pitch)
    f()

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering


GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(7,GPIO.RISING,callback=unload_cassette)

GPIO.setup(29, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(29,GPIO.RISING,callback=pitch)

GPIO.setup(31, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(31,GPIO.RISING,callback=play)



message = input("Press enter to quit\n\n") # Run until someone presses enter

print(message)

GPIO.cleanup() # Clean up