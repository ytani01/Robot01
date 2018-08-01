#!/usr/bin/env python
# -*- coding: utf-8 -*-

import VL53L0X
from ServoMtr import SG90
import pigpio
import time

#####
def main():
    PIN_SERVO = 27

    vl = VL53L0X.VL53L0X()
    vl.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)
    vl_timing = vl.get_timing()
    if vl_timing < 20000:
        vl_timing = 20000

    pi = pigpio.pi()
    sm = SG90(PIN_SERVO, pi)
    
    for i in range(3):
        print('pulse', sm.set_pulse(SG90.PULSE_MIN+i*500))
        
        d = vl.get_distance()
        print('distance', d)
        time.sleep(1)

    sm.set_pulse(SG90.PULSE_CENTER)
    
    for i in range(3):
        d = vl.get_distance()
        print(d)
        time.sleep(1)

    
if __name__ == '__main__':
    main()
