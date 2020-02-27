#!/usr/bin/env python
# coding:utf-8

"""
Weblogic WLS Core Components 反序列化命令执行漏洞（CVE-2018-2628）

Desc
    Oracle 2018年4月补丁中，修复了Weblogic Server WLS Core Components中出现的一个反序列化漏洞（CVE-2018-2628），
    该漏洞通过t3协议触发，可导致未授权的用户在远程服务器执行任意命令。
Version
    Weblogic 10.3.6.0
    Weblogic 12.1.3.0
    Weblogic 12.2.1.2
    Weblogic 12.2.1.3
Referer
    - http://www.oracle.com/technetwork/security-advisory/cpuapr2018-3678067.html
    - CVE-2018-2628 简单复现与分析 http://mp.weixin.qq.com/s/nYY4zg2m2xsqT0GXa9pMGA
    - https://github.com/tdy218/ysoserial-cve-2018-2628
"""

