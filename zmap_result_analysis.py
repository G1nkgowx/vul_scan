#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'JeeWin'


from IPy import IP
from optparse import OptionParser

def get_zmap_dic(filename, range):
    ip_range = IP(range)
    zmap_results_list = []
    for line in open(filename):
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
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="filename",
                      help="Zmap output file", metavar="FILE")
    parser.add_option("-r", "--range", dest="range",
                      help="ip_range")

    (options, args) = parser.parse_args()
    dic = get_zmap_dic(options.filename, options.range)
    #print dic
     # print dic['10.233.50.1']
    # print ""
    # print dic['10.223.2.60']
    # print ""
    # print dic['10.223.2.61']
    # print ""
    # print dic['10.223.2.43']



