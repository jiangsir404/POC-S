# !/usr/bin/env python
#  -*- coding: utf-8 -*-
__author__ = 'xy'

f = open('./dic/1-1000.txt', 'w')
for i in range(123456, 124000):
    f.write(str(i) + '\n')
f.close()
