from typing import List
import time

import RPi.GPIO as GPIO

from ultrasonic_sensor import UltrasonicSensor
from color_sensor import ColorSensor
from motors import DCMotor, Servo

ULTRASONIC_SENSORS: List[UltrasonicSensor] = []
COLOR_SENSORS: List[ColorSensor] = []

motor = DCMotor(21, 20)
servo = Servo(pin_id=26)


def setup() -> None:
    # Using Boardcom pin out reference standard
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    # We'll figure out the pins later on

    ULTRASONIC_SENSORS.extend([
        UltrasonicSensor(25, 27),  # front
        UltrasonicSensor(23, 24),  # back
        UltrasonicSensor(5, 6),   # right
        UltrasonicSensor(13, 19)  # left
    ])

    COLOR_SENSORS.extend([
        ColorSensor(14, 15, 18, 23, 24),
        ColorSensor(23, 24, 25)
    ])


def main() -> None:
    while True:
        front_distance = ULTRASONIC_SENSORS[0].measure()
        back_distance = ULTRASONIC_SENSORS[1].measure()
        right_distance = ULTRASONIC_SENSORS[2].measure()
        left_distance = ULTRASONIC_SENSORS[3].measure()

        if (front_distance < 50 or back_distance < 50):
            motor.start(0)
            time.sleep(0.1)

            motor.reverse()
            motor.start(20)

        else:
            motor.forward()
            motor.start(20)

            if (left_distance < 150):
                position = 30
                servo.write(position)

            elif (right_distance < 150):
                position = 150
                servo.write(position)

        for i, sensor in enumerate(COLOR_SENSORS):
            color = sensor.determine_color()

        time.sleep(1)


if __name__ == "__main__":
    try:
        print("Setting up")
        setup()
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()
