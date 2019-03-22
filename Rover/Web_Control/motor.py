import RPi.GPIO as GPIO
from settings import HB_OUT1, HB_OUT2, HB_OUT3, HB_OUT4
import time

class Motor:
    
    def __init__(self):
        """
        Declare the H-Bridge channels as outputs in GPIO setup
        """
        GPIO.setup(HB_OUT1, GPIO.OUT)
        GPIO.setup(HB_OUT2, GPIO.OUT)
        GPIO.setup(HB_OUT3, GPIO.OUT)
        GPIO.setup(HB_OUT4, GPIO.OUT)

    def motion(self, in1, in2, in3, in4, tf=0):
        """
        Run the motors based off the instruction defined by in1, in2, in3, in4
        tf: time frame to run the motor by second. default=0 -> continuous tf until stop_motion is executed
        """
        GPIO.output(HB_OUT1, in1)
        GPIO.output(HB_OUT2, in2)
        GPIO.output(HB_OUT3, in3)
        GPIO.output(HB_OUT4, in4)
        # Let motors run for tf
        time.sleep(tf)

        # tf is defined > 0, stop motors
        if tf:
            self.stop_motion()

    def stop_motion(self):
        """
        Stop the rover's motors
        """
        self.motion(False, False, False, False)

    def Forward(self, tf=0):
        """
        Run motors forward
        """
        self.motion(False, True, True, False, tf)

    def Reverse(self, tf=0):    
        """
        Run motors reverse
        """
        self.motion(True, False, False, True, tf)

    def Left(self, tf=0):
        """
        Run motors left turn
        """
        self.motion(True, True, True, False, tf)

    def Right(self, tf=0):
        """
        Run motors right turn
        """
        self.motion(False, True, False, False, tf)

    def Pivot_Left(self, tf=0):
        """
        Run motors pivot left
        """
        self.motion(True, False, True, False, tf)

    def Pivot_Right(self, tf=0):
        """
        Run motors pivot right
        """
        self.motion(False, True, False, True, tf)

