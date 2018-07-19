#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import telnetlib
import sys
import time

DEF_HOST = 'localhost'
DEF_PORT = 12345

#####
def main():
    host = DEF_HOST
    port = DEF_PORT
    
    sys.argv.pop(0)

    if len(sys.argv) > 0:
        host = sys.argv.pop(0)
    if len(sys.argv) > 0:
        port = int(sys.argv.pop(0))
    print('host =', host)
    print('port =', port)

    tn = telnetlib.Telnet(host, port)

    while len(sys.argv) > 0:
        in_data = tn.read_very_eager()
        print('in_data:', in_data)
        s = sys.argv.pop(0)
        for ch in s:
            print('ch =', ch)
            tn.write(ch.encode('utf-8'))
            in_data = tn.read_very_eager()
            print('in_data:', in_data)

    tn.close()
                
if __name__ == '__main__':
    main()
