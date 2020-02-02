#!/usr/bin/env python
# -*- coding: utf-8 -*-
# project = https://github.com/Xyntax/POC-T
# author = i@cdxy.me

import sys
from lib.api.zoomeye.base import ZoomEye
from lib.core.data import logger


def _initial():
    z = ZoomEye()
    z.auto_login()
    info = z.resources_info().get('resources')
    if info:
        msg = 'Available ZoomEye search: (search:%s)' % (info.get('search', 'NO FOUND'))
        logger.info(msg)
    else:
        msg = 'ZoomEye API authorization failed, Please re-run it and enter a new token.'
        sys.exit(logger.error(msg))
    return z


def ZoomEyeSearch(query, limit, type='host', offset=0):
    z = _initial()
    ans = []
    limit += offset
    for page_n in range(int(offset / 10), int((limit + 10 - 1) / 10)):
        data = z.dork_search(query, resource=type, page=page_n)
        if data:
            for i in data:
                ip_str = i.get('ip')
                if 'portinfo' in i:
                    ip_str = ip_str + ':' + str(i.get('portinfo').get('port'))
                ans.append(ip_str)
        else:
            break
    return ans
