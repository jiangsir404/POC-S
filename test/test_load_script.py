#!/usr/bin/env python		
#coding:utf-8

import imp

# 模块文件为: /home/scripts/env.py, 第二个参数为列表，可以从多个目录里面找
file, path_name, description = imp.find_module('phpstudy_backdoor', ['../script/'])
print file, path_name, description

obj = imp.load_module('_1', file,path_name, description)
print obj
print obj.poc()