#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author = i@cdxy.me
# project = https://github.com/Xyntax/POC-T

import os
import glob
import time
import sys
from lib.core.data import conf, paths, th, logger
from lib.core.enums import CUSTOM_LOGGING, TARGET_MODE_STATUS, ENGINE_MODE_STATUS
import lib.utils.cnhelp as cnhelp
from lib.utils.update import update
from lib.core.enums import API_MODE_STATUS
from lib.core.register import Register


def initOptions(args):
    if '--debug' in sys.argv:  # cannot use dataToStdout before init
        infoMsg = '---args---\n%s' % args
        logger.log(CUSTOM_LOGGING.SYSINFO, infoMsg)
    _checkCNhelp(args)
    _checkUpdate(args)
    _checkShow(args)
    _initEngine(args)
    _initModule(args)
    _initTargetMode(args)
    _initOutput(args)
    _initSafeOptions(args)


def _checkUpdate(args):
    # conflict with args.update(),so we use args['update'] here
    if args['update']:
        conf.UPDATE = args['update']
        update()


def _checkShow(args):
    if args.show:
        module_name_list = glob.glob(os.path.join(paths.SCRIPT_PATH, '*.py'))
        infoMsg = 'Module Name (total:%s)\n' % str(len(module_name_list) - 1)
        for each in module_name_list:
            _str = os.path.splitext(os.path.split(each)[1])[0]
            if _str not in ['__init__']:
                infoMsg += '  %s\n' % _str
        sys.exit(logger.log(CUSTOM_LOGGING.SYSINFO, infoMsg))


def _initEngine(args):
    def __thread():
        conf.ENGINE = ENGINE_MODE_STATUS.THREAD

    def __gevent():
        conf.ENGINE = ENGINE_MODE_STATUS.GEVENT

    msg = 'Use -T to set Multi-Threaded mode or -C to set Coroutine mode.'
    r = Register(mutex=True, mutex_errmsg=msg)
    r.add(__thread, args.T)
    r.add(__gevent, args.C)
    r.run()

    if args.t > 0 and args.t < 101:
        th.THREADS_NUM = conf.THREADS_NUM = args.t
    else:
        msg = 'Invalid input in [-t], range: 1 to 100'
        sys.exit(logger.log(CUSTOM_LOGGING.ERROR, msg))


def _initModule(args):
    if not args.m:
        msg = 'Use -m to select a module name. Example: -m spider'
        sys.exit(logger.log(CUSTOM_LOGGING.ERROR, msg))
    if args.m and not os.path.isfile(os.path.join(paths.SCRIPT_PATH, args.m + ".py")):
        msg = 'module not exist. Use --show to view all available module names.'
        sys.exit(logger.log(CUSTOM_LOGGING.ERROR, msg))
    conf.MODULE_NAME = args.m
    conf.MODULE_FILE_PATH = os.path.join(paths.SCRIPT_PATH, conf.MODULE_NAME + ".py")


def _initTargetMode(args):
    def __file():
        if not os.path.isfile(args.f):
            msg = 'TargetFile not found: %s' % args.f
            sys.exit(logger.log(CUSTOM_LOGGING.ERROR, msg))
        conf.TARGET_MODE = TARGET_MODE_STATUS.FILE
        conf.INPUT_FILE_PATH = args.f

    def __range():
        help_str = "invalid input in [-i], Example: python POC-T -m test -i 1-100."
        try:
            _int = args.i.strip().split('-')
            if int(_int[0]) < int(_int[1]):
                if int(_int[1]) - int(_int[0]) > 1000000:
                    warnMsg = 'Loading %d Payloads...\nMaybe its too much, continue? [y/N]' % (
                        int(_int[1]) - int(_int[0]))
                    logger.log(CUSTOM_LOGGING.WARNING, warnMsg)
                    a = raw_input()
                    if a in ('Y', 'y', 'yes'):
                        pass
                    else:
                        msg = 'User quit!'
                        sys.exit(logger.log(CUSTOM_LOGGING.ERROR, msg))
            else:
                sys.exit(logger.log(CUSTOM_LOGGING.ERROR, help_str))
        except Exception, e:
            sys.exit(logger.log(CUSTOM_LOGGING.ERROR, help_str))
        conf.TARGET_MODE = TARGET_MODE_STATUS.RANGE
        conf.I_NUM2 = args.i
        conf.INPUT_FILE_PATH = None

    def __ipmask():
        conf.TARGET_MODE = TARGET_MODE_STATUS.IPMASK
        conf.NETWORK_STR = args.n
        conf.INPUT_FILE_PATH = None

    def __single():
        conf.TARGET_MODE = TARGET_MODE_STATUS.SINGLE
        conf.SINGLE_TARGET_STR = args.s
        th.THREADS_NUM = conf.THREADS_NUM = 1
        conf.INPUT_FILE_PATH = None

    def __api():
        conf.TARGET_MODE = TARGET_MODE_STATUS.API
        _checkAPI(args)

    msg = 'To load targets, please choose one from [-s|-i|-f|-n|--api].'
    r = Register(mutex=True, mutex_errmsg=msg)
    r.add(__file, args.f)
    r.add(__api, args.api)
    r.add(__ipmask, args.n)
    r.add(__range, args.i)
    r.add(__single, args.s)
    r.run()


