# -*- coding: utf-8 -*-
# Last Change : Tue 29 Jan 2019 17:53:04.

from tkinter import *

def motor1_dir_callback(*args):
    print("motor 1 direction :", dir1.get())

def motor2_dir_callback(*args):
    print("motor 2 direction :", dir2.get())

def motor3_dir_callback(*args):
    print("motor 3 direction :", dir3.get())

def motor4_dir_callback(*args):
    print("motor 4 direction :", dir4.get())

def motor1_duty_callback(*args):
    print("motor 1 duty :", duty1.get())

def motor2_duty_callback(*args):
    print("motor 2 duty :", duty2.get())

def motor3_duty_callback(*args):
    print("motor 3 duty :", duty3.get())

def motor4_duty_callback(*args):
    print("motor 4 duty :", duty4.get())

def motor_state(*args):
    pass

fnt=("Noto Sans CJK JP", 14)

if __name__ == '__main__':
    # Tk frame
    myframe = Tk()
    myframe.title("Motor Tester")

    ## Frames
    f0=LabelFrame(myframe, text='Motor State Control', padx=52, bd=4, font=fnt, labelanchor = N)
    f0.pack()

    f1=LabelFrame(myframe, text='Front', bd=4, font=fnt, labelanchor = N)
    f1.pack()

    f2=LabelFrame(myframe, text='Back', bd=4, font=fnt, labelanchor = N)
    f2.pack()

    ### SubFrames
    state = BooleanVar()
    state.set(True)
    Checkbutton(f0, text="Stop All Motors", font=fnt, variable=state, command=motor_state).pack()


    #### Motor2
    duty2 = IntVar()
    duty2.trace("w", motor2_duty_callback)
    duty2.set(0)
    dir2 = BooleanVar()
    dir2.trace("w", motor2_dir_callback)
    dir2.set(False)

    f01=LabelFrame(f1, text='Motor2 Duty', bd=2, font=fnt)
    f01.pack(side='left')
    Checkbutton(f01, text="DIR reverse", font=fnt, variable=dir2).pack()
    Scale(f01, font=fnt,orient=HORIZONTAL, variable=duty2, from_=0, to=100).pack()

    #### Motor3
    duty3 = IntVar()
    duty3.trace("w", motor3_duty_callback)
    duty3.set(0)
    dir3 = BooleanVar()
    dir3.trace("w", motor3_dir_callback)
    dir3.set(False)

    f02=LabelFrame(f1, text='Motor3 Duty', bd=2, font=fnt)
    f02.pack(side='left')
    Checkbutton(f02, text="DIR reverse", font=fnt, variable=dir3).pack()
    Scale(f02, font=fnt, orient=HORIZONTAL, variable=duty3, from_=0, to=100).pack()

    #### Motor1
    duty1 = IntVar()
    duty1.trace("w", motor1_duty_callback)
    duty1.set(0)
    dir1 = BooleanVar()
    dir1.trace("w", motor1_dir_callback)
    dir1.set(False)

    f11=LabelFrame(f2, text='Motor1 Duty', bd=2, font=fnt)
    f11.pack(side='left')
    Checkbutton(f11, text="DIR reverse", font=fnt, variable=dir1).pack()
    Scale(f11, font=fnt, orient=HORIZONTAL, variable=duty1, from_=0, to=100).pack()

    #### Motor4
    duty4 = IntVar()
    duty4.trace("w", motor4_duty_callback)
    duty4.set(0)
    dir4 = BooleanVar()
    dir4.trace("w", motor4_dir_callback)
    dir4.set(False)

    f12=LabelFrame(f2, text='Motor4 Duty', bd=2, font=fnt)
    f12.pack(side='left')
    Checkbutton(f12, text="DIR reverse", font=fnt, variable=dir4).pack()
    Scale(f12, font=fnt, orient=HORIZONTAL, variable=duty4, from_=0, to=100).pack()

    myframe.mainloop()