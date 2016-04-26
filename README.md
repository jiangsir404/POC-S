# POC-T
[![Python 2.6|2.7](https://img.shields.io/badge/python-2.6|2.7-yellow.svg)](https://www.python.org/) [![License](https://img.shields.io/badge/license-GPLv2-red.svg)](https://raw.githubusercontent.com/sqlmapproject/sqlmap/master/doc/COPYING)  
  
![](http://www.cdxy.me/wp-content/uploads/2016/04/2016-04-23-180429屏幕截图.png)  
  
简易并发框架，为用户脚本提供并发解决方案。  
支持 **多线程** 和 **协程(单线程异步)** 两种并发模式。
  
(开发中，一些功能不稳定，欢迎issue)  
## 它能做什么？  
它只提供了一个并发框架，附带一些示例模块，功能需要用户自行添加模块实现。   
  
### 功能示例 
#### 批量漏洞验证 
 - `./module/jboss.py` JBoss漏洞检测  
 - `./module/fzxy_sqli.py` 方正翔宇某系统SQLI检测  
 - `./module/S2032.py` Struts2 S2-032 远程命令执行  
  
#### 爆破&扫描 
 - `./module/zabbix_wp.py` zabbix弱口令扫描  
  
#### 爬虫&采集
 - `./module/spider.py` B站用户签名档爬虫  
 - `./module/pycurl_ip` html页面采集示例  
  
#### 其他 
 - `./module/vote++.py` 给基友开发的刷票脚本  
 - 等你开脑洞  
  

## 开始 
### 快速开始 
 - `pip install -r requirement.txt` 
 - `python POC-T.py`  

### 参数中文说明 
```
usage: POC-T.py [-T|-C] [-m] [-f|-i|-n] [options]
  
example:
    python POC-T.py -T -m test -f ./dic/1-100.txt
    python POC-T.py -C -m test -i 1-100
    python POC-T.py -C -m spider -n 10.0.0.0/24
  
engine:
  -T                多线程模式
  -C                协程(单线程异步)模式
  -t [num]          设置并发数量(线程数量)
  
module:
  -m [module]       指定加载的POC或模块名称

target mode:
  -f [target]       从文件加载目标列表(常用于扫描或批量漏洞验证)
  -i [start]-[end]  给定起始数字和结束数字，自动生成payload(常用于有数字规则的遍历，爬虫等)
  -n [IP/MASK]      从IP和子网掩码加载目标，如:10.0.0.0/28 (用于扫描网段)

optimization:
  -o [output]       输出文件路径，默认保存在./output/目录下
  --single          当验证到一个结果时退出(常用于密码爆破)
  --nF              取消文件输出
  --nS              取消屏幕输出
  --show            显示./module/文件夹下所有可用的模块名称
  --debug           开启debug模式，输出一些细节
  --update          自动从github更新程序
```  
  
## 运行效果  
  
### B站用户爬虫模块(kali2) 
![](http://www.cdxy.me/wp-content/uploads/2016/04/2016-04-15-102129屏幕截图.png)  
### JBoss漏洞检测模块(win7)  
![](http://www.cdxy.me/wp-content/uploads/2016/04/微信截图_20160419213553.png)  
  
  
## 结构  
 - `POC-T.py` 程序入口  
 - `module` POC脚本库  
 - `data` 资源库  
 - `lib` 项目代码  
  
## 模块编写规则
新建py文件,添加以下三个函数,其中**poc()**必需要有,添加逻辑使验证成功(漏洞存在)时`return True`,验证失败时`return False`    
将文件保存为 `testPOC.py` 并拷贝到 `./module/` 文件夹下  
使用 `-m testPOC` 参数即可完成加载  
  
**注**:一些功能在开发中，目前只用到了`poc()`  
  
```
def info():
    return info_string
def poc(str):
    return True or false
def exp():
    return True or false
```  

## 开发日志 
#### 1.0 
2016.03.12 - 完成多线程框架，增加`-t` `-m` `-f` `-o` `--show`选项    
#### 1.1 
2016.04.11 - 优化参数处理，增加`--nF` `--nS`参数  
2016.04.12 - 添加`-i`参数  
#### 1.2 
2016.04.18 - 参考sqlmap重构项目，增加`--single`参数  
2016.04.19 - 添加协程引擎，增加`-T -C`参数    
#### 1.3 
2016.04.23 - 使用`logging`优化输出，增加`banner`和`--debug`参数，修复bugs  
2016.04.24 - 增加`--update`支持自动更新  
2016.04.25 - 增加`-n`支持从网段导入IP地址列表  
  
## 反馈  
 - mail:i@cdxy.me  
 - 博客:[http://www.cdxy.me](http://www.cdxy.me)  
  
