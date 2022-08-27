import RPi.GPIO as GPIO


class Laser:

    laserPin = 6

    def __init__(self):
        self.setup()

    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.laserPin, GPIO.OUT)

    def on(self):
        GPIO.output(self.laserPin, GPIO.HIGH)

    def off(self):
        GPIO.output(self.laserPin, GPIO.LOW)
