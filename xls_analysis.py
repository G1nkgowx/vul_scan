#!/usr/bin/env python
# -*- coding: utf-8 -*-
#author="JeeWin'

import xlrd
from tld import get_tld
import socket

if __name__ == "__main__":
    ba_data = xlrd.open_workbook('sjzx.xls')
    ba_table = ba_data.sheets()[0]
    yba_dic = {} # 已备案
    # nrows = table.nrows

    for i in range(6,55):# line range
        if ba_table.row_values(i)[25] == '' and ba_table.row_values(i)[28] == '':
            continue
        else:
            ips = ba_table.row_values(i)[25]
            if ips == '': # get url ip
                if ba_table.row_values(i)[28][0:4]=='http':
                    try:
                        ips = socket.getaddrinfo(get_tld(ba_table.row_values(i)[28]), 'http')[0][4][0]
                    except Exception as e:
                        continue
                else:
                    continue
            for ip in ips.split(','):
                if not -1==ip.find('-'): # x.x.x.x-x
                    for j in range(int(ip[ip.rfind('.')+1:].split('-')[0]),int(ip[ip.rfind('.')+1:].split('-')[1])+1): # ip range
                        p = [] # port list
                        for port in ba_table.row_values(i)[26].split(','):  # append port
                            if not -1 == port.find('-'): # x-x
                                for k in range(int(port[port.rfind('p') + 1:].split('-')[0]),int(port[port.rfind('p') + 1:].split('-')[1]) + 1): # port range
                                    p.append((port[:3] + str(k)).encode('utf-8')) # tcpk
                            else:
                                p.append(port.encode('utf-8'))
                        yba_dic[(ip[:ip.rfind('.')+1]+str(j)).encode('utf-8')] = p # add ip
                else: # x.x.x.x
                    p=[] # port list
                    for port in ba_table.row_values(i)[26].split(','): # append port
                        if not -1 == port.find('-'): # x-x
                            for j in range(int(port[port.rfind('p') + 1:].split('-')[0]),int(port[port.rfind('p') + 1:].split('-')[1]) + 1):
                                p.append((port[:3]+str(j)).encode('utf-8'))
                        else:
                            p.append(port.encode('utf-8'))
                    yba_dic[ip.encode('utf-8')] = p # add ip

    zmap_results_list = []
    for line in open('sjzx_output.txt'):
        line = line.strip('\n')
        if not line.split(',')[0] == "saddr":
            zmap_results_list.append([line.split(',')[0] , line.split(',')[1]])

    zmap_results_dic = {}
    for i in zmap_results_list:
        zmap_results_dic[i[0]]=[]
        for j in zmap_results_list:
            if j[0]==i[0]:
                zmap_results_dic[i[0]].append('tcp'+j[1])

    for i in zmap_results_dic: # find wba
        if yba_dic.has_key(i): # 已备案
            for j in zmap_results_dic[i]:
                if j not in yba_dic[i]:
                    print i + ':' + j + '  not found'
        else:
            for j in zmap_results_dic[i]:
                print i + ':' + j + '  not found'







