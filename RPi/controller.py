# -*- coding: utf-8 -*-
# Last Change : Wed 26 Dec 2018 20:55:37.
import pigpio

class Motor(object):
    """Motor Class"""
    pi = pigpio.pi()
    def __init__(self, pwm_pin=3, dir_pin=2):
        """constructor"""
        self.pwm_pin = pwm_pin
        self.dir_pin = dir_pin
        self.pi.set_mode(self.pwm_pin, pigpio.OUTPUT)
        self.pi.set_mode(self.dir_pin, pigpio.OUTPUT)

    """Setter"""
    def set_pwm_pin(self, pin):
        """set PWM pin"""
        self.pwm_pin = pin

    def set_dir_pin(self, pin):
        """set DIR pin"""
        self.dir_pin = pin

    def set_frequency(self, freq=1000):
        """set frequency"""
        self.freq = freq
        # 1ms
        self.pi.set_PWM_frequency(self.pwm_pin, freq)

    def set_duty(self, duty=25):
        """set duty"""
        self.duty = duty
        # duty 10%
        self.pi.set_PWM_dutycycle(self.pwm_pin, duty)

    def set_direction(self, direction=1):
        self.pi.write(self.dir_pin, direction)
        self.direction = direction

    """Getter"""
    def get_pwm_pin(self):
        """get PWM pin"""
        return self.pwm_pin

    def get_dir_pin(self):
        """get DIR pin"""
        return self.dir_pin

    def get_frequency(self):
        """get frequency"""
        return self.freq

    def get_duty(self):
        """get duty"""
        return self.duty

    def get_direction(self, direction=1):
        return direction

class MotorControl(object):
    def __init__(self):
        self.M1 = Motor(20, 26)
        self.M2 = Motor(16, 19)
        self.M3 = Motor(12, 6 )
        self.M4 = Motor(17, 18)

    def set_frequency_all(self):
        self.M1.set_frequency()
        self.M2.set_frequency()
        self.M3.set_frequency()
        self.M4.set_frequency()

    def set_dutycycle_all(self):
        self.M1.set_duty(40)
        self.M2.set_duty(33)
        self.M3.set_duty(40)
        self.M4.set_duty(40)

    def set_direction_all(self):
        self.M1.set_direction(1)
        self.M2.set_direction(1)
        self.M3.set_direction(0)
        self.M4.set_direction(0)

    def stop_motor(self):
        self.M1.set_duty(0)
        self.M2.set_duty(0)
        self.M3.set_duty(0)
        self.M4.set_duty(0)
