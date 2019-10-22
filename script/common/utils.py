# coding=utf-8
import re
import random
import ipaddress
import platform
import logging
import urlparse

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

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/68.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) '
    'Gecko/20100101 Firefox/68.0',
    'Mozilla/5.0 (X11; Linux i586; rv:31.0) Gecko/20100101 Firefox/68.0']


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




def check_response(method, resp):
    if resp.status_code == 200 and resp.content:
        return True
    logging.error(resp.content)
    content_type = resp.headers.get('Content-Type')
    if content_type and 'json' in content_type and resp.content:
        try:
            msg = resp.json()
        except Exception as e:
            logging.debug(e.args)
        else:
            logging.error(msg)
    return False


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