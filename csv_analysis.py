#!/usr/bin/env python
#coding=utf-8
#author="JeeWin'



import xlrd
data = xlrd.open_workbook('sjzx.xls')
table = data.sheets()[0]

# nrows = table.nrows
for i in range(6,55):
    print table.row_values(i)[25],table.row_values(i)[26]

