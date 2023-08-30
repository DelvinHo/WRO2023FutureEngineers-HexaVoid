import time
import math
import RPi.GPIO as GPIO

def euclidean_distance(color1, color2):
    """Calculates the Euclidean distance between two colour vectors.

    Args:
        color1 (Tuple[int, int, int]): The first colour vector in RGB order.
        color2 (Tuple[int, int, int]): The second colour vector in RGB order.

    Returns:
        float: The Euclidean distance between the two colour vectors.
    """
    
    return math.sqrt(sum((c1 - c2) ** 2 for c1, c2 in zip(color1, color2)))

def pulseIn(pin: int, value: GPIO.LOW or GPIO.HIGH) -> float:
    GPIO.setup(pin, GPIO.IN)

    while GPIO.input(pin) == value:
        pass

    while GPIO.input(pin) != value:
        pass

    start_time = time.time()

    while GPIO.input(pin) == value:
        pass

    stop_time = time.time()

    elapsed_time = stop_time - start_time

    return elapsed_time
