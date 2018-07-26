#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import telnetlib
import time

#####
class RobotClient:
    DEF_HOST = 'localhost'
    DEF_PORT = 12345
    
    def __init__(self, host='', port=0):
        self.myname = __class__.__name__
        print(self.myname + ': __init__(' + host + ',' + str(port) + ')')
        self.open(host, port)

    def __del__(self):
        self.close()

    def open(self, host, port):
        self.host = RobotClient.DEF_HOST
        self.port = RobotClient.DEF_PORT
        
        if host != '':
            self.host = host
        if port != 0:
            self.port = port

        self.tn = telnetlib.Telnet(self.host, self.port)
        
    def close(self):
        self.tn.close()

    def send_cmd(self, cmd):
        in_data = self.tn.read_very_eager()
        if len(in_data) > 0:
            print(self.myname + ': in_data:', in_data)

        for ch in cmd:
            print(self.myname + ': ch =', ch, '(0x%02x)' % ord(ch))
            self.tn.write(ch.encode('utf-8'))
            
            in_data = self.tn.read_very_eager()
            if len(in_data) > 0:
                print(self.myname + ': in_data:', in_data)


##### Main
def main():
    cl = RobotClient()

    cl.send_cmd('d')
    time.sleep(0.5)
    cl.send_cmd('s')

if __name__ == '__main__':
    main()
