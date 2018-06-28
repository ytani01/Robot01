#!/usr/bin/env python3
# -*- encode: utf-8 -*-
#
import pigpio
import VL53L0X
import DcMtr

import time
import sys
import os

MYNAME = sys.argv[0].split('/').pop()
#####
PIN_DC_MOTOR = [[13,12],[17,18]]

#####

class RobotTank:
    CONF_FILENAME = 'robot_tank.conf'
    CONF_FILE = os.environ['HOME']+'/'+CONF_FILENAME

#    DEF_SPEED={}
#    DEF_SPEED['forward'] = [100,100]
#    DEF_SPEED['backward'] = [100,100]
#    DEF_SPEED['left'] = [100,100]
#    DEF_SPEED['right'] = [100,100]
#    print(DEF_SPEED)
    DEF_SPEED_FORWARD = [100,100]
    DEF_SPEED_BACKWARD = [-100, -100]
    DEF_SPEED_LEFT = [-100, 100]
    DEF_SPEED_RIGHT = [100, -100]

    def __init__(self, pin, conf_file):
        self.speed_forward = RobotTank.DEF_SPEED_FORWARD
        self.speed_backward = RobotTank.DEF_SPEED_BACKWARD
        self.speed_left = RobotTank.DEF_SPEED_LEFT
        self.speed_right = RobotTank.DEF_SPEED_RIGHT

        self.set_conf_file(conf_file)
        self.conf_load()

        self.pi = pigpio.pi()

        self.tof = VL53L0X.VL53L0X()
        self.tof.start_ranging()

        self.dc_mtr = DcMtr.DcMtrN(self.pi, pin)

        self.move_stop()

        print(self.__dict__)

    def end(self):
        print('set_stop()')
        self.move_stop()
        print('self.conf_save()')
        self.conf_save()
        print('self.pi.stop()')
        self.pi.stop()
        print('self.tof.stop_ranging()')
        self.tof.stop_ranging()

    ###
    def move_stop(self, sec=0):
        self.dc_mtr.set_stop(sec)

    def move_break(self, sec=0):
        self.dc_mtr.set_break(sec)

    def move_speed(self, speed, sec=0):
        self.dc_mtr.set_speed(speed, sec)


    ###
    def set_conf_file(self, conf_file):
        self.conf_file = conf_file

    def conf_load(self):
        try:
            with open(self.conf_file, 'r', encoding='utf-8') as f:
                line = f.readline().strip('\r\n')
                self.speed_forward = list(map(int,line.split(' ')))
    
                line = f.readline().strip('\r\n')
                self.speed_backward = list(map(int,line.split(' ')))
    
                line = f.readline().strip('\r\n')
                self.speed_left = list(map(int,line.split(' ')))
    
                line = f.readline().strip('\r\n')
                self.speed_right = list(map(int,line.split(' ')))
    
        except(FileNotFoundError):
            print('!! '+conf_file+': not found .. use default value.')
    
        print(self.speed_forward, self.speed_backward, self.speed_left, self.speed_right)
    
    def conf_save(self):
        with open(self.conf_file, 'w', encoding='utf-8') as f:
            f.write(' '.join(map(str, self.speed_forward))+'\n')
            f.write(' '.join(map(str, self.speed_backward))+'\n')
            f.write(' '.join(map(str, self.speed_left))+'\n')
            f.write(' '.join(map(str, self.speed_right))+'\n')


#####
def main1(robot):
    print(MYNAME)
    print(RobotTank.CONF_FILE)

    robot.move_speed(robot.speed_forward)
    time.sleep(2)
    robot.move_break(0.3)
    robot.move_speed(robot.speed_backward)
    time.sleep(2)
    robot.move_break(0.3)


if __name__ == '__main__':
    robot = RobotTank(PIN_DC_MOTOR, RobotTank.CONF_FILE)
    try:
        main1(robot)
    finally:
        print('=== finally ===')
        robot.end()
