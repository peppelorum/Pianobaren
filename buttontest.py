import RPi.GPIO as GPIO


GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering


GPIO.setup(32, GPIO.IN, pull_up_down=GPIO.PUD_UP)

if GPIO.input(32):
    print('Input was HIGH')
else:
    print('Input was LOW')