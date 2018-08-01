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
        self.servo_angle_min = 500
        self.servo_angle_max = 2300
        self.servo_angle_center = 1400
        self.servo_angle_left = self.servo_angle_max
        self.servo_angle_right = self.servo_angle_min

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
        print(self.tof.get_distance())

    def set_servo_angle(self, angle=0):
        if angle == 0:
            angle = self.servo_angle_center
        if angle < self.servo_angle_min:
            angle = self.servo_angle_min
        if angle > self.servo_angle_max:
            angle = self.servo_angle_max

        print('set_servo_angle(): angle =', angle)
            
        self.servo.set_pulse(angle)

    def get_distance(self, angle=0):
        N_MAX = 70

        '''
        if angle > 0:
            self.set_servo_angle(angle)
        '''

        ### XXX 
        distance = self.tof.get_distance()
        #distance = 1000
        print('%5.1fcm ' % (distance/10), end='')
        ###
        
        n = int(distance/10)
        if n > N_MAX:
            n = N_MAX
        for i in range(n):
            print('*', end='')
        print('\r')
        return distance

    def auto(self):
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
                self.get_distance(self.servo_angle_left)
            elif cmd == 'd':
                self.get_distance(self.servo_angle_right)
            else:
                self.get_distance(self.servo_angle_center)
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
