#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from AutoRobotTank import AutoRobotTank
from RobotTank import RobotTank
from RobotServer import RobotServer
import pigpio
import sys
import os

MyName = os.path.basename(sys.argv[0])

DEF_PIN_DC = [[12, 13], [18, 17]]
DEF_PIN_SERVO = 22
DEF_PORT_NUM = 12345

##### Main
def main():
    pin_dc = DEF_PIN_DC
    pin_servo = DEF_PIN_SERVO
    port_num = DEF_PORT_NUM

    if len(sys.argv) > 1:
        port_num = int(sys.argv[1])

    pi = pigpio.pi()
    
    print(MyName + ': pin_dc =', pin_dc)
    print(MyName + ': pin_servo =', pin_servo)
    robot = AutoRobotTank(pin_dc, pin_servo, pi)
#    robot = RobotTank(pin_dc, pi)
    robot.start()
    print(MyName + ': robot: started')

    print(MyName + ': port_num =', port_num)
    robot_server = RobotServer(robot, port_num)
    robot_server.serve_forever()

if __name__ == '__main__':
    try:
        main()
    except(KeyboardInterrupt):
        print(MyName + ': [Ctrl]+[C]')
    finally:
        print('=== ' + MyName + ': End ===')
