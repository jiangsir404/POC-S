#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author = i@cdxy.me
# project = https://github.com/Xyntax/POC-T

import random
import hashlib
import requests
import socket
from string import ascii_lowercase
from urlparse import urlparse
from lib.core.exception import ToolkitPluginException


def randomString(length=8):
    """
    生成随机字符串

    randomString()  ==> ndzldryt
    """

    return ''.join([random.choice(ascii_lowercase) for _ in range(length)])


def randomMD5(hex=True):
    """
    生成随机MD5 key-value
    hex True:32位 False:16位

    randomMD5()  ==>  ['ftx', '6aecac5e4af18f283d09b56e3d5dc5b8']
    """
    plain = randomString(3)
    m = hashlib.md5()
    m.update(plain)
    cipher = m.hexdigest() if hex else m.hexdigest()[8:-8]
    return [plain, cipher]


def redirectURL(url):
    """
    获取跳转后的真实URL

    http://123.132.112.21  ==>  http://123.132.112.21/dxy/index.action
    """

    try:
        url = url if '://' in url else 'http://' + url
        r = requests.get(url, allow_redirects=False)
        return r.headers.get('location') if r.status_code == 302 else url
    except:
        raise ToolkitPluginException('Get redirect URL failed, plsase check your PoC code.')


def host2IP(url):
    """
    检查target是否为IP格式,如果是IP格式直接返回,是URL格式则自动转为IP:PORT

    http://www.cdxy.me/test/index.php?id=1       ==>  139.129.132.156
    http://www.cdxy.me:8080/test/index.php?id=1  ==>  139.129.132.156:8080
    """

    for offset in url:
        if offset.isalpha():
            break
    else:
        return url
    try:
        url = url if '://' in url else 'http://' + url  # to get netloc
        url = urlparse(url).netloc
        ans = [i for i in socket.getaddrinfo(url.split(':')[0], None)[0][4] if i != 0][0]
        if ':' in url:
            ans += ':' + url.split(':')[1]
        return ans
    except:
        raise ToolkitPluginException('Get host IP failed, plsase check your PoC code.')
