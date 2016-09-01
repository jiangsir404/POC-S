#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author = i@cdxy.me
# project = https://github.com/Xyntax/POC-T

import os
import time
from lib.core.data import conf, logger
from lib.core.exception import ToolkitValueException
from lib.core.enums import API_MODE_NAME
from lib.api.shodan.query import advancedQuery
from lib.api.zoomeye.search import dorkSearch
from lib.api.google.geturl import googleSearch


def runApi():
    output = conf.API_OUTPUT
    dork = conf.API_DORK
    limit = conf.API_LIMIT
    logger.info('Activate %s API' % conf.API_MODE)
    if conf.API_MODE is API_MODE_NAME.ZOOMEYE:
        anslist = dorkSearch(query=dork, type=conf.ZOOMEYE_SEARCH_TYPE, page=conf.ZOOMEYE_MAX_PAGE)
    elif conf.API_MODE is API_MODE_NAME.SHODAN:
        anslist = advancedQuery(query=dork, offset=conf.SHODAN_OFFSET, limit=limit)
    elif conf.API_MODE is API_MODE_NAME.GOOGLE:
        googleSearch(query=dork, limit=limit)
    else:
        raise ToolkitValueException('Unknown API mode')

    tmpIpFile = os.path.join(output, '%s_%s.txt' % (
        dork.replace(':', '-').replace(' ', '-').strip(), time.strftime('%Y%m%d%H%M%S')))
    with open(tmpIpFile, 'w') as fp:
        for each in anslist:
            if isinstance(each, list):  # for ZoomEye web type
                each = each[0]
            fp.write(each + '\n')
    return tmpIpFile
