# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'

import sys
from lib.core.data import paths, logger
from lib.utils.config import ConfigFileParser
import getpass
import urllib
import base64
import simplejson

def check(email,key):
    if email!="" and key !="":
        auth_url = "https://fofa.so/api/v1/info/my?email={0}&key={1}".format(email, key)
        try:
            response = urllib.urlopen(auth_url)
            if response.code == 200:
                return True
        except Exception,e:
            #logger.error(e)
            return False

def FofaSearch(query, limit=100, offset=0):#超过数量需要付费;不付费的情况下只能获取100个结果
    try:
        msg = 'Trying to login with credentials in config file: %s.' % paths.CONFIG_PATH
        logger.info(msg)
        email = ConfigFileParser().FofaEmail()
        key= ConfigFileParser().FofaKey()
        if check(email,key):
            pass
        else:
            raise # will go to except block
    except:
        msg = 'Automatic authorization failed.'
        logger.warning(msg)
        msg = 'Please input your FoFa Email and API Key below.'
        logger.info(msg)
        email = raw_input("Fofa Email: ").strip()
        key = getpass.getpass(prompt='Fofa API Key: ').strip()

    query = base64.b64encode(query)#"Powered+by+vancheer"

    request = "https://fofa.so/api/v1/search/all?email={0}&key={1}&qbase64={2}".format(email,key,query)
    result = []
    try:
        response = urllib.urlopen(request)
        resp = response.readlines()[0]
        resp = simplejson.loads(resp)
        #print resp
        if resp["error"] == None:
            #print resp['results']
            for item in resp['results']: #['219.159.80.242:23', '219.159.80.242', '23']
                result.append(item[0])
            if resp['size'] >=100:
                logger.info("{0} items found! just 100 returned....".format(resp['size']))
    except Exception,e:
        sys.exit(logger.error(e))
    finally:
        return result

if __name__ == "__main__":
    check("bit4woo@163.com","xxxx")