#!/usr/bin/env python
# -*- coding: utf-8 -*-
# project = https://github.com/Xyntax/POC-T
# author = i@cdxy.me

import os
import time
from lib.core.data import conf, logger
from lib.core.exception import ToolkitValueException
from lib.core.enums import API_MODE_NAME
from lib.api.shodan.pack import ShodanSearch
from lib.api.zoomeye.pack import ZoomEyeSearch
from lib.api.google.pack import GoogleSearch
from lib.api.fofa.pack import FofaSearch


def runApi():
    output = conf.API_OUTPUT
    dork = conf.API_DORK
    limit = conf.API_LIMIT
    logger.info('Activate %s API' % conf.API_MODE)
    if conf.API_MODE is API_MODE_NAME.ZOOMEYE:
        anslist = ZoomEyeSearch(query=dork, limit=limit, type=conf.ZOOMEYE_SEARCH_TYPE, offset=conf.API_OFFSET)
    elif conf.API_MODE is API_MODE_NAME.SHODAN:
        anslist = ShodanSearch(query=dork, limit=limit, offset=conf.API_OFFSET)
    elif conf.API_MODE is API_MODE_NAME.GOOGLE:
        anslist = GoogleSearch(query=dork, limit=limit, offset=conf.API_OFFSET)
    elif conf.API_MODE is API_MODE_NAME.FOFA:
        anslist = FofaSearch(query=dork, limit=limit, offset=conf.API_OFFSET)
    else:
        raise ToolkitValueException('Unknown API mode')

    tmpIpFile = os.path.join(output, '%s.txt' % (time.strftime('%Y%m%d%H%M%S')))
    with open(tmpIpFile, 'w') as fp:
        for each in anslist:
            if isinstance(each, list):  # for ZoomEye web type
                each = each[0]
            fp.write(each + '\n')
    return tmpIpFile
