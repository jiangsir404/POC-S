#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author = i@cdxy.me
# project = https://github.com/Xyntax/POC-T

import ConfigParser
from lib.core.data import paths


class ConfigFileParser:
    def __init__(self):
        self.cf = ConfigParser.ConfigParser()
        self.cf.read(paths.CONFIG_PATH)

    def ZoomEyeEmail(self):
        return self.cf.get('zoomeye', 'email')

    def setZoomEyeCertificate(self, email, password):
        self.cf.set('zoomeye', 'email', email)
        self.cf.set('zoomeye', 'email', password)

    def ZoomEyePassword(self):
        return self.cf.get('zoomeye', 'password')

    def ShodanApikey(self):
        return self.cf.get('shodan', 'api_key')

    def BingApikey(self):
        return self.cf.get('bing', 'api_key')

    def CloudEyeApikey(self):
        return self.cf.get('cloudeye', 'api_key')

    def ColudEyePersonaldomain(self):
        return self.cf.get('cloudeye', 'personal_domain')

    def GoogleProxy(self):
        return self.cf.get('google', 'proxy')

    def GoogleDeveloperKey(self):
        return self.cf.get('google', 'developer_key')

    def GoogleEngine(self):
        return self.cf.get('google', 'search_engine')


def setConfig():
    pass  # TODO
