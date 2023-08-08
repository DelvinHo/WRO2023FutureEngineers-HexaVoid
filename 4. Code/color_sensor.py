from typing import Tuple
import time
import math

import RPi.GPIO as GPIO


# Helper functions
def euclidean_distance(color1, color2):
    """Calculates the Euclidean distance between two colour vectors.

    Args:
        color1 (Tuple[int, int, int]): The first colour vector in RGB order.
        color2 (Tuple[int, int, int]): The second colour vector in RGB order.

    Returns:
        float: The Euclidean distance between the two colour vectors.
    """
    
    return math.sqrt(sum((c1 - c2) ** 2 for c1, c2 in zip(color1, color2)))


# Constants
ORANGE_LINE = (255, 102, 0)
BLUE_LINE = (0, 51, 255)
ORANGE_EUCLIDEAN = euclidean_distance(ORANGE_LINE, (0, 0, 0))
BLUE_EUCLIDEAN = euclidean_distance(BLUE_LINE, (0, 0, 0))
COLOR_TOLERANCE = 0.1


class ColorSensor:
    def __init__(self, s2: int, s3: int, out: int) -> None:
        """Initialise a colour sensor object.

        The TCS3200 colour sensor module is used to calibrate direction and to calculate the angle from the difference of the two sensors.
        https://sg.cytron.io/p-colour-sensor-module

        Args:
            s2 (int): The GPIO pin number connected to the S2 control input of the colour sensor.
            s3 (int): The GPIO pin number connected to the S3 control input of the colour sensor.
            out (int): The GPIO pin number connected to the OUT output of the colour sensor.
        """

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
        """Reads the colour components from the colour sensor.

        Returns:
            Tuple[int, int, int]: A tuple representing the colour components in RGB order.
        """

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

        We are using Euclidean Distance to calculate the distances between
        the detected colour (specified by the input red, green, and blue values)
        and the predefined orange and blue colours.

        We then compare the distances to the tolerance-adjusted distance from the
        predefined colour to the origin (black). If the calculated distances are
        within the tolerance (10% of the distance from the predefined colour to black)
        - The lower the more accurate/less tolerance to errors.

        This statistical approach allows for a more flexible determination of line colours,
        accounting for slight variations and noise in the RGB values of the detected colours.
        """

        color = self.read_color()
        orange_distance = euclidean_distance(color, ORANGE_LINE)
        blue_distance = euclidean_distance(color, BLUE_LINE)

        if orange_distance <= COLOR_TOLERANCE * ORANGE_EUCLIDEAN:
            self.time_since_color = time.time()
            return "orange"
        elif blue_distance <= COLOR_TOLERANCE * BLUE_EUCLIDEAN:
            self.time_since_color = time.time()
            return "blue"
        else:
            return "unknown"
