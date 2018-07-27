#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from AutoRobotCar import AutoRobotCar
from RobotServer import RobotServer
import sys
import os

MyName = os.path.basename(sys.argv[0])
    
DEF_PIN = [13, 12]
DEF_PORT_NUM = 12345

##### Main
def main():
    pin = DEF_PIN
    port = DEF_PORT_NUM

    if len(sys.argv) > 1:
        port_num = int(sys.argv[1])

    print(MyName + ': pin =', pin)
    robot = AutoRobotCar(pin)
    robot.start()
    print(MyName + ': robot: started')

    print(MyName + ': port =', port)
    robot_server = RobotServer(robot, port)
    robot_server.serve_forever()

if __name__ == '__main__':
    try:
        main()
    except(KeyboardInterrupt):
        print(MyName + ': [Ctrl]-[C]')
    finally:
        print('=== ' + MyName + ': End ===')
