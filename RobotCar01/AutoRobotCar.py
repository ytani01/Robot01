#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import RobotCar
import pigpio
import VL53L0X
import time
import sys

#####
class AutoRobotCar(RobotCar.RobotCar):
    Tof = None
    TofTiming = 0
    
    def __init__(self, pin, pi='', conf_file=''):
        self.init_VL53L0X()

        print('AutoRobotCar: super().__init__(pin, pi, conf_file)')
        super().__init__(pin, pi, conf_file)
        print('AutoRobotCar: init():done')

    def init_VL53L0X(self):
        AutoRobotCar.Tof = VL53L0X.VL53L0X()
        AutoRobotCar.Tof.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)
        AutoRobotCar.TofTiming = AutoRobotCar.Tof.get_timing()
        if AutoRobotCar.TofTiming < 20000:
            AutoRobotCar.TofTiming = 20000
        print('TofTiming = %d ms' % (AutoRobotCar.TofTiming/1000))
        
    def get_distance(self):
        N_MAX = 70

        distance = AutoRobotCar.Tof.get_distance()
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

        DISTANCE_FAR	= 700	# mm
        DISTANCE_NEAR	= 350	# mm
        DISTANCE_NEAR2	= 150	# mm

        left_or_right = 'left'
        forward_count = 0
        FORWARD_COUNT_MAX = 10

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

            if distance > DISTANCE_NEAR and forward_count < FORWARD_COUNT_MAX:
                self.move('forward', 0.05)
                forward_count += 1
                continue

            if forward_count > FORWARD_COUNT_MAX:
                left_or_right = next_turn_random(left_or_right)
                self.move(left_or_right, 0.1)
                if distance < DISTANCE_FAR:
                    self.move('stop', 0.5)
                forward_count = 0
                continue

            ## Near
            self.move('stop', 1)
            distance = self.get_distance()

            forward_count = 0

            left_or_right = next_turn_random(left_or_right)
            while distance < DISTANCE_NEAR + 20:
                print('!')
                if not self.cmd_empty():
                    break

                if distance < DISTANCE_NEAR2:
                    print('!!')
                    self.move('backward', 0.2)
                    distance = self.get_distance()
                    continue

                self.move(left_or_right, 0.5)
                self.move('stop', 1)
                distance = self.get_distance()

        print('auto(): end')

    ### Thread
    def run(self):
        self.auto()
                
#####
def main():
    pin = [13, 12]
    pi = pigpio.pi()

    robot = AutoRobotCar(pin, pi)
    robot.start()

    count = 10
    c = 0
    for c in range(count, 0, -1):
        print('### count:', c)
        time.sleep(1)
    print('### count: 0')
    robot.send_cmd('stop')
    robot.join()

if __name__ == '__main__':
    main()
