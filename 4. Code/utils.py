import time
import RPi.GPIO as GPIO


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
