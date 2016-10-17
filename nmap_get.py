#!/usr/bin/env python
#coding=utf-8
#author="JeeWin'

from libnmap.parser import NmapParser
import urllib2
import sys
from multiprocessing import Pool

def getUrl(url):
    print url+'@',
    try:
        response = urllib2.urlopen(url,timeout=10)
        #r = requests.get(url, verify=False)
        print response.getcode()
    except urllib2.URLError,e:
        print e.reason
    except urllib2.HTTPError,e:
        print e.code
    except Exception,e:
        print e
        
if __name__ == "__main__":
    nmap_report = NmapParser.parse_fromfile(sys.argv[1])
    urls = [ 'http://' + a.address + ':' + str(b.port) + '/' for a in nmap_report.hosts for b in a.services if b.open() ]
    #print urls
    pool = Pool(20)
    pool.map(getUrl, urls)
