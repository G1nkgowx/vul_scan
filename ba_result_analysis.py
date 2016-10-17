#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'JeeWin'

import xlrd
from tld import get_tld
import socket


def get_ba_dic():
    ba_data = xlrd.open_workbook('sjzx1.xls')
    ba_table = ba_data.sheets()[0]
    ba_dic = {} # 已备案ba_dic
    nrows = ba_table.nrows
    for i in range(5,nrows):# line range row (number -1,nrows)
        ips = ba_table.row_values(i)[25]
        ports = ba_table.row_values(i)[26]
        url = ba_table.row_values(i)[28]
        if ips == '' and url == '':
            continue
        else:
            if ips == '':
                if url[0:4]=='http':
                    try:
                        ips = socket.getaddrinfo(get_tld(url), 'http')[0][4][0] # get url ip
                    except Exception as e:
                        continue
                else:
                    continue
            for ip in ips.split(','):
                if not -1==ip.find('-'): # x.x.x.x-x
                    for j in range(int(ip[ip.rfind('.')+1:].split('-')[0]),int(ip[ip.rfind('.')+1:].split('-')[1])+1): # ip range
                        p = [] # port list
                        for port in ports.split(','):  # append port
                            if not -1 == port.find('-'): # x-x
                                for k in range(int(port[port.rfind('p') + 1:].split('-')[0]),int(port[port.rfind('p') + 1:].split('-')[1]) + 1): # port range
                                    p.append((port[:3] + str(k)).encode('utf-8')) # tcpk
                            else:
                                p.append(port.encode('utf-8'))
                        ba_dic[(ip[:ip.rfind('.')+1]+str(j)).encode('utf-8')] = p # add ip
                else: # x.x.x.x
                    p=[] # port list
                    for port in ports.split(','): # append port
                        if not -1 == port.find('-'): # x-x
                            for j in range(int(port[port.rfind('p') + 1:].split('-')[0]),int(port[port.rfind('p') + 1:].split('-')[1]) + 1):
                                p.append((port[:3]+str(j)).encode('utf-8'))
                        else:
                            p.append(port.encode('utf-8'))
                    ba_dic[ip.encode('utf-8')] = p # add ip
    return ba_dic



if __name__ == "__main__": 

    ba_results = get_ba_dic()

    print ba_results['10.223.32.142']






