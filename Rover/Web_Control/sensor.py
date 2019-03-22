import RPi.GPIO as GPIO
import maestro
from settings import TRIG1, TRIG2, TRIG3, TRIG4,TRIG5, ECHO1, ECHO2, ECHO3, ECHO4, ECHO5
import time

class Sensor:
    
    def __init__(self):
        """ 
        Initialize variables
        """
        # Declare the GPIO Echo channels as inputs in GPIO setup
        GPIO.setup(ECHO1, GPIO.IN)
        GPIO.setup(ECHO2, GPIO.IN)
        GPIO.setup(ECHO3, GPIO.IN)
        GPIO.setup(ECHO4, GPIO.IN)
        GPIO.setup(ECHO5, GPIO.IN)
        # Declare mastero controller object
        self.servo = maestro.Controller()
        """
        The output is low unless the position value is greater than or equal to 1500.00 us.
        (https://www.pololu.com/docs/0J40/4.b)
        The servos are in quarter-microseconds. So, we'll have to multiply by 4.
        """
        self.__TARGET_LOW = 992*4  
        self.__TARGET_HIGH = 1800*4 # set for high (VCC) to trigger sensor TRIG

        """
        HC-SR04 ultrasonic sensor has a range from 2cm to 400cm.
        Speed of sound is 340 meter/second => 0.0000588 second/cm
        0.0000588 * 400 = .02352 seconds => we'll set timeout as .024
        """
        self.__TIMEOUT_VALUE = .024
        # Max distance in cm
        self.__MAX_DISTANCE = 400

        # Sequencial order to trigger each sensor
        self.__SEQ_LIST = [[TRIG1, ECHO1], [TRIG3, ECHO3], [TRIG5, ECHO5], [TRIG2, ECHO2], [TRIG4, ECHO4]]
        

    def get_distance(self, trig, echo, timeout):
        """
        Return the distance in cm for the HC-SR04 sensor
        Parameters
        trig: trig channel to fire 5v on sensor output
        echo: echo channel to receive sensor input
        timeout: the amount of time to wait for the echo to receive an response
                 measure in seconds: return __MAX_DISTANCE if timeout

        Return: distance in cm (integer)
        """

        # Fire off TRIG with 5V, then shut it off after .00001 second
        self.servo.setTarget(trig, self.__TARGET_HIGH)
        time.sleep(0.00001)
        self.servo.setTarget(trig, self.__TARGET_LOW)

        # Assign timeout value after firing off TRIG
        timeout += time.time()

        # Wait for bounce back echo
        start = time.time()
        end = time.time()
        while GPIO.input(echo) == False:
            start = time.time()
            # timed out... gone beyond the sensor's range of 400cm return MAX_DISTANCE set at 400cm
            if start > timeout:
                return self.__MAX_DISTANCE
            
        while GPIO.input(echo) == True:
            end = time.time()

        sig_time = end-start

        """
        Calculate distance in centimeter
            speed of sound is 340 meter/second => 0.0029411second/meter, 
            since we're measuring bounce back x2  => 0.0058822
            0.0058822 / 100 for cm => 0.0000588 second/cm
        """
        distance = sig_time / 0.0000588

        return int(distance)

    def runSensors(self):
        """
        runSensors should have a max runtime of 0.24s: 
            0.024(timeout_value)*5(5 sensor units)*2(get_distance+sleep)
        
        return a list of the sensors' distance in this case 5 values within the list
        """
        distance_list = []
        # Run sensors in seqential order defined by [1, 3, 5, 2, 4]
        for seq_order in self.__SEQ_LIST:
            distance = self.get_distance(seq_order[0], seq_order[1], self.__TIMEOUT_VALUE)
            # Give some time for the previous sonar wave to be cleared
            time.sleep(self.__TIMEOUT_VALUE)
            distance_list.append(distance)

        return distance_list

