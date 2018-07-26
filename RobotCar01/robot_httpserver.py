#!/usr/bin/env python3
#
from flask import Flask, render_template, request
from RobotClient import RobotClient
import sys
import os

MyName = os.path.basename(sys.argv[0])

app = Flask(__name__)

DEF_HOST = 'localhost'
DEF_PORT = 12345

RobotHost = DEF_HOST
RobotPort = DEF_PORT

#####
@app.route('/')
def index():
    return render_template('index.html')

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
    
