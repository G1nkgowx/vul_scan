#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'JeeWin'

from libnmap.parser import NmapParser

def get_nmap_dic(filename):

    nmap_report = NmapParser.parse_fromfile(filename)

    nmap_results_dic = {}

    for host in nmap_report.hosts:
        for service in host.services:
            if service.open():
                if nmap_results_dic.has_key(host.address):
                    nmap_results_dic[host.address].append('tcp' + str(service.port))
                else:
                    nmap_results_dic[host.address] = ['tcp' + str(service.port)]

    return nmap_results_dic

def main():
    res = get_nmap_dic('ww_all2.xml')
    for r in res:
        print r+'@',
        for j in res[r]:
            print j,
        print ""

if __name__ == "__main__":
    main()


