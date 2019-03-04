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

def forward(tf):
    motion(tf, False, True, True, False)
    
def reverse(tf):    
    motion(tf, True, False, False, True)

def turn_left(tf):
    motion(tf, True, True, True, False)
    
def turn_right(tf):
    motion(tf, False, True, False, False)
    
def pivot_left(tf):
    motion(tf, True, False, True, False)

def pivot_right(tf):
    motion(tf, False, True, False, True)

forward(1)
reverse(1)
turn_left(1)
turn_right(1)
pivot_left(1)
pivot_right(1)