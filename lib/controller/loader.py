# !/usr/bin/env python
#  -*- coding: utf-8 -*-
__author__ = 'xy'

import Queue
import sys
import imp
from lib.core.data import th, conf, logger, paths
from lib.core.enums import CUSTOM_LOGGING, EXIT_STATUS
from lib.core.common import debugPause, systemQuit
from lib.core.settings import ESSENTIAL_MODULE_METHODS
from lib.core.exception import ToolkitValueException
from thirdparty.IPy import IPy


def loadModule():
    _name = conf.MODULE_NAME
    infoMsg = 'Loading custom module: %s.py' % _name
    logger.log(CUSTOM_LOGGING.SUCCESS, infoMsg)

    fp, pathname, description = imp.find_module(_name, [paths.MODULES_PATH])
    try:
        th.module_obj = imp.load_module("_", fp, pathname, description)
        for each in ESSENTIAL_MODULE_METHODS:
            if not hasattr(th.module_obj, each):
                errorMsg = "Can't find essential method:'%s()' in current script:'module/%s.py'\n%s" \
                           % (each, _name, 'Please modify your script/PoC.')
                logger.log(CUSTOM_LOGGING.ERROR, errorMsg)
                systemQuit(EXIT_STATUS.ERROR_EXIT)
    except ImportError, e:
        errorMsg = "Your current scipt [%s.py] caused this exception\n%s\n%s" \
                   % (_name, '[Error Msg]: ' + str(e), 'Maybe you can download this module from pip or easy_install')
        logger.log(CUSTOM_LOGGING.ERROR, errorMsg)
        systemQuit(EXIT_STATUS.ERROR_EXIT)
    debugPause()


def loadPayloads():
    infoMsg = 'Loading payloads...'
    logger.log(CUSTOM_LOGGING.SUCCESS, infoMsg)
    th.queue = Queue.Queue()
    if conf.MODULE_MODE is 'i':
        int_mode()
    elif conf.MODULE_MODE is 'f':
        file_mode()
    elif conf.MODULE_MODE is 'n':
        net_mode()
    elif conf.MODULE_MODE is 'target':
        single_target_mode()

    else:
        raise ToolkitValueException('conf.MODULE_MODE value ERROR.')
    logger.log(CUSTOM_LOGGING.SUCCESS, 'Total: %s' % str(th.queue.qsize()))
    debugPause()


def file_mode():
    with open(conf.INPUT_FILE_PATH) as f:
        for line in f:
            sub = line.strip()
            if sub:
                th.queue.put(sub)


def int_mode():
    _int = conf.I_NUM2.strip().split('-')
    for each in range(int(_int[0].strip()), int(_int[1].strip())):
        th.queue.put(str(each))


def net_mode():
    ori_str = conf.NETWORK_STR
    try:
        _list = IPy.IP(ori_str)
    except Exception, e:
        sys.exit(logger.error('Invalid IP/MASK,%s' % e))
    for each in _list:
        th.queue.put(str(each))


def single_target_mode():
    th.queue.put(str(conf.SINGLE_TARGET_STR))
