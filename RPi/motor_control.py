# -*- coding: utf-8 -*-
# Last Change : Fri 18 Jan 2019 15:11:56.

import time
import pigpio

from motor import Motor  # import Motor class

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

class MotorControl(object):
    def __init__(self):
        """MotorControl constructor"""
        self.wheel1 = Motor(20, 26)
        self.wheel2 = Motor(16, 19)
        self.wheel3 = Motor(12, 6 )
        self.wheel4 = Motor(18, 17)
        self.set_car_frequency()

    def set_wheel_frequency(self, wheel, freq=1000):
        """set wheel frequency
           Args:
                motor:motorN
                freq:wheel frequency (default=1000)
           Return:
                motor frequency
        """
        wheel.set_frequency(freq)
        return wheel.get_frequency()

    def set_wheel_dutycycle(self, wheel, duty=30):
        """set wheel dutycycle
           Args:
                motor:motorN
                duty:wheel duty (default=30)
           Return:
                motor duty
        """
        wheel.set_duty(duty)
        return wheel.get_duty()

    def set_wheel_direction(self, wheel, dir=1):
        """set wheel direction
           Args:
                motor:motorN
                dir:wheel direction (default=1)
           Return:
                motor direction
        """
        wheel.set_direction(dir)
        return wheel.get_direction()

    def set_car_frequency(self, freq=[1000, 1000, 1000, 1000]):
        """set car frequency"""
        self.wheel1.set_frequency(freq[0])
        self.wheel2.set_frequency(freq[1])
        self.wheel3.set_frequency(freq[2])
        self.wheel4.set_frequency(freq[3])

        fl = [
                self.wheel1.get_frequency(),self.wheel2.get_frequency(),
                self.wheel3.get_frequency(),self.wheel4.get_frequency()
             ]
        return fl

    def set_car_dutycycle(self, duty=[30,27,30,30]):
        """set car duty cycle"""
        self.wheel1.set_duty(duty[0])
        self.wheel2.set_duty(duty[1])
        self.wheel3.set_duty(duty[2])
        self.wheel4.set_duty(duty[3])

        dl = [
                self.wheel1.get_duty(),self.wheel2.get_duty(),
                self.wheel3.get_duty(),self.wheel4.get_duty()
             ]
        return dl
 
    def set_car_direction(self, dir=[1, 1, 0, 0]):
        """set car direction
           Args:
                dir:car direction list
        """
        self.wheel1.set_direction(dir[0])
        self.wheel2.set_direction(dir[1])
        self.wheel3.set_direction(dir[2])
        self.wheel4.set_direction(dir[3])

        dl = [
                self.wheel1.get_direction(),self.wheel2.get_direction(),
                self.wheel3.get_direction(),self.wheel4.get_direction()
             ]
        return dl

    def go_ahead(self):
        """go ahead"""
        print("go ahead [1, 1, 0, 0]")
        self.set_car_direction(dir=[1, 1, 0, 0])
        self.set_car_dutycycle()
        self.set_car_frequency()

    def go_back(self):
        """go back"""
        print("go back [0, 0, 1, 1]")
        self.set_car_direction(dir=[0, 0, 1, 1])
        self.set_car_dutycycle()
        self.set_car_frequency()

    def go_left(self):
        """go left"""
        print("go left [1, 0, 0, 1]")
        self.set_car_direction([1, 0, 0, 1])
        self.set_car_dutycycle()
        self.set_car_frequency()

    def go_right(self):
        """go right"""
        print("go right [0, 1, 1, 0]")
        self.set_car_direction([0, 1, 1, 0])
        self.set_car_dutycycle()
        self.set_car_frequency()

    def go_upperleft(self):
        """go upperleft"""
        print("go upperleft [1, 0, 0, 1]")
        self.set_car_direction([1, 0, 0, 1])
        self.set_car_dutycycle([30, 0, 30, 0])
        self.set_car_frequency()

    def go_upperright(self):
        """go upperright"""
        print("go upperright [0, 1, 1, 0]")
        self.set_car_direction([0, 1, 1, 0])
        self.set_car_dutycycle([0, 27, 0, 30])
        self.set_car_frequency()

    def go_lowerleft(self):
        """go lowerleft"""
        print("go lowerleft [1, 0, 0, 1]")
        self.set_car_direction([1, 0, 0, 1])
        self.set_car_dutycycle([0, 27, 0, 30])
        self.set_car_frequency()

    def go_lowerright(self):
        """go lowerright"""
        print("go lowerright [0, 1, 1, 0]")
        self.set_car_direction([0, 1, 1, 0])
        self.set_car_dutycycle([30, 0, 30, 0])
        self.set_car_frequency()

    def turn_left(self):
        """turn left"""
        print("turn left [0, 0, 0, 0]")
        self.set_car_direction([0, 0, 0, 0])
        self.set_car_dutycycle()
        self.set_car_frequency()

    def turn_right(self):
        """turn right"""
        print("turn right [1, 1, 1, 1]")
        self.set_car_direction([1, 1, 1, 1])
        self.set_car_dutycycle()
        self.set_car_frequency()

    def stop_motor(self):
        """stop motor(dutycycle=0)"""
        self.wheel1.set_duty(0)
        self.wheel2.set_duty(0)
        self.wheel3.set_duty(0)
        self.wheel4.set_duty(0)

    def demo_action(self, delay=3):
        self.go_ahead()
        time.sleep(delay)
        self.stop_motor()
        time.sleep(delay)
        
        self.go_back()
        time.sleep(delay)
        self.stop_motor()
        time.sleep(delay)
        
        self.go_left()
        time.sleep(delay)
        self.stop_motor()
        time.sleep(delay)
        
        self.go_right()
        time.sleep(delay)
        self.stop_motor()
        time.sleep(delay)
        
        self.go_upperleft()
        time.sleep(delay)
        self.stop_motor()
        time.sleep(delay)
        
        self.go_lowerright()
        time.sleep(delay)
        self.stop_motor()
        time.sleep(delay)
        
        self.go_upperright()
        time.sleep(delay)
        self.stop_motor()
        time.sleep(delay)
        
        self.go_lowerleft()
        time.sleep(delay)
        self.stop_motor()
        time.sleep(delay)
        
        self.turn_left()
        time.sleep(delay)
        self.stop_motor()
        time.sleep(delay)
        
        self.turn_right()
        time.sleep(delay)
        self.stop_motor()
        time.sleep(delay)
