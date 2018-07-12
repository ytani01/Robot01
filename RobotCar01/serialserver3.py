#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import sys
import socketserver
import serial
import time
import threading

port = 12340
ser = None
devNamePrefix = '/dev/ttyACM'
net_wfile = None
net_wfile_lock = threading.Lock()
ser_speed = 9600



def openSerial():
  global ser

  open_flag = False
  for d in [0,1,2]:
    dev_name = devNamePrefix + str(d)
    print('*** dev_name=', dev_name)

    try:
        ser = serial.Serial(dev_name, ser_speed, timeout=2.0)
        open_flag = True
        break
    except (serial.serialutil.SerialException, FileNotFoundError):
        print("*** openSerial(): Fail to open {}.".format(dev_name))
        #raise
        continue

  if open_flag :
      print("*** openSerial(): open {}.".format(dev_name))
  else:
      print("*** openSerial(): Fail to open serial device.")



def net_write(msg):
  net_wfile_lock.acquire()
  try:
    net_wfile.write(msg)
  except:
    print('net_write(): Error!')
    pass
  net_wfile_lock.release()


def serialReader():
  err_flag = False

  while True:
    try:
        ser_data = ser.readline(1024)

        if len(ser_data) == 0:
            print('len(ser_data)==0')
            continue

        print('SER>', ser_data)
        if net_wfile:
            net_write(ser_data)

    except serial.serialutil.SerialException:
        print('*** serialReader(): SerialException')
        err_flag = True
        #raise

    except:
        raise

    if err_flag:
        openSerial()
        err_flag = False


class MyHandler(socketserver.StreamRequestHandler):
    def __init__(self, request, client_address, server):
        #print('*** '+__class__.__name__+'.__init__()')
        return socketserver.StreamRequestHandler.__init__(self, request, client_address, server)


    def setup(self):
        #print('*** '+__class__.__name__+'.setup()')

        #print("connect from:", self.client_address)
        
        return socketserver.StreamRequestHandler.setup(self)


    def handle(self):
        global ser
        global net_wfile

        #print('*** '+__class__.__name__+'.handle()')

        net_wfile = self.wfile
        net_write('#OK\r\n'.encode('utf-8'))

        # Telnt Protocol
        #
        # mode character 
        # 0xff IAC
        # 0xfd DO
        # 0x22 LINEMODE
        #
        net_write(b'\xff\xfd\x22')
        #print('NET< IAC(0xff) DO(0xfd) LINEMODE(0x22)')
        
        #for net_data in self.rfile:
        #    net_data = net_data.strip()
        while True:
            net_data = self.request.recv(1024);
            if len(net_data) == 0:
              break

            #print('NET>', net_data)

            try:
              for ch in net_data.decode('utf-8'):
                net_write('\r\n'.encode('utf-8'))

                ser.write(ch.encode('utf-8'))
                #print('SER<', ch.encode('utf-8'))

                net_write(("#SER<'"+ch+"'\r\n").encode('utf-8'))

            except UnicodeDecodeError:
              pass

            except serial.serialutil.SerialException:
              print('*** handle(): SerialException')
              openSerial()
              pass

        net_wfile = None


    def finish(self):
        #print('*** '+__class__.__name__+'.finish()')

        #print("close connection.")

        return socketserver.StreamRequestHandler.finish(self)

###
### Main
###
if __name__ == '__main__':
    ##print("sys.argv =", sys.argv)

    openSerial()

    try:
        #ser = serial.Serial(sys.argv[1], ser_speed, timeout=2.0)
        #print(ser)
        #print()
        t = threading.Thread(target = serialReader)
        t.daemon = True
        t.start()

        port = int(sys.argv[1])

    except serial.serialutil.SerialException:
        #print('Error: SerialException')
        raise
        sys.exit()
    except (IndexError, ValueError):
        #print('usage: '+sys.argv[0]+' /dev/ttyXXX port')
        sys.exit()
    except:
        raise
        sys.exit()

    server = socketserver.TCPServer(('', port), MyHandler)
    print('listening ...', server.socket.getsockname())
    server.serve_forever()
