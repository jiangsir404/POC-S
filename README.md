# POC-T: *Pentest Over Concurrent Toolkit* 

使用文档: https://github.com/Xyntax/POC-T/wiki  (doc目录下)

> 由于第三方接口需要认证，您可以在根目录下的新建tookit.conf配置文件中预先设置好您的API-KEY。如无预配置，程序将在运行时提示您输入API-KEY。

## 使用
- `poc-t.py --batch -iF 1.txt` 使用fuzz脚本
- `poc-t.py -eT -t 20 -s xx -iF 1w.txt`
- `python .\POC-T.py -b test -t 20 -iF .\data\Shodan\20200130230506.txt` 批量使用test脚本来测试

## 插件
- waf 检测waf 并返回没有waf的url
- craw 爬取链接中的相关地址
- vulscan 检测sql注入漏洞
- portscan 端口扫描，检测弱口令服务
  
