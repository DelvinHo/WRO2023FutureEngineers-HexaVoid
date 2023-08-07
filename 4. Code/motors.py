import RPi.GPIO as GPIO
from servo import Servo

class DCMotor:
    def __init__(self, PWM_pin: int, DIR_pin: int, pluse = 100) -> None:
        self.PWM_pin = PWM_pin
        self.pluse = pluse

        self.DIR_pin = DIR_pin
        self.current_direction = GPIO.HIGH

        GPIO.setup(PWM_pin, GPIO.OUT)
        self.motor = GPIO.PWM(PWM_pin, pluse)

    def __getattr__(self, attr):
        # Delegate unknown attributes to GPIO.PWM object
        # e.g. start and stop, ChangeFrequency methods
        # in https://sourceforge.net/p/raspberry-gpio-python/wiki/PWM/
        return getattr(self.motor, attr)

    def forward(self) -> None:
        self.current_direction = GPIO.HIGH
        GPIO.setup(self.DIR_pin, self.current_direction)

    def backward(self) -> None:
        self.current_direction = GPIO.LOW
        GPIO.setup(self.DIR_pin, self.current_direction)

    def reverse(self) -> None:
        self.current_direction = GPIO.LOW if self.current_direction == GPIO.HIGH else GPIO.HIGH
        GPIO.output(self.DIR_pin, self.current_direction)


my_servo = Servo(pin_id=26)
