import RPi.GPIO as GPIO
import maestro
import time


# Declar constant global variables
# https://www.pololu.com/docs/0J40/4.b
# Setted channels 13-17 mode to output. The output is low unless the position value is greater than or equal to 1500.00 us.
TARGET_LOW = 992*4  #set for high (VCC) to trigger sensor TRIG
TARGET_HIGH = 1800*4
# HC-SR04 ultrasonic sensor has a range from 2cm to 400cm.
# Speed of sound is 340 meter/second => 0.0000588 second/cm
# 0.0000588 * 400 = .02352 seconds => we'll set timeout as .024
TIMEOUT_VALUE = .024
# Max distance in cm
MAX_DISTANCE = 400

# Create mastero controller object
servo = maestro.Controller()

# Set trig from servo maestro channel # & maestro controller has channels set as PWM output by default
TRIG_1 = 13
TRIG_2 = 14
TRIG_3 = 15
TRIG_4 = 16
TRIG_5 = 17

# Set echo from GPIO BCM # & setup as Input 
ECHO_1 = 5
ECHO_2 = 6
ECHO_3 = 13
ECHO_4 = 19
ECHO_5 = 26


def init():
    # Setup mode to Boardcom SOC channel
    GPIO.setmode(GPIO.BCM)
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

    Return: distance in cm (integer)
    """

    # Fire off TRIG with 5V, then shut it off
    servo.setTarget(trig, TARGET_HIGH)
    time.sleep(0.00001)
    servo.setTarget(trig, TARGET_LOW)

    # Assign timeout value after firing off TRIG
    timeout += time.time()

    # Wait for bounce back echo
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

    return int(distance)


# Sequencial order to trigger each sensor
seq_order_list = [[TRIG_1, ECHO_1], [TRIG_3, ECHO_3], [TRIG_5, ECHO_5], [TRIG_2, ECHO_2], [TRIG_4, ECHO_4]]

def runSensors():
    # init setup gpio
    init()
    
    distance_list = []
    for seq_order in seq_order_list:
        distance = get_distance(seq_order[0], seq_order[1], TIMEOUT_VALUE)
        time.sleep(TIMEOUT_VALUE * 1.5)
        distance_list.append(distance)

    # cleanup
    GPIO.cleanup()
    
    return distance_list



