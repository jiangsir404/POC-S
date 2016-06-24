# !/usr/bin/env python
#  -*- coding: utf-8 -*-
# author = i@cdxy.me
# project = https://github.com/Xyntax/POC-T

"""
基于Bing搜索引擎的 IP反查域名

Usage:
  查询C段域名  - python POC-T.py -T -m bingc -n 139.24.102.0/24 -t 20
  批量反查域名 - python POC-T.py -T -m bingc -f ip.txt -t 20
"""
import requests
import re


def info():
    return __doc__


def poc(ip):
    domains = set()
    q = "https://www.bing.com/search?q=ip%3A" + ip
    c = requests.get(q, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'}).content
    p = re.compile(r'<cite>(.*?)</cite>')
    l = re.findall(p, c)
    for each in l:
        domain = each.split('://')[-1].split('/')[0]
        domains.add(domain)
    if len(domains) > 0:
        ans_1 = ip + ' -> '
        for each in domains:
            ans_1 += each + ' '
        return ans_1
    else:
        return False
