#!/usr/bin/env python
# -*- coding: utf-8 -*-
#__author__ = 'JeeWin'

import urllib2
import sys
from multiprocessing import Pool
import json


def getUrl(ip_port):

    url = 'http://' + ip_port[0] + ':' + ip_port[1] + '/version'
    print url+' @',
    headers = {"User-Agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1"}
    req = urllib2.Request(url, headers=headers)

    try:
        response = urllib2.urlopen(req, timeout=5)
        print 'code:', response.getcode(),
        content = response.read()
        ret = json.loads(content)
        if ret['ApiVersion']:
            print 'have vul ' + ret['ApiVersion']

    except urllib2.HTTPError, e:
        print 'http error:', e.code

    except Exception, e:globals()
        print 'other error:', e


if __name__ == "__main__":

    urls = []
    for line in open(sys.argv[1]):
        line = line.strip('\n')

        if not line.split(',')[0] == "saddr":
            urls.append(line.split(','))

    #getUrl(['192.168.28.132','2375'])

    pool = Pool(40)
    pool.map(getUrl, urls)
    pool.close()
    pool.join()