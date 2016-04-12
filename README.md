#POC-T  
简易批量漏洞验证框架，给脚本搭上多线程的顺风车   
  
#结构  
##POC-T.py  
快速开始 `python POC-T.py`  
查看帮助 `-h`  
查看可用模块 `--show`  
取消实时进度打印 `--nS`  
取消结果文件输出 `--nF`  
  
##module  
POC脚本库  
##dic  
字典库  
  
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
##V 1.0  
2016.03.12 - 完成多线程框架，增加`-t` `-m` `-f` `-o` `--show`选项 
##V 1.1
2016.04.11 - 优化参数处理，整理函数到`/lib/cmdline.py`，增加`--nF` `--nS`选项  
2016.04.12 - 添加`-i`参数，重构部分代码  
#已有模块/POC  
脚本在`./module/`目录下:  
 - `test.py` 测试模块  
 - `pycurl_ip.py` 下载指定IP的html页面  
 - `spider.py` B站用户签名档爬虫  
  
#反馈  
 - mail:i@cdxy.me  
 - [http://www.cdxy.me](http://www.cdxy.me)  
