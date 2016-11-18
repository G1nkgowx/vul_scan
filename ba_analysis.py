#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'JeeWin'

import xlrd
from tld import get_tld
import socket
from libnmap.parser import NmapParser
from optparse import OptionParser


def get_ba_dic(filename):
    ba_data = xlrd.open_workbook(filename)
    ba_table = ba_data.sheets()[0]
    ba_dic = []
    nrows = ba_table.nrows
    for i in range(0, nrows):  # line range row (number -1,nrows)
        ips = ba_table.row_values(i)[0]
        for ip in ips.split(','):
            if not -1 == ip.find('-'):  # x.x.x.x-x
                for j in range(int(ip[ip.rfind('.') + 1:].split('-')[0]),
                               int(ip[ip.rfind('.') + 1:].split('-')[1]) + 1):  # ip range

                    ba_dic.append((ip[:ip.rfind('.')+1]+str(j)).encode('utf-8'))
            else:  # x.x.x.
                ba_dic.append(ip.encode('utf-8'))
    return ba_dic


def get_zmap_dic(filename):
    zmap_results_list = []
    for line in open(filename):
        line = line.strip('\n')
        if not line.split(',')[0] == "saddr":
            zmap_results_list.append([line.split(',')[0], line.split(',')[1]])

    zmap_results_dic = {}

    for i in zmap_results_list:
        if not zmap_results_dic.has_key(i[0]):
            zmap_results_dic[i[0]] = []
            for j in zmap_results_list:
                if j[0] == i[0]:
                    zmap_results_dic[i[0]].append('tcp' + j[1])
    return zmap_results_dic



def main():
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="filename",
                      help="Zmap or nmap output file", metavar="FILE")
    parser.add_option("-x", "--xlsfile", dest="xlsfilename",
                      help="xls file", metavar="FILE")

    (options, args) = parser.parse_args()

    scan_results = get_zmap_dic(options.filename)

    ba_results = get_ba_dic(options.xlsfilename)

    #print ba_results

    for i in scan_results:  # find wba
        if i not in ba_results:  # 未备案
            print i,
            for j in scan_results[i]:
                print j,
            print ''


if __name__ == "__main__":
    main()










