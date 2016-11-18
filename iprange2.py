#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'JeeWin'


from IPy import IP
from optparse import OptionParser
import sys
def get_dic(filename, range):
    ip_range = IP(range)
    zmap_results_list = []
    for line in open(filename):
        line = line.strip('\n')
        if not line.split(',')[0] == "saddr":
            ip = line.split(',')[0]
            if ip not in ip_range:
                zmap_results_list.append([line.split(',')[0], line.split(',')[1]])
    return zmap_results_list


if __name__ == "__main__":
    r =  get_dic(sys.argv[1], sys.argv[2])
    for i in r:
        print i[0]+','+i[1]





