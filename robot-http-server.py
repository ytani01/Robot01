#!/usr/bin/env python3
#
from flask import Flask, render_template, request
from RobotClient import RobotClient
import netifaces
import sys
import os

MyName = os.path.basename(sys.argv[0])

app = Flask(__name__)

DEF_HOST = 'localhost'
DEF_PORT = 12345

RobotHost = DEF_HOST
RobotPort = DEF_PORT

Flag_Video = 'off'

#####
def get_ipaddr():
    for if_name in netifaces.interfaces():
        if if_name == 'lo':
            continue

        print(if_name)
        
        addrs = netifaces.ifaddresses(if_name)
        print(addrs)

        try:
            ip = addrs[netifaces.AF_INET]
        except(KeyError):
            continue
        print(ip)

        return ip[0]['addr']

    return ''

def index0(video_sw):
    ipaddr = get_ipaddr()
    return render_template('index.html', ipaddr=ipaddr, video=video_sw)
    
#####
@app.route('/')
def index():
    return index0('off')

@app.route('/video')
def video_movde():
    return index0('on')
        
@app.route('/action', methods=['POST'])
def action():
    global RobotHost, RobotPort
    
    if request.method != 'POST':
        return

    cmd = str(request.form['cmd'])
    print(MyName + ': cmd = \'' + cmd + '\'')

    rc = RobotClient(RobotHost, RobotPort)
    rc.send_cmd(cmd)
    rc.close()

    return ''
    

#####
def main():
    global RobotHost, RobotPort

    if len(sys.argv) >= 2:
        RobotHost = sys.argv[1]

    if len(sys.argv) >= 3:
        RobotPort = int(sys.argv[2])

    print(MyName + ': RobotHost = ' + RobotHost)
    print(MyName + ': RobotPort = ' + str(RobotPort))
    
    try:
        app.run(host='0.0.0.0', debug=True)
    finally:
        print('=== ' + MyName + ': finally ===')
    
if __name__ == '__main__':
    main()
    
