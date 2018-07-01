#!/usr/bin/env python3
#

import RobotTank
import VL53L0X

import threading
import queue
import readchar

import time

PIN_DC_MOTOR = [[17, 18], [13, 12]]

CmdQ = queue.Queue()

Tof = None
TofTimeing = 0

DISTANCE_NEAR	= 300	# mm
DISTANCE_NEAR2	= 100	# mm

#####
def get_distance():
    N_MAX = 70

    distance = Tof.get_distance()
    print('distance: %d mm ' % distance, end='')
    n = int(distance / 10)
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
            robot.move('break', 0.2)
            break

        distance = get_distance()

        if distance > DISTANCE_NEAR and forward_count < FORWARD_COUNT_MAX:
            robot.move('forward', 0.1)
            forward_count += 1
            print('forward_count =', forward_count, '\r')
            continue

        if forward_count >= FORWARD_COUNT_MAX:
            if last_turn == 'left':
                last_turn = 'right'
            else:
                last_turn = 'left'
            robot.move(last_turn, 0.7)
            robot.move('break', 1)
            forward_count = 0
            continue

        ## Near
        robot.move('break', 1)
        
        distance = get_distance()

        forward_count = 0

        if last_turn == 'left':
            last_turn = 'right'
        else:
            last_turn = 'left'
            
        while distance < DISTANCE_NEAR:
            print('!', '\r')

            robot.move(last_turn, 0.5)
            robot.move('break', 1)
            distance = get_distance()

        print('last_turn =', last_turn, '\r')

    print(myid, 'robot_auto():end', '\r')

#####
def robot_thread():
    myid = 'robot_thread()'
    print(myid, 'start', '\r')

    robot = RobotTank.RobotTank(PIN_DC_MOTOR)

    [idx_left, idx_right] = [0, 1]

    move_cmd = {}
    move_cmd['s'] = 'stop'
    move_cmd['S'] = 'break'
    move_cmd['w'] = 'forward'
    move_cmd['x'] = 'backward'
    move_cmd['a'] = 'left'
    move_cmd['d'] = 'right'
    move_cmd[' '] = 'off'

    move_stat = 'stop'
    robot.move('stop')

    while True:
        cmd = CmdQ.get()

        get_distance()
        
        if len(cmd) > 0:
            print(myid, '"'+cmd+'"', '\r')

        if cmd == ' ' or ord(cmd) < 20:
            robot.move('off')
            break
        
        ###
        if cmd == '@':
            robot_auto(myid, robot)

        if cmd == 'q':
            sv = robot.change_speed_val(move_stat, idx_left, +5)
            robot.move(move_stat)
            print(move_stat, idx_left, sv)

        if cmd == 'z':
            sv = robot.change_speed_val(move_stat, idx_left, -5)
            robot.move(move_stat)
            print(move_stat, idx_left, sv)

        if cmd == 'e':
            sv = robot.change_speed_val(move_stat, idx_right, +5)
            robot.move(move_stat)
            print(move_stat, idx_left, sv)

        if cmd == 'c':
            sv = robot.change_speed_val(move_stat, idx_right, -5)
            robot.move(move_stat)
            print(move_stat, idx_left, sv)

        ###
        if cmd in move_cmd.keys():
            move_stat = move_cmd[cmd]
            print('break', '\r')
            robot.move('break', 0.2)
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
    print("TofTiming = %d ms" % (TofTiming / 1000))
    get_distance()

    robot_th = threading.Thread(target=robot_thread, daemon=True)
    robot_th.start()

    readchar_th = threading.Thread(target=readchar_thread, daemon=True)
    readchar_th.start()

    readchar_th.join()
    print('join: readchar_th')

    robot_th.join()
    print('join: robot_th')

    print('jone: done.')

if __name__ == '__main__':
    main()
    
