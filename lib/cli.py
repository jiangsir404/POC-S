# !/usr/bin/env python
#  -*- coding: utf-8 -*-
__author__ = 'xy'

import os.path
from lib.parse.parser import parse_args
from lib.controller.loader import load_payloads
from lib.core.common import setPaths, showDebugData, banner, sysquit
from lib.core.data import paths, conf, logger
from lib.core.enums import CUSTOM_LOGGING
from lib.utils.update import update
from lib.core.settings import IS_WIN
from thirdparty.colorama.initialise import init as win_color_init


def main():
    """
    Main function of POC-T when running from command line.
    """
    try:
        paths['ROOT_PATH'] = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        try:
            os.path.isdir(paths['ROOT_PATH'])
        except UnicodeEncodeError:
            errMsg = "your system does not properly handle non-ASCII paths. "
            errMsg += "Please move the project root directory to another location"
            logger.error(errMsg)
            raise SystemExit

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

        sysquit(0)

    except KeyboardInterrupt, e:
        sysquit(1)


if __name__ == "__main__":
    main()
