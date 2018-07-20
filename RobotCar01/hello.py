#!/usr/bin/env python3
#
from flask import Flask, render_template, request

app = Flask(__name__)

#####
@app.route('/')
def hello():
    s = "Hello, world."
    return render_template('index.html', s=s)

@app.route('/action', methods=['POST'])
def action():
    if request.method != 'POST':
        return

    v = str(request.form['cmd'])
    print(v)

    return ''
    

#####
def main():
    try:
        app.run(host='0.0.0.0', debug=True)
    finally:
        print('=== finally ===')
    
if __name__ == '__main__':
    main()
    
