


from signal import pause
from time import sleep
from gpiozero import Button


unload_button = Button(4)
pitch_button = Button(13)
annan_button = Button(15)


def unload():
    print('unload')

def pitch():
    print('pitch')

def annan():
    print('annan')

unload_button.when_pressed = unload
pitch_button.when_prssed = pitch
annan_button.when_prssed = annan


pause()



# import RPi.GPIO as GPIO

# GPIO.setwarnings(False) # Ignore warning for now
# GPIO.setmode(GPIO.BCM) # Use physical pin numbering

# GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# if GPIO.input(12):
#      print('Input was HIGH')
# else:
#      print('Input was LOW')