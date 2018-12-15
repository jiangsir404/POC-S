# -*- coding: utf-8 -*-
# @Author: zeroyu
# @Date:   2018-12-15 23:12:09
# @Last Modified by:   zeroyu
# @Last Modified time: 2018-12-15 23:26:50

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
# 	比如使用下面命令获取子域名
# 	python POC-T.py -iS "site:test.com" -s test.py -eG

def subdomin_finder_by_bing(target):

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

	#bing最多也是1000
	start=1000

	subdomins=[]

	for step in range(0,start+10,10):

		url="https://www.bing.com/search?q={}".format(target)
		url=url+"&first={}".format(step)
		print "step:",step

		try:
			# call method with timeout
			tab.Page.navigate(url=url, _timeout=5)
			tab.wait(5)

			exp='document.getElementsByClassName("b_algo").length'
			length= tab.Runtime.evaluate(expression=exp)

			#从每一页上抓取url
			for l in range(0,length['result']['value']):
				exp1='document.getElementsByClassName("b_algo")[{}].getElementsByTagName("a")[0].href'.format(l)
				res1= tab.Runtime.evaluate(expression=exp1)
				# print res1['result']['value']
				subdomins.append(res1['result']['value'])
		except:
			pass

	tab.stop()
	browser.close_tab(tab)
	return subdomins

def poc(target):
	subdomins=subdomin_finder_by_bing(target)
	tmp=[]
	for sub in subdomins:
		url=urlparse.urlparse(sub)
		tmp.append(url.scheme+"://"+url.netloc)
	subdomins=list(set(tmp))
	if subdomins:
		# for s in subdomins:
		# 	print s
		return True
	return False
