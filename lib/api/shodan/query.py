#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author = i@cdxy.me
# project = https://github.com/Xyntax/POC-T

import shodan
import os
from shodan.exception import APIError


def _initial():
    api_path = os.path.join(os.path.expanduser('~'), '.shodan-api-key')
    if not os.path.isfile(api_path):
        with open(api_path, 'w') as fp:
            fp.write(raw_input('[-] First time using Shodan-API, please input your API-KEY > '))
    API_KEY = open(api_path).read().strip()
    return shodan.Shodan(API_KEY)


def advancedQuery(query, offset=0, limit=100):
    api = _initial()
    try:
        result = api.search(query=query, offset=offset, limit=limit)
    except APIError, e:
        print e
        print 'Please re-run it and enter a new API-KEY.'
        os.remove(os.path.join(os.path.expanduser('~'), '.shodan-api-key'))
        return []
    if result.has_key('matches'):
        anslist = []
        for match in result['matches']:
            anslist.append(match['ip_str'] + ':' + str(match['port']))
        return anslist
    else:
        return []
