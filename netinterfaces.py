#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import netifaces
import sys

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

    print('<h1>', end='')
    for if_name in netifaces.interfaces():
        if if_name == 'lo':
            continue

        print(if_name + ' ', end='')

        addrs = netifaces.ifaddresses(if_name)

        mac = addrs[netifaces.AF_LINK]
        for a in mac:
            macaddr = a['addr']
            print('[' + macaddr + '] ', end='')

        ip = addrs[netifaces.AF_INET]
        for a in ip:
            ipaddr = a['addr']
            print(mklink(ipaddr, ipaddr) + ' ', end='')

            for p in sys.argv:
                print(mklink(p, ipaddr, p) + ' ', end='')

#        ipv6_addr = addrs[netifaces.AF_INET6]
#        for a in ipv6_addr:
#            print(a['addr'])

    print('</h1>')
    
    html_bottom()
        

if __name__ == '__main__':
    main()
