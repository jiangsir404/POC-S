#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author = i@cdxy.me
# project = https://github.com/Xyntax/POC-T

"""
Functions to extract IP from content string
edit by cdxy [i@cdxy.me]
May 23 Mon, 2016

parameters：
  content
  remove_duplicate  (default:true)
  remove_private    (default:False)

usage:
 from lib.util.extracts import *
 ip_list = getIP(content)

private address：
 10.0.0.0 - 10.255.255.255
 172.16.0.0 - 172.31.255.255
 192.168.0.0 - 192.168.255.255
 127.0.0.0 - 127.255.255.255
"""

import re


def getIP(content, remove_duplicate=True, remove_private=False):
    """
    > print getIP('ffeac12.2.2.2asf^&10.10\n.1.1ffa2\n')
    ['12.2.2.2','10.10.1.1']

    """
    content = content.replace('\n', ',')
    p = re.compile(r'(?:(?:2[0-4]\d|25[0-5]|[01]?\d\d?)\.){3}(?:2[0-4]\d|25[0-5]|[01]?\d\d?)')
    _ = re.findall(p, content)
    ans = list(set(_)) if remove_duplicate else _

    if remove_private:
        for each in ans:
            if _isPrivateIP(each):
                ans.remove(each)

    return ans


def _isPrivateIP(strict_IP):
    p1 = re.compile(r'^10\.|^172\.(?:1[6789]|2\d|31)\.|^192\.168\.|^127\.')
    return True if re.match(p1, strict_IP) else False


if __name__ == '__main__':
    import sys

    try:
        c = sys.argv[1]
    except Exception:
        c = raw_input('content > ')
    finally:
        print getIP(c)
