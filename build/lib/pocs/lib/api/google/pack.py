#!/usr/bin/env python
# -*- coding: utf-8 -*-
# project = https://github.com/Xyntax/POC-T
# author = i@cdxy.me

import sys
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError as ServerHttpDenied
from lib.core.common import getSafeExString
from lib.core.enums import PROXY_TYPE
from lib.utils.config import ConfigFileParser
from lib.core.data import logger, conf
from thirdparty.httplib2 import Http, ProxyInfo
from socket import error as SocketError


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


def GoogleSearch(query, limit, offset=0):
    key = ConfigFileParser().GoogleDeveloperKey()
    engine = ConfigFileParser().GoogleEngine()
    if not key or not engine:
        msg = "Please config your 'developer_key' and 'search_enging' at toolkit.conf"
        sys.exit(logger.error(msg))
    try:
        service = build("customsearch", "v1", http=_initHttpClient(), developerKey=key)

        result_info = service.cse().list(q=query, cx=engine).execute()
        msg = 'Max query results: %s' % str(result_info.get('searchInformation',{}).get('totalResults'))
        logger.info(msg)

        ans = set()
        limit += offset
        for i in range(int(offset / 10), int((limit + 10 - 1) / 10)):
            result = service.cse().list(q=query, cx=engine, num=10, start=i * 10 + 1).execute()
            if 'items' in result:
                for url in result.get('items'):
                    ans.add(url.get('link'))
        return ans
    except SocketError:
        sys.exit(logger.error('Unable to connect Google, maybe agent/proxy error.'))
    except ServerHttpDenied, e:
        logger.warning('It seems like Google-Server denied this request.')
        sys.exit(logger.error(getSafeExString(e)))
