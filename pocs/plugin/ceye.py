#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

"""
Author: rivir
Date: 2020/2/22

api
    curl http://api.ceye.io/v1/records?token={token}&type={dns|http}&filter={filter}
param
    token: your ceye api token.
    type: type of query, 'dns' or 'request'.
    filter: match url name rule, the filter max length is 20.

return
    {"meta": {"code": 200, "message": "OK"}, "data": [
        {"id": "39493615", "name": "svlzqvohnw.s2045.h7x7ty.ceye.io", "remote_addr": "183.235.39.38", "created_at": "2020-03-01 04:16:39"},
        {"id": "39493614", "name": "svlzqvohnw.s2045.h7x7ty.ceye.io", "remote_addr": "211.139.129.230", "created_at": "2020-03-01 04:16:39"}
    ]}
"""
import random
import requests
import time
from string import ascii_lowercase
import sys
sys.path.append('../')
from lib.core.data import logger, paths
# paths.CONFIG_PATH = "../toolkit.conf"
from lib.utils.config import ConfigFileParser

key = ConfigFileParser().CeyeApikey()
uniq_domain = ConfigFileParser().CeyePersonaldomain().split('.')[0]

class Ceye:
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
