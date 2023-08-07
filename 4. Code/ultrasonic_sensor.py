import RPi.GPIO as GPIO
import time

class UltrasonicSensor:
    def __init__(self, trigger: int, echo: int) -> None:
        self.trigger = trigger
        self.echo = echo

        GPIO.setup(trigger, GPIO.OUT)
        GPIO.setup(echo, GPIO.IN)

    def measure(self) -> float:
        GPIO.output(self.trigger, GPIO.HIGH)

        # Try 0.01 if this doesn't work, most OS support 10 ms at least
        time.sleep(0.00001)

        GPIO.output(self.trigger, GPIO.LOW)

        start = time.time()
        stop = time.time()

        while GPIO.input(self.echo) == 0:
            start = time.time() # capture start of high pulse

        while GPIO.input(self.echo) == 1:
            stop = time.time() # capture end of high pulse

        elpased = start - stop

        # Compute distance in cm, from time of flight of ultrasound using
        # distance formula, distance = speed * time.
        # Divide by two since the wave travel and bounces back (to and fro)
        return (34300.0 * elpased) / 2.0
