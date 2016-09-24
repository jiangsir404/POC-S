#!/usr/bin/env python
# -*- coding: utf-8 -*-
# project = https://github.com/Xyntax/POC-T
# author = i@cdxy.me

import shodan
import sys
from lib.core.data import paths, logger
from shodan.exception import APIError
from lib.utils.config import ConfigFileParser


def _readKey():
    msg = 'Trying to auth with credentials in config file: %s.' % paths.CONFIG_PATH
    logger.info(msg)
    try:
        key = ConfigFileParser().ShodanApikey()
    except:
        key = ''
    return key


def ShodanSearch(query, limit, offset=0):
    key = _readKey()
    try:
        api = shodan.Shodan(key)
        result = api.search(query=query, offset=offset, limit=limit)
    except APIError:
        msg = 'Automatic authorization failed.'
        logger.warning(msg)
        key = raw_input('Input API-KEY >')
        try:
            api = shodan.Shodan(key)
            result = api.search(query=query, offset=offset, limit=limit)
        except APIError:
            msg = 'Invalid Shodan API key.'
            sys.exit(logger.error(msg))
    if 'matches' in result:
        anslist = []
        for match in result['matches']:
            anslist.append(match['ip_str'] + ':' + str(match['port']))
        return anslist
    else:
        return []
