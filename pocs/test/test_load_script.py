#!/usr/bin/env python		
#coding:utf-8

import imp
import unittest
import sys
import subprocess
import os

os.chdir('../')

def load_module():
	file, path_name, description = imp.find_module('phpstudy_backdoor', ['../script/'])
	print file, path_name, description
	# 第一个参数为完整的package名称，可以随意指定
	obj = imp.load_module('xxx', file,path_name, description)
	print obj
	# print obj.poc()

class TestSearchApi(unittest.TestCase):
	"""测试加载插件的一些方式"""
	def setUp(self):
		pass
	def tearDown(self):
		pass

	def test_cmd1(self):
		cmd = "python pocs.py -s test/test2.py -iS 127.0.0.1"
		res = subprocess.call(cmd, stdout=subprocess.PIPE, shell=True)
		self.assertTrue(res == 0)

	def test_cmd2(self):
		cmd = "python pocs.py -s ./script/test/test2.py -iS 127.0.0.1"
		res = subprocess.call(cmd, stdout=subprocess.PIPE, shell=True)
		self.assertTrue(res == 0)

	def test_cmd3(self):
		cmd = "python pocs.py -s test2 -iS 127.0.0.1"
		res = subprocess.call(cmd, stdout=subprocess.PIPE, shell=True)
		self.assertTrue(res == 0)

	def test_cmd4(self):
		cmd = "python pocs.py -b test -iS 127.0.0.1"
		res = subprocess.call(cmd, stdout=subprocess.PIPE, shell=True)
		self.assertTrue(res == 0)

	def test_cmd5(self):
		cmd = "python pocs.py -b test -s test2.py -iS 127.0.0.1"
		res = subprocess.call(cmd, stdout=subprocess.PIPE, shell=True)
		self.assertTrue(res == 0)

def test():
	unittest.main()
	# suite = unittest.TestSuite()
	# suite.addTest(TestSearchApi("test_cmd1"))
	# unittest.TextTestRunner().run(suite)  	

if __name__ == '__main__':
	test()