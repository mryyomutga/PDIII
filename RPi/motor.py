# -*- coding: utf-8 -*-
# Last Change : Fri 11 Jan 2019 18:12:01.

import time
import pigpio

# default Motor dir = 0
#  wheel2           wheel3
#         +-------+
#         |       |   ^
#     | - |       | - |
#     v   |       |
#         |       |   ^
#     | - |       | - |
#     v   |       |
#         +-------+
#  wheel1           wheel4

class Motor(object):
    """Motor Class"""
    pi = pigpio.pi("192.168.200.1")
    def __init__(self, pwm_pin=20, dir_pin=26):
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
        """set direction"""
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
        """get direction"""
        return direction

if __name__ == '__main__':
    pass

