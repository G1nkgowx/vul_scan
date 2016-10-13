#!/usr/bin/env python
#coding=utf-8
#author="JeeWin'

import xlrd
import requests
from tld import get_tld
import socket
data = xlrd.open_workbook('sjzx.xls')
table = data.sheets()[0]

# nrows = table.nrows
for i in range(6,55):
    if table.row_values(i)[25]=='' and table.row_values(i)[28]=='':
        continue
    else:
        ips = table.row_values(i)[25]
        if ips=='':
            if  table.row_values(i)[28][0:4]=='http':
                try:
                    ips = socket.getaddrinfo(get_tld(table.row_values(i)[28]), 'http')[0][4][0]
                except Exception as e:
                    continue

            else:
                continue
        for ip in ips.split(','):
            if not -1==ip.find('-'): # x.x.x.x-x
                for x in range(int(ip[ip.rfind('.')+1:].split('-')[0]),int(ip[ip.rfind('.')+1:].split('-')[1])+1):
                    print ip[:ip.rfind('.')+1]+str(x)+':',

                    for port in table.row_values(i)[26].split(','):  # print port
                        if not -1 == port.find('-'):
                            for x in range(int(port[port.rfind('p') + 1:].split('-')[0]),
                                           int(port[port.rfind('p') + 1:].split('-')[1]) + 1):
                                print port[:3] + str(x),
                        else:
                            print port,
                    print ''
            else: # x.x.x.x
                print ip+':',

                for port in table.row_values(i)[26].split(','): # print port
                    if not -1 == port.find('-'):
                        for x in range(int(port[port.rfind('p') + 1:].split('-')[0]),int(port[port.rfind('p') + 1:].split('-')[1]) + 1):
                            print port[:3]+str(x),
                    else:
                        print port,
                print ''

