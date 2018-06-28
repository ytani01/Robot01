#!/usr/bin/env python3
#
# -*- coding: utf-8 -*-
#
import pigpio
import time

class DcMtr:
    PWM_FREQ = 50
    PWM_RANGE = 100

    def __init__(self, pi, pin):
        self.pi = pi
        self.pin = pin
        self.n = len(pin)
        self.freq = list(range(self.n))
        self.range = list(range(self.n))

        for i in range(self.n):
            pi.set_mode(pin[i], pigpio.OUTPUT)
            self.freq[i] = pi.set_PWM_frequency(pin[i], DcMtr.PWM_FREQ)
            self.range[i] = pi.set_PWM_range(pin[i], DcMtr.PWM_RANGE)
            pi.set_PWM_dutycycle(pin[i], 0)

    def set(self, in1, in2):
        if in1 < 0:
            in1 = 0
        if in1 > DcMtr.PWM_RANGE:
            in1 = DcMtr.PWM_RANGE
        if in2 < 0:
            in2 = 0
        if in2 > DcMtr.PWM_RANGE:
            in2 = DcMtr.PWM_RANGE

        self.pi.set_PWM_dutycycle(self.pin[0], in1)
        self.pi.set_PWM_dutycycle(self.pin[1], in2)

    def set_speed(self, speed, sec=0):
        if speed < -100:
            speed = -100
        if speed > 100:
            speed = 100

        if speed >= 0:
            self.set(speed, 0)
        else:
            self.set(0, -speed)

        time.sleep(sec)

    def set_break(self, sec=0):
        self.set(100,100)
        time.sleep(sec)

    def set_stop(self, sec=0):
        self.set(0,0)
        time.sleep(sec)

class DcMtrN:
    def __init__(self, pi, pin):
        self.pi = pi
        self.n = len(pin)
        self.dc_mtr = list(range(self.n))

        for i in range(self.n):
            self.dc_mtr[i] = DcMtr(self.pi, pin[i])

    def set_speed(self, speed, sec=0):
        for i in range(self.n):
            self.dc_mtr[i].set_speed(speed[i])
        time.sleep(sec)

    def set_break(self, sec=0):
        for i in range(self.n):
            self.dc_mtr[i].set_break()
        time.sleep(sec)

    def set_stop(self, sec=0):
        for i in range(self.n):
            self.dc_mtr[i].set_stop()
        time.sleep(sec)


#####
def main1(pi):
    pin = [[13,12],[17,18]]

    dc_mtr = DcMtrN(pi, pin)
    print(dc_mtr.n)
    for i in range(dc_mtr.n):
        print(dc_mtr.dc_mtr[i].freq)
        print(dc_mtr.dc_mtr[i].range)

    try:
        dc_mtr.set_speed([100,30],2)
        dc_mtr.set_break(0.3)
        dc_mtr.set_speed([-30,-100],2)
        dc_mtr.set_break(0.3)
    finally:
        print('dc_mtr.set_stop()')
        dc_mtr.set_stop()


if __name__ == '__main__':
    pi = pigpio.pi()
    try:
        main1(pi)
    finally:
        print('pi.stop()')
        pi.stop()
