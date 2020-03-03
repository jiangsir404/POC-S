#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-


import sys
import unittest
sys.path.append('../')
from lib.core.data import logger, paths
paths.CONFIG_PATH = "../toolkit.conf"
from plugin.dnslog import Dnslog


import os, requests

class TestCeye(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dnslog = Dnslog("s7045")
        cls.domain = cls.dnslog.getDomain()
        cls.dns_command = cls.dnslog.getCommand("dns")
        cls.web_command = cls.dnslog.getCommand("web")
        cls.web_curl_command = cls.dnslog.getCommand("web_curl")

    def test_getDomain(self):
        print("domain: %s" % self.domain)

    def test_getCommand(self):
        print("dns command: %s" % self.dns_command)
        print("web_curl command: %s" % self.web_curl_command)

    def test_getDnsRecord(self):
        os.popen(self.dns_command).read()
        resp = self.dnslog.getDnsRecord(delay=2)
        print("[test_getDnsRecord] %s" % resp)
        self.assertTrue('"status": "success"' in resp)

    def test_getHttpRecord(self):
        os.popen(self.web_curl_command).read()
        resp = self.dnslog.getHttpRecord(delay=2)
        print("[test_getHttpRecord] %s" % resp)
        self.assertTrue('"status": "success"' in resp)

def test_single():
    suite = unittest.TestSuite()
    suite.addTest(TestCeye('test_getdomain'))
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__':
    unittest.main()
