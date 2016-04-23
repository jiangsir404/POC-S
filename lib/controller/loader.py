# !/usr/bin/env python
#  -*- coding: utf-8 -*-
__author__ = 'xy'

import Queue
from lib.core.data import th, conf, logger
from lib.core.enums import CUSTOM_LOGGING
from lib.core.common import debugPause


def load_payloads():
    infoMsg = 'Loading payloads...'
    logger.log(CUSTOM_LOGGING.SUCCESS, infoMsg)
    th['queue'] = Queue.Queue()
    if conf['MODULE_MODE'] is 'i':
        _int = conf['I_NUM2'].strip().split('-')
        for each in range(int(_int[0].strip()), int(_int[1].strip())):
            th['queue'].put(str(each))

    elif conf['MODULE_MODE'] is 'f':
        with open(conf['INPUT_FILE_PATH']) as f:
            for line in f:
                sub = line.strip()
                if sub:
                    th['queue'].put(sub)
    else:
        raise Exception('conf[\'MODULE_MODE\'] value ERROR.')
    logger.log(CUSTOM_LOGGING.SUCCESS, 'Total: %s' % str(th['queue'].qsize()))
    debugPause()
