#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from RobotTank import RobotTank
from ServoMtr import SG90
import VL53L0X
import pigpio
import time
import sys


#####
class AutoRobotTank(RobotTank):
    DISTANCE_FAR	= 1000	# mm
    DISTANCE_NEAR	= 300	# mm
    DISTANCE_NEAR2	= 150	# mm

    def __init__(self, pin_dc, pin_servo, pi='', conf_file=''):
        self.myname = __class__.__name__
        print(self.myname + ': __init__()')
        print(self.myname + ': pin_dc =', pin_dc)
        print(self.myname + ': pin_servo =', pin_servo)

        self.cmd_auto = '@'

        self.servo = SG90(pin_servo, pi)

        self.tof = None
        self.tof_timing = 0
        self.init_VL53L0X()

        super().__init__(pin_dc, pi, conf_file)

    def init_VL53L0X(self):
        self.tof = VL53L0X.VL53L0X()
        self.tof.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)
        self.tof_timing = self.tof.get_timing()
        if self.tof_timing < 20000:
            self.tof_timing = 20000
        print('self.tof_timing = %d ms' % (self.tof_timing/1000))

    def get_distance(self):
        N_MAX = 70

        distance = self.tof.get_distance()
        print('%5.1fcm ' % (distance/10), end='')
        n = int(distance/10)
        if n > N_MAX:
            n = N_MAX
        for i in range(n):
            print('*', end='')
        print('\r')
        return distance

    def auto(sefl):
        print(self.myname + ': auto(): start')

        ## XXX
        while True:
            if not self.cmd_empty():
                self.move('break')
                break

        print(self.myname + ':auto(): end')

    def exec_cmd(self, cmd):
        if cmd == self.cmd_auto:
            self.auto()
        else:
            if cmd == 'a':
                self.servo.set_pulse(2000)
            elif cmd == 'd':
                self.servo.set_pulse(1000)
            else:
                self.servo.set_pulse(1400)
            super().exec_cmd(cmd)

        return cmd

#####
def main():
    pin_dc = [[12, 13], [18, 17]]
    pin_servo = 27
    pi = pigpio.pi()

    robot = AutoRobotTank(pin_dc, pin_servo, pi)
    robot.start()
    time.sleep(1)

    robot.send_cmd('w')
    time.sleep(1)
    robot.send_cmd('S')
    time.sleep(1)
    robot.send_cmd('x')
    time.sleep(1)
    robot.send_cmd('S')
    time.sleep(1)
    robot.send_cmd('a')
    time.sleep(1)
    robot.send_cmd('S')
    time.sleep(1)
    robot.send_cmd('d')
    time.sleep(1)
    robot.send_cmd('S')
    time.sleep(1)
    robot.send_cmd('s')

    robot.send_cmd(robot.cmd_end)

if __name__ == '__main__':
    main()
