#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from AutoRobotCar import AutoRobotCar
from RobotServer import RobotServer
import sys
import os

DEF_PIN = [13, 12]
DEF_PORT_NUM = 12345

##### Main
def main(myname):
    pin = DEF_PIN
    port = DEF_PORT_NUM

    if len(sys.argv) > 1:
        port_num = int(sys.argv[1])

    print(myname + ': pin =', pin)
    robot = AutoRobotCar(pin)
    robot.start()
    print(myname + ': robot: started')

    print(myname + ': port =', port)
    robot_server = RobotServer(robot, port)
    robot_server.serve_forever()

if __name__ == '__main__':
    myname = os.path.basename(sys.argv[0])
    
    try:
        main(myname)
    except(KeyboardInterrupt):
        print(myname + ': [Ctrl]-[C]')
    finally:
        print('=== ' + myname + ': End ===')
