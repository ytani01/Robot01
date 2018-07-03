#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import RobotCar
import VL53L0X
import threading
import queue
import readchar
import time

PIN_CR_SERVO = [13, 12]

CmdQ = queue.Queue()

Tof = None
TofTiming = 0

DISTANCE_FAR = 1500
DISTANCE_NEAR = 300	# mm
DISTANCE_NEAR2 = 100	# mm

#####
def get_distance():
    N_MAX = 70
    
    distance = Tof.get_distance()
    print('distance: %d mm ' % distance, end='')
    n = int(distance/10)
    if n > N_MAX:
        n = N_MAX
    for i in range(n):
        print('*', end='')
    print('\r')
    return distance

#####
def robot_auto(myid, robot):
    print(myid, 'robot_auto():start', '\r')

    last_turn = 'left'
    forward_count = 0
    FORWARD_COUNT_MAX = 10

    robot.move('stop')
    
    while True:
        if not CmdQ.empty():
            robot.move('stop', 0.1)
            break

        distance = get_distance()

        if distance > DISTANCE_NEAR and forward_count < FORWARD_COUNT_MAX:
            robot.move('forward', 0.05)
            forward_count += 1
            #print('forward_count =', forward_count, '\r')
            continue

        if forward_count >= FORWARD_COUNT_MAX:
            if last_turn == 'left':
                last_turn = 'right'
            else:
                last_turn = 'left'
            robot.move(last_turn, 0.2)
            if distance < DISTANCE_FAR:
                robot.move('stop', 1)
            forward_count = 0
            continue

        ## Near
        robot.move('stop', 1)
        distance = get_distance()
        
        forward_count = 0

        while distance < DISTANCE_NEAR:
            print('!', '\r')
            if not CmdQ.empty():
                break
            
            if distance < DISTANCE_NEAR2:
                print('!!', '\r')
                robot.move('backward', 0.3)
                if last_turn == 'left':
                    last_turn = 'right'
                else:
                    last_turn = 'left'
                robot.move(last_turn, 1.0)

                robot.move('stop', 1)
                distance = get_distance()
                continue
            
            if last_turn == 'left':
                robot.move('right', 0.5)
            else:
                robot.move('left', 0.5)
            robot.move('stop', 1)
            distance = get_distance()

        if last_turn == 'left':
            last_turn = 'right'
        else:
            last_turn = 'left'
        print('last_turn =', last_turn, '\r')
            

    print(myid, 'robot_auto():end', '\r')

        
def robot_thread():
    myid = "robot_thread()"
    print(myid, 'start', '\r')

    robot = RobotCar.RobotCar(PIN_CR_SERVO)

    [idx_left, idx_right] = [0, 1]

    move_cmd = {\
                's':'stop', \
                'S':'break', \
                'w':'forward', \
                'x':'backward', \
                'a':'left', \
                'd':'right' \
    }

    move_stat = 'stop'
    robot.move('stop')
    
    while True:
        cmd = CmdQ.get()
        print('distance: %d mm' % get_distance(), '\r')

        if len(cmd) > 0:
            print(myid, '"'+cmd+'"', '\r')

        if cmd == ' ' or ord(cmd) < 20:
            robot.move('off')
            break

        ###
        if cmd == '@':
            robot_auto(myid, robot)

        if cmd == 'z':
            robot.increment_pulse_val(move_stat, idx_left, -5)
            robot.move(move_stat)
        if cmd == 'q':
            robot.increment_pulse_val(move_stat, idx_left, 5)
            robot.move(move_stat)
        if cmd == 'e':
            robot.increment_pulse_val(move_stat, idx_right, -5)
            robot.move(move_stat)
        if cmd == 'c':
            robot.increment_pulse_val(move_stat, idx_right, 5)
            robot.move(move_stat)

        ###
        if cmd in move_cmd.keys():
            move_stat = move_cmd[cmd]
            print(myid, cmd, '->', move_stat, '\r')
            robot.move(move_stat)

    robot = None
    print(myid, 'end', '\r')
           
#####
def readchar_thread():
    myid = 'readchar_thread()'
    print(myid, 'start', '\r')

    while True:
        ch = readchar.readchar()
        print(myid, '"'+ch+'"', '\r')

        CmdQ.put(ch)

        if ch == ' ' or ord(ch) <= 20:
            break

    print(myid, 'end', '\r')
    
#####
def main():
    global Tof
    global TofTiming

    Tof = VL53L0X.VL53L0X()
    Tof.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)
    TofTiming = Tof.get_timing()
    if TofTiming < 20000:
        TofTiming = 20000
    print("TofTiming = %d ms" % (TofTiming/1000))
    print('distance: %d mm' % get_distance())

    robot_th = threading.Thread(target=robot_thread, daemon=True)
    robot_th.start()

    readchar_th = threading.Thread(target=readchar_thread, daemon=True)
    readchar_th.start()

    
    #CmdQ.join()
    readchar_th.join()
    print('join: readchar_th')
    robot_th.join()
    print('join: robot_th')
    print('join done.')

if __name__ == '__main__':
    main()
