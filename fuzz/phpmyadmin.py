#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author = w8ay
import requests
import urlparse
import md5

def poc(url):
    if '://' not in url:
        url = 'http://' + url
    if not url.endswith('/'):
        url = url + "/"
    payload = url + "phpmyadmin/themes/pmahomme/jquery/jquery-ui-1.8.16.custom.css"
    try:
        header = dict()
        header["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
        r = requests.get(payload, headers=header, timeout=5)
        if r.status_code == 200:
            md5_value = md5.new(r.content).hexdigest()
            if md5_value == "2059c4c1ec104e7554df5da1edb07a77":
                return url + "phpmyadmin/"
        else:
            return False
    except Exception:
        return False