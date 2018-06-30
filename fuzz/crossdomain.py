#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import urlparse
'''
name: crossdomain.xml文件发现
referer: unknown
author: Lucifer
description: crossdomain错误配置可导致。
'''
def poc(url):
    if '://' not in url:
        url = 'http://' + url
    if not url.endswith('/'):
        url = url + "/"
    url = url + "crossdomain.xml"
    try:
        header = dict()
        header["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
        r = requests.get(url, headers=header, timeout=5)
        if 'allow-access-from domain="*"' in r.text:
            return u'[目标存crossdomain.xml domain值为*,可能造成非法窃取目标网站源码] '+url
        else:
            return False
    except Exception:
        return False