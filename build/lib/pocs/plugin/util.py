#!/usr/bin/env python
# -*- coding: utf-8 -*-
# project = https://github.com/Xyntax/POC-T
# author = i@cdxy.me

# coding=utf-8
import ipaddress
import platform
import logging
import urlparse
import random
import hashlib
import requests
import socket
import re
from string import ascii_lowercase, digits
from urlparse import urlparse


def randomString(length=8):
    """
    生成随机字母串

    :param length:生成字符串长度
    :return 字母串
    """
    return ''.join([random.choice(ascii_lowercase) for _ in range(length)])


def randomDigits(length=8):
    """
    生成随机数字串

    :param length:生成字符串长度
    :return 数字串
    """
    return ''.join([random.choice(digits) for _ in range(length)])


def randomMD5(length=10, hex=True):
    """
    生成随机MD5键值对

    :param length:指定明文长度
    :param hex:指定密文长度为32位
    :returns 原文，密文(32位或16位)
    """
    plain = randomDigits(length)
    m = hashlib.md5()
    m.update(plain)
    cipher = m.hexdigest() if hex else m.hexdigest()[8:-8]
    return [plain, cipher]


def redirectURL(url, timeout=3):
    """
    获取跳转后的真实URL

    :param url:原始URL
    :param timeout:超时时间
    :return 跳转后的真实URL
    """
    try:
        url = url if '://' in url else 'http://' + url
        r = requests.get(url, allow_redirects=False, timeout=timeout)
        return r.headers.get('location') if r.status_code == 302 else url
    except Exception:
        return url


def host2IP(url):
    """
    URL转IP

    :param url:原始URL
    :return IP:PORT
    :except 返回原始URL
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
    except Exception:
        return url


def IP2domain(base, timeout=3):
    """
    IP转域名

    :param base:原始IP
    :param timeout:超时时间
    :return 域名 / False
    :except 返回False
    """
    try:
        domains = set()
        ip = base.split(':')[0] if ':' in base else base
        q = "https://www.bing.com/search?q=ip%3A" + ip
        c = requests.get(url=q,
                         headers={
                             'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'},
                         timeout=timeout
                         ).content
        p = re.compile(r'<cite>(.*?)</cite>')
        l = re.findall(p, c)
        for each in l:
            domain = each.split('://')[-1].split('/')[0]
            domains.add(domain)
        if len(domains) > 0:
            ans_1 = base + ' -> '
            for each in domains:
                ans_1 += '|' + each
            return ans_1
        else:
            return False
    except Exception:
        return False


def checkPortTcp(target, port, timeout=3):
    """
    检查端口是否开放

    :param target:目标IP
    :param port:目标端口
    :param timeout:超时时间
    :return True / False
    :except 返回False
    """
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.settimeout(timeout)
    try:
        sk.connect((target, port))
        return True
    except Exception:
        return False


def listwrite(iplist,file):
    with open(file,'a') as f:
        for i in iplist:
            f.write(i+"\n")

def listread(file):
    iplist = []
    with open(file) as f:
        for i in f:
            iplist.append(i.strip())
    return iplist

def match_subdomain(domain, text, distinct=True):
    """
    匹配text中domain的子域名

    :param str domain: 域名
    :param str text: 响应文本
    :param bool distinct: 结果去重
    :return: 匹配结果
    :rtype: set or list
    """
    regexp = r'(?:[a-z0-9](?:[a-z0-9\-]{0,61}[a-z0-9])?\.){0,}' \
             + domain.replace('.', r'\.')
    result = re.findall(regexp, text, re.I)
    if not result:
        return set()
    deal = map(lambda s: s.lower(), result)
    if distinct:
        return set(deal)
    else:
        return list(deal)


def gen_random_ip():
    """
    生成随机的点分十进制的IP字符串
    """
    while True:
        ip = ipaddress.IPv4Address(random.randint(0, 2 ** 32 - 1))
        return ip.exploded


def gen_fake_header():
    """
    生成伪造请求头
    """
    ua = random.choice(user_agents)
    ip = gen_random_ip()
    headers = {
        'Referer': 'https://www.google.com/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': ua,
        'X-Forwarded-For': ip,
        'X-Real-IP': ip
    }
    return headers


def split_list(ls, size):
    """
    将ls列表按size大小划分并返回新的划分结果列表

    :param list ls: 要划分的列表
    :param int size: 划分大小
    :return 划分结果

    >>> split_list([1, 2, 3, 4], 3)
    [[1, 2, 3], [4]]
    """
    if size == 0:
        return ls
    return [ls[i:i + size] for i in range(0, len(ls), size)]


def match(domain, html, distinct=True):
    """
    正则匹配出子域

    :param str domain: 域名
    :param str html: 要匹配的html响应体
    :param bool distinct: 匹配结果去除
    :return: 匹配出的子域集合或列表
    :rtype: set or list
    """
    logging.debug('正则匹配响应体中的子域')
    regexp = r'(?:\>|\"|\'|\=|\,)(?:http\:\/\/|https\:\/\/)?' \
             r'(?:[a-z0-9](?:[a-z0-9\-]{0,61}[a-z0-9])?\.){0,}' \
             + domain.replace('.', r'\.')
    result = re.findall(regexp, html, re.I)
    if not result:
        return set()
    regexp = r'(?:http://|https://)'
    deal = map(lambda s: re.sub(regexp, '', s[1:].lower()), result)
    if distinct:
        return set(deal)
    else:
        return list(deal)

def fix_url(url):
    """修复url成标准的schem://host:port/ 的形式
    """
    if not url:
        return None
    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'http://'+url
    if not url.endswith('/'):
        url += '/'
    return url

def grep_host_from_url(url):
    _url = fix_url(url)
    url_struct = urlparse.urlparse(_url)
    # 去掉scheme
    new_host = url_struct.netloc
    # 去掉ip和端口
    if ':' in new_host:
        new_host = new_host.partition(':')[0]
    if new_host.replace('.', '').isdigit():
        return None
    return new_host

def grep_host_from_url_list(urlList):
    """去掉url的scheme和port, 以及ip 只保留host, 这样方便nmap可以批量扫
        :return: set([subdomain]) 可以自动去重
    """
    new_iplist = set()
    for url in urlList:
        new_host = grep_host_from_url(url)
        if new_host:
            new_iplist.add(new_host)

    return new_iplist

if __name__ == '__main__':
    print get_random_proxy()
    print gen_random_ip()
    print gen_fake_header()
    print grep_host_from_url_list(["http://www.blogsir.com.cn",'http://www.blogsir.com.cn:82/'])