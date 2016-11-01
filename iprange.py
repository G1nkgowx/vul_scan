#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'JeeWin'
import sys

def get_ip_range():
    ip_list = []
    for line in open(sys.argv[1]):
        ip = line.strip('\r\n')

        if not -1==ip.find('-'): # x.x.x.x-x
            for j in range(int(ip[ip.rfind('.')+1:].split('-')[0]),int(ip[ip.rfind('.')+1:].split('-')[1])+1): # ip range
                ip_list.append((ip[:ip.rfind('.') + 1] + str(j)).encode('utf-8'))

    return ip_list


if __name__ == "__main__":
    for i in get_ip_range():
        print i




