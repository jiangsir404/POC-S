#!/usr/bin/env python
# -*- coding: utf-8 -*-
# project = https://github.com/Xyntax/POC-T
# author = i@cdxy.me

import shodan
import sys
from lib.core.data import paths, logger
from shodan.exception import APIError
from lib.utils.config import ConfigFileParser


class ShodanBase:
    def __init__(self, query, limit, offset):
        self.query = query
        self.limit = limit
        self.offset = offset
        self.api_key = None
        self.result = None

    def login(self):
        msg = 'Trying to login with credentials in config file: %s.' % paths.CONFIG_PATH
        logger.info(msg)
        self.api_key = ConfigFileParser().ShodanApikey()

        if not self.api_key:
            msg = 'Automatic authorization failed.'
            logger.warning(msg)
            msg = 'Please input your Shodan API Key (https://account.shodan.io/).'
            logger.info(msg)
            self.api_key = raw_input('API KEY > ').strip()

    def account_info(self):
        try:
            api = shodan.Shodan(self.api_key)
            account_info = api.info()
            msg = "Available Shodan query credits: %d" % account_info['query_credits']
            logger.info(msg)
        except APIError, e:
            sys.exit(logger.error(e))
        return True

    def api_query(self):
        try:
            api = shodan.Shodan(self.api_key)
            result = api.search(query=self.query, offset=self.offset, limit=self.limit)
        except APIError, e:
            sys.exit(logger.error(e))

        if 'matches' in result:
            anslist = []
            for match in result['matches']:
                anslist.append(match['ip_str'] + ':' + str(match['port']))
            self.result = anslist
        else:
            self.result = []


def ShodanSearch(query, limit, offset=0):
    s = ShodanBase(query, limit, offset)
    s.login()
    s.account_info()
    s.api_query()
    return s.result
