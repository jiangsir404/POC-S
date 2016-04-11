#POC-T  
批量漏洞验证框架，支持多线程，个人维护字典库和poc库  
  
#结构  
##POC-T.py  
快速开始 `python POC-T.py -t [线程数] -m [POC脚本] -f [目标列表文件] -o [输出路径]`  
查看帮助 `-h`  
查看可用模块 `--show`  
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
2016.03.12 - 完成多线程框架，增加-t -m -f -o --show选项  
2016.04.11 - 提取参数处理函数到/lib/cmdline.py，增加--nF --nS选项  
  
#反馈
mail:i@cdxy.me  
http://www.cdxy.me  
