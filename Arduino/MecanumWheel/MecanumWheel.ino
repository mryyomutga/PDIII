/**
 * MecanumWheel.ino
 * Author: Ryoga Miyamoto
 */
#include <PinChangeInt.h>
#include <PinChangeIntConfig.h>
#include <EEPROM.h>
#define _NAMIKI_MOTOR	 //for Namiki 22CL-103501PG80:1
#include <fuzzy_table.h>
#include <PID_Beta6.h>
#include <MotorWheel.h>
#include <Omni4WD.h>

#include <fuzzy_table.h>
#include <PID_Beta6.h>

/*

            \                    /
   wheel1   \                    /   wheel4
   Left     \                    /   Right


                              power switch

            /                    \
   wheel2   /                    \   wheel3
   Right    /                    \   Left

 */

/*
 * MotorWheel Class
 *   args:
 *      Struct ISRVars
 *      Class Motor
 *      Class GearedMotor
 *      Class MotorWheel
 */
// PWM:Pin5 DIR:Pin4, Encoder A:Pin12, B:Pin13

irqISR(irq1,isr1);
MotorWheel wheel1(3,2,4,5,&irq1);

irqISR(irq2,isr2);
MotorWheel wheel2(11,12,14,15,&irq2);

irqISR(irq3,isr3);
MotorWheel wheel3(9,8,16,17,&irq3);

irqISR(irq4,isr4);
MotorWheel wheel4(10,7,18,19,&irq4);

//           wheelUL wheelLL wheelLR wheelUR
Omni4WD Omni(&wheel1,&wheel2,&wheel3,&wheel4);

/**
 *  モーターを回す
 *    1. 進行方向を決める（動き方を決定する）
 *    2. どの速度でどの時間回すか決める
 *  NOTO:setCar*()の内部でOmni4WD::wheel**SetSpeedMMPS()とOmni4WD::setCarStat()を呼んでいるっぽくて
 * 　　　　細かく調整できない？
 *   
 */
void goAhead(unsigned int speedMMPS) { 
//    if(Omni.getCarStat() != Omni4WD::STAT_ADVANCE)
//        Omni.setCarSlow2Stop(300);
    Omni.setCarAdvance(0);
    Omni.setCarSpeedMMPS(speedMMPS, 300);
}

void goBack(unsigned int speedMMPS) {
//    if(Omni.getCarStat() != Omni4WD::STAT_BACKOFF) 
//        Omni.setCarSlow2Stop(300);
    Omni.setCarBackoff(0);
    Omni.setCarSpeedMMPS(speedMMPS, 300);
}

void goLeft(unsigned int speedMMPS) {
//    if(Omni.getCarStat() != Omni4WD::STAT_LEFT)
//        Omni.setCarSlow2Stop(300);
    Omni.setCarLeft(0);
    Omni.setCarSpeedMMPS(speedMMPS, 300);
}

void goRight(unsigned int speedMMPS) {
//    if(Omni.getCarStat() != Omni4WD::STAT_RIGHT)
//        Omni.setCarSlow2Stop(300);
    Omni.setCarRight(0);
    Omni.setCarSpeedMMPS(speedMMPS, 300);
}


void motorStop() {
//    if(Omni.getCarStat() != Omni4WD::STAT_STOP)
//        Omni.setCarSlow2Stop(300);
    Omni.setCarStop();
    for(int i = 0; i < 300; i++){
    Omni.wheelLRSetSpeedMMPS(0,1);
    Omni.delayMS(10);
//    Omni.wheelLRSetSpeedMMPS(10,1);
//    Omni.delayMS(10);
    }
}
void stop() {
    if(Omni.getCarStat() != Omni4WD::STAT_STOP)
        Omni.setCarSlow2Stop(300);
    Omni.setCarStop();
//    Omni.delayMS(10);
    for(int i = 0; i < 300; i++){
    goAhead(1);
    Omni.delayMS(10);
    goBack(1);
    Omni.delayMS(10);
    }
}

void setup() {
    //TCCR0B=TCCR0B&0xf8|0x01;    // warning!! it will change millis()
    TCCR1B=TCCR1B&0xf8|0x01;    // Pin9,Pin10 PWM 31250Hz
    TCCR2B=TCCR2B&0xf8|0x01;    // Pin3,Pin11 PWM 31250Hz
    Omni.PIDEnable(0.31,0.01,0,10);
}

void loop() {
    // Omni.demoActions(100,1500,500,false);
    goAhead(1000);
    stop();
    goBack(1000);
    stop();
}
