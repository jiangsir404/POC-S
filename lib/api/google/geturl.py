#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author = i@cdxy.me
# project = https://github.com/Xyntax/POC-T

import sys
from googleapiclient.discovery import build
from lib.core.enums import PROXY_TYPE
from lib.utils.config import ConfigFileParser
from lib.core.data import logger, conf
from thirdparty.httplib2 import Http, ProxyInfo


def _initHttpClient():
    if conf.GOOGLE_PROXY:
        proxy_str = conf.GOOGLE_PROXY
    elif ConfigFileParser().GoogleProxy():
        proxy_str = ConfigFileParser().GoogleProxy()
    else:
        proxy_str = None

    if not proxy_str:
        return Http()

    msg = 'Proxy: %s' % proxy_str
    logger.info(msg)
    proxy = proxy_str.strip().split(' ')
    if len(proxy) != 3:
        msg = 'SyntaxError in GoogleProxy string, Please check your args or config file.'
        sys.exit(logger.error(msg))
    if proxy[0].lower() == 'http':
        type = PROXY_TYPE.HTTP
    elif proxy[0].lower() == 'sock5':
        type = PROXY_TYPE.SOCKS5
    elif proxy[0].lower() == 'sock4':
        type = PROXY_TYPE.SOCKS4
    else:
        msg = 'Invalid proxy-type in GoogleProxy string, Please check your args or config file.'
        sys.exit(logger.error(msg))
    try:
        port = int(proxy[2])
    except ValueError:
        msg = 'Invalid port in GoogleProxy string, Please check your args or config file.'
        sys.exit(logger.error(msg))
    else:
        http_client = Http(proxy_info=ProxyInfo(type, proxy[1], port))
    return http_client


def GoogleSearch(query, limit):  # TODO handle exception for invalid key or dork
    key = ConfigFileParser().GoogleDeveloperKey()
    engine = ConfigFileParser().GoogleEngine()
    service = build("customsearch", "v1", http=_initHttpClient(), developerKey=key)

    result_info = service.cse().list(q=query, cx=engine).execute()
    msg = 'Max query results: %s' % str(result_info['searchInformation']['totalResults'])
    logger.info(msg)

    ans = set()
    for i in range(int((limit + 10 - 1) / 10)):
        result = service.cse().list(q=query, cx=engine, num=10, start=i * 10 + 1).execute()
        for url in result['items']:
            ans.add(url['link'])

    return ans
