#!/usr/bin/env python		
#coding:utf-8

import sys
sys.path.append('../')
from plugin.util import *

def test_util():
	print host2IP("http://127.0.0.1:6379/12")
	print IP2domain("127.0.0.1")
	print checkPortTcp("123.206.65.167", 81)

def test_cloudeye():
	pass

if __name__ == '__main__':
	test_util()