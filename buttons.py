import RPi.GPIO as GPIO
import rpyc

conn = rpyc.connect("localhost", 12345)

def unload_cassette(channel):
    print("Button was pushed!")

    unload = rpyc.async_(conn.root.unload)
    unload()

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)

GPIO.add_event_detect(12,GPIO.RISING,callback=unload_cassette) # Setup event on pin 10 rising edge

message = input("Press enter to quit\n\n") # Run until someone presses enter

print(message)

GPIO.cleanup() # Clean up