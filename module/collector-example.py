# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author = i@cdxy.me
# project = https://github.com/Xyntax/POC-T

"""
采集示例
简单页面采集-下载IP对应的html页面
"""

import sys

try:
    import pycurl
except ImportError, e:
    sys.exit(e)


def poc(str):
    # As long as the file is opened in binary mode, both Python 2 and Python 3
    # can write response body to it without decoding.
    try:
        with open(str + '.html', 'wb') as f:
            c = pycurl.Curl()
            c.setopt(c.URL, 'http://' + str)
            c.setopt(c.WRITEDATA, f)
            c.perform()
            c.close()
        return True
    except:
        return False
