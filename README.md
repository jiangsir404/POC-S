#POC-T 
[![Python 2.6|2.7](https://img.shields.io/badge/python-2.6|2.7-yellow.svg)](https://www.python.org/) [![License](https://img.shields.io/badge/license-GPLv2-red.svg)](https://raw.githubusercontent.com/sqlmapproject/sqlmap/master/doc/COPYING)  
  
多线程应用框架, 加载用户自定义脚本  
  
可用于:
 - 批量漏洞验证  
 - 爆破&扫描  
 - 爬虫&采集  
  
##效果图
![效果图](http://www.cdxy.me/wp-content/uploads/2016/04/2016-04-15-102129屏幕截图.png)  

  
##开始  
###快速开始  
`python POC-T.py -h`  
  
###参数中文说明  
```
usage: POC-T.py [-m] [-f or -i] [options]

optional arguments:
  -h, --help        
  --version         
  --show            显示./module/文件夹下所有可用的模块名称

module:
  -m [module]       指定加载的POC或模块名称

target mode:
  -f [target]       从文件加载目标列表(常用于扫描或批量漏洞验证)
  -i [start]-[end]  给定起始数字和结束数字，自动生成payload(常用于有数字规则的遍历，爬虫等)

optimization:
  -t [threads]      线程数，默认为10
  -o [output]       输出文件路径，默认保存在./output/目录下
  --single          当验证到一个结果时退出(常用于密码爆破)
  --nF              取消文件输出
  --nS              取消屏幕输出

```  
  
##结构  
 - `POC-T.py` 程序入口  
 - `module` POC脚本库  
 - `data` 资源库  
 - `lib` 项目代码  
  
##模块编写规则  
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

##开发日志  
####V 1.0  
2016.03.12 - 完成多线程框架，增加`-t` `-m` `-f` `-o` `--show`选项  
####V 1.1  
2016.04.11 - 优化参数处理，增加`--nF` `--nS`参数  
2016.04.12 - 添加`-i`参数  
####V 1.2  
2016.04.18 - 参考sqlmap重构项目，增加`--single`参数  
    
    
##反馈  
 - mail:i@cdxy.me  
 - [http://www.cdxy.me](http://www.cdxy.me)  
  
