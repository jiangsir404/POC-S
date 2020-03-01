#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

"""
Author: rivir
Date: 2020/2/29

POC-S自实现的DSNLog功能

api: http://www.xxxx.cn:88/api/?token={api_key}&type={web|dns}&filter=

param:
    - api_key: 你搭建dnslog时候要求你输入的api_key
    - type 可选值有web和dns
    - filter 过滤出请求的随机子域名
return:
    {"status": "success", "data": {}}
"""


import random
import requests
import time
from string import ascii_lowercase
import sys
sys.path.append('../')
from lib.core.data import logger, paths
paths.CONFIG_PATH = "../toolkit.conf"
from lib.utils.config import ConfigFileParser

key = ConfigFileParser().CeyeApikey()
uniq_domain = ConfigFileParser().CeyePersonaldomain().split('.')[0]

class Dnslog:
    def __init__(self):
        self.unique = uniq_domain
        self.random = ''.join([random.choice(ascii_lowercase) for _ in range(10)])

    def getRandomDomain(self, custom='poc'):
        """获取随机域名
        full domain = [random].[custom].[unique].dnslog.info
        e.g. fezarvgo.poc.ee8a6f.dnslog.info
        """
        self.custom = custom
        return '%s.%s.%s.ceye.io' % (self.random, self.custom, self.unique)

    def getDnsRecord(self, delay=2):
        time.sleep(delay)
        query = self.random + '.' + self.custom
        api_base = 'http://api.ceye.io/v1/records?token={token}&type=dns&filter={filter}'.format(token=key, filter=query)
        return requests.get(api_base).content

    def getHttpRecord(self, delay=2):
        time.sleep(delay)
        query = self.random + '.' + self.custom
        api_base = 'http://api.ceye.io/v1/records?token={token}&type=dns&filter={filter}'.format(token=key,
                                                                                                 filter=query)
        return requests.get(api_base).content

    def verifyDNS(self, delay=2):
        return '{"code": 200, "message": "OK"}' in self.getDnsRecord(delay)

    def verifyHTTP(self, delay=2):
        return '{"code": 200, "message": "OK"}' in self.getHttpRecord(delay)


if __name__ == "__main__":
    import subprocess
    c = Ceye()
    domain = c.getRandomDomain("test")
    subprocess.call("ping %s" % domain, shell=True)
    res = c.getDnsRecord(5)
    print domain, res