def _initOutput(args):
    if not args.nF and args.o:
        msg = 'You cannot use [--nF] and [-o] together, please read the usage with [-h].'
        sys.exit(logger.log(CUSTOM_LOGGING.ERROR, msg))

    if not args.nF and args.browser:
        msg = '[--browser] is based on file output, please remove [--nF] in your command and try again.'
        sys.exit(logger.log(CUSTOM_LOGGING.ERROR, msg))

    conf.SCREEN_OUTPUT = args.nS
    conf.FILE_OUTPUT = args.nF
    conf.OUTPUT_FILE_PATH = os.path.abspath(args.o) if args.o else \
        os.path.abspath(
            os.path.join(
                paths.OUTPUT_PATH, time.strftime(
                    '[%Y%m%d-%H%M%S]', time.localtime(
                        time.time())) + conf.MODULE_NAME + '.txt'))


def _initSafeOptions(args):
    conf.SINGLE_MODE = args.single
    conf.DEBUG = args.debug
    conf.OPEN_BROWSER = args.browser


def _checkCNhelp(args):
    if args.helpCN:
        print cnhelp.__doc__
        sys.exit(0)


def _checkAPI(args):
    api_mode_flag = 0
    if args.dork or args.max_page != 1 or args.search_type != 'host':
        api_mode_flag += 1
    if args.shodan_query or args.shodan_limit != 100 or args.shodan_offset != 0:
        api_mode_flag += 2
    if api_mode_flag not in (1, 2):
        msg = 'You can only use args from ZoonEye-API *or* Shodan-API.'
        sys.exit(logger.log(CUSTOM_LOGGING.ERROR, msg))
    if args.dork:
        try:
            if int(args.max_page) <= 0:
                msg = 'Invalid value in [--max-page], show usage with [-h].'
                logger.error(msg)
        except Exception:
            msg = 'Invalid value in [--max-page], show usage with [-h].'
            logger.error(msg)

        if args.search_type not in ['web', 'host']:
            msg = 'Invalid value in [--search-type], show usage with [-h].'
            logger.error(msg)

        conf.API_MODE = API_MODE_STATUS.ZOOMEYE
        conf.zoomeye_dork = args.dork
        conf.zoomeye_max_page = args.max_page
        conf.zoomeye_search_type = args.search_type

    elif args.shodan_query:
        try:
            if int(args.shodan_limit) <= 0:
                msg = 'Invalid value in [--limit], show usage with [-h].'
                logger.error(msg)
        except Exception:
            msg = 'Invalid value in [--limit], show usage with [-h].'
            logger.error(msg)

        try:
            if int(args.shodan_limit) <= 0:
                msg = 'Invalid value in [--offset], show usage with [-h].'
                logger.error(msg)
        except Exception:
            msg = 'Invalid value in [--offset], show usage with [-h].'
            logger.error(msg)

        conf.API_MODE = API_MODE_STATUS.SHODAN
        conf.shodan_query = args.shodan_query
        conf.shodan_limit = args.shodan_limit
        conf.shodan_offset = args.shodan_offset
