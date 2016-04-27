# !/usr/bin/env python
#  -*- coding: utf-8 -*-
__author__ = 'xy'

import os.path
from lib.parse.parser import parse_args
from lib.controller.loader import load_payloads
from lib.core.common import setPaths, showDebugData, banner
from lib.core.data import paths, conf, logger
from lib.core.enums import CUSTOM_LOGGING
from lib.utils.update import update
from lib.core.settings import IS_WIN
from thirdparty.colorama.initialise import init as win_color_init

def main():
    try:
        paths['ROOT_PATH'] = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        setPaths()
        parse_args()

        if IS_WIN:
            win_color_init()
        banner()

        if conf['DEBUG']:
            showDebugData()
        if conf['UPDATE']:
            update()

        load_payloads()

        if conf['ENGINE'] is 't':
            from lib.controller.threads import ThreadsEngine
            ThreadsEngine().run()
        elif conf['ENGINE'] is 'c':
            from lib.controller.coroutine import CoroutineEngine
            CoroutineEngine().run()
    except KeyboardInterrupt, e:
        logger.log(CUSTOM_LOGGING.ERROR, 'User quit!')


if __name__ == "__main__":
    main()
