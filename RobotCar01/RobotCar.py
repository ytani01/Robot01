#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pigpio
import CR_Servo

import os
import sys
import time
import csv
import queue
import threading

#####
class RobotCar(threading.Thread):
    CHCMD_END = ' '
    
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

    def __init__(self, pin, pi='', conf_file=''):
        self.pin = pin
        self.n = len(pin)

        self.cmdq = queue.Queue()

        ## init pigpio
        if type(pi) == pigpio.pi:
            self.pi = pi
            self.mypi = False
        else:
            self.pi = pigpio.pi()
            self.mypi = True

        ## init Servo
        self.cr_servo = CR_Servo.CR_Servo_N(self.pi, self.pin)

        ## move_cmd
        self.move_cmd = {}
        self.move_cmd['s'] = 'stop'
        self.move_cmd['S'] = 'break'
        self.move_cmd['w'] = 'forward'
        self.move_cmd['x'] = 'backward'
        self.move_cmd['a'] = 'left'
        self.move_cmd['d'] = 'right'

        ## init pulse value
        self.pulse_val = RobotCar.DEF_PULSE_VAL

        self.conf_file = conf_file
        if self.conf_file == '':
            self.conf_file = RobotCar.DEF_CONF_FILE
        self.conf_load(self.conf_file)

        ##
        self.cur_move = ''
        self.move('stop')

        print('RobotCar: super()__init__()')
        super().__init__()
        print('RobotCar: init():done')

    def __del__(self):
        print('=== RobotCar: self.__del__() ===')
        '''
        print('RobotCar self.move(\'stop\')')
        self.move('stop')
        print('RobotCar self.move(\'off\')')
        self.move('off')
        '''
        if self.mypi:
            print('=== RobotCar: self.pi.stop() ===')
            self.pi.stop()
        print('=== RoBotCar: End ===')

    ### cmdq
    def send_cmd(self, cmd):
        print('send_cmd(\''+str(cmd)+'\')')
        self.cmdq.put(cmd)

    def recv_cmd(self):
        cmd = self.cmdq.get()
        print('recv_cmd(\''+str(cmd)+'\')')
        return cmd

    def cmd_empty(self):
        return self.cmdq.empty()

    ### move
    def move(self, key, sec=0.0):
        self.set_pulse(self.pulse_val[key], sec)
        self.cur_move = key

    ### pulse 
    def set_pulse(self, pulse, sec=0.0):
        self.cr_servo.set_pulse(pulse, sec)

    def increment_pulse_val(self, idx, d_val):
        key = self.cur_move
        
        self.pulse_val[key][idx] += d_val
        self.conf_save(self.conf_file)

        self.move(key)

    ### config file
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

    ### Control
    def exec_cmd(self, cmd):
        print('exec_cmd(\''+str(cmd)+'\')')

        [idx_left, idx_right] = [0, 1]
        
        if cmd in self.move_cmd.keys():
            print(cmd, ':', self.move_cmd[cmd])
            self.move(self.move_cmd[cmd])
            return cmd
        
        if cmd == 'z':
            self.increment_pulse_val(idx_left, -5)
        if cmd == 'q':
            self.increment_pulse_val(idx_left, +5)
        if cmd == 'e':
            self.increment_pulse_val(idx_right, -5)
        if cmd == 'c':
            self.increment_pulse_val(idx_right, +5)

        if cmd == '.':
            time.sleep(0.5)
            
        return cmd
            
    ### Thread
    def run(self):
        while True:
            cmd = self.recv_cmd()
            self.exec_cmd(cmd)
            if cmd == RobotCar.CHCMD_END:
                break

            time.sleep(0.01)

#####
def main():
    pin = [13, 12]

    robot = RobotCar(pin)
    robot.start()
    time.sleep(1)
    
    print('send_cmd(x)')
    robot.send_cmd('x')
    time.sleep(0.2)
    robot.send_cmd('s')
    time.sleep(1)

    print('move(forward)')
    robot.move('forward', 0.2)
    robot.move('stop', 1)
    print('move(backward)')
    robot.move('backward', 0.2)
    robot.move('stop', 1)

    print('send_cmd( )')
    robot.send_cmd(RobotCar.CHCMD_END)

    print('join')
    robot.join()
    robot.move('off')

if __name__ == '__main__':
    main()
