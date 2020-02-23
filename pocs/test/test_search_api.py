#!/usr/bin/env python		
#coding:utf-8

"""
测试fofa, zoomeye, google, shodan四个接口的搜索可否可用
"""

import unittest
import sys
import os

from pocs.lib.core.data import logger, paths
from pocs.lib.api.zoomeye.pack import ZoomEyeSearch
from pocs.lib.api.zoomeye.pack import ZoomEyeSearch
from pocs.lib.api.fofa.pack import FofaSearch

paths.CONFIG_PATH = "../toolkit.conf"
# paths.CONFIG_PATH = os.path.dirname(os.path.dirname(__file__)) + "/toolkit.conf"
# print paths

class TestSearchApi(unittest.TestCase):
	def setUp(self):
		paths.CONFIG_PATH = os.path.dirname(os.path.dirname(__file__)) + "/toolkit.conf"
		print paths
		
	def tearDown(self):
		pass

	# def testShodan(self):
	# 	from lib.api.shodan.pack import ShodanSearch
	# 	res = ShodanSearch("ThinkPHP", 100)
	# 	print res

	def testZoomeye(self):
		res = ZoomEyeSearch("ThinkPHP", 10)
		print res, len(res)
		self.assertTrue(len(res) == 20 and isinstance(res, list))

	def testFofa(self):
		res = FofaSearch('domain="sangfor.com.cn"')
		print res

if __name__ == '__main__':
	suite = unittest.TestSuite()
	suite.addTest(TestSearchApi("testZoomeye"))
	#suite.addTest(TestSearchApi("testFofa"))
	unittest.TextTestRunner().run(suite)  
