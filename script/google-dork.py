#!/usr/bin/env python
# -*- coding: utf-8 -*-
# project = https://github.com/Xyntax/POC-T
# author = z3r0yu

import pychrome
import urlparse

# 环境配置:
# 	本地配置chrome的headless，执行如下命令:
# 	headless mode (chrome version >= 59):
# 	$ google-chrome --headless --disable-gpu --remote-debugging-port=9222

# 	或者直接使用docker
# 	$ docker pull fate0/headless-chrome
# 	$ docker run -it --rm --cap-add=SYS_ADMIN -p9222:9222 fate0/headless-chrome

# 	PS:使用google插件的时候打开ss就好


# 使用说明:
# 	对目标使用google dork语法，程序会返回抓取的域名
# 	python POC-T.py -iS "site:test.com" -s test.py -eG

def subdomin_finder_by_google(target):

	# create a browser instance
	browser = pychrome.Browser(url="http://127.0.0.1:9222")

	# create a tab
	tab = browser.new_tab()

	# start the tab
	tab.start()

	tab.Page.enable()

	# call method
	tab.Network.enable()
	tab.Runtime.enable()

	start=1000

	subdomins=[]

	for step in range(0,start+10,10):

		url="https://www.google.com/search?q={}".format(target)
		url=url+"&start={}".format(step)
		print "step:",step

		# call method with timeout
		tab.Page.navigate(url=url, _timeout=5)
		tab.wait(5)

		exp='document.getElementsByClassName("r").length'
		length= tab.Runtime.evaluate(expression=exp)		

		# google就看报不报错，报错了的话document.getElementsByClassName("r").length是为0的
		if length['result']['value']==0:
			break

		#从每一页上抓取url
		for l in range(0,length['result']['value']):
			# tab.wait(1)
			exp1='document.getElementsByClassName("r")[{}].getElementsByTagName("a")[0].href'.format(l)
			res1= tab.Runtime.evaluate(expression=exp1)
			# print res1['result']['value']
			subdomins.append(res1['result']['value'])

	tab.stop()
	browser.close_tab(tab)
	return subdomins

def poc(target):
	subdomins=subdomin_finder_by_google(target)
	tmp=[]
	for sub in subdomins:
		url=urlparse.urlparse(sub)
		if url.scheme+"://"+url.netloc != 'https://www.google.com':
			tmp.append(url.scheme+"://"+url.netloc)
	subdomins=list(set(tmp))
	if subdomins:
		# for s in subdomins:
		# 	print s
		return True
	return False