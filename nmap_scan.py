#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'JeeWin'

if __name__ == "__main__":


def run(self):
    while True:
        target = self.ipq.get()
        # print "scanning %s"%(target)
        options = '-d -max-scan-delay 10 -max-retries 1 -p- -PS21,22,23,80,111,135,139,443,445,2425,3389 -T4 -min-rate 175'

        try:
            nmap_proc = NmapProcess(target, options)
            rc = nmap_proc.run()
            # print 'scanning',nmap_proc.targets,
            if rc != 0:
                print("nmap scan failed: {0}".format(nmap_proc.stderr))
                continue

            print("rc: {0} output: {1}".format(nmap_proc.rc, nmap_proc.summary))
            parsed = NmapParser.parse(nmap_proc.stdout)
            # parsed = NmapParser.parse_fromfile('port_scan.xml')

        except NmapParserException as e:
            print "Exception raised while parsing scan: {0}".format(e.msg)
            self.queue.task_done()
            time.sleep(1)
            continue

        for ip in parsed.hosts:
            ports = ''
            for port in ip.get_open_ports():
                # print ip.address
                ports += str(port[0]) + '/'
                self.vulq.put([str(ip.address), str(port[0])])
            if ports != '':
                self.dbq.put([str(ip.address), ports[:-1]])

        # 在完成这项工作之后，使用 queue.task_done() 函数向任务已经完成的队列发送一个信号
        self.ipq.task_done()
        time.sleep(1)

def main():
    urls = []
    for line in open(sys.argv[1]):
        line = line.strip()
        urls.append(line)

    for i in urls:
       getUrl(i)

if __name__ == "__main__":
    main()