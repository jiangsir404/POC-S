#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author = i@cdxy.me
# project = https://github.com/Xyntax/POC-T

import random
import requests
import time
from string import ascii_lowercase

# your API-key in "http://cloudeye.me/?a=list"
key = '1e860ff056b33000----------------'

# your personal sub-domain, like: xxxxxx.dnslog.info
uniq_domain = 'xxxxxx'


class CloudEye:
    def __init__(self):
        self.unique = uniq_domain
        self.random = ''.join([random.choice(ascii_lowercase) for _ in range(10)])

    def getRandomDomain(self, custom='poc'):
        """
        full domain = [random].[custom].[unique].dnslog.info
        e.g. fezarvgo.poc.ee8a6f.dnslog.info
        """
        self.custom = custom
        return '%s.%s.%s.dnslog.info' % (self.random, self.custom, self.unique)

    def getDnsRecord(self, delay=2):
        time.sleep(delay)
        query = self.random + '.' + self.custom
        api_base = 'http://cloudeye.me/api/{key}/{domain}/DNSLog/'.format(key=key, domain=query)
        return requests.post(api_base).content

    def getHttpRecord(self, delay=2):
        time.sleep(delay)
        query = self.random + '.' + self.custom
        api_base = 'http://cloudeye.me/api/{key}/{domain}/ApacheLog/'.format(key=key, domain=query)
        return requests.post(api_base).content

    def verifyDNS(self, delay=2):
        return 'dnslog.info' in self.getDnsRecord(delay)

    def verifyHTTP(self, delay=2):
        return 'dnslog.info' in self.getHttpRecord(delay)


if __name__ == '__main__':
    c = CloudEye()
    a = c.getRandomDomain('cdxy')
    try:
        requests.get('http://' + a, timeout=1)
    except:
        pass
    print c.verifyDNS(delay=0)
    print c.verifyHTTP(delay=0)
    print c.getDnsRecord(delay=0)
    print c.getHttpRecord(delay=0)
