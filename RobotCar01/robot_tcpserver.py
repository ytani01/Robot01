#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import AutoRobotCar
import pigpio
import threading
import socketserver
import time
import sys

DEF_PORT = 12345

PIN_CR_SERVO = [13, 12]


def robot_thread():
    global RobotServer
    
    myid = "robot_thread()"
    print(myid, 'start', '\r')

    robot = AutoRobotCar.AutoRobotCar(PIN_CR_SERVO)

    [idx_left, idx_right] = [0, 1]

    move_cmd = {}
    move_cmd['s'] = 'stop'
    move_cmd['S'] = 'break'
    move_cmd['w'] = 'forward'
    move_cmd['x'] = 'backward'
    move_cmd['a'] = 'left'
    move_cmd['d'] = 'right'

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
        if cmd == 'q':
            robot.increment_pulse_val(move_stat, idx_left, 5)
        if cmd == 'e':
            robot.increment_pulse_val(move_stat, idx_right, -5)
        if cmd == 'c':
            robot.increment_pulse_val(move_stat, idx_right, 5)

        ###
        if cmd in move_cmd.keys():
            move_stat = move_cmd[cmd]
            print(myid, cmd, '->', move_stat, '\r')
            robot.move(move_stat)

    robot = None
    print(myid, 'end', '\r')
           
    
#####
class MyTcpHandler(socketserver.StreamRequestHandler):
    def __init__(self, request, client_address, server):
        net_lock = ''
        
        if net_lock == '':
            self.wfile_lock = threading.Lock()
        else:
            self.wfile_lock = net_lock
        
        return socketserver.StreamRequestHandler.__init__(self, \
                                                          request, \
                                                          client_address, \
                                                          server)

    def net_write(self, msg):
        self.wfile_lock.acquire()

        try:
            self.wfile.write(msg)
        except:
            print('net_write(): Error!!!')
            pass

        self.wfile_lock.release()
        
    def setup(self):
        return socketserver.StreamRequestHandler.setup(self)

    def handle(self):
        print('***', __class__.__name__+'.handle()')

        self.net_write('#OK\r\n'.encode('utf-8'))

        # Telnet Protocol
        #
        # mode character
        # 0xff IAC
        # 0xfd DO
        # 0x22 LINEMODE
        self.net_write(b'\xff\xfd\x22')

        while True:
            net_data = self.request.recv(512)
            print('net_data:', net_data)
            if len(net_data) == 0:
                break

            try:
                for ch in net_data.decode('utf-8'):
                    self.net_write('\r\n'.encode('utf-8'))
                    CmdQ.put(ch)

            except UnicodeDecodeError:
                pass

    def finish(self):
        return socketserver.StreamRequestHandler.finish(self)


##### Main
def main():
    global RobotServer

    port_num = DEF_PORT

    sys.argv.pop(0)
    if len(sys.argv) > 0:
        port_num = int(sys.argv.pop(0))
    print('port_num =', port_num)

    pi = pigpio.pi()
    robot = AutoRobotCar(pin, pi)
    robot.start()

    RobotServer = socketserver.TCPServer(('', port_num), MyTcpHandler)
    print('listening ...', RobotServer.socket.getsockname())
    RobotServer.serve_forever()
    
    robot.join()
    print('join: robot')

if __name__ == '__main__':
    main()
