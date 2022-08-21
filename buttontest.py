


from signal import pause
from time import sleep
from gpiozero import Button


button = Button(13)


def unload():
    print('unload')

button.when_pressed = unload
pause()



# import RPi.GPIO as GPIO

# GPIO.setwarnings(False) # Ignore warning for now
# GPIO.setmode(GPIO.BCM) # Use physical pin numbering

# GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# if GPIO.input(12):
#      print('Input was HIGH')
# else:
#      print('Input was LOW')