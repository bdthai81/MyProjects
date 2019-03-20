import RPi.GPIO as GPIO
import maestro
import time

GPIO.setwarnings(False)
# doing this first, since we're using a while True.
GPIO.cleanup()
# Setup mode to Boardcom config
GPIO.setmode(GPIO.BCM)
# Create mastero controller object
servo = maestro.Controller()


# https://www.pololu.com/docs/0J40/4.a
# PWM values: The periods 1020 (47.1 kHz), 4080 (11.7 kHz), and 16320 (2.9 kHz) provide the best possible resolution with 100% and 0% duty cycle options, so you should use one of these periods if possible.
TARGET_VALUE = 16320
# HC-SR04 ultrasonic sensor has a range from 2cm to 400cm.
# Speed of sound is 340 meter/second => 0.0000588 second/cm
# 0.0000588 * 400 = .02352 seconds => we'll set timeout as .024
TIMEOUT_VALUE = .024
# Max distance in cm
MAX_DISTANCE = 400

# Set trig from servo maestro channel # & maestro controller has channels set as PWM output by default
TRIG_1 = 3
TRIG_2 = 4
TRIG_3 = 5
TRIG_4 = 6
TRIG_5 = 7

# Set echo from GPIO PIN # & setup as Input 
ECHO_1 = 5
ECHO_2 = 6
ECHO_3 = 13
ECHO_4 = 19
ECHO_5 = 26
GPIO.setup(ECHO_1, GPIO.IN)
GPIO.setup(ECHO_2, GPIO.IN)
GPIO.setup(ECHO_3, GPIO.IN)
GPIO.setup(ECHO_4, GPIO.IN)
GPIO.setup(ECHO_5, GPIO.IN)

def get_distance(trig, echo, timeout):
    """
    Parameters
    trig: trigger pin # for sensor output
    echo: echo pin # for sensor input
    timeout: measure in seconds: return 1000cm if timeout

    Return: distance in cm
    """

    timeout += time.time()
    #servo.setAccel(trig, 25)
    servo.setTarget(trig, TARGET_VALUE)
    #time.sleep(0.00001)

    while GPIO.input(echo) == False:
        start = time.time()
        # out of bounds, timed out... gone beyond the sensor's range of 400cm return MAX_DISTANCE set at 400cm
        if start > timeout:
            return MAX_DISTANCE
        
    while GPIO.input(echo) == True:
        end = time.time()

    sig_time = end-start

    #CM: speed of sound is 340 meter/second => 0.0029411second/meter, since we're measuring bounce back x2  => 0.0058822
    # 0.0058822 / 100 for cm => 0.0000588 second/cm
    distance = sig_time / 0.0000588

    #inches: speed of sound is 1130 ft/second
    #distance = sig_time / 0.000148

    return distance


# Sequencial order to trigger each sensor
seq_order_list = [[TRIG_1, ECHO_1], [TRIG_3, ECHO_3], [TRIG_5, ECHO_5], [TRIG_2, ECHO_2], [TRIG_4, ECHO_4]]

def runSensors():
    distance_list = []
    for seq_order in seq_order_list:
        distance = get_distance(seq_order[0], seq_order[1], TIMEOUT_VALUE)
        time.sleep(TIMEOUT_VALUE * 1.05)
        distance_list.append(distance)

    # cleanup
    GPIO.cleanup()
    
    return distance_list