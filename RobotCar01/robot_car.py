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

DISTANCE_FAR = 700
DISTANCE_NEAR = 350	# mm
DISTANCE_NEAR2 = 150	# mm

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
def next_turn_random(last_turn):
    r = int(time.time() * 100) % 10
    if r < 8:
        if last_turn == 'left':
            next_turn = 'right'
        else:
            next_turn = 'left'
        return next_turn
    else:
        r = int(time.time() * 100) % 2
        if r == 0:
            next_turn = 'left'
        else:
            next_turn = 'right'

    print('next_turn_random(): next_turn =', next_turn, '\r')
    return next_turn
    
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
            last_turn = next_turn_random(last_turn)
            robot.move(last_turn, 0.2)
            if distance < DISTANCE_FAR:
                robot.move('stop', 1)
            forward_count = 0
            continue

        ## Near
        robot.move('stop', 1)
        distance = get_distance()
        
        forward_count = 0

        next_turn = next_turn_random(last_turn)
        while distance < DISTANCE_NEAR + 30:
            print('!', '\r')
            if not CmdQ.empty():
                break
            
            if distance < DISTANCE_NEAR2:
                print('!!', '\r')
                robot.move('backward', 0.3)
                #robot.move('stop', 1)
                distance = get_distance()
                continue
            
            robot.move(next_turn, 0.5)
            last_turn = next_turn
            robot.move('stop', 1)
            distance = get_distance()

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
