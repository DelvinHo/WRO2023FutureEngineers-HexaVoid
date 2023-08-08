import RPi.GPIO as GPIO
import time


class UltrasonicSensor:
    def __init__(self, trigger: int, echo: int) -> None:
        """Initialise a ultrasonic sensor object.

        The ultrasonic sensor US-015 used for the measurement of distances
        between the ultrasonic sensor and the object in front of the sensor.

        https://sg.cytron.io/p-high-precision-ultrasonic-range-finder-us-015

        Args:
            trigger (int): The GPIO pin number connected to the Trigger output of the ultrasonic sensor
            echo (int): The GPIO pin number connected to the Echo input of the ultrasonic sensor
        """

        self.trigger = trigger
        self.echo = echo

        GPIO.setup(trigger, GPIO.OUT)
        GPIO.setup(echo, GPIO.IN)

    def measure(self) -> float:
        """Measures the distance using an ultrasonic sensor.

        Returns:
            float: The calculated distance in centimetres.
        """

        # Set trigger pin to LOW for stabilisation. To lower the duration after testing
        GPIO.output(self.trigger, GPIO.LOW)
        time.sleep(0.2)

        # Trigger for 10 microseconds, should send 8 ultrasonic bursts at 40KHz
        # Try 0.01 if this doesn't work, most OS support 10 ms at least
        GPIO.output(self.trigger, GPIO.HIGH)
        time.sleep(0.00001)

        GPIO.output(self.trigger, GPIO.LOW)

        start_time = time.time()
        stop_time = time.time()

        while GPIO.input(self.echo) == 0:
            print("Waiting for echo to go HIGH...")
            start_time = time.time()

        while GPIO.input(self.echo) == 1:
            print("Echo is HIGH, measuring...")
            stop_time = time.time()

        elapsed_time = stop_time - start_time

        # Compute distance in cm, from time of flight of ultrasound using
        # Distance formula, distance = speed * time.
        # Divide by two since the wave travels back and forth.
        distance = (34300.0 * elapsed_time) / 2.0
        return distance
