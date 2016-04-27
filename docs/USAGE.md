快速开始
----
```
    pip install -r requirement.txt
    python POC-T.py
```

参数中文说明
----
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