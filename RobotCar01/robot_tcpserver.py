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

Robot = AutoRobotCar.AutoRobotCar(PIN_CR_SERVO)

##### Global function
def robot_send_cmd(cmd):
    global Robot

    Robot.send_cmd(cmd)
    

##### Server Class
class MyTcpHandler(socketserver.StreamRequestHandler):

    def __init__(self, request, client_address, server):
        print('client_address =', client_address)
        ## Lock
        #self.wfile_lock = threading.Lock()
        return socketserver.StreamRequestHandler.__init__(self, request, \
                                                          client_address, \
                                                          server)

    def net_write(self, msg):
        #self.wfile_lock.acquire()

        try:
            self.wfile.write(msg)
        except:
            print('net_write(): Error!!!')
            pass

        #self.wfile_lock.release()
        
    def setup(self):
        return socketserver.StreamRequestHandler.setup(self)

    def handle(self):
        print('***', __class__.__name__+'.handle()')

        # Telnet Protocol
        #
        # mode character
        # 0xff IAC
        # 0xfd DO
        # 0x22 LINEMODE
        self.net_write(b'\xff\xfd\x22')

        self.net_write('# Ready\r\n'.encode('utf-8'))

        flag_continue = True
        while flag_continue:
            try:
                net_data = self.request.recv(512)
            except ConnectionResetError:
                #flag_continue = False
                return

            print('net_data:', net_data)
            if len(net_data) == 0:
                break

            try:
                for ch in net_data.decode('utf-8'):
                    self.net_write('\r\n'.encode('utf-8'))

                    print('ch:0x%02x' % ord(ch))
                    
                    if ord(ch) > 0x20:
                        robot_send_cmd(ch)
                    else:
                        flag_continue = False

            except UnicodeDecodeError:
                pass

    def finish(self):
        print('finish()')
        return socketserver.StreamRequestHandler.finish(self)

##### Main
def main():
    port_num = DEF_PORT

    sys.argv.pop(0)
    if len(sys.argv) > 0:
        port_num = int(sys.argv.pop(0))
    print('port_num =', port_num)

    Robot.start()

    RobotServer = socketserver.TCPServer(('', port_num), MyTcpHandler)
    print('listening ...', RobotServer.socket.getsockname())
    RobotServer.serve_forever()

if __name__ == '__main__':
    try:
        main()
    finally:
        print('finally:')
        Robot.send_cmd(' ')
        print('Robot.join()')
        Robot.join()
        print('-- End --')
        
