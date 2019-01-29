# -*- coding: utf-8 -*-
# Last Change : Fri 25 Jan 2019 17:27:52.

import time
import pigpio

# Motor1 param
# PWM Pin   : 20
# DIR Pin   : 26
# Frequency : 1ms
# duty      : 0
# direction : 1 (Front)

class Motor(object):
    """Motor Class"""
    pi = pigpio.pi("192.168.200.1")

    """Constructor"""
    def __init__(self, pwm_pin=20, dir_pin=26, freq=1000, duty=0, dir=1):
        # set Raspberry Pi gpio pin number
        self.pwm_pin = pwm_pin
        self.dir_pin = dir_pin
        self.pi.set_mode(self.pwm_pin, pigpio.OUTPUT)
        self.pi.set_mode(self.dir_pin, pigpio.OUTPUT)

        # set motor parameters
        self.set_frequency(freq)
        self.set_duty(duty)
        self.set_direction(dir)

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

    def set_duty(self, duty=30):
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

    def get_direction(self):
        """get direction"""
        return self.direction

if __name__ == '__main__':
    pass

