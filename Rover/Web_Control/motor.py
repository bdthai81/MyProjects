import RPi.GPIO as gpio
import time

def init():
    gpio.setmode(gpio.BOARD)
    gpio.setup(11, gpio.OUT)
    gpio.setup(12, gpio.OUT)
    gpio.setup(13, gpio.OUT)
    gpio.setup(15, gpio.OUT)

def motion(tf, in_1, in_2, in_3, in_4):
    init()
    gpio.output(11, in_1)
    gpio.output(12, in_2)
    gpio.output(13, in_3)
    gpio.output(15, in_4)
    time.sleep(tf)
    gpio.cleanup()

def Forward(tf):
    motion(tf, False, True, True, False)
    
def Reverse(tf):    
    motion(tf, True, False, False, True)

def Left(tf):
    motion(tf, True, True, True, False)
    
def Right(tf):
    motion(tf, False, True, False, False)
    
def Pivot_Left(tf):
    motion(tf, True, False, True, False)

def Pivot_Right(tf):
    motion(tf, False, True, False, True)

