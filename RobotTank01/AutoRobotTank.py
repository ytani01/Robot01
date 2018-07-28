#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from RobotTank import RobotTank
from ServoMtr import SG90
import pigpio
import VL53L0X
import time
import sys


#####
class AutoRobotTank(RobotTank):
    DISTANCE_FAR	= 1000	# mm
    DISTANCE_NEAR	= 300	# mm
    DISTANCE_NEAR2	= 150	# mm

    def __init__(self, pin, pi='', conf_file=''):
        self.myname = __class__.__name__
        print(self.myname + ': __init__()')

        self.tof = None
        self.tof_timing = 0
        self.init_VL53L0X()

        self.cmd_auto = '@'

        super().__init__(pin, pi, conf_file)

    def init_VL53L0X(self):
        self.tof = VL53L0X.VL53L0X()
        self.tof.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)
        self.tof_timing = self.tof.get_timing()
        if self.tof_timing < 20000:
            self.tof_timing = 20000
        print('self.tof_timing = %d ms' % (self.tof_timing/1000))

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
            super().exec_cmd(cmd)

        return cmd

#####
def main():
    pin = [[17, 18], [13, 12]]

    robot = AutoRobotTank(pin)
    robot.start()
    time.sleep(1)

    robot.send_cmd('w')
    time.sleep(1)
    robot.send_cmd('S')
    time.sleep(1)
    robot.send_cmd('x')
    time.sleep(1)
    robot.sned_cmd('S')
    time.sleep(1)
    robot.send_cmd('s')
    robot.send_cmd(' ')

if __name__ == '__main__':
    main()
