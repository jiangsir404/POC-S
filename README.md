#POC-T 
[![Python 2.6|2.7](https://img.shields.io/badge/python-2.6|2.7-yellow.svg)](https://www.python.org/) [![License](https://img.shields.io/badge/license-GPLv2-red.svg)](https://raw.githubusercontent.com/sqlmapproject/sqlmap/master/doc/COPYING)  
  
简易批量漏洞验证框架，给脚本搭上多线程的顺风车   
  
![效果图](http://www.cdxy.me/wp-content/uploads/2016/04/2016-04-15-102129屏幕截图.png)  

  
#开始  
`python POC-T.py -h`
  
#结构  
 - `POC-T.py` 程序入口  
 - `module` POC脚本库  
 - `data` 资源库  
 - `lib` 项目代码  
  
#module/POC编写规则  
重写以下三个函数,其中**poc()**必需要有,添加逻辑使漏洞存在时return True    
将文件保存为 `testPOC.py` 并拷贝到 `./module/` 文件夹下  
使用 `-m testPOC` 参数即可完成加载  
```
def info():
    return info_string
def poc(str):
    return True or false
def exp():
    return True or false
```  

#开发日志  
####V 1.0  
2016.03.12 - 完成多线程框架，增加`-t` `-m` `-f` `-o` `--show`选项 
####V 1.1  
2016.04.11 - 优化参数处理，增加`--nF` `--nS`选项  
2016.04.12 - 添加`-i`参数  
####V 1.2  
2016.04.18 - 参考sqlmap重构项目，多项稳定性改进  
  
    
#反馈  
 - mail:i@cdxy.me  
 - [http://www.cdxy.me](http://www.cdxy.me)  
  
