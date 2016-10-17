#!/usr/bin/env python
#coding=utf-8
#author="JeeWin'

import urllib2
import sys
from multiprocessing import Pool
from BeautifulSoup import BeautifulSoup
import socket

def getUrl(ip_port):
    url = 'http://' + ip_port[0] + ':' + ip_port[1]
    print url+'@',

    headers = {"User-Agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1"}
    req = urllib2.Request(url, headers=headers)

    try:
        response = urllib2.urlopen(req, timeout=10)
        print response.getcode(),
        soup = BeautifulSoup(response)
        title = soup.title.string
        print title

        print url + '/console @',
        req = urllib2.Request(url+'/console', headers=headers)
        response = urllib2.urlopen(req, timeout=10)
        print response.getcode()
    except urllib2.HTTPError, e:
        print e.code
    except Exception, e:
        code = -1

    if code == -1:
        try:
            socket.setdefaulttimeout(2)
            s = socket.socket()
            s.connect((ip_port[0], ip_port[1]))
            banner = s.recv(1024)
            print banner
        except Exception, e:
            print ''
            return

if __name__ == "__main__":

    urls = []
    for line in open(sys.argv[1]):
        line = line.strip('\n')

        if not line.split(',')[0] == "saddr":
            #url = 'http://' + line.split(',')[0] + ':' + line.split(',')[1]
            urls.append(line.split(','))


    # print urls
    pool = Pool(20)
    pool.map(getUrl, urls)
    pool.close()
    pool.join()