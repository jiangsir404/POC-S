#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author = w8ay
import requests
import urlparse

def poc(url):
    if '://' not in url:
        url = 'http://' + url
    if not url.endswith('/'):
        url = url + "/"
    phpinfoList = r"""
    phpinfo.php
PhpInfo.php
PHPinfo.php
PHPINFO.php
phpInfo.php
info.php
Info.php
INFO.php
phpversion.php
phpVersion.php
test1.php
test.php
test2.php
phpinfo1.php
phpInfo1.php
info1.php
PHPversion.php
x.php
xx.php
xxx.php
    """
    paths = phpinfoList.strip().splitlines()
    result = []
    for path in paths:
        try:
            payload = url + path.strip()
            header = dict()
            header["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
            r = requests.get(payload, headers=header, timeout=5)
            if "allow_url_fopen" in r.text and r.status_code == 200:
                result.append(payload)
        except Exception:
            pass
    if result:
        return result
    else:
        return False