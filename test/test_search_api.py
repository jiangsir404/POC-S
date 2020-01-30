#!/usr/bin/env python		
#coding:utf-8

"""
测试fofa, zoomeye, google, shodan四个接口的搜索可否可用
"""

import unittest
import sys

sys.path.append('../')
from lib.core.data import logger, paths
paths.CONFIG_PATH = "../toolkit.conf"

class TestSearchApi(unittest.TestCase):
	def setUp(self):
		pass
	def tearDown(self):
		pass

	# def testShodan(self):
	# 	from lib.api.shodan.pack import ShodanSearch
	# 	res = ShodanSearch("ThinkPHP", 100)
	# 	print res

	def testZoomeye(self):
		from lib.api.zoomeye.pack import ZoomEyeSearch
		res = ZoomEyeSearch("ThinkPHP", 10)
		print res, len(res)
		self.assertTrue(len(res) == 20 and isinstance(res, list))

	def testFofa(self):
		from lib.api.fofa.pack import FofaSearch
		res = FofaSearch('domain="sangfor.com.cn"')
		print res

if __name__ == '__main__':
	suite = unittest.TestSuite()
	suite.addTest(TestSearchApi("testZoomeye"))
	suite.addTest(TestSearchApi("testFofa"))
	unittest.TextTestRunner().run(suite)  
