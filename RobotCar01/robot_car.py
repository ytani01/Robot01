#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import AutoRobotCar
import threading
import readchar
import time

robot_th = None
readchar_th = None

#####
def readchar_thread():
    myid = 'readchar_thread()'
    print(myid, 'start', '\r')

    while True:
        ch = readchar.readchar()
        print(myid, '"'+ch+'"', '\r')

        if ch == ' ' or ord(ch) <= 20:
            break

    print(myid, 'end', '\r')
    
#####
def main():
    global robot_th, readchar_th
    
    pin = [13, 12]
    pi = pigpio.pi()
    
    robot_th = AutoRobotCar(pin, pi)
    robot_th.start()

    readchar_th = threading.Thread(target=readchar_thread, daemon=True)
    readchar_th.start()

    ##
    readchar_th.join()
    print('join: readchar_th')
    robot_th.join()
    print('join: robot_th')
    print('join done.')

if __name__ == '__main__':
    main()
