# -*- coding: utf-8 -*-
# Last Change : Fri 18 Jan 2019 23:20:47.

import motor_control as ctl
from tkinter import *

ct = ctl.MotorControl()

def motor1_dir_callback(*args):
    if dir1.get() == True:
        ct.set_wheel_direction(ct.wheel1, dir=0)
    else:
        ct.set_wheel_direction(ct.wheel1, dir=1)

def motor2_dir_callback(*args):
    if dir2.get() == True:
        ct.set_wheel_direction(ct.wheel2, dir=0)
    else:
        ct.set_wheel_direction(ct.wheel2, dir=1)

def motor3_dir_callback(*args):
    if dir3.get() == True:
        ct.set_wheel_direction(ct.wheel3, dir=1)
    else:
        ct.set_wheel_direction(ct.wheel3, dir=0)

def motor4_dir_callback(*args):
    if dir4.get() == True:
        ct.set_wheel_direction(ct.wheel4, dir=1)
    else:
        ct.set_wheel_direction(ct.wheel4, dir=0)

def motor1_duty_callback(*args):
    duty = duty1.get()
    ct.set_wheel_dutycycle(wheel=ct.wheel1, duty=duty)

def motor2_duty_callback(*args):
    duty = duty2.get()
    ct.set_wheel_dutycycle(wheel=ct.wheel2, duty=duty)

def motor3_duty_callback(*args):
    duty = duty3.get()
    ct.set_wheel_dutycycle(wheel=ct.wheel3, duty=duty)

def motor4_duty_callback(*args):
    duty = duty4.get()
    ct.set_wheel_dutycycle(wheel=ct.wheel4, duty=duty)

if __name__ == '__main__':
    myframe = Tk()

    duty1 = IntVar()
    duty1.trace("w", motor1_duty_callback)
    duty1.set(30)
    Scale(myframe, orient=HORIZONTAL, variable=duty1, from_=0, to=100).pack()
    dir1 = BooleanVar()
    dir1.trace("w", motor1_dir_callback)
    dir1.set(False)
    Checkbutton(myframe, text="M1 DIR reverse", font=("Monospace", 20), variable=dir1).pack()
    
    duty2 = IntVar()
    duty2.trace("w", motor2_duty_callback)
    duty2.set(27)
    Scale(myframe, orient=HORIZONTAL, variable=duty2, from_=0, to=100).pack()
    dir2 = BooleanVar()
    dir2.trace("w", motor2_dir_callback)
    dir2.set(False)
    Checkbutton(myframe, text="M2 DIR reverse", font=("Monospace", 20), variable=dir2).pack()
    
    duty3 = IntVar()
    duty3.trace("w", motor3_duty_callback)
    duty3.set(30)
    Scale(myframe, orient=HORIZONTAL, variable=duty3, from_=0, to=100).pack()
    dir3 = BooleanVar()
    dir3.trace("w", motor3_dir_callback)
    dir3.set(False)
    Checkbutton(myframe, text="M3 DIR reverse", font=("Monospace", 20), variable=dir3).pack()
    
    duty4 = IntVar()
    duty4.trace("w", motor4_duty_callback)
    duty4.set(30)
    Scale(myframe, orient=HORIZONTAL, variable=duty4, from_=0, to=100).pack()
    dir4 = BooleanVar()
    dir4.trace("w", motor4_dir_callback)
    dir4.set(False)
    Checkbutton(myframe, text="M4 DIR reverse", font=("Monospace", 20), variable=dir4).pack()

    myframe.mainloop()
