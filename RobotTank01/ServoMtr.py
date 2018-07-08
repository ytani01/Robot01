#!/usr/bin/env python3
#
import pigpio
import time
import sys

class SG90:
    PULSE_OFF = 0
    PULSE_CENTER = 1500
    PULSE_MIN = 500
    PULSE_MAX = 2500

    SEC_PULSE = 0.6 / (PULSE_MAX - PULSE_MIN)
    print(SEC_PULSE)
    
    def __init__(self, pin, pi=''):
        if type(pi) == pigpio.pi:
            self.pi = pi
            self.mypi = False
        else:
            self.pi = pigpio.pi()
            self.mypi = True
            
        self.pin = pin

        self.cur_pulse = SG90.PULSE_CENTER
        self.set_pulse(self.cur_pulse)
        time.sleep(1)

    def __del__(self):
        self.set_pulse(SG90.PULSE_OFF)
        if self.mypi:
            self.pi.stop()

    def set_pulse(self, pulse, sec = 0):
        if pulse == SG90.PULSE_OFF:
            def_pulse = 0
        else:
            if pulse < SG90.PULSE_MIN:
                pulse = SG90.PULSE_MIN
            if pulse > SG90.PULSE_MAX:
                pulse = SG90.PULSE_MAX
            def_pulse = pulse - self.cur_pulse

        self.cur_pulse = pulse

        self.pi.set_servo_pulsewidth(self.pin, self.cur_pulse)
        time.sleep(abs(def_pulse) * SG90.SEC_PULSE + 0.2)

        if sec > 0:
            time.sleep(sec)

        return self.cur_pulse
        
#####
def main():
    Pin = 15
    
    pi = pigpio.pi()

    sm = SG90(Pin, pi)

    sys.argv.pop(0)
    print(len(sys.argv), sys.argv)
    if len(sys.argv) < 1:
        print(sm.set_pulse(SG90.PULSE_CENTER))
        print(sm.set_pulse(SG90.PULSE_MIN))
        print(sm.set_pulse(SG90.PULSE_MAX))
        print(sm.set_pulse(SG90.PULSE_MIN))
        print(sm.set_pulse(1400))
    else:
        for p in sys.argv:
            print(sm.set_pulse(int(p)))

if __name__ == '__main__':
    main()
