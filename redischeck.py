#!/usr/bin/env python
# -*- coding: utf-8 -*-
#__author__ = 'JeeWin'


from optparse import OptionParser
from multiprocessing import Pool

def verify(url):
    host = url[0]
    port = url[1]

    payload = "\x2a\x31\x0d\x0a\x24\x34\x0d\x0a\x69\x6e\x66\x6f\x0d\x0a"

    socket.setdefaulttimeout(10)
    s = socket.socket()
    try:

        s.connect((host, port))
        s.send(payload)
        recvdata = s.recv(1024)
        repr(recvdata)

        if recvdata and 'redis_version' in recvdata:
            print host + ':' + str(port) + ' have redis infoleak'
        else:
            print host + ':' + str(port)
    except Exception, e:
        print host + ':' + str(port) + ' socket error:', e
    s.close()


def main():
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="filename", help="ip list file", metavar="FILE")
    (options, args) = parser.parse_args()
    urls = []
    for line in open(options.filename):
        line = line.strip('\n')
        if not line.split(',')[0] == "saddr":
            ip = line.split(',')[0]
            urls.append([ip,int(line.split(',')[1])])

    pool = Pool(40)
    pool.map(verify, urls)
    pool.close()
    pool.join()

if __name__ == "__main__":
    main()

