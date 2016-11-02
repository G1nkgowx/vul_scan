#!/usr/bin/env python
# -*- coding: utf-8 -*-



import urllib2
import argparse,urlparse
from multiprocessing import Pool

def test_put(url):
    filepath=url+'/a.txt'
    #print filepath
    req=urllib2.Request(filepath)

    req.add_data('hi')
    req.get_method=lambda :"PUT"
    try:
        res=urllib2.urlopen(req,timeout=5)
    except:
        return False
    h=res.info()

    if (h.getheader("Location")==None):
        return False
    return True


def verify(url):
    req=urllib2.Request(url)
    #req.add_header("host","192.168.199.151")
    print url,
    req.get_method=lambda :"OPTIONS"
    try:
        res=urllib2.urlopen(req,timeout=5)
    except Exception,e:
        print e
        return False
    h=res.info()
    if (h.getheader("Server")==None) or (h.getheader("Server")<>'Microsoft-IIS/6.0'):
        print 'none'
        return False

    s=res.info().getheader("Public")

    if (s.count('MOVE')>0) and ((s.count('PUT')>0)):
        if test_put(url):
            print 'have vul'
            return True
        else:
            print 'have put'
            return False
    print 'none'
    return False

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('-u', '--URL')
    parser.add_argument('-f', '--file_path', help='file path.')
    args = parser.parse_args()
    url = args.URL
    file_path = args.file_path
    if url:
        if url.startswith('http://' or 'https://'):
            url = urlparse.urlparse(url).geturl()
            verify(url)
        else:
            url = 'http://' + url
            verify(url)
    elif file_path:
        urls = []
        for url in open(file_path).readlines():
            if url != '\n':
                if url.startswith('http://' or 'https://'):
                    url = urlparse.urlparse(url).geturl().strip()
                    urls.append(url)

                else:
                    if not url.split(',')[0] == "saddr":
                        url = url.split(',')[0] + ':' + url.split(',')[1]
                        url = 'http://' + url
                        url = url.strip()
                        urls.append(url)
        pool = Pool(40)
        pool.map(verify, urls)
        pool.close()
        pool.join()


