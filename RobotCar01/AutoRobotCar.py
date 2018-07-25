#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import RobotCar
import pigpio
import VL53L0X
import time
import sys

#####
class AutoRobotCar(RobotCar.RobotCar):
    DISTANCE_FAR	= 700	# mm
    DISTANCE_NEAR	= 300	# mm
    DISTANCE_NEAR2	= 150	# mm
    FORWARD_COUNT_MAX = 10

    def __init__(self, pin, pi='', conf_file=''):
        self.tof = None
        self.tof_timing = 0
        self.init_VL53L0X()

        print('AutoRobotCar: super().__init__(pin, pi, conf_file)')
        super().__init__(pin, pi, conf_file)
        print('AutoRobotCar: init():done')

    def init_VL53L0X(self):
        self.tof = VL53L0X.VL53L0X()
        self.tof.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)
        self.tof_timing = self.tof.get_timing()
        if self.tof_timing < 20000:
            self.tof_timing = 20000
        print('TofTiming = %d ms' % (self.tof_timing/1000))
        
    def get_distance(self):
        N_MAX = 70

        distance = self.tof.get_distance()
        print('%5.1fcm ' % (distance/10), end='')
        n = int(distance/10)
        if n > N_MAX:
            n = N_MAX
        for i in range(n):
            print('*', end='')
        print('\r')
        return distance

    def auto(self):
        print('auto(): start')

        left_or_right = 'left'
        forward_count = 0

        self.move('stop')

        ###
        def next_turn_random(last_turn):
            next_turn = ''
            r = int(time.time() * 100) % 10
            if r < 8:  # 80%
                if last_turn == 'left':
                    next_turn = 'right'
                elif last_turn == 'right':
                    next_turn = 'left'

            if next_turn == '':
                r = r % 2
                if r == 0:
                    next_turn = 'left'
                else:
                    next_turn = 'right'

            print('next_turn =', next_turn)
            return next_turn

        ###
        while True:
            if not self.cmd_empty():
                self.move('stop')
                break

            distance = self.get_distance()
            if distance > AutoRobotCar.DISTANCE_NEAR and \
               forward_count < AutoRobotCar.FORWARD_COUNT_MAX:
                self.move('forward', 0.05)
                forward_count += 1
                continue

            if forward_count >= AutoRobotCar.FORWARD_COUNT_MAX:
                left_or_right = next_turn_random(left_or_right)
                print(left_or_right)
                self.move(left_or_right, 0.2)
                if distance < AutoRobotCar.DISTANCE_FAR:
                    self.move('stop', 0.5)
                forward_count = 0
                continue

            ## Near
            self.move('stop', 1)
            distance = self.get_distance()

            forward_count = 0

            left_or_right = next_turn_random(left_or_right)
            while distance < AutoRobotCar.DISTANCE_NEAR + 20:
                print('!')
                if not self.cmd_empty():
                    break

                if distance < AutoRobotCar.DISTANCE_NEAR2:
                    print('!!')
                    self.move('backward', 0.1)
                    self.move(left_or_right, 0.5)
                    self.move('stop', 1)
                    distance = self.get_distance()
                    continue

                self.move(left_or_right, 0.5)
                self.move('stop', 1)
                distance = self.get_distance()

        print('auto(): end')

    ### Control
    def exec_cmd(self, cmd):
        if cmd == '@':
            self.auto()
        else:
            super().exec_cmd(cmd)

        return cmd
                
#####
def main():
    pin = [13, 12]
    pi = pigpio.pi()

    robot = AutoRobotCar(pin, pi)
    robot.start()
    time.sleep(1)

    robot.send_cmd('a')
    time.sleep(0.2)
    robot.send_cmd('s')
    time.sleep(1)
    robot.send_cmd('d')
    time.sleep(0.2)
    robot.send_cmd('s')
    time.sleep(1)
    
    robot.send_cmd('@')
    count = 7
    c = 0
    for c in range(count, 0, -1):
        print('### count:', c)
        time.sleep(1)
    print('### count: 0')

    robot.send_cmd('s')
    time.sleep(1)

    robot.send_cmd('a')
    time.sleep(0.2)
    robot.send_cmd('s')
    time.sleep(1)
    robot.send_cmd('d')
    time.sleep(0.2)
    robot.send_cmd('s')
    time.sleep(1)

    robot.send_cmd(AutoRobotCar.CHCMD_END)
    robot.join()

if __name__ == '__main__':
    main()
