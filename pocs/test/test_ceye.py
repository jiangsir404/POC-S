#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

"""
Author: rivir
Date: 2020/2/22
"""
import sys
import unittest
sys.path.append('../')
from plugin.ceye import Ceye
import os, requests

class TestCeye(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dnslog = Ceye()
        cls.domain = cls.dnslog.getRandomDomain('s2045')
        print("domain: %s" % cls.domain)

    def test_getRandomDomain(self):
        self.assertTrue("s2045" in self.domain)

    def test_getDnsRecord(self):
        os.popen("ping -n 1 %s" % self.domain).read()
        resp = self.dnslog.getDnsRecord(delay=2)
        print("[test_getDnsRecord] %s" % resp)
        self.assertTrue('{"code": 200, "message": "OK"}' in resp)

    def test_getHttpRecord(self):
        requests.get("http://%s" % self.domain)
        resp = self.dnslog.getHttpRecord(delay=2)
        print("[test_getHttpRecord] %s" % resp)
        self.assertTrue('{"code": 200, "message": "OK"}' in resp)

def test_single():
    suite = unittest.TestSuite()
    suite.addTest(TestCeye('test_getRandomDomain'))
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__':
    unittest.main()


