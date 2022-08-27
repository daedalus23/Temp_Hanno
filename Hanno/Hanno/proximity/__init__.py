import RPi.GPIO as GPIO


class Proximity:

    proximityPin = 7

    def __init__(self):
        self.setup()

    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.proximityPin, GPIO.IN)

    def state(self):
        if GPIO.input(self.proximityPin) == GPIO.HIGH:
            return True
        else:
            return False
