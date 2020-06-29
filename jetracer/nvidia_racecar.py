from .racecar import Racecar
import traitlets
from adafruit_servokit import ServoKit
# For RPi.GPIO, GPIO.TEGRA_SOC mode is utilized in the former packages.
import RPi.GPIO as GPIO

class NvidiaRacecar(Racecar):
    
    i2c_address = traitlets.Integer(default_value=0x40)
    steering_gain = traitlets.Float(default_value=-0.65)
    steering_offset = traitlets.Float(default_value=0)
    steering_channel = traitlets.Integer(default_value=0)
    throttle_gain = traitlets.Float(default_value=0.8)
    # The two channels control the two motors correspondingly.
    throttle_channel = traitlets.Integer(default_value=1)
    throttle_channel_1 = traitlets.Integer(default_value=2)
   
    def __init__(self, *args, **kwargs):
        super(NvidiaRacecar, self).__init__(*args, **kwargs)
        self.kit = ServoKit(channels=16, address=self.i2c_address)
        self.steering_motor = self.kit.continuous_servo[self.steering_channel]
        self.throttle_motor = self.kit.continuous_servo[self.throttle_channel]
        self.throttle_motor_1 = self.kit.continuous_servo[self.throttle_channel_1]

        # Set up the direction control pins for the two motors. Here, PIN 16 and PIN 18 are utilized to control two motors.
        GPIO.setup('SPI2_CS1', GPIO.OUT, initial = GPIO.HIGH) # This sets up the motor which needs to run reversely. PIN16
        GPIO.setup('SPI2_CS0', GPIO.OUT, initial = GPIO.LOW) # PIN18
        
    @traitlets.observe('steering')
    def _on_steering(self, change):
        self.steering_motor.throttle = change['new'] * self.steering_gain + self.steering_offset
    
    @traitlets.observe('throttle')
    def _on_throttle(self, change):
        self.throttle_motor.throttle = change['new'] * self.throttle_gain
        self.throttle_motor_1.throttle = change['new'] * self.throttle_gain
    
    # Moving forward: 1; moving backward: 2
    @traitlets.observe('direction')
    def _on_direction(self, change):
        if change['new'] == 1:
            GPIO.output('SPI2_CS1', GPIO.HIGH)
            GPIO.output('SPI2_CS0', GPIO.LOW)            
        if change['new'] == -1:
            GPIO.output('SPI2_CS1', GPIO.LOW)
            GPIO.output('SPI2_CS0', GPIO.HIGH)
