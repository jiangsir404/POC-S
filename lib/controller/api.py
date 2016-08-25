#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author = i@cdxy.me
# project = https://github.com/Xyntax/POC-T

import os
import time
from lib.core.data import conf, logger
from lib.core.log import CUSTOM_LOGGING
from lib.core.enums import API_MODE_STATUS
from lib.api.shodan.query import advancedQuery
from lib.api.zoomeye.search import dorkSearch


def runShodanApi():
    logger.log(CUSTOM_LOGGING.SYSINFO, 'Retriving targets from Shodan...')
    anslist = advancedQuery(query=conf.shodan_query, offset=conf.shodan_offset, limit=conf.shodan_limit)
    tmpIpFile = os.path.join(conf.SHODAN_OUTPUT_PATH, '%s_%s.txt' % (
        conf.shodan_query.replace(':', '-').replace(' ', '-').strip(), time.strftime('%Y_%m_%d_%H_%M_%S')))
    with open(tmpIpFile, 'w') as fp:
        for each in anslist:
            fp.write(each + '\n')
    return tmpIpFile


def runZoomEyeApi():
    logger.log(CUSTOM_LOGGING.SYSINFO, 'Enable ZoomEye API.')
    anslist = dorkSearch(query=conf.zoomeye_dork, type=conf.zoomeye_search_type, page=conf.zoomeye_max_page)
    tmpIpFile = os.path.join(conf.ZOOMEYE_OUTPUT_PATH, '%s_%s.txt' % (
        conf.zoomeye_dork.replace(':', '-').replace(' ', '-').strip(), time.strftime('%Y_%m_%d_%H_%M_%S')))
    with open(tmpIpFile, 'w') as fp:
        for each in anslist:
            if isinstance(each, list):
                each = each[0]
            fp.write(each + '\n')
    return tmpIpFile


def setApi():
    if conf.API_MODE is API_MODE_STATUS.ZOOMEYE:
        return runZoomEyeApi()
    elif conf.API_MODE is API_MODE_STATUS.SHODAN:
        return runShodanApi()
