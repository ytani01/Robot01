#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import netifaces

def mklink(server, port, path, label):
    return '<a href="' + mkurl(server, port, path) + '">' + str(label) + '</a>'

def mkurl(server, port, path):
    return 'http://' + str(server) + ':' + str(port) + '/' + str(path)

##### Main
def main():
    print('<!DOCTYPE html>')
    print('<html lang="ja"')
    print('<head>')
    print('<meta charset="utf-8"')
    print('<meta name="viewport" content="width=devicewidth, initial-scale=1, maximum-scale=3">')
    print('</head>')
    print('<body>')

    for if_name in netifaces.interfaces():
        if if_name == 'lo':
            continue

        print(if_name + ', ', end='')

        addrs = netifaces.ifaddresses(if_name)

        mac = addrs[netifaces.AF_LINK]
        for a in mac:
            macaddr = a['addr']
            print(macaddr + ', ', end='')

        ip = addrs[netifaces.AF_INET]
        for a in ip:
            ipaddr = a['addr']
            print(ipaddr + ', ', end='')

            for p in [5000, 9000]:
                print(mklink(ipaddr, p, '', p) + ' ', end='')

#        ipv6_addr = addrs[netifaces.AF_INET6]
#        for a in ipv6_addr:
#            print(a['addr'])

    print()

    print('</body>')
    print('</html>')
        

if __name__ == '__main__':
    main()
