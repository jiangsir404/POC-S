# !/usr/bin/env python
#  -*- coding: utf-8 -*-
# from __future__ import unicode_literals

u"""
本文档为程序中文使用说明，您也可以使用 -h 查看英文版使用说明
powered by cdxy <mail:i@cdxy.me>

使用方法:
  python POC-T.py [-T|-C] [-m NAME] [-s|-f|-i|-n VALUE] [options]
  python POC-T.py [-h|-v|--show|--update]

示例:
  python POC-T.py -T -m jboss-poc -s http://www.cdxy.me
  python POC-T.py -T -m test -f ./dic/1-100.txt
  python POC-T.py -C -m test -i 1-100
  python POC-T.py -C -m spider -n 10.0.0.0/24

引擎(必需项):
  -T             多线程模式
  -C             协程(单线程异步)模式
  -t NUM         设置并发数量(线程数量)，默认为10

模块(必需项):
  -m NAME        指定加载的POC或模块名称(结尾不需加.py)

目标(必需项):
  -s TARGET      验证单个目标 (e.g. www.wooyun.org)
  -f FILE        从文件加载目标列表(常用于扫描或批量漏洞验证) (e.g. ./data/wooyun_domain)
  -i START-END   给定起始数字和结束数字，自动生成payload(常用于有数字规则的遍历，爬虫等) (e.g. 1-100)
  -n IP/MASK     从IP和子网掩码加载目标(用于扫描网段) (e.g. 127.0.0.0/24)

可选项:
  -o FILE        输出文件路径，默认保存在./output/目录下
  --single       当验证到一个结果时退出(常用于密码爆破)
  --nF           取消文件输出
  --nS           取消屏幕输出
  --show         显示所有可用的模块名称(./module/文件夹下)
  --browser      程序结束后，将运行结果在浏览器/记事本中打开
  --debug        开启debug模式，运行时将输出一些参数细节
  --update       自动从github更新程序
  -v, --version  版本号
  -h, --help     英文帮助
  -hc, --helpCN  中文帮助
"""