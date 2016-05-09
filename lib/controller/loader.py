# !/usr/bin/env python
#  -*- coding: utf-8 -*-
__author__ = 'xy'

import Queue
import sys
from lib.core.data import th, conf, logger
from lib.core.enums import CUSTOM_LOGGING
from lib.core.common import debugPause
from thirdparty.IPy import IPy


def load_payloads():
    infoMsg = 'Loading payloads...'
    logger.log(CUSTOM_LOGGING.SYSINFO, infoMsg)
    th['queue'] = Queue.Queue()
    if conf['MODULE_MODE'] is 'i':
        int_mode()
    elif conf['MODULE_MODE'] is 'f':
        file_mode()
    elif conf['MODULE_MODE'] is 'n':
        net_mode()
    else:
        raise Exception('conf[\'MODULE_MODE\'] value ERROR.')
    logger.log(CUSTOM_LOGGING.SUCCESS, 'Total: %s' % str(th['queue'].qsize()))
    debugPause()


def file_mode():
    with open(conf['INPUT_FILE_PATH']) as f:
        for line in f:
            sub = line.strip()
            if sub:
                th['queue'].put(sub)


def int_mode():
    _int = conf['I_NUM2'].strip().split('-')
    for each in range(int(_int[0].strip()), int(_int[1].strip())):
        th['queue'].put(str(each))


def net_mode():
    ori_str = conf['NETWORK_STR']
    try:
        _list = IPy.IP(ori_str)
    except Exception, e:
        sys.exit(logger.error('Invalid IP/MASK,%s' % e))
    for each in _list:
        th['queue'].put(str(each))
