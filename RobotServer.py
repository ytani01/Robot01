#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socketserver

#
# RobotHandler
#
class RobotHandler(socketserver.StreamRequestHandler):
    def __init__(self, request, client_address, server):
        self.myname = __class__.__name__
        print(self.myname + ': client_address =', client_address)

        self.robot = server.robot

        return super().__init__(request, client_address, server)

    def setup(self):
        print(self.myname + ': setup()')
        return super().setup()

    def net_write(self, msg):
        try:
            self.wfile.write(msg)
        except:
            print(self.myname + ': net_write(', msg, '): Error !!')

    def handle(self):
        print(self.myname + ': handle()')

        # Telnet Protocol
        #
        # mode character
        #  0xff IAC
        #  0xfd DO
        #  0x22 LINEMODE
        self.net_write(b'\xff\xfd\x22')

        self.net_write('# Ready\r\n'.encode('utf-8'))

        flag_continue = True
        while flag_continue:
            try:
                net_data = self.request.recv(512)
            except ConnectionResetError:
                return

            print('net_data:', net_data)
            if len(net_data) == 0:
                break

            try:
                for ch in net_data.decode('utf-8'):
                    self.net_write('\r\n'.encode('utf-8'))

                    print('ch:0x%02x' % ord(ch))

                    if ord(ch) > 0x20:
                        self.robot.send_cmd(ch)
                    else:
                        flag_continue = False
            except UnicodeDecodeError:
                pass

    def finish(self):
        print(self.myname + ': finish()')
        return super().finish()

    
#
# RobotServer
#
class RobotServer(socketserver.TCPServer):
    DEF_PORT_NUM = 12345

    def __init__(self, robot, port_num=0):
        self.myname = __class__.__name__
        print(self.myname + ': __init__()')

        self.robot = robot
        if not self.robot.is_alive():
            self.robot.start()
        
        self.port_num = port_num
        if self.port_num == 0:
            self.port_num = RobotServer.DEF_PORT_NUM
            
        super().__init__(('', self.port_num), RobotHandler)

    def __del__(self):
        print(self.myname + ': __del__()')

        self.robot.send_cmd(self.robot.cmd_end)
        self.robot.join()
        print(self.myname + ': __del__(): done')
