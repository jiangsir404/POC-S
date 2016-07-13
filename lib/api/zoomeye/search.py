#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author = i@cdxy.me
# project = https://github.com/Xyntax/POC-T

import os
from lib.api.zoomeye.zoomeye import ZoomEye
from lib.core.data import logger
from lib.core.log import CUSTOM_LOGGING
from lib.core.enums import EXIT_STATUS
from lib.core.common import systemQuit


def _initial():
    z = ZoomEye()
    token_path = os.path.join(os.path.expanduser('~'), '.zoomeye-token')
    if not os.path.isfile(token_path):
        msg = 'ZoomEye API authorization failed, Please input ZoomEye Email and Password.'
        logger.log(CUSTOM_LOGGING.SUCCESS, msg)
        token = z.login()
        if token:
            open(token_path, 'w').write(token)
            msg = 'Save ZoomEye access token to: ' + token_path
            logger.log(CUSTOM_LOGGING.SUCCESS, msg)
        else:
            msg = 'Invalid ZoomEye username or password.'
            logger.log(CUSTOM_LOGGING.ERROR, msg)
            systemQuit(EXIT_STATUS.ERROR_EXIT)

    else:
        msg = 'Load ZoomEye access token from: ' + token_path
        logger.log(CUSTOM_LOGGING.SUCCESS, msg)
        z.setToken(open(token_path).read())
    try:
        info = z.resources_info()['resources']
    except TypeError:
        msg = 'Token invalid or expired, please re-run it to get a new token.'
        logger.log(CUSTOM_LOGGING.WARNING, msg)
        os.remove(token_path)
        systemQuit(EXIT_STATUS.ERROR_EXIT)

    if info:
        msg = 'Available ZoomEye search, web-search:{}, host-search:{}'.format(info['web-search'], info['host-search'])
        logger.log(CUSTOM_LOGGING.SYSINFO, msg)
    else:
        os.remove(token_path)
        msg = 'ZoomEye API authorization failed, Please re-run it and enter a new token.'
        logger.log(CUSTOM_LOGGING.ERROR, msg)
        systemQuit(EXIT_STATUS.ERROR_EXIT)

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
