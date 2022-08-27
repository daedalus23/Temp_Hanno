import RPi.GPIO as GPIO
import time as time

servoPin = 8

GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPin, GPIO.OUT)
GPIO.setwarnings(False)


def servo_cycle():
    p = GPIO.PWM(servoPin, 50) # PWM with 50Hz
    p.start(0) # Initialization
    top = 11
    bottom = 1.1
    setpoint = 1.0
    cycleDelay = 0.1
    try:
        while True:
            while setpoint <= top:
                if setpoint >= bottom:
                    p.ChangeDutyCycle(setpoint)
                    print(f"Current Setpoint: {setpoint}")
                setpoint += 0.1
                time.sleep(cycleDelay)
            while setpoint >= bottom:
                if setpoint <= top:
                    p.ChangeDutyCycle(setpoint)
                    print(f"Current Setpoint: {setpoint}")
                setpoint -= 0.1
                time.sleep(cycleDelay)
    except KeyboardInterrupt:
        p.stop()
        GPIO.cleanup()


def manual_move():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servoPin, GPIO.OUT)
    GPIO.setwarnings(False)

    p = GPIO.PWM(servoPin, 50) # PWM with 50Hz
    p.start(0) # Initialization
    try:
        setpoint = float(input("Enter setpoint value: "))
        p.ChangeDutyCycle(setpoint)
        time.sleep(0.1)
    except KeyboardInterrupt:
        p.stop()
        GPIO.cleanup()
