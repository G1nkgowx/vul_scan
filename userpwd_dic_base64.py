#!/usr/bin/env python
# -*- coding: utf-8 -*-
"base64 encode username:password for http auth"
__author__ = 'JeeWin'
import sys
import base64
def read_file(filename):
    l = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            l.append(line)
    return l
def main():
    username = read_file(sys.argv[1])
    password = read_file(sys.argv[2])
    for u in username:
        for p in password:
            print base64.b64encode(u + ':' + p)
if __name__ == "__main__":
    main()
