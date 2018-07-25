#!/usr/bin/env python3
#
from flask import Flask, render_template, request
import RobotTcpClient
import sys
import os

app = Flask(__name__)

DEF_HOST = 'localhost'
DEF_PORT = 12345


def robot_cmd(cmd):
    cl = RobotTcpClient.RobotTcpClient(DEF_HOST, DEF_PORT)
    cl.send_cmd(cmd)
    cl.close()

#####
@app.route('/')
def hello():
    s = "Hello, world."
    return render_template('index.html', s=s)

@app.route('/action', methods=['POST'])
def action():
    global cl
    
    if request.method != 'POST':
        return

    cmd = str(request.form['cmd'])
    print(cmd)
    robot_cmd(cmd)

    return ''
    

#####
def main():
    myname = os.path.basename(sys.argv[0])
    
    try:
        app.run(host='0.0.0.0', debug=True)
    finally:
        print('=== ' + myname + ': finally ===')
    
if __name__ == '__main__':
    main()
    
