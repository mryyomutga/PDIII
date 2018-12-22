
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
irqISR(irq1,isr1);
MotorWheel wheel1(5,4,12,13,&irq1);

irqISR(irq2,isr2);
MotorWheel wheel2(6,7,14,15,&irq2);

irqISR(irq3,isr3);
MotorWheel wheel3(9,8,16,17,&irq3);

irqISR(irq4,isr4);
MotorWheel wheel4(10,11,18,19,&irq4);
 */

/*
 * MotorWheel Class
 *   args:
 *      Struct ISRVars
 *      Class Motor
 *      Class GearedMotor
 *      Class MotorWheel
 */

irqISR(irq1,isr1);
MotorWheel wheel1(3,2,4,5,&irq1);

irqISR(irq2,isr2);
MotorWheel wheel2(11,12,14,15,&irq2);

 irqISR(irq3,isr3);
 MotorWheel wheel3(9,8,16,17,&irq3);

 irqISR(irq4,isr4);
 MotorWheel wheel4(10,7,18,19,&irq4);

//           wheelUL wheelLL wheelLR wheelUR
// Omni4WD Omni(&wheel1,&wheel2,&wheel3,&wheel4);

void setup() {
//	TCCR0B=TCCR0B&0xf8|0x01;    // warning!! it will change millis()
	// TCCR1B=TCCR1B&0xf8|0x01;    // Pin9,Pin10 PWM 31250Hz
	// TCCR2B=TCCR2B&0xf8|0x01;    // Pin3,Pin11 PWM 31250Hz
    
	// Omni.PIDEnable(1,0,0.01,10);
    TCCR1B=TCCR1B&0xf8|0x01;
    TCCR2B=TCCR2B&0xf8|0x01;
//    wheel1.setSpeedMMPS(100, DIR_BACKOFF);
    wheel1.PIDEnable(KC,TAUI,TAUD,10);
//    wheel2.setSpeedMMPS(100, DIR_BACKOFF);
    wheel2.PIDEnable(KC,TAUI,TAUD,10);
//    wheel1.setSpeedMMPS(100, DIR_BACKOFF);
    wheel3.PIDEnable(KC,TAUI,TAUD,10);
//    wheel2.setSpeedMMPS(100, DIR_BACKOFF);
    wheel4.PIDEnable(KC,TAUI,TAUD,10);
    Serial.begin(9600);
    wheel1.PIDRegulate();
    wheel2.PIDRegulate();
    wheel3.PIDRegulate();
    wheel4.PIDRegulate();  
}

void loop() {
	// Omni.demoActions(100,1500,200,true);
  wheel1.PIDRegulate();
  wheel2.PIDRegulate();
  wheel3.PIDRegulate();
  wheel4.PIDRegulate();  
  wheel1.setSpeedMMPS(100, DIR_ADVANCE);
  wheel2.setSpeedMMPS(100, DIR_ADVANCE);
  wheel3.setSpeedMMPS(100, DIR_BACKOFF);
  wheel4.setSpeedMMPS(100, DIR_BACKOFF);
  delay(5000);
//  wheel1.PIDRegulate();
//  wheel2.PIDRegulate();
//  wheel3.PIDRegulate();
//  wheel4.PIDRegulate();
//  wheel1.setSpeedMMPS(0, DIR_ADVANCE);
//  wheel2.setSpeedMMPS(0, DIR_ADVANCE);
//  wheel3.setSpeedMMPS(0, DIR_BACKOFF);
//  wheel4.setSpeedMMPS(0, DIR_BACKOFF);
//  delay(5000);
//  wheel1.PIDRegulate();
//  wheel2.PIDRegulate();
//  wheel3.PIDRegulate();
//  wheel4.PIDRegulate();
  wheel1.setSpeedMMPS(100, DIR_BACKOFF);
  wheel2.setSpeedMMPS(100, DIR_BACKOFF);
  wheel3.setSpeedMMPS(100, DIR_ADVANCE);
  wheel4.setSpeedMMPS(100, DIR_ADVANCE);
  delay(5000);
//  wheel1.PIDRegulate();
//  wheel2.PIDRegulate();
//  wheel3.PIDRegulate();
//  wheel4.PIDRegulate();
//  wheel1.setSpeedMMPS(100, DIR_BACKOFF);
//  wheel2.setSpeedMMPS(100, DIR_BACKOFF);
//  wheel3.setSpeedMMPS(100, DIR_ADVANCE);
//  wheel4.setSpeedMMPS(100, DIR_ADVANCE);
//  delay(5000);
}
