""" 
This file sets all the channel variables in rPi GPIO, H-Bridge, and Pololu Maestro Servo Controller
"""

"""
Direct wire from GPIO to Pololu Maestro Servo Controller (establish commuication)
GND (GPIO PIN 6) -> GND (Maestro)
Rx (GPIO 14) -> Tx (Maestro)
Tx (GPIO 15) -> Rx (Maestro)
Board power fed together with servo power 
"""

### GPIO settings ###
# Output channels to H-Bridge
HB_OUT1 = 17
HB_OUT2 = 18
HB_OUT3 = 27
HB_OUT4 = 22

# Inputs channels for echo from HC-SR04
ECHO1 = 5
ECHO2 = 6
ECHO3 = 13
ECHO4 = 19
ECHO5 = 26

### Pololu Maestro Servo Controller settings ###
# Output channels for camera tilt: Horizontal & Vertical (left default mode at "PWM")
H_SERVO = 0
V_SERVO = 1

"""
First element and last element are the minimum and maxium positions for the servos
in quarter-microseconds. The defaults are set on the board. See the Maestro
manual for how to change these values. The factory defaults are 992us and
2000us.
Allowing quarter-microseconds gives you more resolution to work with.
e.g. If you want a maximum of 2000us then use 8000us (4 x 2000us).
"""

# Changed range in Pololu maestro control center to 656-2480 [right, center, left]
H_POS = [656*4, 1500*4, 2480*4]
# Changed range in Pololu maestro control center to 1296-2096 [down, center, up]
V_POS = [1296*4, 1700*4, 2096*4]

# Output channels for trig from HC-SR04 (set Maestro mode to "output" using Maestro Control Center)
TRIG1 = 13
TRIG2 = 14
TRIG3 = 15
TRIG4 = 16
TRIG5 = 17
