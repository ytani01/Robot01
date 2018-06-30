#!/usr/bin/env python3
#
import pigpio
import DcMtr

import csv
import time
import sys
import os

MYNAME = sys.argv[0].split('/').pop()
#####

class RobotTank:
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
    print(DEF_SPEED_VAL)

    def __init__(self, pin, conf_file=''):
        self.pin = pin
        self.n = len(pin)

        self.pi = pigpio.pi()

        self.speed_val = RobotTank.DEF_SPEED_VAL

        self.dc_mtr = DcMtr.DcMtrN(self.pi, self.pin)

        self.set_conf_file(conf_file)
        self.conf_load()

        self.move_stop()

    def __del__(self):
        print('set_stop()', '\r')
        self.move_stop()
        print('self.pi.stop()', '\r')
        self.pi.stop()
        print('self.conf_save()', '\r')
        self.conf_save()


    ### move command
    def move(self, key, sec=0):
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


#####
def main():
    PIN_DC_MOTOR = [[13,12],[17,18]]

    print(MYNAME)

    robot = RobotTank(PIN_DC_MOTOR)

    robot.move('forward', 0.5)
    robot.move_break(0.3)
    robot.move('left', 0.5)
    robot.move_break(0.3)


if __name__ == '__main__':
    try:
        main()
    finally:
        print('=== finally ===')
#        robot.end()
