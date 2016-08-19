#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author = i@cdxy.me
# project = https://github.com/Xyntax/POC-T

u"""
本文档为程序中文使用说明，您也可以使用 -h 查看英文版使用说明
powered by cdxy <mail:i@cdxy.me>

使用方法:
  python POC-T.py [-T|-C] [-m NAME] [-s|-f|-i|-n VALUE] [options]
  python POC-T.py [-h|-v|--show|--update]

示例:
  python POC-T.py -T -m jboss-poc -s http://www.cdxy.me
  python POC-T.py -T -m test -f ./dic/1-100.txt
  python POC-T.py -C -m spider -i 1-100
  python POC-T.py -C -m ./script/spider.py -n 10.0.0.0/24
  python POC-T.py -T -m test --api --dork "port:21" --max-page 5
  python POC-T.py -T -m test --api --query "solr country:cn" --limit 10 --offset 0

引擎(必需项):
  -T             多线程模式
  -C             协程(单线程异步)模式
  -t NUM         设置并发数量(线程数量)，默认为10

脚本(必需项):
  -m NAME        指定加载的脚本名称或路径(例: test|test.py|./script/test.py)

目标(必需项):
  -s TARGET      验证单个目标 (e.g. www.wooyun.org)
  -f FILE        从文件加载目标列表(常用于扫描或批量漏洞验证) (例: ./data/wooyun_domain)
  -i START-END   给定起始数字和结束数字，自动生成payload(常用于有数字规则的遍历，爬虫等) (例: 1-100)
  -n IP/MASK     从IP和子网掩码加载目标(用于扫描网段) (例: 127.0.0.0/24)
  --api          从搜索引擎中获取目标(ZoomEye/Shodan/Censys)

可选项:
  -o FILE        输出文件路径，默认保存在./output/目录下
  --single       当验证到一个结果时退出(常用于密码爆破)
  --nF           取消文件输出
  --nS           取消屏幕输出
  --show         显示所有可用的脚本名称(./script/文件夹下)
  --browser      程序结束后，将运行结果在浏览器/记事本中打开
  --debug        开启debug模式，运行时将输出一些参数细节
  --update       自动从github更新程序
  -v, --version  版本号
  -h, --help     英文帮助
  -hc, --helpCN  中文帮助

ZoomEye API:
  --dork STRING       ZoomEye 搜索关键字
  --max-page PAGE     (可选) 最大爬取页数(每页20条数据/默认获取一页)
  --search-type TYPE  (可选) 选取搜索模式:web/host，默认为二者均是

Shodan API:
  --query STRING      Shodan 搜索关键字
  --limit LIMIT       (可选) 最大爬取记录数(默认获取100条)
  --offset OFFSET     (可选) 设置从第几条记录开始爬取

"""
