# -*- coding: utf-8 -*-
# Last Change : Fri 25 Jan 2019 17:39:21.

from motor import Motor
# import motor_control as ctl
from tkinter import *

# Motor object
motor1 = Motor(20, 26, dir=1)
motor2 = Motor(16, 19, dir=1)
motor3 = Motor(12, 6 , dir=0)
motor4 = Motor(18, 17, dir=0)

fnt=("Noto Sans CJK JP", 14)

# Stop all motors
def motor_state(*args):
    if state.get():
        # Stop
        motor1.set_duty(0)
        motor2.set_duty(0)
        motor3.set_duty(0)
        motor4.set_duty(0)
    else:
        # Run
        motor1.set_duty(duty1.get())
        motor2.set_duty(duty2.get())
        motor3.set_duty(duty3.get())
        motor4.set_duty(duty4.get())

# Switch motor direction
def motor1_dir_callback(*args):
    if dir1.get() == True:
        motor1.set_direction(0)
    else:
        motor1.set_direction(1)

    print("Motor1 dir :", motor1.get_direction())

def motor2_dir_callback(*args):
    if dir2.get() == True:
        motor2.set_direction(0)
    else:
        motor2.set_direction(1)

    print("Motor2 dir :", motor2.get_direction())

def motor3_dir_callback(*args):
    if dir3.get() == True:
        motor3.set_direction(1)
    else:
        motor3.set_direction(0)

    print("Motor3 dir :", motor3.get_direction())

def motor4_dir_callback(*args):
    if dir4.get() == True:
        motor4.set_direction(1)
    else:
        motor4.set_direction(0)

    print("Motor4 dir :", motor4.get_direction())

# Change duty
## don't move the if motor direction control checkbox is put a check mark.
def motor1_duty_callback(*args):
    duty = duty1.get()
    if state.get() == False:
        motor1.set_duty(duty)
        print("Motor1 : duty", duty)

def motor2_duty_callback(*args):
    duty = duty2.get()
    if state.get() == False:
        motor2.set_duty(duty)
        print("Motor2 : duty", duty)

def motor3_duty_callback(*args):
    duty = duty3.get()
    if state.get() == False:
        motor3.set_duty(duty)
        print("Motor3 : duty", duty)

def motor4_duty_callback(*args):
    duty = duty4.get()
    if state.get() == False:
        motor4.set_duty(duty)
        print("Motor4 : duty", duty)

if __name__ == '__main__':
    myframe = Tk()
    myframe.title("Motor Tester")

    ## Frames
    f0 = LabelFrame(myframe, text='Motor State Control', padx=52, bd=4, font=fnt, labelanchor = N)
    f0.pack()

    f1 = LabelFrame(myframe, text='Front', bd=4, font=fnt, labelanchor = N)
    f1.pack()

    f2 = LabelFrame(myframe, text='Back', bd=4, font=fnt, labelanchor = N)
    f2.pack()

    ### SubFrames
    state = BooleanVar()
    state.set(True)
    Checkbutton(f0, text="Stop All Motors", font=fnt, variable=state, command=motor_state).pack()

    ### Front
    #### Motor2
    duty2 = IntVar()
    duty2.trace("w", motor2_duty_callback)
    duty2.set(27)
    dir2 = BooleanVar()
    dir2.trace("w", motor2_dir_callback)
    dir2.set(False)

    f01 = LabelFrame(f1, text='Motor2 Duty', bd=2, font=fnt)
    f01.pack(side='left')
    Checkbutton(f01, text="DIR reverse", font=fnt, variable=dir2).pack()
    Scale(f01, font=fnt,orient=HORIZONTAL, variable=duty2, from_=0, to=100).pack()

    #### Motor3
    duty3 = IntVar()
    duty3.trace("w", motor3_duty_callback)
    duty3.set(30)
    dir3 = BooleanVar()
    dir3.trace("w", motor3_dir_callback)
    dir3.set(False)

    f02 = LabelFrame(f1, text='Motor3 Duty', bd=2, font=fnt)
    f02.pack(side='left')
    Checkbutton(f02, text="DIR reverse", font=fnt, variable=dir3).pack()
    Scale(f02, font=fnt, orient=HORIZONTAL, variable=duty3, from_=0, to=100).pack()

    ### Back
    #### Motor1
    duty1 = IntVar()
    duty1.trace("w", motor1_duty_callback)
    duty1.set(30)
    dir1 = BooleanVar()
    dir1.trace("w", motor1_dir_callback)
    dir1.set(False)

    f11 = LabelFrame(f2, text='Motor1 Duty', bd=2, font=fnt)
    f11.pack(side='left')
    Checkbutton(f11, text="DIR reverse", font=fnt, variable=dir1).pack()
    Scale(f11, font=fnt, orient=HORIZONTAL, variable=duty1, from_=0, to=100).pack()

    #### Motor4
    duty4 = IntVar()
    duty4.trace("w", motor4_duty_callback)
    duty4.set(30)
    dir4 = BooleanVar()
    dir4.trace("w", motor4_dir_callback)
    dir4.set(False)

    f12 = LabelFrame(f2, text='Motor4 Duty', bd=2, font=fnt)
    f12.pack(side='left')
    Checkbutton(f12, text="DIR reverse", font=fnt, variable=dir4).pack()
    Scale(f12, font=fnt, orient=HORIZONTAL, variable=duty4, from_=0, to=100).pack()

    myframe.mainloop()