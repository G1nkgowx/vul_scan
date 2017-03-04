#!/usr/bin/env python
# -*- coding: utf-8 -*-
#__author__ = 'JeeWin'

import sys
import requests as req

def getUrl(url):
    url = 'http://' + url
    try:
        response = req.get(url, timeout=5)
        if response.status_code == 200 or response.status_code == 302:
            print url, response.status_code, ">>>>"
        else:
            print url, response.status_code
    except Exception, e:
        print url, 'Other error'#, e


def main():
    urls = []
    for line in open(sys.argv[1]):
        line = line.strip()
        urls.append(line)

    for i in urls:
        getUrl(i)

if __name__ == "__main__":
    main()


