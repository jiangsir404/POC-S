# !/usr/bin/env python
#  -*- coding: utf-8 -*-
__author__ = 'xy'

import requests

"""
测试用例
"""


def info():
    return "info"


def poc(str):
    url = 'http://www.baidu.com'
    c = requests.get(url).content
    return True if c else False


def exp():
    return "exp"


print poc(1)
