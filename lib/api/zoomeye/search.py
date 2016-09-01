#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author = i@cdxy.me
# project = https://github.com/Xyntax/POC-T

import os
import sys
from lib.api.zoomeye.zoomeye import ZoomEye
from lib.core.data import logger


def _initial():
    z = ZoomEye()
    z.auto_login()
    info = z.resources_info()['resources']
    if info:
        msg = 'Available ZoomEye search: (web:%s,host:%s)' % (info['web-search'], info['host-search'])
        logger.info(msg)
    else:
        msg = 'ZoomEye API authorization failed, Please re-run it and enter a new token.'
        sys.exit(logger.error(msg))
    return z


def dorkSearch(query, type='host', page=1):
    z = _initial()
    ans = []
    for page_n in range(page):
        data = z.dork_search(query, resource=type, page=page_n)
        if data:
            for i in data:
                ip_str = i.get('ip')
                if i.has_key('portinfo'):
                    ip_str = ip_str + ':' + str(i.get('portinfo').get('port'))
                ans.append(ip_str)
        else:
            break
    return ans
