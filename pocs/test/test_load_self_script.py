#!/usr/bin/env python		
#coding:utf-8

"""
测试自定义的script脚本加载
"""

#!/usr/bin/env python		
#coding:utf-8

import imp
import unittest
import sys
import subprocess
import os


class TestSearchApi(unittest.TestCase):
	"""测试加载插件的一些方式"""
	def setUp(self):
		pass
	def tearDown(self):
		pass

	def test_cmd1(self):
		"""需要加上.py, 否则无法识别"""
		cmd = "pocs -s myself_script.py -iS 127.0.0.1"
		res = subprocess.call(cmd, stdout=None, shell=True)
		self.assertTrue(res == 0)

	def test_cmd2(self):
		cmd = "pocs -b myscriptdir -iS 127.0.0.1"
		res = subprocess.call(cmd, stdout=None, shell=True)
		self.assertTrue(res == 0)

	def test_cmd3(self):
		cmd = "pocs -b myscriptdir -s test2.py -iS 127.0.0.1"
		res = subprocess.call(cmd, stdout=None, shell=True)
		self.assertTrue(res == 0)


def test():
	unittest.main()	

if __name__ == '__main__':
	test()