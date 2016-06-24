# POC-T: *Pentest Over Concurrent Toolkit* 
[![Python 2.6|2.7](https://img.shields.io/badge/python-2.6|2.7-yellow.svg)](https://www.python.org/) [![License](https://img.shields.io/badge/license-GPLv2-red.svg)](https://raw.githubusercontent.com/Xyntax/POC-T/master/docs/LICENSE.txt)  

> 跨平台模块化并发框架，可用于采集/爬虫/爆破/批量PoC等需要并发的地方。

* 支持两种并发模式*(多线程/单线程异步)*和多种输入方式
* 极简式模块编写
* 无交互运行，方便部署自动化
* 实用工具/PoC更新中

*(欢迎提交代码和改进建议)*
  
![banner.png](https://github.com/Xyntax/POC-T/blob/master/docs/banner.png) 

## 它能做什么？  
这个小巧的并发框架可以满足许多日常需求.  
用户可参考以下已集成的脚本(`./module/`)来编写自己的功能模块.    

#### 漏洞验证 
|模块|说明|
|:---|:---|
|`sqli-poc-example.py`| SQL注入PoC示例|  
|`jboss-poc.py`       | jboss漏洞PoC(jexboss去后门版)|  
|`struts2-s2032.py`   | Struts2 S2-032 远程命令执行|  
|`zonetransfer-poc.py`| DNS域传送漏洞PoC|
  
#### 爆破&扫描 
|模块|说明|
|:---|:---|
|`zabbix-weakpass.py`  |zabbix弱口令扫描|  
|`brute-example.py`    |密码爆破示例(51idc某站)|
  
#### 爬虫&采集
|模块|说明|
|:---|:---|
|`spider-example.py`   |爬虫示例(B站用户签名档爬虫)|  
|`collector-example.py`|页面采集示例|  

  
#### 其他 
|模块|说明|
|:---|:---|
|`vote-example.py`     |给基友开发的刷票脚本|  
|`bingc.py`|基于Bing搜索引擎的IP反查域名|  
|`others`|等你开脑洞|  
  
  
## 快速开始 
* `pip install -r requirement.txt` 
* `python POC-T.py`  

## 使用说明 

![usage.png](https://github.com/Xyntax/POC-T/blob/master/docs/usage.png) 

## 结构  
以下含@的目录表示用户可控区域，用户可根据需要*增加/修改/调用*其中的内容

| 目录 | 说明 |
| :-----  |:-----|
| `POC-T.py` | 程序入口 |
| module   | @自定义模块/PoC脚本库 |
| util     | @工具库 |
| data     | @资源库 |
| output   | 默认输出位置 |
| lib      | 项目代码 |
| docs     | 文档及版权声明 |
| thirdparty | 第三方库 |

  
## 模块编写
极简式模块编写，它只需要声明一个函数作为接口，没有其他任何限制．

#### 新建文件
* 进入`./module`目录
* 在此目录下新建Python文件 `poctest.py`

#### 添加接口函数-poc()
* 在代码中添加函数 **poc()**
* 添加逻辑使验证成功(漏洞存在)时`return True`,验证失败时`return False`
* (程序运行时，每个子线程调用该文件的poc()方法，并将队列中的取出的字符串传入该方法)
```
def poc(input_str):
    return True or false
```  
#### 结果判断(可选)
针对一些复杂的需求，poc()函数可以使用多种返回值来控制验证状态和输出。
以下模拟一个简单的密码爆破模块代码
```
def poc(input_str):
    url = 'http://xxx.com/login.php?pass=' + input_str
    try:
        c = requests.get(url).content
    except ConnectionError:
        return 2     # 把input_str重新加入任务列表重新验证(本次验证作废)
    if 'success' in c:
        return True  # 验证成功，屏幕结果输出为123456
        return 1     # 同上
        return url   # 验证成功，屏幕结果输出为"http://xxx.com/login.php?pass=123456"
    else
        return False # 验证失败，无输出
        return 0     # 同上

```

#### 查看及使用模块
* `python POC-T.py --show` 查看全部模块名称
* 在命令行中使用 `-m poctest` 参数即可完成`poctest`模块的加载 (注意名称末尾不需要写`.py`)  
  
工具目录 
----
`util`文件夹中收集了具有通用性的工具组件．用于简化代码，提高PoC准确性，赋予脚本更多功能.
编写模块时，可以使用`from util.xxx import xxx()`直接调用，具体功能请查看原文件注释.  
  
|工具|说明|
|:---|:---|
|urlparser.py | URL处理工具，可对采集到的杂乱URL进行格式化/自动生成等|
|useragent.py | User-Agent处理工具, 支持随机化UA以绕过防御规则|
|extracts.py  | 正则提取工具，从采集到的杂乱文本中筛选IP地址|

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

  
