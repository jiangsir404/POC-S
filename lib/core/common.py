# !/usr/bin/env python
#  -*- coding: utf-8 -*-
__author__ = 'xy'

import os
import re
import sys
from lib.core.data import *
from lib.core.log import CUSTOM_LOGGING,LOGGER_HANDLER
from lib.core.settings import BANNER

def setPaths():
    """
    Sets absolute paths for project directories and files
    """
    ROOT_PATH = paths['ROOT_PATH']
    paths['DATA_PATH'] = os.path.join(ROOT_PATH, "data")
    paths['MODULES_PATH'] = os.path.join(ROOT_PATH, "module")
    paths['OUTPUT_PATH'] = os.path.join(ROOT_PATH, "output")
    paths['WEAK_PASS'] = os.path.join(paths['DATA_PATH'], "pass100.txt")
    paths['LARGE_WEAK_PASS'] = os.path.join(paths['DATA_PATH'], "pass1000.txt")


def checkFile(filename):
    """
    @function Checks for file existence and readability
    """

    valid = True

    if filename is None or not os.path.isfile(filename):
        valid = False

    if valid:
        try:
            with open(filename, "rb"):
                pass
        except:
            valid = False

    if not valid:
        raise Exception("unable to read file '%s'" % filename)


def debugPause():
    if conf['DEBUG']:
        raw_input('[Debug] Press any key to continue.')


def showDebugData():
    logger.log(CUSTOM_LOGGING.SYSINFO, '----conf---=\n%s' % conf)
    logger.log(CUSTOM_LOGGING.SYSINFO, '----paths---=\n%s' % paths)
    logger.log(CUSTOM_LOGGING.SYSINFO, '----th---=\n%s' % th)
    debugPause()

def banner():
    _ = BANNER
    if not getattr(LOGGER_HANDLER, "is_tty", False):
        _ = re.sub("\033.+?m", "", _)
    # dataToStdout(_)
    sys.stdout.flush()
    print BANNER
