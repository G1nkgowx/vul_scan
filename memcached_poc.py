#!/usr/bin/env python
# -*- coding: utf-8 -*-
#__author__ = 'JeeWin'


from optparse import OptionParser
from multiprocessing import Pool
import socket


def verify(ip_port):
    host = ip_port[0]
    port = ip_port[1]
    payload = "stats items\n"
    socket.setdefaulttimeout(10)
    s = socket.socket()
    try:
        s.connect((host, port))
        s.send(payload)
        recvdata = s.recv(1024)
        if recvdata and 'STAT items' in recvdata:
            print host + ':' + str(port) + ' have vul'
        else:
            print host + ':' + str(port)
    except Exception, e:
        print host + ':' + str(port) + ' socket error:', e
    s.close()


def main():
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="filename", help="ip list file,ex:1.1.1.1,80", metavar="FILE")
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

