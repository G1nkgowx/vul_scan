#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'JeeWin'

import sys
from multiprocessing import Pool
import re
import requests as req

def getUrl(ip_port):
    url = 'http://' + ip_port[0] + ':' + ip_port[1]
    print url+' @',

    try:
        response = req.get(url, timeout=5)
        print response.status_code
        if re.findall(r".*<input.*", response.content) and re.findall(r".*password.*", response.content):
            f = open(ip_port[0] + '_' + ip_port[1] + '.html', 'w')
            f.write(response.content)
            f.close()
            print url, 'have key'

    except Exception, e:
        print 'Other error:', e

def main():
    urls = []
    for line in open(sys.argv[1]):
        line = line.strip('\n')
        if not line.split(',')[0] == "saddr":
            urls.append(line.split(','))

    pool = Pool(20)
    pool.map(getUrl, urls)
    pool.close()
    pool.join()


if __name__ == "__main__":
    main()

