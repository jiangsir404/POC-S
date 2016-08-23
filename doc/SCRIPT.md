# 已集成脚本

漏洞验证 
----
|脚本|说明|
|:---|:---|
|`jboss-rce.py`       | JBoss 命令执行 (jexboss去后门版) |  
|`struts2-s2032.py`   | Struts2 S2-032 命令执行 | 
|`struts2-devmode.py` | Struts2 devMode 命令执行 |
|`zonetransfer-poc.py`| DNS域传送漏洞 |
|`solr-unauth.py`     | Apache Solr 未授权访问 |
|`redis-unauth.py`    | Redis 未授权访问 |
|`redis-web-probe.py`| Redis利用之 webshell|
|`redis-cron-getshell.py`| Redis利用之 cron.d|
|`redis-sshkey-getshell.py`| Redis利用之 ssh-key|
|`activemq-weakpass.py`    | ActiveMQ 弱口令 |
|`activemq-upload.py`    | ActiveMQ 文件上传 |
|`memcached-unauth.py`    | Memcached 未授权访问 |
|`opensshd-user-enum.py`| Opensshd 用户猜解 |
|`glassfish-traversal.py`| GlassFish 任意文件读取|
|`confluence-file-read.py`| Atlassian Confluence 文件读取 |
|`jetspeed-rest-unauth.py`| Apache Jetspeed REST API未授权访问|
|`phpmyadmin-auth-rce.py` | phpMyAdmin 登入后命令执行|
|`shiro-deserial-rce.py`  | Apache Shiro 反序列化命令执行|
|`metinfo-504-sqli.py`| MetInfo 5.0.4 id参数SQL注入|
|`joomla-videoflow-sqli.py`| Joomla videoflow组件SQL注入|
|`navis-webaccess-sqli.py`| Navis WebAccess SQL注入|
|`vbulletin-ssrf.py`| vBulletin SSRF |
|`wp-4.4-ssrf.py`| WordPress 4.4 SSRF |
|`wp-forcedownload.py`| WordPress forcedownload 任意文件下载|
|`wp-ypo-filedownload.py`| WordPress ypo theme 任意文件下载|
|`samsoftech-admin-bypass.py`| SAM Softech后台登录绕过|
|`joomla-registrationpro-sqli.py`| Joomla registrationpro组件SQL注入|
|`zabbix-jsrpc-sqli.py`  | Zabbix jsrpc.php SQL注入检测|
|`zabbix-jsrpc-mysql-exp.py`| Zabbix jsrpc.php MySQL注入利用 (作者:B0t0w1)|  
|`siemens-camera-getpwd.py`| SIEMENS IP-Camrea 密码泄露|


爆破&扫描 
-----
|脚本|说明|
|:---|:---|
|`brute-example.py`    | 表单爆破示例(51idc某站)|
|`rsync-weakpass.py`   | rsync 弱口令爆破|
|`zabbix-weakpass.py`  | zabbix 弱口令爆破|
|`weblogic-ssrf-netmap`|利用SSRF漏洞扫描内网端口(nmap 1000 ports)|
  
爬虫&采集
-----
|脚本|说明|
|:---|:---|
|`spider-example.py`   |爬虫示例(B站用户签名档爬虫)|  
  
其他
---
|脚本|说明|
|:---|:---|
|`vote-example.py`     |给基友开发的刷票脚本|  
|`bingc.py`            |基于Bing搜索引擎的C段/旁站扫描(支持Bing-API)|  
  
  
