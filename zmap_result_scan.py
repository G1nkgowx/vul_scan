#!/usr/bin/env python
# -*- coding: utf-8 -*-
#__author__ = 'JeeWin'

import urllib2
import sys
from multiprocessing import Pool
from BeautifulSoup import BeautifulSoup
import socket
import re

def getUrl(ip_port):
    url = 'http://' + ip_port[0] + ':' + ip_port[1]
    print url+' @',
    headers = {"User-Agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1"}
    req = urllib2.Request(url, headers=headers)

    try:
        response = urllib2.urlopen(req, timeout=5)
        print 'code:', response.getcode(),
        soup = BeautifulSoup(response)
        title = soup.title.string
        print "title:", title.strip()
        #print 'yes'
    except urllib2.HTTPError, e:
        print 'http error:', e.code
        #print 'yes'

    except Exception, e:
        print 'other error:', e,
        try:
            socket.setdefaulttimeout(3)
            s = socket.socket()
            s.connect((ip_port[0], int(ip_port[1])))
            banner = s.recv(1024)
            s = re.findall(r"[\w\W\s\S]+", banner)
            if s:
                print 'banner:', s
        except Exception, e:
            print 'socket error:', e

if __name__ == "__main__":

    urls = []
    for line in open(sys.argv[1]):
        line = line.strip('\n')

        if not line.split(',')[0] == "saddr":
            urls.append(line.split(','))


    pool = Pool(20)
    pool.map(getUrl, urls)
    pool.close()
    pool.join()