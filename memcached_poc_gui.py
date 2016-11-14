#!/usr/bin/python
# -*- coding: utf-8 -*-
#__author__ = 'JeeWin'

import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
import socket
import os


class Scan(QtGui.QWidget):

    def __init__(self):
        super(Scan, self).__init__()
        self.initUI()

    def initUI(self):

        self.logo_label = QtGui.QLabel(self)
        self.logo_label.setPixmap(QtGui.QPixmap("%s/logo.png" % (os.getcwd())))
        self.logo_label.move(30, 20)

        self.text_label = QtGui.QLabel(self)
        self.text_label.setText('Memcached 未授权访问漏洞扫描器 V0.1  \n输入文件格式:每行一个ip,端口 如1.1.1.1,11211 '
                                '\n环境:Python 2.7.10 Qt 5.7.0 PyQt 4.11.4')
        self.text_label.move(150, 30)

        self.inputfile_LineEdit = QtGui.QLineEdit(self)
        self.inputfile_LineEdit.setGeometry(QtCore.QRect(10, 10, 420, 20))
        self.inputfile_LineEdit.move(20, 115)

        self.openfile_button = QtGui.QPushButton('Open File', self)
        self.openfile_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.openfile_button.move(450, 110)

        self.start_button = QtGui.QPushButton('Start', self)
        self.start_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.start_button.move(560, 110)

        self.res_textBrowser = QtGui.QTextBrowser(self)
        self.res_textBrowser.setGeometry(QtCore.QRect(10, 10, 650, 300))
        self.res_textBrowser.move(20, 150)

        self.connect(self.openfile_button, QtCore.SIGNAL('clicked()'),
            self.openFile)

        self.connect(self.start_button, QtCore.SIGNAL('clicked()'),
                     self.start)

        self.setFocus()

    def openFile(self):
        self.filename = QtGui.QFileDialog.getOpenFileName(self, 'Open file','/')
        self.inputfile_LineEdit.setText(self.filename)

    def verify(self, ip_port):
        ip = ip_port[0]
        port = ip_port[1]
        payload = "stats items\n"
        socket.setdefaulttimeout(10)
        s = socket.socket()
        QtGui.QApplication.processEvents()
        try:
            s.connect((ip, port))
            s.send(payload)
            recvdata = s.recv(1024)
            if recvdata and 'STAT items' in recvdata:
                print ip + ':' + str(port) + ' have vul'
                self.res_textBrowser.append(ip + ':' + str(port) + ' have vul')
            else:
                print ip + ':' + str(port) + ' no vul'
                self.res_textBrowser.append(ip + ':' + str(port) + ' no vul')
        except Exception, e:
            print ip + ':' + str(port) + ' socket error:', e
            self.res_textBrowser.append(ip + ':' + str(port) + ' socket error:' + str(e))
        s.close()

    def start(self):
        urls = []
        inputfile = self.inputfile_LineEdit.text()

        if ',' in inputfile:
            self.verify([inputfile.split(',')[0], int(inputfile.split(',')[1])])
        else:

            for line in open(inputfile):
                line = line.strip()
                if not line.split(',')[0] == 'saddr':
                    ip = line.split(',')[0]
                    port = line.split(',')[1]
                    urls.append([ip, int(line.split(',')[1])])
                    self.verify([ip, int(port)])
                    QtGui.QApplication.processEvents()
                    # verify(['10.232.246.11',11211]) 10.233.32.46


if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    ex = Scan()
    ex.show()
    app.exec_()
