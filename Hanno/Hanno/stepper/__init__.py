# from proximity import Proximity

import RPi.GPIO as GPIO
import itertools
import time


class Stepper:

    stepPins = [
        12, 16, 20, 21
    ]
    hallPin = 15
    rightCycle = [
        (1, 0, 0, 0),
        (0, 1, 0, 0),
        (0, 0, 1, 0),
        (0, 0, 0, 1)
    ]
    leftCycle = [
        (0, 0, 0, 1),
        (0, 0, 1, 0),
        (0, 1, 0, 0),
        (1, 0, 0, 0)
    ]
    currentStep = None
    currentDegree = 0
    goalCount = 0
    delay = 0.005
    degreePerCount = 4.35555556     # Dont change!!!!

    def __init__(self):
        self.GPIO = GPIO
        self.GPIO.setmode(self.GPIO.BCM)
        self.GPIO.setwarnings(False)
        self.GPIO.setup(self.stepPins, self.GPIO.OUT)
        # self.proximity = Proximity()

    def set_stepper(self):
        self.GPIO.output(self.stepPins, self.currentStep)
        time.sleep(self.delay)

    # def home_theta(self):
    #     print("Homing Theta")
    #     leftBound = False
    #     rightBound = False
    #     count = True
    #     while True:
    #         while leftBound == False:
    #             for seq in itertools.cycle(self.leftCycle):
    #                 self.currentStep = seq
    #                 self.set_stepper()
    #                 if self.proximity.fetch_state():
    #                     print("Left Bound.")
    #                     leftBound = True
    #                     break
    #         while count == True:
    #             for seq in itertools.cycle(self.rightCycle):
    #                 self.currentStep = seq
    #                 self.set_stepper()
    #                 count += 1
    #                 if count >= 5:
    #                     print("break buffer")
    #                     count = False
    #         for seq in itertools.cycle(self.rightCycle):
    #             self.currentStep = seq
    #             self.set_stepper()
    #             if self.proximity.fetch_state():
    #                 print("Right Bound.")
    #                 break
    #     return False
                    

    def move_stepper(self, goalDegree=0):
        self.goalCount = round(4 * (goalDegree - self.currentDegree) * self.degreePerCount)
        self.currentDegree = self.currentDegree + goalDegree
        currentCount = 0

        print(f"goalCount: {self.goalCount}")
        print(f"currentDegree: {self.currentDegree}")

        while True:
            if goalDegree <= 180:
                print("moving right...")
                for seq in itertools.cycle(self.rightCycle):
                    self.currentStep = seq
                    self.set_stepper()
                    currentCount += 1
                    # print(f"currentCount: {currentCount}")
                    if currentCount >= self.goalCount:
                        break
                self.goalCount = 0
                break
            else:
                print("moving left...")
                for seq in itertools.cycle(self.leftCycle):
                    self.currentStep = seq
                    self.set_stepper()
                    currentCount += 1
                    # print(f"currentCount: {currentCount}")
                    if currentCount >= self.goalCount:
                        break
                self.goalCount = 0
                break
