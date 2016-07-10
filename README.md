# POC-T: *Pentest Over Concurrent Toolkit* 
[![Python 2.6|2.7](https://img.shields.io/badge/python-2.6|2.7-yellow.svg)](https://www.python.org/) [![License](https://img.shields.io/badge/license-GPLv2-red.svg)](https://raw.githubusercontent.com/Xyntax/POC-T/master/docs/LICENSE.txt)  

> 模块化并发框架，可处理渗透测试中 **采集/爬虫/爆破/批量PoC** 等需要并发的任务。
  
* 两种并发模式、五种信息输入格式  
* 极简式插件编写，无需参考文档  
* 实用扩展工具，让插件更加精细优雅  
* 支持第三方搜索引擎API(已完成ZoomEye/Shodan)  
* 其他人性化功能参数  
* 跨平台，免安装  
  
*(欢迎提交代码和改进建议)*
   
![banner.png](https://github.com/Xyntax/POC-T/blob/master/docs/banner.png) 

## 不止于PoC 
这个小巧的并发框架可以满足许多日常需求.  
用户可参考以下已经集成的脚本，打开脑洞，自行编写更多实用插件.      

* [查看已集成插件](https://github.com/Xyntax/POC-T/blob/master/docs/module.md)

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
| api      | 搜索引擎接口 |

  
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
* 在命令行中使用 `-m poctest` 参数即可完成`poctest`插件的加载 (注意名称末尾不需要写`.py`)  
  
插件扩展工具 
------
`util`文件夹中收集了具有通用性的工具组件．用于简化代码，提高PoC准确性，赋予脚本更多功能.
编写模块时，可以使用`from util.xxx import xxx()`直接调用，具体功能请查看原文件注释.  
  
|工具|说明|
|:---|:---|
|urlparser.py | URL处理工具，可对采集到的杂乱URL进行格式化/自动生成等|
|useragent.py | User-Agent处理工具, 支持随机化UA以绕过防御规则|
|extracts.py  | 正则提取工具，从采集到的杂乱文本中筛选IP地址|

第三方搜索引擎接口
---------

本工具拟支持主流空间搜索引擎的API，如ZoomEye/Shodan/Censys等(目前已支持ZoomEye/Shodan)．
从搜索引擎中直接获取目标，并结合本地插件进行扫描．

#### ZoomEye
以下命令表示使用ZoomEye接口，搜索全网中开启`8080`号端口的服务，并使用`test.py`插件进行验证．  
设置爬取10页搜索结果，搜索结果将存入本地`/data/zoomeye`文件夹下．  

`python POC-T.py -T -m test --api --dork "port:8080" --max-page 10`  
  
如第一次使用接口，需按提示输入ZoomEye的帐号和密码．  
ZoomEye现已开放注册，普通用户每月可以通过API下载5000页的搜索结果．  

* [ZoomEye-API官方文档](https://www.zoomeye.org/api/doc)

#### Shodan
以下命令表示使用Shodan接口，搜索全网中关键字为`solr`，国家为`cn`的服务，并使用`solr-unauth`插件进行验证．  
设置从第0条记录为起点，爬取10条记录，搜索结果将存入本地`/data/shodan`文件夹下．  
  
`python POC-T.py -T -m solr-unauth --api --query "solr country:cn" --limit 10 --offset 0`  
  
如第一次使用接口，需按提示输入Shodan的API-KEY([https://account.shodan.io/](https://account.shodan.io/))  
Shodan-API接口使用限制及详细功能，可参考官方文档.

* [Shodan-API官方文档](https://developer.shodan.io/api/requirements)

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

  
