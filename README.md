# POC-T
[![Python 2.6|2.7](https://img.shields.io/badge/python-2.6|2.7-yellow.svg)](https://www.python.org/) [![License](https://img.shields.io/badge/license-GPLv2-red.svg)](https://raw.githubusercontent.com/Xyntax/POC-T/master/docs/LICENSE.txt)  

模块化并发框架，提升用户脚本的运行效率。  
支持 **多线程** 和 **协程(单线程异步)** 两种并发模式。
  
*(开发中，欢迎提交POC和改进建议)*  
  
![banner.png](https://github.com/Xyntax/POC-T/blob/cdxy/docs/banner.png) 

## 它能做什么？  
这个小巧的并发框架可以满足许多日常需求.  
用户可参考以下已集成的脚本来编写您的功能模块.    

#### 漏洞验证 
* `./module/sqli-poc-example.py` SQL注入POC示例(方正翔宇某系统)  
* `./module/jboss-poc.py`        jboss漏洞POC(jexboss去后门版)  
* `./module/struts2-s2032.py`    Struts2 S2-032 远程命令执行  
* `./module/zonetransfer-poc.py` DNS域传送漏洞POC
  
#### 爆破&扫描 
* `./module/zabbix-weakpass.py`  zabbix弱口令扫描  
* `./module/brute-example.py`    密码爆破示例(51idc某站)
  
#### 爬虫&采集
* `./module/spider-example.py`   爬虫示例(B站用户签名档爬虫)  
* `./module/collector-example.py`页面采集示例  
  
#### 其他 
* `./module/vote-example.py`     给基友开发的刷票脚本  
* 等你开脑洞  
  


  
## 开始 
### 快速开始 
* `pip install -r requirement.txt` 
* `python POC-T.py`  

### 参数中文说明 
```
usage: POC-T.py [-T|-C] [-m] [-f|-i|-n] [options]
  
example:
    python POC-T.py -T -m test -f ./dic/1-100.txt
    python POC-T.py -C -m test -i 1-100
    python POC-T.py -C -m spider-example -n 10.0.0.0/24
  
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
  
  
## 结构  
* `POC-T.py`    程序入口  
* `module`      POC脚本库  
* `data`        资源库  
* `output`      默认输出路径
* `lib`         项目代码  
* `docs`        文档及版权声明
* `thirdparty`  第三方库
  
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

相关链接
----
* [感谢列表](./docs/THANKS.md)
* [开发日志](./docs/CHANGELOG.md)
* [版权声明](./docs/LICENSE.txt)
* [中文文档](./docs/USAGE.md)
* [问题/BUG反馈](https://github.com/Xyntax/POC-T/issues)

联系作者
----
* mail:i@cdxy.me  
* 博客:[http://www.cdxy.me](http://www.cdxy.me)  
  
