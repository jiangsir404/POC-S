#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author = i@cdxy.me
# project = https://github.com/Xyntax/POC-T

import Queue
import sys
import imp
import os
from lib.core.data import th, conf, logger, paths
from lib.core.enums import CUSTOM_LOGGING, EXIT_STATUS, API_MODE_STATUS, TARGET_MODE_STATUS
from lib.core.common import debugPause, systemQuit
from lib.core.settings import ESSENTIAL_MODULE_METHODS
from lib.core.exception import ToolkitValueException
from lib.controller.api import setApi
from thirdparty.IPy import IPy


def loadModule():
    _name = conf.MODULE_NAME
    infoMsg = 'Loading custom script: %s' % _name
    logger.log(CUSTOM_LOGGING.SUCCESS, infoMsg)

    fp, pathname, description = imp.find_module(os.path.splitext(_name)[0], [paths.SCRIPT_PATH])
    try:
        th.module_obj = imp.load_module("_", fp, pathname, description)
        for each in ESSENTIAL_MODULE_METHODS:
            if not hasattr(th.module_obj, each):
                errorMsg = "Can't find essential method:'%s()' in current script，Please modify your script/PoC."
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
    if conf.TARGET_MODE is TARGET_MODE_STATUS.RANGE:
        int_mode()
    elif conf.TARGET_MODE is TARGET_MODE_STATUS.FILE:
        file_mode()
    elif conf.TARGET_MODE is TARGET_MODE_STATUS.IPMASK:
        net_mode()
    elif conf.TARGET_MODE is TARGET_MODE_STATUS.SINGLE:
        single_target_mode()
    elif conf.TARGET_MODE is TARGET_MODE_STATUS.API:
        api_mode()

    else:
        raise ToolkitValueException('conf.TARGET_MODE value ERROR.')
    logger.log(CUSTOM_LOGGING.SUCCESS, 'Total: %s' % str(th.queue.qsize()))
    debugPause()


def file_mode():
    for line in open(conf.INPUT_FILE_PATH):
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


def api_mode():
    if conf.API_MODE is API_MODE_STATUS.ZOOMEYE:
        conf.ZOOMEYE_OUTPUT_PATH = os.path.join(paths.DATA_PATH, 'zoomeye')
        if not os.path.exists(conf.ZOOMEYE_OUTPUT_PATH):
            os.mkdir(conf.ZOOMEYE_OUTPUT_PATH)

    elif conf.API_MODE is API_MODE_STATUS.SHODAN:
        conf.SHODAN_OUTPUT_PATH = os.path.join(paths.DATA_PATH, 'shodan')
        if not os.path.exists(conf.SHODAN_OUTPUT_PATH):
            os.mkdir(conf.SHODAN_OUTPUT_PATH)

    file = setApi()
    for line in open(file):
        sub = line.strip()
        if sub:
            th.queue.put(sub)
