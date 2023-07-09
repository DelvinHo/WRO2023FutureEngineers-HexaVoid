from typing import Tuple
import time
import math

import RPi.GPIO as GPIO

# Helper functions
def euclidean_distance(color1, color2):
    return math.sqrt(sum((c1 - c2) ** 2 for c1, c2 in zip(color1, color2)))


# Constants
ORANGE_LINE = (255, 102, 0)
BLUE_LINE = (0, 51, 255)
ORANGE_EUCLIDEAN = euclidean_distance(ORANGE_LINE, (0, 0, 0))
BLUE_EUCLIDEAN = euclidean_distance(BLUE_LINE, (0, 0, 0))
COLOR_TOLERENCE = 0.1


class ColorSensor:
    def __init__(self, s2: int, s3: int, out: int) -> None:
        # Pin outs
        self.s2 = s2
        self.s3 = s3
        self.out = out

        GPIO.setup(s2, GPIO.IN)
        GPIO.setup(s3, GPIO.IN)
        GPIO.setup(out, GPIO.OUT)

        # Sensor states
        self.time_since_color = None


    def read_color(self) -> Tuple[int, int, int]:
        GPIO.output(self.s2, GPIO.LOW)
        GPIO.output(self.s3, GPIO.LOW)
        red = GPIO.input(self.out)
        
        # Try 0.01 if this doesn't work, most OS support 10 ms at least
        time.sleep(0.001)

        GPIO.output(self.s2, GPIO.HIGH)
        GPIO.output(self.s3, GPIO.HIGH)
        green = GPIO.input(self.out)
        time.sleep(0.001)

        GPIO.output(self.s2, GPIO.LOW)
        GPIO.output(self.s3, GPIO.HIGH)
        blue = GPIO.input(self.out)

        return red, green, blue
    

    def determine_color(self) -> str:
        """
        The colour of the orange lines is CMYK (0, 60, 100, 0) and RGB (255, 102, 0).
        The colour of the blue lines is CMYK (100, 80, 0, 0) and RGB (0, 51, 255).

        We are using Eudlicdean Distance to calculate the distances between
        the detected colour (specified by the input red, green, and blue values)
        and the predefined orange and blue colours.

        We then compare the distances to the tolerance-adjusted distance from the
        predefined color to the origin (black). If the calculated distances are
        within the tolerance (10% of the distance from the predefined color to black)
        - The lower the more accurate/less tolerenet to errors.

        This statistical approach allows for a more flexible determination of line colors,
        accounting for slight variations and noise in the RGB values of the detected colors.
        """
        
        color = self.read_color()
        orange_distance = euclidean_distance(color, ORANGE_LINE)
        blue_distance = euclidean_distance(color, BLUE_LINE)

        if orange_distance <= COLOR_TOLERENCE * ORANGE_EUCLIDEAN:
            self.time_since_color = time.time()
            return "orange"
        elif blue_distance <= COLOR_TOLERENCE * BLUE_EUCLIDEAN:
            self.time_since_color = time.time()
            return "blue"
        else:
            return "unknown"