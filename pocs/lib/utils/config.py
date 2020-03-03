#!/usr/bin/env python
# -*- coding: utf-8 -*-
# project = https://github.com/Xyntax/POC-T
# author = i@cdxy.me

import ConfigParser
from lib.core.data import paths, logger
from lib.core.common import getSafeExString

class ConfigFileParser:
    def __init__(self):
        try:
            self.cf = ConfigParser.ConfigParser()
            self.cf.read(paths.CONFIG_PATH)
        except ConfigParser.NoOptionError, e:
            logger.warning('Missing essential options, please check your config-file.')
            logger.error(getSafeExString(e))

    def _get_option(self, section, option):
        try:
            return self.cf.get(section=section, option=option)
        except Exception as e:
            logger.error(e)
            return ""

    def _set_option(self, section, key, value):
        try:
            self.cf.set(section, key, value)
            self.cf.write(open(paths.CONFIG_PATH, 'w'))
        except Exception, e:
            logger.error(e)
            return False
        return True

    def _get_options(self, section):
        """获取该section的所有options的keys()内容

        :return: [key1, key2, key3]
        """
        try:
            return self.cf.options(section=section)
        except Exception as e:
            logger.error(e)
            return []

    def ZoomEyeEmail(self):
        return self._get_option('zoomeye', 'email')

    def ZoomEyePassword(self):
        return self._get_option('zoomeye', 'password')

    def ShodanApikey(self):
        return self._get_option('shodan', 'api_key')

    def BingApikey(self):
        return self._get_option('bing', 'api_key')

    def CloudEyeApikey(self):
        return self._get_option('cloudeye', 'api_key')

    def ColudEyePersonaldomain(self):
        return self._get_option('cloudeye', 'personal_domain')

    def CeyeApikey(self):
        return self._get_option('ceye', 'api_key')

    def CeyePersonaldomain(self):
        return self._get_option('ceye', 'personal_domain')

    def GoogleProxy(self):
        return self._get_option('google', 'proxy')

    def GoogleDeveloperKey(self):
        return self._get_option('google', 'developer_key')

    def GoogleEngine(self):
        return self._get_option('google', 'search_engine')

    def FofaEmail(self):
        return self._get_option('fofa', 'email')

    def FofaKey(self):
        return self._get_option('fofa', 'api_key')
