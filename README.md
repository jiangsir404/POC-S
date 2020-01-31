# POC-S: *POC-T Stong Version POC-T加强版* 

详细wiki文档请看doc目录


## 使用 
> 由于第三方接口需要认证，您可以在根目录下的新建tookit.conf配置文件中预先设置好您的API-KEY。如无预配置，程序将在运行时提示您输入API-KEY。

some command: 

- `poc-s.py --batch -iF 1.txt` 使用fuzz脚本
- `poc-s.py -eT -t 20 -s xx -iF 1w.txt`
- `python .\POC-S.py -b test -t 20 -iF .\data\Shodan\20200130230506.txt` //
批量使用test脚本来测试
- `python POC-S.py -b redis -t 50 -aZ "port:6379" --limit 100` 测试redis漏洞

## 插件
一共有四个分类的POC: Fuzz POC, OWASP POC, Vuln POC, Tool POC.

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

- cmd_exec
- sql_injection
- xss
- xxe
- csrf
- jsonp_xss
- jsonp_hijacking
- file_read
- ssti
- ssrf
  
### Vuln POC
主要来源于vulhub 以及 POC-T自带的插件poc

- [ ] thinkphp
	- [ ] 5-rce
	- [ ] 2-rce
	- [ ] 5.0.23-rce
	- [ ] in-sqlinjection

- [ ] unauth
	- [x] redis-unauth.py
	- [x] mongodb-unauth.py
	- [x] memcached-unauth.py
	- [x] elasticsearch-unauth.py
	- [x] kubernetes-unauth.py
	- [x] jenkins-unauth.py
	- [ ] docker-unauth-rce.py
	- [ ] hadoop-unauth.py


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
	- [x] struts2-s2045.py
	- [x] struts2-s2032.py
	- [ ] struts2-s2016.py

- [ ] weblogic
	- [x] weblogic-ssrf-netmap.py
	- [ ] weblogc_wls_rce.py
	- [ ] weblogic_upload.py
	- [ ] web

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