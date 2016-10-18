#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'JeeWin'

from IPy import IP


def get_zmap_dic():
    ip_range = IP('10.232.64.0/19')
    zmap_results_list = []
    for line in open('zmap_all_port3B.txt'):
        line = line.strip('\n')
        if not line.split(',')[0] == "saddr":
            ip = line.split(',')[0]
            if ip in ip_range:
                print line.split(',')[0] + ',' + line.split(',')[1]
                zmap_results_list.append([line.split(',')[0], line.split(',')[1]])

    zmap_results_dic = {}

    for i in zmap_results_list:
        if not zmap_results_dic.has_key(i[0]):
            zmap_results_dic[i[0]] = []
            for j in zmap_results_list:
                if j[0]==i[0]:
                    zmap_results_dic[i[0]].append('tcp'+j[1])
    return zmap_results_dic

if __name__ == "__main__":
    dic = get_zmap_dic()

     # print dic['10.233.50.1']
    # print ""
    # print dic['10.223.2.60']
    # print ""
    # print dic['10.223.2.61']
    # print ""
    # print dic['10.223.2.43']



