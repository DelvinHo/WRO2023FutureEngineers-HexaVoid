from typing import List
import time
import RPi.GPIO as GPIO

from ultrasonic_sensor import UltrasonicSensor
from color_sensor import ColorSensor
from imu import IMU
from motors import DCMotor, Servo

ULTRASONIC_SENSORS: List[UltrasonicSensor] = []
COLOR_SENSORS: List[ColorSensor] = []
MOTOR: DCMotor = None
SERVO: Servo = None
IMU_SENSOR: IMU = None

def setup() -> None:
    global MOTOR, SERVO, IMU_SENSOR

    # Using phyiscal board pin out reference
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)

    # We'll figure out the pins later on

    ULTRASONIC_SENSORS.extend([
        UltrasonicSensor(25, 27),  # front
        UltrasonicSensor(23, 24),  # back
        UltrasonicSensor(13, 19),  # left
        UltrasonicSensor(5, 6)     # right
    ])

    COLOR_SENSORS.extend([
        ColorSensor(14, 15, 18, 23, 24), # left
        ColorSensor(23, 24, 25)          # right
    ])

    # Pins here are done

    MOTOR = DCMotor(32, 31)
    SERVO = Servo(33)
    IMU_SENSOR = IMU(5, 3, 0x68)


def main() -> None:
    # Input -> process -> output
    # inputs are ultasonic, colour sensor, imu, camera

    for i, sensor in enumerate(COLOR_SENSORS):
        color = sensor.determine_color()

    front_distance = ULTRASONIC_SENSORS[0].measure()
    back_distance = ULTRASONIC_SENSORS[1].measure()
    right_distance = ULTRASONIC_SENSORS[2].measure()
    left_distance = ULTRASONIC_SENSORS[3].measure()

    if (front_distance < 50 or back_distance < 50):
        MOTOR.start(0)
        time.sleep(0.1)

        MOTOR.reverse()
        MOTOR.start(20)

    else:
        MOTOR.forward()
        MOTOR.start(20)

        if (left_distance < 150):
            position = 30
            SERVO.write(position)

        elif (right_distance < 150):
            position = 150
            SERVO.write(position)

    time.sleep(1)


if __name__ == "__main__":
    try:
        print("Setting up")
        setup()

        time.sleep(1)

        # Run startup sequence: e.g. servo turning, move back etc. etc.

        while True:
            main()
    except KeyboardInterrupt:
        print("Exiting. Cleaning up")
        
        SERVO.set_angle(0)
        time.sleep(1)

        GPIO.cleanup()
