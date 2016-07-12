# !/usr/bin/env python
#  -*- coding: utf-8 -*-
import os
import time
from lib.core.data import conf, logger
from lib.core.log import CUSTOM_LOGGING
from lib.core.enums import API_MODE_STATUS
from lib.api.shodan.query import advancedQuery
from lib.api.zoomeye.search import dorkSearch


# def runZoomeyeApi():
#     if conf.dork:
#         z = ZoomEye()
#         if z.newToken():
#             logger.log(CUSTOM_LOGGING.SUCCESS, 'ZoomEye API authorization success.')
#             z.resourceInfo()
#         else:
#             logger.log(CUSTOM_LOGGING.SUCCESS,
#                        'ZoomEye API authorization failed,Please input ZoomEye Email and Password for use ZoomEye API!')
#             z.write_conf()
#             if z.newToken():
#                 logger.log(CUSTOM_LOGGING.SUCCESS, 'ZoomEye API authorization success.')
#                 z.resourceInfo()
#             else:
#                 sys.exit(logger.log(CUSTOM_LOGGING.ERROR,
#                                     '))
#
#         info = z.resources
#         logger.log(
#             CUSTOM_LOGGING.SYSINFO,
#             'Available ZoomEye search, web-search:{}, host-search:{}'.format(info['web-search'], info['host-search'])
#         )
#
#         tmpIpFile = os.path.join(conf.ZOOMEYE_OUTPUT_PATH, '%s_%s.txt' % (
#             conf['dork'].replace(':', '-').replace(' ', '-').strip(), time.strftime('%Y_%m_%d_%H_%M_%S')))
#         with open(tmpIpFile, 'w') as fp:
#             search_types = conf.get('search_type', 'web')
#             if 'host' not in search_types and 'web' not in search_types:
#                 search_types = 'web'
#             for page in range(conf.get('max_page', 1)):
#                 for search_type in search_types.split(','):
#                     if search_type in ['web', 'host']:
#                         for ip in z.search(conf['dork'], page, search_type):
#                             if type(ip) == list:
#                                 fp.write('%s\n' % ip[0])
#                             else:
#                                 fp.write('%s\n' % ip)
#         return tmpIpFile
#

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
            fp.write(each + '\n')
    return tmpIpFile


def setApi():
    if conf.API_MODE is API_MODE_STATUS.ZOOMEYE:
        return runZoomEyeApi()
    elif conf.API_MODE is API_MODE_STATUS.SHODAN:
        return runShodanApi()
