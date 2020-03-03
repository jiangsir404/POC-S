#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

"""
Author: rivir
Date: 2020/3/1
"""
import sys
import unittest
sys.path.append('../')
import os, requests
from lib.core.data import logger, paths
paths.CONFIG_PATH = "../toolkit.conf"
from lib.utils.config import ConfigFileParser

class TestCeye(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cf = ConfigFileParser()
        print("CONFIG PATH: %s" % paths.CONFIG_PATH)

    def test_get_option(self):
        zoomeye_email = self.cf.ZoomEyeEmail()
        zoomeye_password = self.cf.ZoomEyePassword()
        print("get zoomeye", zoomeye_email, zoomeye_password)

    def test_set_option(self):
        res = self.cf._set_option("zoomeye", "email", "xxx@qq.com")
        self.assertTrue(res == True)

    def test_get_options(self):
        options = self.cf._get_options("dnslog")
        print("[test_get_options] %s" % options)
        self.assertTrue(options)

    def test_get_wrong(self):
        no_key  = self.cf._get_option("zoomeye", "aaa")
        print("no_key:", [no_key])


def test_single():
    suite = unittest.TestSuite()
    suite.addTest(TestCeye('test_getRandomDomain'))
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__':
    unittest.main()

