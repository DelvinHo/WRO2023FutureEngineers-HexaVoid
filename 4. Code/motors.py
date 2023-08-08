import RPi.GPIO as GPIO
from servo import Servo


class DCMotor:
    def __init__(self, PWM_pin: int, DIR_pin: int, frequency=1000) -> None:
        """Initialise a DC motor object.
        
        The MD10C motor driver gets 14.8V from the LiPo battery and outputs 12V to the DC motor.
        Take note that there's no reverse polarity protection.
        
        https://sg.cytron.io/p-10amp-5v-30v-dc-motor-driver
        
        LiPo battery: https://shopee.sg/(24h-Delivery)-IMAX-B6-80W-Balance-Battery-Charger-Lipo-NiMh-Li-ion-Ni-Cd-Digital-RC-Discharger-Power-Supply-T-Tamiya-XT60-Plug-15V-6A-Adapter-i.567389541.19272852943
        Fireproof LiPo Bag: https://shopee.sg/Fireproof-Waterproof-Lipo-Battery-Explosion-Proof-Safety-Bag-Fire-Resistant-for-Lipo-Battery-FPV-Racing-Drone-RC-Model-i.53026959.10341761540

        Args:
            PWM_pin (int): The GPIO pin number connected to the PWM input of the motor driver.
            DIR_pin (int): The GPIO pin number connected to the direction control input of the motor driver.
            frequency (int, optional): The PWM frequency in Hertz. Defaults to 1000.
        """
        self.PWM_pin = PWM_pin
        self.frequency = frequency

        self.DIR_pin = DIR_pin
        self.current_direction = GPIO.HIGH

        GPIO.setup(PWM_pin, GPIO.OUT)
        self.motor = GPIO.PWM(PWM_pin, frequency)

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
