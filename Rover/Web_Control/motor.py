import RPi.GPIO as gpio
import time

def init():
    gpio.setmode(gpio.BOARD)
    gpio.setup(11, gpio.OUT)
    gpio.setup(12, gpio.OUT)
    gpio.setup(13, gpio.OUT)
    gpio.setup(15, gpio.OUT)

def motion(in_1, in_2, in_3, in_4, tf=0):
    init()
    gpio.output(11, in_1)
    gpio.output(12, in_2)
    gpio.output(13, in_3)
    gpio.output(15, in_4)
    time.sleep(tf)
    
    # continuious motion, if tf is 0
    if tf:
        gpio.cleanup()
    
def stop_motion():
    init()
    gpio.cleanup()

def Forward(tf=0):
    motion(False, True, True, False, tf)
    
def Reverse(tf=0):    
    motion(True, False, False, True, tf)

def Left(tf=0):
    motion(True, True, True, False, tf)
    
def Right(tf=0):
    motion(False, True, False, False, tf)
    
def Pivot_Left(tf=0):
    motion(True, False, True, False, tf)

def Pivot_Right(tf=0):
    motion(False, True, False, True, tf)

