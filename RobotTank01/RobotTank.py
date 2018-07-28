#!/usr/bin/env python3
#
import pigpio
import DcMtr

import queue
import threading
import csv
import time
import sys
import os

#####

class RobotTank(threading.Thread):
    DEF_CONF_FILENAME = 'robot_tank.csv'
    DEF_CONF_FILE = './' + DEF_CONF_FILENAME

    MAX_SPEED_VAL = 100
    MIN_SPEED_VAL = -MAX_SPEED_VAL
    
    DEF_SPEED_VAL={}
    DEF_SPEED_VAL['off'] 	= [0,0]
    DEF_SPEED_VAL['stop'] 	= [0,0]
    DEF_SPEED_VAL['break'] 	= [0,0]
    DEF_SPEED_VAL['forward']	= [100,100]
    DEF_SPEED_VAL['backward']	= [-100,-100]
    DEF_SPEED_VAL['left'] 	= [-100,100]
    DEF_SPEED_VAL['right'] 	= [100,-100]

    def __init__(self, pin, pi='', conf_file=''):
        self.myname = __class__.__name__
        print(self.myname + ': __init__()')
        
        self.pin = pin
        self.n = len(pin)

        ## Command queue
        self.cmdq = queue.Queue()

        ## Init pigpio
        if type(pi) == pigpio.pi:
            self.pi = pi
            self.mypi = False
        else:
            self.pi = pigpio.pi()
            self.mypi = True

        ## Init DC Motors
        self.dc_mtr = DcMtr.DcMtrN(self.pi, self.pin)

        ## move_cmd
        self.move_cmd = {}
        self.move_cmd['s'] = 'stop'
        self.move_cmd['S'] = 'break'
        self.move_cmd['w'] = 'forward'
        self.move_cmd['x'] = 'backward'
        self.move_cmd['a'] = 'left'
        self.move_cmd['d'] = 'right'
        self.cmd_end = ' '

        self.move_stat = 'stop'
        
        ## Init speed values
        self.speed_val = RobotTank.DEF_SPEED_VAL

        self.set_conf_file(conf_file)
        self.conf_load()

        ## Stop Motors
        self.move_stop()

        super().__init__()

    def __del__(self):
        print(self.myname + ': __del__()')

        print('set_stop()', '\r')
        self.move_stop()
        if self.mypi:
            print('self.pi.stop()', '\r')
            self.pi.stop()
        print('self.conf_save()', '\r')
        self.conf_save()

    ### cmdq
    def send_cmd(self, cmd):
        print(self.myname + ': send_cmd(\'' + str(cmd) + '\')')
        self.cmdq.put(cmd)

    def recv_cmd(self):
        cmd = self.cmdq.get()
        print(self.myname + ': recv_cmd(\'' + str(cmd) + '\')')
        return cmd

    def cmd_empty(self):
        return self.cmdq.empty()

    ### move command
    def move(self, key, sec=0):
        self.move_stat = key
        
        if key == 'break':
            self.move_break()
        elif key == 'stop':
            self.move_stop()
        else:
            self.move_speed(self.speed_val[key])

        time.sleep(sec)
            
    ### move primitive
    def move_stop(self, sec=0):
        self.dc_mtr.set_stop(sec)

    def move_break(self, sec=0):
        self.dc_mtr.set_break(sec)

    def move_speed(self, speed, sec=0):
        #print('speed=', speed)
        self.dc_mtr.set_speed(speed, sec)

    ### change speed value
    def change_speed_val(self, key, idx, d_val):
        new_val = self.speed_val[key][idx] + d_val
        if new_val < RobotTank.MIN_SPEED_VAL:
            new_val = RobotTank.MIN_SPEED_VAL
        if new_val > RobotTank.MAX_SPEED_VAL:
            new_val = RobotTank.MAX_SPEED_VAL
        self.speed_val[key][idx] = new_val
        
        self.conf_save(self.conf_file)
        return self.speed_val[key][idx]

    ### conf_file
    def set_conf_file(self, conf_file=''):
        if conf_file == '':
            conf_file = RobotTank.DEF_CONF_FILE
        self.conf_file = conf_file

    def conf_load(self, conf_file=''):
        if conf_file == '':
            conf_file = self.conf_file
        
        if conf_file == '':
            conf_file = RobotTank.DEF_CONF_FILE

        try:
            with open(conf_file, 'r', encoding='utf-8') as f:
                csv_reader = csv.reader(f, delimiter=',', quotechar='"')
                for row in csv_reader:
                    if len(row) < len(self.speed_val['stop']):
                        continue
                    if row[0][0:1] == '#':
                        continue

                    self.speed_val[row[0].lower()] = [int(row[1]), int(row[2])]
                
        except(FileNotFoundError):
            print('!! '+conf_file+': not found .. use default value.')
    
    
    def conf_save(self, conf_file=''):
        if conf_file == '':
            conf_file = self.conf_file
        
        if conf_file == '':
            conf_file = RobotTank.DEF_CONF_FILE

        try:
            with open(self.conf_file, 'w', encoding='utf-8') as f:
                csv_writer = csv.writer(f, lineterminator='\n')
                csv_writer.writerow(['#Key', 'Left Motor', 'Right Motor'])

                for k in self.speed_val.keys():
                    csv_writer.writerow([k, \
                                         self.speed_val[k][0], \
                                         self.speed_val[k][1]])

        except(FileNotFoundError):
            print('!! '+conf_file+': not found .. use default value.')

    ## Control
    def exec_cmd(self, cmd):
        print(self.myname + ': exec_cmd(\'' + str(cmd) + '\')')

        [idx_left, idx_right] = [0, 1]
        
        if cmd in self.move_cmd.keys():
            print(cmd + ': ' + self.move_cmd[cmd])
            self.move(self.move_cmd[cmd])
            return cmd

        ###
        if cmd == 'q':
            sv = self.change_speed_val(move_stat, idx_left, +5)
            self.move(move_stat)
            print(move_stat, idx_left, sv)
            
        if cmd == 'z':
            sv = self.change_speed_val(move_stat, idx_left, -5)
            self.move(move_stat)
            print(move_stat, idx_left, sv)

        if cmd == 'e':
            sv = self.change_speed_val(move_stat, idx_right, +5)
            self.move(move_stat)
            print(move_stat, idx_right, sv)

        if cmd == 'c':
            sv = self.change_speed_val(move_stat, idx_right, +5)
            self.move(move_stat)
            print(move_stat, idx_right, sv)

        if cmd == '.':
            time.sleep(0.5)
            
    ## Thread
    def run(self):
        while True:
            cmd = self.recv_cmd()
            self.exec_cmd(cmd)
            if cmd == self.cmd_end:
                break

            time.sleep(0.01)

#####
def main():
    PIN_DC_MOTOR = [[17,18], [13,12]]

    robot = RobotTank(PIN_DC_MOTOR)
    robot.start()
    time.sleep(1)

    robot.send_cmd('a')
    time.sleep(1)
    robot.send_cmd('S')
    time.sleep(1)
    robot.send_cmd('d')
    time.sleep(1)
    robot.send_cmd('S')
    time.sleep(1)
    robot.send_cmd('s')
    time.sleep(1)
    robot.send_cmd(' ')

if __name__ == '__main__':
    try:
        main()
    finally:
        print('=== finally ===')
