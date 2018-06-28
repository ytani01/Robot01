#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

import pigpio
import time

#####
class CR_Servo:
    DEF_PULSE = {'stop': 1480}

    def __init__(self, pi, pin):
        self.pi = pi
        self.pin = pin

        self.pulse = {}
        self.change_pulse_value('stop', CR_Servo.DEF_PULSE['stop'])

        self.pi.set_mode(self.pin, pigpio.OUTPUT)

    def change_pulse_value(self, key, value):
        self.pulse[key] = value

    def set_stop(self, sec=0):
        self.set_pulse(self.pulse['stop'], sec)

    def set_pulse(self, pulse, sec=0):
        self.pi.set_servo_pulsewidth(self.pin, pulse)
        if sec > 0:
            time.sleep(sec)

#####
class CR_Servo_N:
    def __init__(self, pi, pin):
        self.pi = pi
        self.pin = pin
        self.n = len(pin)

        self.cr_servo = list(range(self.n))
        for i in range(self.n):
            self.cr_servo[i] = CR_Servo(self.pi, self.pin[i])

    def set_pulse(self, pulse, sec=0):
        for i in range(self.n):
            self.cr_servo[i].set_pulse(pulse[i])
        if sec > 0:
            time.sleep(sec)

    def set_stop(self, sec=0):
        for i in range(self.n):
            self.cr_servo[i].set_stop()
        if sec > 0:
            time.sleep(sec)

    def change_pulse_value(self, key, value):
        for i in range(self.n):
            self.cr_servo.change_pulse_value(key, value[i])

#####
def main1(pi):
    pin = [12,13]

    cr_servo = CR_Servo_N(pi, pin)
    print('cr_servo:\n', cr_servo.__dict__)
    for i in range(len(pin)):
        print('cr_servo.sr_servo[i].__dict__:\n', cr_servo.cr_servo[i].__dict__)

    cr_servo.set_pulse([1400,1600], 0.2)
    cr_servo.set_stop()


if __name__ == '__main__':
    pi = pigpio.pi()
    try:
        main1(pi)
    finally:
        print('=== finally ===')
        print('pi.stop()')
        pi.stop()
