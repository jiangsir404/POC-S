# !/usr/bin/env python
#  -*- coding: utf-8 -*-
__author__ = 'xy'

import os
import glob
import time
import sys
from lib.core.data import conf, paths, th, logger
from lib.core.enums import CUSTOM_LOGGING
import lib.utils.cnhelp as cnhelp
from lib.utils.update import update


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
        raw_input('update?')
        conf.UPDATE = args['update']
        update()


def _checkShow(args):
    if args.show:
        module_name_list = glob.glob(r'./module/*.py')
        infoMsg = 'Module Name (total:%s)\n' % str(len(module_name_list) - 1)
        for each in module_name_list:
            _str = os.path.splitext(os.path.split(each)[1])[0]
            if _str not in ['__init__']:
                infoMsg += '  %s\n' % _str
        sys.exit(logger.log(CUSTOM_LOGGING.SYSINFO, infoMsg))


def _initEngine(args):
    if (not args.T and not args.C) or (args.T and args.C):
        msg = 'Use -T to set Multi-Threaded mode or -C to set Coroutine mode.'
        sys.exit(logger.log(CUSTOM_LOGGING.ERROR, msg))
    else:
        conf.ENGINE = 't' if args.T else 'c'
        th.THREADS_NUM = conf.THREADS_NUM = args.t


def _initModule(args):
    if not args.m:
        msg = 'Use -m to select a module name. Example: -m spider'
        sys.exit(logger.log(CUSTOM_LOGGING.ERROR, msg))
    if args.m and not os.path.isfile("./module/" + args.m + ".py"):
        msg = 'module not exist. Use --show to view all available module names.'
        sys.exit(logger.log(CUSTOM_LOGGING.ERROR, msg))
    conf.MODULE_NAME = args.m
    conf.MODULE_FILE_PATH = os.path.join(paths.MODULES_PATH, conf.MODULE_NAME + ".py")


def _initTargetMode(args):
    target_mode_flag = 0
    if args.s:
        target_mode_flag += 1
    if args.f:
        target_mode_flag += 2
    if args.i:
        target_mode_flag += 4
    if args.n:
        target_mode_flag += 8
    if target_mode_flag not in (1, 2, 4, 8):
        msg = 'To load targets, please choose one from [-s|-i|-f|-n].'
        sys.exit(logger.log(CUSTOM_LOGGING.ERROR, msg))

    if args.f:
        if not os.path.isfile(args.f):
            msg = 'TargetFile not found: %s' % args.f
            sys.exit(logger.log(CUSTOM_LOGGING.ERROR, msg))
        conf.MODULE_MODE = 'f'
        conf.INPUT_FILE_PATH = args.f

    if args.i:
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
        conf.MODULE_MODE = 'i'
        conf.I_NUM2 = args.i
        conf.INPUT_FILE_PATH = None
    if args.n:
        conf.MODULE_MODE = 'n'
        conf.NETWORK_STR = args.n
        conf.INPUT_FILE_PATH = None
    if args.s:
        conf.MODULE_MODE = 'target'
        conf.SINGLE_TARGET_STR = args.s
        th.THREADS_NUM = conf.THREADS_NUM = 1
        conf.INPUT_FILE_PATH = None


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
