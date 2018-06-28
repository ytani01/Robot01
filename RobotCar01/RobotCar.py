#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pigpio
import CR_Servo

import os
import sys
import time
import csv

#####
class RobotCar:
    DEF_CONF_FILENAME = 'robot_car.csv'
    #DEF_CONF_FILE = os.environ['HOME']+'/'+DEF_CONF_FILENAME
    DEF_CONF_FILE = './'+DEF_CONF_FILENAME

    DEF_PULSE_VAL = { 'off':      [0,0], \
                      'stop':     [1480,1480], \
                      'break':    [1480,1480], \
                      'forward':  [1580,1380], \
                      'backward': [1380,1580], \
                      'left':     [1580,1580], \
                      'right':    [1380,1380]   }

    def __init__(self, pin, conf_file=''):
        self.pi = pigpio.pi()
        self.pin = pin
        self.n = len(pin)

        self.cr_servo = CR_Servo.CR_Servo_N(self.pi, self.pin)

        self.pulse_val = RobotCar.DEF_PULSE_VAL

        self.conf_file = conf_file
        if self.conf_file == '':
            self.conf_file = RobotCar.DEF_CONF_FILE
        self.conf_load(self.conf_file)

        self.move('stop')

    def __del__(self):
        print('=== RobotCar self.__del__() ===')
        print('RobotCar self.move(\'stop\')')
        self.move('stop')
        print('RobotCar self.move(\'off\')')
        self.move('off')
        print('RobotCar self.pi.stop()', end='')
        self.pi.stop()
        print('.')
       
    ###
    def move(self, key, sec=0.0):
        #print(key)
        self.set_pulse(self.pulse_val[key], sec)

    ###
    def set_pulse(self, pulse, sec=0.0):
        self.cr_servo.set_pulse(pulse, sec)

    def increment_pulse_val(self, key, idx, d_val):
        self.pulse_val[key][idx] += d_val
        #print(key, self.pulse_val[key][idx])
        self.conf_save(self.conf_file)
        
    def change_pulse_val(self, key, val):
        self.pulse_val[key] = val
        self.conf_save(self.conf_file)

    def conf_load(self, conf_file=''):
        if conf_file == '':
            conf_file = RobotCar.DEF_CONF_FILE
        #print('conf_file =', conf_file)

        with open(conf_file, 'r', encoding='utf-8') as f:
            csv_reader = csv.reader(f, delimiter=',', quotechar='"')
            for row in csv_reader:
                #print(row)
                if len(row) < len(self.pulse_val['stop']):
                    #print('empty')
                    continue
                if row[0][0:1] == '#':
                    #print('ignore')
                    continue

                self.pulse_val[row[0].lower()] = [int(row[1]), int(row[2])]

        #print(self.pulse_val)

    def conf_save(self, conf_file=''):
        if conf_file == '':
            conf_file = RobotCar.DEF_CONF_FILE
        #print('conf_file =', conf_file)

        with open(conf_file, 'w', encoding='utf-8') as f:
            csv_writer = csv.writer(f, lineterminator='\n')
            csv_writer.writerow(['#Key', 'Left Motor', 'Right Motor'])

            for k in self.pulse_val.keys():
                #print(k, self.pulse_val[k])
                csv_writer.writerow([k, \
                                     self.pulse_val[k][0], \
                                     self.pulse_val[k][1]])


#####
def main():
    pin = [12, 13]

    robot = RobotCar(pin)

    robot.conf_save()
    
    robot.move('forward', 0.1)
    robot.move('stop', 1)
    robot.increment_pulse_val('stop', 0, +10)
    robot.move('backward', 0.1)
    robot.move('stop', 1)
    robot.increment_pulse_val('stop', 0, -10)
    robot.move('left', 0.5)
    robot.move('stop', 1)
    robot.move('right', 1)
    robot.move('stop', 1)
    robot.move('off')

if __name__ == '__main__':
    main()
