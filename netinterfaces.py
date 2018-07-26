#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import netifaces
import sys
#from datetime import datetime

def mklink(label, server, port='', path=''):
    return '<a href="' + mkurl(server, port, path) + '">' + str(label) + '</a>'

def mkurl(server, port='', path=''):
    urlstr = 'http://' + str(server)
    if port != '':
        urlstr += ':' + str(port)
    urlstr += '/' + str(path)
    return urlstr

def html_head():
    print('<!DOCTYPE html>')
    print('<html lang="ja">')
    print('<head>')
    print('<meta charset="utf-8"')
    print('<meta name="viewport" content="width=devicewidth, initial-scale=1, maximum-scale=3">')
    print('</head>')
    print('<body>')

def html_bottom():    
    print('</body>')
    print('</html>')

##### Main
def main():
    sys.argv.pop(0)
    #print(sys.argv)

    html_head()

    #timestr = datetime.now().strftime('%Y/%m/%d(%a) %H:%M:%S')
    #print('<h1>' + timestr + '</h1>')
    print('<h1>')
    for if_name in netifaces.interfaces():
        if if_name == 'lo':
            continue

        print(if_name)

        addrs = netifaces.ifaddresses(if_name)

        mac = addrs[netifaces.AF_LINK]
        for a in mac:
            macaddr = a['addr']
            print('[' + macaddr + ']')

        try:
            ip = addrs[netifaces.AF_INET]
        except(KeyError):
            print('???.???.???.???')
            continue
        for a in ip:
            ipaddr = a['addr']
            print(mklink(ipaddr, ipaddr))

            for p in sys.argv:
                print(mklink(p, ipaddr, p))

#        ipv6_addr = addrs[netifaces.AF_INET6]
#        for a in ipv6_addr:
#            print(a['addr'])

    print('</h1>')
    
    html_bottom()
        

if __name__ == '__main__':
    main()
