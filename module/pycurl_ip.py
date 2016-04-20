# !/usr/bin/env python
#  -*- coding: utf-8 -*-
__author__ = 'xy'
import sys

try:
    import pycurl
except ImportError, e:
    sys.exit(e)
"""
下载IP对应的html页面
"""


def info():
    pass


def exp():
    pass


def poc(str):
    # As long as the file is opened in binary mode, both Python 2 and Python 3
    # can write response body to it without decoding.
    with open(str + '.html', 'wb') as f:
        c = pycurl.Curl()
        c.setopt(c.URL, 'http://' + str)
        c.setopt(c.WRITEDATA, f)
        c.perform()
        c.close()

    return True
